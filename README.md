# 🧠 MLOps Template – Classification or Regression (AWS + Docker + GitHub Actions)

This project is a reusable template for machine learning pipelines — supporting both **classification and regression tasks**.  
It provides a production-ready MLOps setup powered by:

- ✅ **GitHub Actions** for CI/CD
- 🐳 **Docker** for containerization
- ☁️ **AWS services** including:
  - **ECR** for image hosting
  - **ECS Fargate** for task execution
  - **S3** for data and model storage
  - **Secrets Manager** for secure credentials
  - **CloudFormation** for infrastructure provisioning
  - **CloudWatch** for logging
  - **RDS (MySQL)** for structured data

---

## 🚀 Quick Start

### 📦 Prerequisites

Make sure you have the following installed locally:

- [Poetry](https://python-poetry.org/docs/) – for dependency management  
- [Docker](https://www.docker.com/products/docker-desktop) – for building and running containers  
- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) – for interacting with AWS  

Then configure AWS credentials locally:

```bash
aws configure
```

---

### 💻 In your IDE

1. **Clone the repository**

```bash
git clone https://github.com/your-username/mlops-template.git
cd mlops-template
```

2. **Create your `.env` file**

```bash
cp .env.template .env
```

Edit the `.env` file with your own values (e.g., database, CSV URL, S3 bucket).

3. **Configure your pipeline settings**

Update the `config/dev.yaml` file based on your project needs:

- `data_source`: `"csv_url"` or `"mysql"`
- `target`: column to predict
- `csv_separator`, `id_column`, etc.

---

### 🔐 GitHub Secrets

In your GitHub repo, go to:  
`Settings → Secrets and variables → Actions → New repository secret`

Create the following **required secrets**:

| Name                  | Description                         |
|-----------------------|-------------------------------------|
| `AWS_ACCESS_KEY_ID`   | AWS access key                      |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key             |
| `S3_BUCKET_NAME`      | Name of your S3 bucket              |

---

### 🔐 AWS Secrets Manager

Store your secrets securely in Secrets Manager depending on your data source:

- If using a **CSV URL**:
  - `csv_url` (secret key: e.g. `CSV_URL`)
- If using a **MySQL database**:
  - `db_password`
  - `db_host` (if dynamic)

You can reference these secrets by ARN in your ECS Task Definitions.

---

### ☁️ CloudFormation

File: `infra/cloudformation/ecs_task.yaml`

1. **Update the `Secrets` block** of each task (`Train` and `Predict`) with the correct ARNs from AWS Secrets Manager  
2. **Remove secrets** that are not required (e.g., remove `CSV_URL` if using MySQL only)  
3. **Update for each task the `Environment` block** with your static variables like `MYSQL_DATABASE`, `MYSQL_USERNAME`, etc.

---

### ⚙️ GitHub Actions workflow

Folder: `.github/workflows/`

- Open the relevant workflow files (e.g. `train.yaml`, `aws_infra.yaml`)
- Edit the `env:` section at the top with your own project configuration (e.g., subnet ID, security group ID, S3 bucket)

---

### 🐳 Dockerfiles

- Open `Dockerfile.train` and `Dockerfile.predict`
- Update any paths or script names as needed to reflect your project structure

---

