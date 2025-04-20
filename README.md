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
poetry shell
```

Create a `.env` file at the root, following the `.env.template` 


---

### 3. Provision infrastructure

Before running pipelines, you must create the base infrastructure (e.g., S3 bucket for datasets & MLflow).

#### 🗏️ S3 Bucket via GitHub Actions

1. Go to the **Actions** tab in your GitHub repo
2. Launch the workflow `Deploy MLOps 1 - DEV`
3. Your bucket will be created automatically via CloudFormation

> Note: Make sure to define:\
>   `S3_BUCKET_NAME` in **GitHub → Settings → Variables**
>   `AWS_SECRET_ACCESS_KEY` in **GitHub → Settings → Secrets**
>   `AWS_ACCESS_KEY_ID` in **GitHub → Settings → Secrets**
>   `CSV_FILENAME` in **GitHub → Settings → Secrets**
>   `CSV_URL` in **GitHub → Settings → Secrets**

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



