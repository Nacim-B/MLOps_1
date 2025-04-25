# 🧠 MLOps Project Template

Welcome to the documentation for your MLOps pipeline project.  
This project aims to provide a complete, automated, and production-ready machine learning pipeline.

---

## 📦 Project structure

- `config/` – Project configuration (YAML-based)
- `run/` – Executable scripts for each pipeline step (download, preprocess, train, predict)
- `utils/` – Utility modules for S3, preprocessing, modeling, etc.
- `infra/` – Cloud infrastructure (e.g., AWS CloudFormation)
- `docs/` – Project documentation (this site)

---

## 🚀 Purpose

This MLOps template is designed to:

- Train and retrain models on a schedule
- Run automated predictions
- Use CI/CD pipelines via GitHub Actions
- Be fully documented with MkDocs & GitHub Pages
