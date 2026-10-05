"""
demo_data.py
Rich, realistic demo resume for demonstration, testing, and portfolio showcases.
Allows users to experience the full AI Resume Analyzer without needing to upload a file first.
"""

from typing import Dict, Any
from nlp.resume_parser import parse_resume
from analyzer.resume_score import calculate_resume_score

DEMO_RESUME_TEXT = """Alex Chen
San Francisco, CA | (650) 492-8173 | alex.chen@stanford.edu | linkedin.com/in/alexchen-dev | github.com/alexchen-eng | alexchen.dev

PROFESSIONAL SUMMARY
Results-driven Software Engineer with a strong foundation in distributed backend systems, full-stack web applications, and applied machine learning. Proven track record of architecting high-throughput microservices, reducing database latency by 42%, and delivering scalable features for over 15,000 active users. Passionate about automated testing, clean code, and ATS-optimized engineering standards.

TECHNICAL SKILLS
Languages: Python, Java, C++, TypeScript, JavaScript, SQL, Bash
Web Frameworks: React, Next.js, FastAPI, Node.js, Express.js, Tailwind CSS
Databases & Cache: PostgreSQL, MongoDB, Redis, SQLite
Cloud & DevOps: Docker, Kubernetes, AWS (S3, EC2, Lambda), Git, GitHub Actions, CI/CD, Linux, Nginx
Machine Learning & Data: Scikit-learn, PyTorch, Pandas, NumPy, Data Analysis, TF-IDF
Methodologies: REST API Design, Microservices, Agile, Unit Testing, Test-Driven Development (TDD)

WORK EXPERIENCE
Software Engineering Intern | CloudScale Technologies | San Francisco, CA
June 2025 - September 2025
- Architected and deployed asynchronous background worker pipeline using Python, FastAPI, and Redis, reducing API endpoint response times by 42% for 15,000+ daily active users.
- Optimized PostgreSQL relational queries and added composite indexes, decreasing database read latency from 480ms to 95ms under peak traffic loads.
- Implemented comprehensive automated test suite with pytest, increasing backend code coverage from 68% to 92% and preventing regression defects.
- Collaborated in an Agile Scrum environment with 8 senior engineers, conducting peer code reviews and participating in weekly sprint planning.

Undergraduate Research Assistant | Stanford AI & Systems Lab | Stanford, CA
January 2025 - May 2025
- Engineered high-performance feature extraction pipeline with Scikit-learn and Pandas processing 250,000+ unstructured records.
- Deployed PyTorch neural network model inside Dockerized container with REST API endpoints, achieving 93.8% validation accuracy.
- Authored technical documentation and presented system benchmarks at regional undergraduate research symposium.

TECHNICAL PROJECTS
AI Resume Analyzer & Job Matcher | Python, Streamlit, Scikit-learn, PyMuPDF, SQLite
- Built an intelligent candidate evaluation engine parsing PDF resumes and computing TF-IDF cosine similarity against job descriptions.
- Engineered rule-based ATS compliance audit checking section completeness, action verbs, and quantifiable metrics with zero paid APIs.
- Designed responsive ChatGPT-style UI with interactive Plotly radar charts, donut graphs, and local SQLite persistence.

Real-Time Distributed Task Queue | Python, Redis, Docker, FastAPI
- Developed an asynchronous task distribution system utilizing Redis streams and Token Bucket rate-limiting algorithm.
- Benchmarked system throughput to successfully process over 5,000 tasks/second with sub-10ms queuing latency.
- Packaged services into multi-container Docker Compose setup with health checks and Prometheus metrics export.

EDUCATION
Bachelor of Science in Computer Science | Stanford University | Stanford, CA
Expected Graduation: June 2026 | GPA: 3.85 / 4.0
Relevant Coursework: Data Structures & Algorithms, Operating Systems, Database Systems, Computer Networks, Machine Learning, Software Engineering Principles

CERTIFICATIONS & LICENSES
- AWS Certified Cloud Practitioner (Amazon Web Services, 2025)
- HashiCorp Certified: Terraform Associate (HashiCorp, 2025)
"""


def get_demo_resume() -> Dict[str, Any]:
    """
    Parses and scores the demo resume, returning both parsed metadata and score breakdown.
    """
    parsed = parse_resume(DEMO_RESUME_TEXT, filename="Alex_Chen_Resume_Demo.pdf")
    score_data = calculate_resume_score(parsed)
    return {
        "resume_data": parsed,
        "resume_score": score_data,
        "file_hash": "demo_alex_chen_hash_778899",
    }
