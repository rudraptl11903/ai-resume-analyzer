"""
Database package for AI Resume Analyzer & Job Matcher.
Manages SQLite connections, schema initialization, and persistence.
"""
from .database import (
    init_db,
    get_db_connection,
    save_resume,
    save_analysis,
    get_recent_analyses,
    get_analytics_summary,
    load_default_roles_if_empty
)

__all__ = [
    "init_db",
    "get_db_connection",
    "save_resume",
    "save_analysis",
    "get_recent_analyses",
    "get_analytics_summary",
    "load_default_roles_if_empty",
]
