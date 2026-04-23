const fs = require("fs");
const path = require("path");
const {
  Document,
  Packer,
  Paragraph,
  TextRun,
  HeadingLevel,
  AlignmentType,
  PageBreak,
  ExternalHyperlink,
  ImageRun,
} = require("../docx_builder/node_modules/docx");

const [inputPath, outputPath] = process.argv.slice(2);

if (!inputPath || !outputPath) {
  console.error("Usage: node markdown_to_docx.js <input.md> <output.docx>");
  process.exit(1);
}

const source = fs.readFileSync(inputPath, "utf8").replace(/\r\n/g, "\n");
const baseDir = path.dirname(inputPath);

function decodeEntities(text) {
  return text
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"');
}

function stripMarkdown(text) {
  return decodeEntities(text)
    .replace(/\*\*([^*]+)\*\*/g, "$1")
    .replace(/\*([^*]+)\*/g, "$1")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, "$1 ($2)")
    .trim();
}

function textRun(text, options = {}) {
  return new TextRun({
    text,
    font: "Times New Roman",
    size: options.size || 22,
    bold: options.bold || false,
    italics: options.italics || false,
    color: options.color,
  });
}

function paragraph(text, options = {}) {
  const children = [];
  const regex = /(`[^`]+`|\*\*[^*]+\*\*|\[[^\]]+\]\([^)]+\))/g;
  let lastIndex = 0;
  let match;

  while ((match = regex.exec(text)) !== null) {
    if (match.index > lastIndex) {
      children.push(textRun(decodeEntities(text.slice(lastIndex, match.index)), options));
    }
    const token = match[0];
    if (token.startsWith("`")) {
      children.push(textRun(token.slice(1, -1), { ...options, color: "44546A" }));
    } else if (token.startsWith("**")) {
      children.push(textRun(stripMarkdown(token), { ...options, bold: true }));
    } else {
      const linkMatch = token.match(/^\[([^\]]+)\]\(([^)]+)\)$/);
      if (linkMatch) {
        const [, label, url] = linkMatch;
        if (/^https?:\/\//.test(url)) {
          children.push(
            new ExternalHyperlink({
              link: url,
              children: [textRun(label, { ...options, color: "0563C1" })],
            })
          );
        } else {
          children.push(textRun(`${label} (${url})`, options));
        }
      }
    }
    lastIndex = regex.lastIndex;
  }

  if (lastIndex < text.length) {
    children.push(textRun(decodeEntities(text.slice(lastIndex)), options));
  }

  return new Paragraph({
    children: children.length ? children : [textRun(stripMarkdown(text), options)],
    spacing: { after: options.after || 120, line: 330 },
    alignment: options.alignment || AlignmentType.LEFT,
    bullet: options.bullet,
  });
}

function heading(text, level) {
  const map = {
    1: HeadingLevel.TITLE,
    2: HeadingLevel.HEADING_1,
    3: HeadingLevel.HEADING_2,
    4: HeadingLevel.HEADING_3,
  };
  const size = level === 1 ? 34 : level === 2 ? 30 : level === 3 ? 26 : 24;
  return new Paragraph({
    text: stripMarkdown(text),
    heading: map[level] || HeadingLevel.HEADING_4,
    spacing: { before: level === 1 ? 80 : 220, after: 120 },
    children: [textRun(stripMarkdown(text), { size, bold: true })],
  });
}

function imageParagraph(line) {
  const match = line.match(/^!\[([^\]]*)\]\(([^)]+)\)$/);
  if (!match) return null;
  const alt = match[1] || "figure";
  const target = match[2];
  const resolved = path.isAbsolute(target) ? target : path.resolve(baseDir, target);
  if (!fs.existsSync(resolved)) {
    return [paragraph(`[Missing image: ${alt} - ${target}]`)];
  }
  const ext = path.extname(resolved).toLowerCase();
  if (![".png", ".jpg", ".jpeg"].includes(ext)) {
    return [paragraph(`[Unsupported image format: ${alt} - ${resolved}]`)];
  }

  const buffer = fs.readFileSync(resolved);
  const imageBlock = new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { before: 120, after: 80 },
    children: [
      new ImageRun({
        data: buffer,
        transformation: {
          width: 520,
          height: 300,
        },
      }),
    ],
  });

  const captionBlock = new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 120 },
    children: [textRun(alt, { italics: true, size: 20, color: "44546A" })],
  });

  return [imageBlock, captionBlock];
}

function convert(markdown) {
  const lines = markdown.split("\n");
  const children = [];
  let inCode = false;
  let codeBuffer = [];

  for (const rawLine of lines) {
    const line = rawLine.trimEnd();

    if (line.startsWith("```")) {
      if (inCode) {
        children.push(
          new Paragraph({
            children: [textRun(codeBuffer.join("\n"), { color: "44546A", size: 19 })],
            spacing: { before: 80, after: 120 },
          })
        );
        codeBuffer = [];
        inCode = false;
      } else {
        inCode = true;
      }
      continue;
    }

    if (inCode) {
      codeBuffer.push(rawLine);
      continue;
    }

    if (!line.trim()) continue;
    if (/^---+$/.test(line.trim())) {
      children.push(new Paragraph({ children: [new PageBreak()] }));
      continue;
    }

    const img = imageParagraph(line.trim());
    if (img) {
      children.push(...img);
      continue;
    }

    const headingMatch = line.match(/^(#{1,6})\s+(.+)$/);
    if (headingMatch) {
      children.push(heading(headingMatch[2], headingMatch[1].length));
      continue;
    }

    const bulletMatch = line.match(/^\s*[-*]\s+(.+)$/);
    if (bulletMatch) {
      children.push(paragraph(stripMarkdown(bulletMatch[1]), { bullet: { level: 0 } }));
      continue;
    }

    const orderedMatch = line.match(/^\s*\d+\.\s+(.+)$/);
    if (orderedMatch) {
      children.push(paragraph(stripMarkdown(orderedMatch[1]), { bullet: { level: 0 } }));
      continue;
    }

    children.push(paragraph(line.trim()));
  }

  return children;
}

const doc = new Document({
  creator: "Codex",
  title: path.basename(inputPath),
  description: "Generated from Markdown for the underwater image enhancement paper draft.",
  sections: [
    {
      properties: {
        page: {
          margin: {
            top: 1134,
            right: 1134,
            bottom: 1134,
            left: 1134,
          },
        },
      },
      children: convert(source),
    },
  ],
});

Packer.toBuffer(doc)
  .then((buffer) => {
    fs.writeFileSync(outputPath, buffer);
    console.log(`Wrote ${outputPath}`);
  })
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
