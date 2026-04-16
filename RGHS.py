"""Compatibility shim for the historical `RGHS` module name.

Primary implementation now lives in `wb_safe_contrast.py`.
"""

from wb_safe_contrast import wb_safe_contrast

__all__ = ["wb_safe_contrast"]
