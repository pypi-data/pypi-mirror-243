from __future__ import annotations

from typing import Any, TypeVar, cast

from holoviews import save

from utilities.atomicwrites import writer
from utilities.pathlib import PathLike

_T = TypeVar("_T")


def apply_opts(plot: _T, /, **opts: Any) -> _T:
    """Apply a set of options to a plot."""
    return cast(Any, plot).opts(**opts)


def relabel_plot(plot: _T, label: str, /) -> _T:
    """Re-label a plot."""
    return cast(Any, plot).relabel(label)


def save_plot(plot: Any, path: PathLike, /, *, overwrite: bool = False) -> None:
    """Atomically save a plot to disk."""
    with writer(path, overwrite=overwrite) as temp:  # pragma: os-ne-linux
        save(plot, temp, backend="bokeh")


__all__ = ["apply_opts", "relabel_plot", "save_plot"]
