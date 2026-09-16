# Deployment Guide – UC189

## Prerequisites
- Azure subscription
- Azure CLI installed (`az --version`)
- Docker installed (`docker --version`)
- GitHub account (for CI/CD)

## Azure Resources Required
1. Azure App Service (Backend)
2. Azure Static Web Apps (Frontend)
3. Azure SQL Database / Flexible Server PostgreSQL
4. Azure OpenAI Service (GPT-4 deployment)
5. Azure Blob Storage (Interaction audio & PDF quotes)
6. Azure Key Vault (Secure configuration)

## Step-by-Step Deployment

### 1. Create Resource Group
```bash
az group create --name rg-insurance-advisor --location eastus
```

### 2. Create Azure SQL / PostgreSQL
```bash
az sql server create \
  --name insurance-sql-server \
  --resource-group rg-insurance-advisor \
  --admin-user sqladmin \
  --admin-password "<Password123!>"

az sql db create \
  --resource-group rg-insurance-advisor \
  --server insurance-sql-server \
  --name insurance_advisor \
  --service-objective S0
```

### 3. Deploy Backend to Azure App Service
```bash
az appservice plan create \
  --name insurance-plan \
  --resource-group rg-insurance-advisor \
  --sku B1 \
  --is-linux

az webapp create \
  --resource-group rg-insurance-advisor \
  --plan insurance-plan \
  --name uc189-backend \
  --runtime "PYTHON:3.11"

az webapp config appsettings set \
  --resource-group rg-insurance-advisor \
  --name uc189-backend \
  --settings @appsettings.json
```

### 4. Deploy Frontend to Azure Static Web Apps
```bash
cd frontend
npm run build

az staticwebapp create \
  --name uc189-frontend \
  --resource-group rg-insurance-advisor \
  --source ./dist
```

### 5. Local Docker Deployment
```bash
docker-compose -f docker-compose.yml up -d --build
```

### Health Checks
- Backend: `GET http://localhost:8000/health`
- Frontend: Load `http://localhost:3000/`
- Database: Automatic connection check on startup with SQLite fallback
