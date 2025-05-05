# 🛠️ MLOps Project Template

This repository provides a reusable MLOps project template for building, tracking, and deploying machine learning pipelines on AWS using modern tools such as:

- **Docker** & **ECS Fargate** for deployment
- **S3** for storage (datasets & MLflow artifacts)
- **CloudFormation** for infrastructure as code (IaC)
- **GitHub Actions** for CI/CD
- **MLflow** for experiment tracking
- **Poetry** for dependency management
- **Jupyter notebooks** for exploratory analysis

---

## 🚀 Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Nacim-B/MLOps_1.git
cd your-repo
```

### 2. Install dependencies (dev environment)

Make sure [Poetry](https://python-poetry.org/docs/#installation) is installed.

```bash
poetry install
```

Make sure Docker / Docker desktop is installed.

Create a `.env` file at the root, following the `.env.template` 
FIll de dev.yaml file


---

### 3. AWS


configure aws CLI


configurer main.yaml
configurer dev.yaml
define needed secrets in github and aws
configurer Run COnfig pour docker dans l'IDE


#### 🗏️ GitHub Actions


---

## 📁 Project Structure (WIP)

```
.
├── infra/
│   └── cloudformation/
│       └── s3_bucket.yaml
├── notebooks/
├── src/
│   └── mlops_project/
│       ├── data/
│       │   └── fetch_data.py
│       └── run_csv_upload.py
├── .github/
│   └── workflows/
│       └── deploy.yml
├── .env
├── pyproject.toml
└── README.md
```



