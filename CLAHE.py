"""Compatibility shim for the historical `CLAHE` module name.

Primary implementation now lives in `clahe_guided_visibility.py`.
"""

from clahe_guided_visibility import PRESETS, clahe_3ch_wb_safe

__all__ = ["PRESETS", "clahe_3ch_wb_safe"]
