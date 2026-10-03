"""
helpers.py
Utility helpers for Plotly interactive visualizations, session state initialization,
hashing, and aesthetic badge rendering.
"""

import hashlib
from typing import Dict, List, Any
import plotly.graph_objects as go
import plotly.express as px


def calculate_file_hash(content: bytes) -> str:
    """Computes SHA-256 hash of file content to identify duplicates."""
    return hashlib.sha256(content).hexdigest()


def create_gauge_chart(score: float, title: str = "Overall Score", max_val: float = 100.0) -> go.Figure:
    """
    Renders an interactive speedometer / gauge chart for scores using Plotly.
    """
    # Color logic
    if score >= 80:
        bar_color = "#10B981"  # Emerald
    elif score >= 60:
        bar_color = "#3B82F6"  # Blue
    elif score >= 40:
        bar_color = "#F59E0B"  # Amber
    else:
        bar_color = "#EF4444"  # Red

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            domain={"x": [0, 1], "y": [0, 1]},
            title={"text": f"<b>{title}</b>", "font": {"size": 18, "color": "#1E293B"}},
            number={"suffix": "/100", "font": {"size": 32, "color": "#0F172A", "family": "Inter, sans-serif"}},
            gauge={
                "axis": {"range": [0, max_val], "tickwidth": 1, "tickcolor": "#94A3B8"},
                "bar": {"color": bar_color, "thickness": 0.28},
                "bgcolor": "#F1F5F9",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 40], "color": "rgba(239, 68, 68, 0.12)"},
                    {"range": [40, 70], "color": "rgba(245, 158, 11, 0.12)"},
                    {"range": [70, 85], "color": "rgba(59, 130, 246, 0.12)"},
                    {"range": [85, 100], "color": "rgba(16, 185, 129, 0.15)"},
                ],
                "threshold": {
                    "line": {"color": bar_color, "width": 4},
                    "thickness": 0.75,
                    "value": score,
                },
            },
        )
    )
    fig.update_layout(
        height=240,
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"},
    )
    return fig


def create_radar_chart(categories: List[str], values: List[float], title: str = "Dimension Assessment") -> go.Figure:
    """
    Renders a radar / spider chart assessing multidimensional resume attributes.
    """
    if not categories or not values:
        categories = ["ATS Compliance", "Skill Breadth", "Section Health", "Impact Verbs", "Quantification"]
        values = [75, 80, 85, 60, 70]

    # Close the radar loop
    r_vals = values + [values[0]]
    theta_cats = categories + [categories[0]]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=r_vals,
            theta=theta_cats,
            fill="toself",
            fillcolor="rgba(79, 70, 229, 0.22)",
            line={"color": "#4F46E5", "width": 2.5},
            marker={"size": 6, "color": "#4338CA"},
        )
    )
    fig.update_layout(
        polar={
            "radialaxis": {
                "visible": True,
                "range": [0, 100],
                "tickfont": {"size": 10, "color": "#64748B"},
            },
            "angularaxis": {
                "tickfont": {"size": 12, "color": "#1E293B", "family": "Inter, sans-serif"}
            },
            "bgcolor": "rgba(248, 250, 252, 0.5)",
        },
        showlegend=False,
        title={"text": f"<b>{title}</b>", "x": 0.5, "font": {"size": 16, "color": "#1E293B"}},
        height=320,
        margin={"l": 40, "r": 40, "t": 50, "b": 30},
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def create_skills_comparison_chart(matched_count: int, missing_count: int) -> go.Figure:
    """
    Renders an elegant donut chart comparing matched vs missing target skills.
    """
    labels = ["Matched Skills", "Missing Skills"]
    values = [matched_count, missing_count]
    colors = ["#10B981", "#EF4444"]

    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.55,
                marker={"colors": colors},
                textinfo="label+value",
                hoverinfo="label+value+percent",
            )
        ]
    )
    fig.update_layout(
        showlegend=True,
        legend={"orientation": "h", "yanchor": "bottom", "y": -0.2, "xanchor": "center", "x": 0.5},
        height=260,
        margin={"l": 20, "r": 20, "t": 20, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"},
    )
    return fig


def create_category_bar_chart(category_dict: Dict[str, List[str]]) -> go.Figure:
    """
    Renders a clean horizontal bar chart displaying skill distribution across domains.
    """
    categories = list(category_dict.keys())
    counts = [len(v) for v in category_dict.values()]

    fig = go.Figure(
        go.Bar(
            x=counts,
            y=categories,
            orientation="h",
            marker={"color": "#6366F1", "cornerradius": 4},
            text=counts,
            textposition="auto",
        )
    )
    fig.update_layout(
        title={"text": "<b>Skills by Domain</b>", "font": {"size": 15, "color": "#1E293B"}},
        xaxis_title="Skill Count",
        height=260,
        margin={"l": 20, "r": 20, "t": 40, "b": 20},
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"family": "Inter, sans-serif"},
    )
    return fig
