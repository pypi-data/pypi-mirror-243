"""matplatex: export matplotlib figures as pdf and text separately for
use in LaTeX.

Copyright (C) 2023 Johannes Sørby Heines

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from functools import cached_property
from collections.abc import Iterator

import matplotlib.pyplot as plt
from beartype import beartype

from .latex_input import LaTeXinput

def write_tex(output: LaTeXinput, fig, *, graphics, add_anchors=False):
    output.includegraphics(graphics)
    for element in extract_text(fig):
        if add_anchors:  # useful for checking positioning
            draw_anchors(fig, element.position_in_figure)
        output.add_text(
            element.text,
            position=element.position_in_figure,
            anchor=element.tikz_anchor,
            rotation=element.rotation)


class FigureText:
    """Contain text and its tikz properties."""
    def __init__(
            self,
            text: plt.Text,
            fig: plt.Figure,
            ax: plt.Axes | None):
        """Constructor for the FigureText class."""
        self.mpl_text = text
        self._figure_transform = fig.transFigure
        self._ax = ax

    def __str__(self):
        return (
            f"FigureText({self.mpl_text}, position={self._figure_xy}, "
            f"visible={self._visible}, tikz_anchor={self._tikz_anchor})")

    @property
    def text(self) -> str:
        return self.mpl_text.get_text()

    @property  # Disconnect from attribute so I can change how it works.
    def position_in_figure(self) -> tuple[float]:
        return self._figure_xy

    @property
    def rotation(self) -> float:
        return self.mpl_text.get_rotation()

    @property
    def color(self):
        return self.mpl_text.get_color()

    @color.setter
    def color(self, value, /):
        self.mpl_text.set_color(value)

    @cached_property
    def tikz_anchor(self) -> str:
        anchor_by_va = {
            'bottom': 'south',
            'top': 'north',
            'center': '',
            'baseline': 'base',
            'center_baseline': 'mid'
            }
        anchor_by_ha = {
            'right': 'east',
            'left': 'west',
            'center': ''
            }
        anchor = (f"{anchor_by_va[self.mpl_text.get_va()]} "
                  f"{anchor_by_ha[self.mpl_text.get_ha()]}")
        if anchor == ' ':
            anchor = 'center'
        return anchor

    @cached_property
    def visible(self) -> bool:
        if not self.mpl_text.get_visible():
            return False
        elif self._ax is None or not self.mpl_text.get_clip_on():
            return True
        else:
            return self._is_inside_ax()

    @cached_property
    def _display_xy(self):
        return self.mpl_text.get_transform().transform(
            self.mpl_text.get_position())

    @cached_property
    def _figure_xy(self):
        return self._figure_transform.inverted().transform(self._display_xy)

    @cached_property
    def _axes_xy(self):
        if self._ax is None:
            raise ValueError("This text does not belong to any Axes")
        return self._ax.transAxes.inverted().transform(self._display_xy)

    def _is_inside_ax(self):
        x, y = self._axes_xy
        if (0 <= x <= 1) or (0 <= y <= 1):
            return True
        else:
            return False


@beartype
def extract_text(fig: plt.Figure, /):
    return remove_transparent(remove_empty(remove_invisible(
        set(get_text_decendents(fig)))))

def remove_invisible(text_set: set, /):
    return {element for element in text_set if element.visible}

def remove_empty(text_set: set, /):
    return {element for element in text_set if element.text != ''}

def remove_transparent(text_set: set, /):
    return {element for element in text_set if element.color != 'none'}

@beartype
def make_all_transparent(fig: plt.Figure, /):
    removed_colors = {}
    for text in get_text_decendents(fig):
        removed_colors[text.mpl_text] = text.color
        text.color = "none"  # avoids messing with the whitespace
    return removed_colors

@beartype
def restore_colors(fig: plt.Figure, colors: dict):
    for text in get_text_decendents(fig):
        text.color = colors[text.mpl_text]

@beartype
def get_text_decendents(fig: plt.Figure, /) -> Iterator[FigureText]:
    stack = [iter(fig.get_children())]
    current_ax = None
    while stack:
        try:
            child = next(stack[-1])
            if isinstance(child, plt.Text):
                yield FigureText(text=child, fig=fig, ax=current_ax)
            else:
                if isinstance(child, plt.Axes):
                    current_ax = child
                stack.append(iter(child.get_children()))
        except StopIteration:
            stack.pop()

def draw_anchors(fig, figure_xy):
    ax = fig.get_children()[1]
    ax.plot(figure_xy[0], figure_xy[1], '+r', clip_on=False,
            transform=fig.transFigure, zorder=20)

def print_family_tree(mpl_object):
    stack = [iter(mpl_object.get_children())]
    print(stack)
    indent = ""
    while stack:
        try:
            child = next(stack[-1])
            print(f"{indent}{child}")
            stack.append(iter(child.get_children()))
            indent = indent[:-2]
            indent += "  |- "
        except StopIteration:
            indent = indent[:-5]
            indent += "- "
            stack.pop()
