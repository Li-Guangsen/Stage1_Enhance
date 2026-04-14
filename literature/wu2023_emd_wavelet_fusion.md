# Wu et al. 2023: EMD and Wavelet Fusion for HAB Enhancement

## Citation

- Title: `Numerical computation of ocean HABs image enhancement based on empirical mode decomposition and wavelet fusion`
- Venue: `Applied Intelligence`
- Year: 2023
- DOI: `10.1007/s10489-023-04502-x`
- URL: `https://doi.org/10.1007/s10489-023-04502-x`

## Why It Matters Here

This paper is not the same as the current repository, but it is an important lineage paper for the decomposition-oriented branch. It gives historical support for using decomposition and fusion ideas on HAB imagery and helps justify why the current project's IMF1/EMD branch is not appearing from nowhere.

## Most Relevant Takeaway

The main value of this paper for the current project is conceptual rather than literal implementation reuse: decomposition-based enhancement can be argued as a meaningful way to recover fine structure in algae imagery, but the current repository's IMF1Ray branch must still be described on its own terms.

## How It Connects to the Current Code

- Supports the use of decomposition-driven detail extraction as a legitimate design family
- Helps position the current `pybemd.py` branch as an evolved project-specific implementation rather than an isolated heuristic
- Can be cited in the related work section when discussing decomposition-based enhancement lines

## Caution

Do not describe the current repository as a reproduction of this paper. Use it as lineage, not identity.
