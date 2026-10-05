"""
components.py
Reusable, modular UI components following the ChatGPT minimal black-and-white design.
Includes top bar, circular progress SVG rings, metric cards, and semantic badges.
"""

import math
from typing import Optional, List, Dict, Any
import streamlit as st


def get_semantic_color(color_name: str) -> str:
    """Returns HEX code for semantic colors strictly used for information."""
    mapping = {
        "green": "#10B981",   # Good / Matched / Success
        "red": "#EF4444",     # Missing / Problem / Low
        "blue": "#3B82F6",    # Info / Metadata
        "purple": "#8B5CF6",  # AI / Recommendation
        "orange": "#F59E0B",  # Warning / Moderate
        "neutral": "#111827", # High contrast black
        "gray": "#6B7280"     # Neutral secondary
    }
    return mapping.get(color_name.lower(), "#111827")


def render_circular_progress(
    score: float,
    label: str,
    sublabel: str = "",
    color_type: str = "auto",
    max_value: float = 100.0,
    size: int = 110,
    suffix: str = "%"
) -> str:
    """
    Generates a crisp, responsive SVG circular progress indicator.
    """
    clamped_score = max(0.0, min(float(score), float(max_value)))
    pct = clamped_score / float(max_value)

    # Auto color determination based on score
    if color_type == "auto":
        if pct >= 0.80:
            stroke_color = "#10B981"  # Green
        elif pct >= 0.65:
            stroke_color = "#3B82F6"  # Blue
        elif pct >= 0.45:
            stroke_color = "#F59E0B"  # Orange
        else:
            stroke_color = "#EF4444"  # Red
    else:
        stroke_color = get_semantic_color(color_type)

    radius = 38
    stroke_width = 7
    circumference = 2 * math.pi * radius
    offset = circumference * (1.0 - pct)
    val_display = int(round(clamped_score)) if suffix == "%" else f"{round(clamped_score, 1)}"

    svg = f"""
    <div class="circular-progress-card">
        <svg width="{size}" height="{size}" viewBox="0 0 100 100" class="circular-svg">
            <circle class="circular-bg" cx="50" cy="50" r="{radius}" stroke-width="{stroke_width}" />
            <circle class="circular-fg" cx="50" cy="50" r="{radius}" stroke="{stroke_color}" stroke-width="{stroke_width}"
                    stroke-dasharray="{circumference:.2f}" stroke-dashoffset="{offset:.2f}" />
            <text x="50" y="52" class="circular-text" text-anchor="middle" dominant-baseline="central" transform="rotate(90 50 50)">
                {val_display}{suffix}
            </text>
        </svg>
        <div class="circular-label">{label}</div>
        {f'<div class="circular-sublabel">{sublabel}</div>' if sublabel else ''}
    </div>
    """
    return svg


def render_top_bar(current_page: str, candidate_name: Optional[str] = None):
    """
    Renders top bar with breadcrumbs, mock search bar, notifications, and profile.
    """
    cand = candidate_name or "Alex Chen"
    initials = "".join([part[0] for part in cand.split() if part])[:2].upper() or "RP"

    top_html = f"""
    <div class="top-nav-bar">
        <div class="top-nav-left">
            <div class="top-breadcrumb">
                <span>AI Resume Analyzer</span>
                <span>/</span>
                <span class="top-breadcrumb-active">{current_page}</span>
            </div>
        </div>
        <div class="top-nav-right">
            <div class="top-search-mock">
                <span>🔍 Search skills, roles, metrics...</span>
                <span class="top-search-kbd">⌘K</span>
            </div>
            <div class="top-icon-btn" title="System Notifications">
                <span>🔔</span>
                <div class="notification-dot"></div>
            </div>
            <div class="top-profile-badge" title="Active Candidate Profile">
                <div class="top-profile-avatar">{initials}</div>
                <div class="top-profile-name">{cand}</div>
            </div>
        </div>
    </div>
    """
    st.markdown(top_html, unsafe_allow_html=True)


def render_clean_card(title: str, description: str, icon: str = "", extra_badge: str = "") -> str:
    """
    Renders a clean white card with subtle border and optional icon/badge.
    """
    badge_html = f'<span class="pill-tag pill-neutral" style="float: right; margin-top: -2px;">{extra_badge}</span>' if extra_badge else ''
    icon_html = f'<span style="font-size: 1.25rem; margin-right: 6px;">{icon}</span>' if icon else ''

    return f"""
    <div class="clean-card">
        {badge_html}
        <div class="card-heading">{icon_html}{title}</div>
        <div class="card-subtext">{description}</div>
    </div>
    """


def render_pill(text: str, pill_type: str = "neutral") -> str:
    """
    Renders a semantic pill badge (neutral, green, red, blue, purple, orange).
    """
    return f'<span class="pill-tag pill-{pill_type}">{text}</span>'


def render_status_alert(message: str, alert_type: str = "blue", title: str = "") -> None:
    """
    Renders an inline alert box with semantic coloring.
    """
    icon_map = {
        "green": "✅",
        "red": "❌",
        "blue": "ℹ️",
        "purple": "💡",
        "orange": "⚠️"
    }
    icon = icon_map.get(alert_type, "ℹ️")
    title_html = f'<div style="font-weight: 600; margin-bottom: 2px;">{title}</div>' if title else ''

    html = f"""
    <div class="status-box status-box-{alert_type}">
        <div style="font-size: 1.15rem; line-height: 1;">{icon}</div>
        <div>
            {title_html}
            <div>{message}</div>
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
