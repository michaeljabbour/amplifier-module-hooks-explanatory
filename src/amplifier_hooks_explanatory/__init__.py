"""Amplifier Hook Module: Explanatory Output Style.

Injects educational style instructions at session start, encouraging
the model to provide Insight blocks with implementation explanations.

Equivalent to the Claude Code explanatory-output-style plugin.
"""

from .main import mount

__all__ = ["mount"]
__version__ = "0.1.0"
