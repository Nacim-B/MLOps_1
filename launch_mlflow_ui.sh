#!/bin/bash
# File: start_mlflow_ui.sh
# Description: Script to start MLflow UI with RDS backend and S3 artifact storage

# Load environment variables from .env file using a more robust method
if [ -f .env ]; then
    # Load each line individually to handle special characters better
    while IFS= read -r line || [[ -n "$line" ]]; do
        # Skip comments and empty lines
        if [[ ! "$line" =~ ^\# ]] && [[ -n "$line" ]]; then
            # Export the variable
            export "$line"
        fi
    done < .env
    echo "✅ Environment variables loaded"
else
    echo "❌ .env file not found"
    exit 1
fi

# Debug: Print loaded variables (hide password)
echo "MYSQL_HOST: $MYSQL_HOST"
echo "MYSQL_USERNAME: $MYSQL_USERNAME"
echo "MYSQL_PASSWORD: [hidden]"
echo "S3_BUCKET_NAME: $S3_BUCKET_NAME"

# Check for required variables
if [ -z "$MYSQL_HOST" ] || [ -z "$MYSQL_USERNAME" ] || [ -z "$MYSQL_PASSWORD" ] || [ -z "$S3_BUCKET_NAME" ]; then
    echo "❌ Missing required environment variables"
    echo "Please ensure the following variables are set in your .env file:"
    echo "  - MYSQL_HOST"
    echo "  - MYSQL_PORT (default: 3306)"
    echo "  - MYSQL_USERNAME"
    echo "  - MYSQL_PASSWORD"
    echo "  - MYSQL_DB_MLFLOW (default: mlflow)"
    echo "  - S3_BUCKET_NAME"
    exit 1
fi

# Set default values if not provided
MYSQL_PORT=${MYSQL_PORT:-3306}
MYSQL_DB_MLFLOW=${MYSQL_DB_MLFLOW:-mlflow}

# Build backend store URI and artifact root
BACKEND_URI="mysql+pymysql://${MYSQL_USERNAME}:${MYSQL_PASSWORD}@${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DB_MLFLOW}"
ARTIFACT_ROOT="s3://${S3_BUCKET_NAME}/mlruns"

# Display configuration
echo "🚀 Starting MLflow UI..."
echo "  Backend: ${MYSQL_HOST}:${MYSQL_PORT}/${MYSQL_DB_MLFLOW}"
echo "  Artifacts: ${ARTIFACT_ROOT}"
echo "  UI will be available at http://localhost:5000"

# Start MLflow UI
mlflow ui --backend-store-uri "$BACKEND_URI" --default-artifact-root "$ARTIFACT_ROOT"