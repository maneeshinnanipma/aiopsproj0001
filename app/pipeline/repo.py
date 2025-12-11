
# app/pipeline/repo.py
import os, json, zipfile
from state import RefactorState
from infra.cloudformation_stub import generate_stub

def node_generate_repo(state: RefactorState, repo_path="cloud-refactor-repo") -> RefactorState:
    os.makedirs(f"{repo_path}/infrastructure/aws", exist_ok=True)
    os.makedirs(f"{repo_path}/.github/workflows", exist_ok=True)
    os.makedirs(f"{repo_path}/src/monolith", exist_ok=True)
    os.makedirs(f"{repo_path}/src/refactored", exist_ok=True)
    os.makedirs(f"{repo_path}/config", exist_ok=True)

    with open(f"{repo_path}/src/monolith/app.py", "w", encoding="utf-8") as f:
        f.write(state.raw_code)

    with open(f"{repo_path}/config/Dockerfile", "w", encoding="utf-8") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
COPY src/monolith/ /app
RUN pip install -r requirements.txt || true
CMD ["python", "app.py"]""")

    with open(f"{repo_path}/config/docker-compose.yaml", "w", encoding="utf-8") as f:
        f.write("""version: '3.8'
services:
  app:
    build: ./config
    ports:
      - "8080:8080"
    environment:
      - ENV=production""")

    with open(f"{repo_path}/config/app-config.json", "w", encoding="utf-8") as f:
        json.dump({"ENV": "production"}, f, indent=2)

    with open(f"{repo_path}/infrastructure/aws/cloudformation.yaml", "w", encoding="utf-8") as f:
        f.write(generate_stub(state.enriched_plan))

    with open(f"{repo_path}/README.md", "w", encoding="utf-8") as f:
        f.write(state.deployment_blueprint or "")

    workflow = """name: Deploy
on:
  push:
    branches: [ main ]
permissions:
  id-token: write
  contents: read
jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Configure AWS Credentials (OIDC)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
          aws-region: ${{ secrets.AWS_REGION }}
      - name: Login to ECR
        uses: aws-actions/amazon-ecr-login@v2
      - name: Build and Push Docker Image
        env:
          ECR_REPO_URI: ${{ secrets.ECR_REPO_URI }}
        run: |
          docker build -t cloud-refactor-app ./config
          docker tag cloud-refactor-app:latest $ECR_REPO_URI:latest
          docker push $ECR_REPO_URI:latest
      - name: Deploy CloudFormation
        run: |
          aws cloudformation deploy \
            --template-file infrastructure/aws/cloudformation.yaml \
            --stack-name refactor-stack \
            --capabilities CAPABILITY_IAM
"""
    os.makedirs(f"{repo_path}/.github/workflows", exist_ok=True)
    with open(f"{repo_path}/.github/workflows/deploy.yml", "w", encoding="utf-8") as f:
        f.write(workflow)

    zip_name = "cloud-refactor-repo.zip"
    with zipfile.ZipFile(zip_name, "w") as zipf:
        for root, _, files in os.walk(repo_path):
            for file in files:
                zipf.write(os.path.join(root, file))
    state.repo_zip = zip_name
    return state  # ← IMPORTANT
