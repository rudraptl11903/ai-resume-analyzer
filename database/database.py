"""
database.py
Local SQLite storage for resumes, analysis history, and target roles.
Explainable, zero-cloud, and interview-ready.
"""

import os
import sqlite3
import pandas as pd
from datetime import datetime
from typing import Dict, Any, List, Optional

DB_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DB_DIR, "resume_analyzer.db")


def get_db_connection() -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes tables for resumes, analysis history, and job roles."""
    os.makedirs(DB_DIR, exist_ok=True)
    with get_db_connection() as conn:
        cursor = conn.cursor()

        # Resumes table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS resumes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                candidate_name TEXT,
                email TEXT,
                phone TEXT,
                raw_text TEXT,
                page_count INTEGER DEFAULT 1,
                file_hash TEXT UNIQUE,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        # Analysis History table
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS analysis_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                resume_id INTEGER,
                target_role TEXT,
                overall_score REAL,
                ats_score REAL,
                match_percentage REAL,
                skills_count INTEGER,
                matched_skills TEXT,
                missing_skills TEXT,
                analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (resume_id) REFERENCES resumes(id) ON DELETE CASCADE
            )
            """
        )

        # Job Roles table (user custom or imported)
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS job_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role_key TEXT UNIQUE,
                role_title TEXT NOT NULL,
                category TEXT,
                experience_level TEXT,
                required_skills TEXT,
                preferred_skills TEXT,
                description TEXT
            )
            """
        )
        conn.commit()


def save_resume(
    filename: str,
    candidate_name: str,
    email: str,
    phone: str,
    raw_text: str,
    page_count: int = 1,
    file_hash: str = ""
) -> int:
    """
    Saves or retrieves existing resume by file hash.
    Returns the resume ID.
    """
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if file_hash:
            cursor.execute("SELECT id FROM resumes WHERE file_hash = ?", (file_hash,))
            row = cursor.fetchone()
            if row:
                return row["id"]

        cursor.execute(
            """
            INSERT INTO resumes (filename, candidate_name, email, phone, raw_text, page_count, file_hash)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (filename, candidate_name, email, phone, raw_text, page_count, file_hash)
        )
        conn.commit()
        return cursor.lastrowid


def save_analysis(
    resume_id: int,
    target_role: str,
    overall_score: float,
    ats_score: float,
    match_percentage: float,
    skills_count: int,
    matched_skills: str,
    missing_skills: str
) -> int:
    """Stores an analysis result linked to a resume."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO analysis_history (
                resume_id, target_role, overall_score, ats_score,
                match_percentage, skills_count, matched_skills, missing_skills
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                resume_id, target_role, overall_score, ats_score,
                match_percentage, skills_count, matched_skills, missing_skills
            )
        )
        conn.commit()
        return cursor.lastrowid


def get_recent_analyses(limit: int = 10) -> List[Dict[str, Any]]:
    """Retrieves recent resume evaluations joined with resume metadata."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                a.id, a.target_role, a.overall_score, a.ats_score,
                a.match_percentage, a.skills_count, a.analyzed_at,
                r.filename, r.candidate_name, r.email
            FROM analysis_history a
            LEFT JOIN resumes r ON a.resume_id = r.id
            ORDER BY a.analyzed_at DESC
            LIMIT ?
            """,
            (limit,)
        )
        rows = cursor.fetchall()
        return [dict(row) for row in rows]


def get_analytics_summary() -> Dict[str, Any]:
    """Computes summary statistics across all processed resumes and analyses."""
    init_db()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as total_resumes FROM resumes")
        total_resumes = cursor.fetchone()["total_resumes"]

        cursor.execute("SELECT COUNT(*) as total_scans, AVG(overall_score) as avg_score, AVG(ats_score) as avg_ats FROM analysis_history")
        scan_row = cursor.fetchone()
        total_scans = scan_row["total_scans"] or 0
        avg_score = round(scan_row["avg_score"] or 0.0, 1)
        avg_ats = round(scan_row["avg_ats"] or 0.0, 1)

        return {
            "total_resumes": total_resumes,
            "total_scans": total_scans,
            "avg_score": avg_score,
            "avg_ats": avg_ats,
        }


def load_default_roles_if_empty(csv_path: Optional[str] = None) -> None:
    """Pre-populates job roles from data/job_roles.csv if table is empty."""
    init_db()
    if csv_path is None:
        csv_path = os.path.abspath(os.path.join(DB_DIR, "..", "data", "job_roles.csv"))

    if not os.path.exists(csv_path):
        return

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM job_roles")
        if cursor.fetchone()["count"] == 0:
            df = pd.read_csv(csv_path)
            for _, row in df.iterrows():
                cursor.execute(
                    """
                    INSERT OR IGNORE INTO job_roles (
                        role_key, role_title, category, experience_level,
                        required_skills, preferred_skills, description
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        str(row.get("role_id", "")),
                        str(row.get("role_title", "")),
                        str(row.get("category", "")),
                        str(row.get("experience_level", "")),
                        str(row.get("required_skills", "")),
                        str(row.get("preferred_skills", "")),
                        str(row.get("description", "")),
                    )
                )
            conn.commit()


if __name__ == "__main__":
    init_db()
    load_default_roles_if_empty()
    print(f"Database successfully initialized at {DB_PATH}")
