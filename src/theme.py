"""Color palette and Plotly template.

Palette values come from the studio dataviz skill's validated default
(references/palette.md): categorical hues are assigned in a fixed order
(never cycled/re-sorted by rank) so a given category always maps to the
same color across every chart, filters included.
"""

import plotly.graph_objects as go
import plotly.io as pio

SURFACE_LIGHT = "#fcfcfb"
TEXT_PRIMARY = "#0b0b0b"
TEXT_SECONDARY = "#52514e"
TEXT_MUTED = "#898781"
GRIDLINE = "#e1e0d9"
BASELINE = "#c3c2b7"

# Fixed-order categorical hues (slot 1..8). Never re-sorted by value/rank.
CATEGORICAL = [
    "#2a78d6",  # 1 blue
    "#eb6834",  # 2 orange
    "#1baf7a",  # 3 aqua
    "#eda100",  # 4 yellow
    "#e87ba4",  # 5 magenta
    "#008300",  # 6 green
    "#4a3aa7",  # 7 violet
    "#e34948",  # 8 red
]

# Sequential single-hue ramp (blue), light -> dark.
SEQUENTIAL_BLUE = [
    "#cde2fb", "#b7d3f6", "#9ec5f4", "#86b6ef", "#6da7ec",
    "#5598e7", "#3987e5", "#2a78d6", "#256abf", "#1c5cab",
    "#184f95", "#104281", "#0d366b",
]

# Diverging blue <-> red, neutral gray midpoint. Low->high (loss -> profit).
DIVERGING_SCALE = [
    (0.0, "#7a1414"),
    (0.25, "#d94f4f"),
    (0.5, "#f0efec"),
    (0.75, "#5598e7"),
    (1.0, "#104281"),
]
DIVERGING_NEG = "#b52020"
DIVERGING_POS = "#1c5cab"

STATUS = {
    "good": "#0ca30c",
    "warning": "#fab219",
    "serious": "#ec835a",
    "critical": "#d03b3b",
}


def category_color_map(categories: list[str]) -> dict[str, str]:
    """Assign fixed-order hues to a sorted category list so color follows entity."""
    ordered = sorted(categories)
    return {cat: CATEGORICAL[i % len(CATEGORICAL)] for i, cat in enumerate(ordered)}


def register_template() -> None:
    template = go.layout.Template()
    template.layout = go.Layout(
        paper_bgcolor=SURFACE_LIGHT,
        plot_bgcolor=SURFACE_LIGHT,
        font=dict(family="system-ui, -apple-system, 'Segoe UI', sans-serif", color=TEXT_PRIMARY, size=13),
        colorway=CATEGORICAL,
        title=dict(font=dict(size=15, color=TEXT_PRIMARY)),
        legend=dict(font=dict(color=TEXT_SECONDARY), bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(
            gridcolor=GRIDLINE, linecolor=BASELINE, zerolinecolor=BASELINE,
            tickfont=dict(color=TEXT_MUTED), title=dict(font=dict(color=TEXT_SECONDARY)),
        ),
        yaxis=dict(
            gridcolor=GRIDLINE, linecolor=BASELINE, zerolinecolor=BASELINE,
            tickfont=dict(color=TEXT_MUTED), title=dict(font=dict(color=TEXT_SECONDARY)),
        ),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    pio.templates["studio"] = template
    pio.templates.default = "studio"
