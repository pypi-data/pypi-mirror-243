import pytest
import matplatex.tools as tools

import matplotlib.pyplot as plt

@pytest.fixture
def make_simple_figure():
    """Make a figure with a single subplot and unique text objects."""
    fig, ax = plt.subplots()
    ax.plot([0,2], [1,0])
    ax.set_xlabel("x axis label")
    ax.set_ylabel("y axis label")
    ax.set_title("axis title")
    ax.set_xticks([0, 1, 2], ['none', 'I', 'II'])
    ax.set_yticks([0, 1/3, 2/3, 1], ['0', '1/3', '2/3', '1'])
    visible_text_objects = set(
        [ax.title, ax.xaxis.label, ax.yaxis.label]
        + ax.get_xticklabels()
        + ax.get_yticklabels()
        )
    return fig, visible_text_objects

def test_get_text(make_simple_figure):
    result = {text.mpl_text for text in
              tools.extract_text(make_simple_figure[0])}
    expected = make_simple_figure[1]
    assert result == expected

def test_make_all_transparent(make_simple_figure):
    tools.make_all_transparent(make_simple_figure[0])
    assert tools.extract_text(make_simple_figure[0]) == set()

def test_restore_colors(make_simple_figure):
    initial_state = {t.mpl_text for t in
                     tools.extract_text(make_simple_figure[0])}
    removed_colors = tools.make_all_transparent(make_simple_figure[0])
    tools.restore_colors(make_simple_figure[0], removed_colors)
    final_state = {t.mpl_text for t in
                   tools.extract_text(make_simple_figure[0])}
    assert initial_state == final_state

@pytest.fixture
def text_only_figure():
    fig = plt.Figure()
    fig.add_artist(plt.Text(0.42, 0.2845, 'text'))
    return fig

def test_get_position_in_figure(text_only_figure):
    text = tools.extract_text(text_only_figure)
    result = text.pop().position_in_figure
    expected = (0.42, 0.2845)
    tolerance = 1e-4
    assert abs(result[0] - expected[0]) < tolerance
    assert abs(result[1] - expected[1]) < tolerance

@pytest.fixture
def figure_with_clipped_text():
    fig, ax = plt.subplots()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.add_artist(plt.Text( 0.7, 0.2, 'text inside axes'))
    ax.add_artist(plt.Text( 1.1, 1.8, 'text outside axes'))
    return fig

def test_is_inside_ax(figure_with_clipped_text):
    expected_by_text = {
        'text inside axes': True,
        'text outside axes': False}
    for text in tools.extract_text(figure_with_clipped_text):
        result = text._is_inside_ax()
        expected = expected_by_text[text.text]

@pytest.fixture
def figure_with_multiple_axes():
    fig, [ax1, ax2] = plt.subplots(1,2)
    fig.add_artist(plt.Text(0.5, 0.5, 'figure text'))
    ax1.annotate('ax1 text', (3.14, 6.28))
    ax2.annotate('ax2 text', (0.35, 6.6))
    return fig

def test_ax_identification(figure_with_multiple_axes):
    expected_by_text = {
        'figure text': None,
        'ax1 text': figure_with_multiple_axes.get_axes()[0],
        'ax2 text': figure_with_multiple_axes.get_axes()[1]}
    for text in tools.extract_text(figure_with_multiple_axes):
        result = text._ax
        expected = expected_by_text[text.text]
        assert result == expected
