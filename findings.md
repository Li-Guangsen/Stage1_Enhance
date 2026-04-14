# Research Findings

## Research Question

How can we strengthen underwater harmful algal bloom microscopic image enhancement so that color recovery, fine texture visibility, and downstream edge extractability all improve in a measurable and publishable way?

## Current Understanding

The current repository already contains a coherent enhancement system rather than a loose collection of filters. The main pipeline is: task-specific white balance and color compensation, three complementary enhancement branches, gated multiscale fusion, and final illumination refinement. The strongest scientific distinction is not the presence of EMD, CLAHE, or RGHS alone, but the way these components are structured and fused for HAB microscopic imagery.

The codebase does not exactly implement the published reference methods. Instead, it has evolved into a modified pipeline whose most defensible novelties are: gray-pixel-guided clipped ACCC-style white balance, an IMF1Ray branch that mixes 2D-EMD with Rayleigh matching and edge-aware high-frequency injection, and a feature-gated three-branch fusion strategy. This is important because the paper should describe what the code actually does, not simply inherit the wording of the reference papers.

## Key Results

- The current enhancement workflow is fully implemented and runnable in the repository.
- Existing metric logs suggest strong enhancement behavior on several no-reference and downstream-friendly indicators, but the evaluation subsets are currently inconsistent across files and need to be re-standardized before formal use in a paper.
- The reference papers confirm that enhancement-to-edge-detection validation is a credible and publication-tested argument for this task family.
- A first controlled pilot subset is now locked: 92 images corresponding to the currently completed run under `results/png/Final`. This is enough to start real ablations without waiting for a full 506-image sweep.

## Patterns and Insights

- The white-balance stage is already more project-specific than the published cyclic compensation baseline and is likely a real contribution if supported by controlled ablation.
- The fusion stage is the clearest code-level innovation and likely the best core method section for a first paper.
- The project is currently strongest as an enhancement paper with downstream edge-validation, not yet as a fully unified “new enhancement + new edge detector” paper unless edge-network experiments are made equally mature.
- From a research-planning standpoint, the best first ablation is H2 rather than H1. H2 directly tests whether the project's main compositional claim is real, and it can be executed with fewer new implementation branches than the white-balance redesign.

## Lessons and Constraints

- The published papers are useful for experiment organization, but their method wording cannot be copied over because the current code differs materially.
- Existing metrics cannot be treated as final paper evidence until all methods are re-evaluated on the same locked subset and file format.
- JPEG should not be the final experimental result format for enhancement outputs; the code has already been updated to save both PNG and JPG, which supports cleaner future evaluation.
- IMF1/EMD is the dominant runtime bottleneck; experiment planning should treat it as the expensive stage.
- The repository is not currently a git repository, so the autoresearch skill's protocol-first commit workflow cannot yet be used as-is in this workspace.

## Open Questions

- Which exact combination of metrics should serve as the locked primary enhancement objective?
- How much of the gain comes from the IMF1 branch vs the gated fusion vs the white-balance redesign?
- What is the most convincing downstream validation path for the first paper: SIFT/ORB + classical edge detectors, or a stronger neural edge baseline?

## Optimization Trajectory

No autoresearch-controlled experiment trajectory has been recorded yet. The next milestone is a standardized PNG rerun on `pilot92-v1`, followed by H2/H1/H3 ablations under the locked evaluation protocol.
