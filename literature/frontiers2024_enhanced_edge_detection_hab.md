# Frontiers 2024: HAB Edge Detection After Enhancement

## Citation

- Title: `Enhanced edge detection of harmful algal Blooms using diffusion probability models and Sobel-convolutional attention mechanisms`
- Venue: `Frontiers in Marine Science`
- Year: 2024
- URL: `https://www.frontiersin.org/journals/marine-science/articles/10.3389/fmars.2024.1471014/full`

## Why It Matters Here

This paper is directly relevant to the downstream-validation story. It strengthens the argument that HAB microscopy work can legitimately connect enhancement and edge-sensitive analysis instead of treating enhancement as a purely aesthetic preprocessing step.

## Most Relevant Takeaway

The most useful lesson is not the exact edge architecture, but the paper's framing: edge extraction quality can be treated as a task-relevant endpoint for HAB image processing. That helps justify the current project's intended paper structure of "enhancement method plus downstream edge-oriented validation."

## How It Connects to the Current Code

- Supports a task-driven evaluation narrative rather than a metric-only enhancement narrative
- Helps bridge the current enhancement repository to a later edge-detection stage without forcing both contributions into one method claim immediately
- Suggests that classical edge evidence can later be extended toward stronger downstream models if needed

## Caution

This paper should be used as a downstream-task reference, not as proof that the current project already contains an equivalent edge-detection contribution.
