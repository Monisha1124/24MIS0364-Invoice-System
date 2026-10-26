# 24MIS0364 – Invoice System

## Versions
- v1: Create/generate invoice.
- v2: Create and edit/modify invoice.
- v3: Create, edit and view/display invoice details.

## Run locally (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:APP_VERSION="v3"
python app.py
```
Open http://127.0.0.1:5000. To run v1/v2, change APP_VERSION to v1 or v2.

## Test
```powershell
python -m pytest -v
```

## Docker
Replace the DockerHub username in Jenkinsfile. Build each tag:
```powershell
docker build -t YOUR_DOCKERHUB_USERNAME/24mis0364-invoice-system:v1 .
docker build -t YOUR_DOCKERHUB_USERNAME/24mis0364-invoice-system:v2 .
docker build -t YOUR_DOCKERHUB_USERNAME/24mis0364-invoice-system:v3 .
```
Note: APP_VERSION is supplied at container runtime in Kubernetes manifests, so the same image build is used for each tag in this starter configuration. For a classroom requirement that expects distinct image builds, build the same source separately with the corresponding APP_VERSION build argument and update the Dockerfile to persist it.

## Kubernetes
See the three deployment/service manifests in `k8s/`. Replace `YOUR_DOCKERHUB_USERNAME` in each manifest before applying. Requires a running Kubernetes cluster and kubectl context.
