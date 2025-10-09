# 🚢 部署指南

本文檔提供東南亞金融新聞搜尋系統的完整部署指南。

## 📋 目錄

1. [本地開發環境](#本地開發環境)
2. [Docker 部署](#docker-部署)
3. [雲端部署](#雲端部署)
4. [環境變數配置](#環境變數配置)
5. [監控與維護](#監控與維護)

---

## 本地開發環境

### Windows

1. **執行自動設置腳本**
```powershell
.\scripts\setup.ps1
```

2. **手動設置**
```powershell
# 建立虛擬環境
uv venv

# 啟動虛擬環境
.\.venv\Scripts\Activate.ps1

# 安裝依賴
uv pip install -e .

# 驗證系統
python main.py validate

# 啟動 Web 介面
streamlit run app.py
```

### macOS / Linux

```bash
# 執行設置腳本
chmod +x scripts/setup.sh
./scripts/setup.sh

# 啟動應用
streamlit run app.py
```

---

## Docker 部署

### 使用 Docker Compose（推薦）

1. **構建並啟動**
```bash
docker-compose up -d
```

2. **查看日誌**
```bash
docker-compose logs -f
```

3. **停止服務**
```bash
docker-compose down
```

### 使用 Docker CLI

1. **構建映像檔**
```bash
docker build -t seanews-system:latest .
```

2. **運行容器**
```bash
docker run -d \
  --name seanews-app \
  -p 8501:8501 \
  --env-file .env \
  -v $(pwd)/reports:/app/reports \
  seanews-system:latest
```

3. **查看日誌**
```bash
docker logs -f seanews-app
```

---

## 雲端部署

### Google Cloud Run

1. **準備配置**
```bash
# 安裝 gcloud CLI
# https://cloud.google.com/sdk/docs/install

# 登入
gcloud auth login

# 設定專案
gcloud config set project YOUR_PROJECT_ID
```

2. **構建並推送映像檔**
```bash
# 啟用 Artifact Registry
gcloud services enable artifactregistry.googleapis.com

# 創建倉庫
gcloud artifacts repositories create seanews-repo \
  --repository-format=docker \
  --location=asia-east1

# 構建並推送
gcloud builds submit --tag asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/seanews-repo/seanews-system
```

3. **部署到 Cloud Run**
```bash
gcloud run deploy seanews-system \
  --image asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/seanews-repo/seanews-system \
  --platform managed \
  --region asia-east1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key,EMAIL_ADDRESS=your_email \
  --set-secrets EMAIL_PASSWORD=email-password:latest
```

### AWS ECS

1. **準備 ECR**
```bash
# 創建 ECR 倉庫
aws ecr create-repository --repository-name seanews-system

# 登入 ECR
aws ecr get-login-password --region ap-southeast-1 | \
  docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com

# 標記並推送
docker tag seanews-system:latest YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/seanews-system:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/seanews-system:latest
```

2. **創建 ECS 任務定義**
```json
{
  "family": "seanews-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [
    {
      "name": "seanews-container",
      "image": "YOUR_ACCOUNT_ID.dkr.ecr.ap-southeast-1.amazonaws.com/seanews-system:latest",
      "portMappings": [
        {
          "containerPort": 8501,
          "protocol": "tcp"
        }
      ],
      "environment": [
        {"name": "AGNO_TELEMETRY", "value": "false"}
      ],
      "secrets": [
        {"name": "OPENAI_API_KEY", "valueFrom": "arn:aws:secretsmanager:..."},
        {"name": "EMAIL_PASSWORD", "valueFrom": "arn:aws:secretsmanager:..."}
      ]
    }
  ]
}
```

3. **創建服務**
```bash
aws ecs create-service \
  --cluster your-cluster \
  --service-name seanews-service \
  --task-definition seanews-task \
  --desired-count 1 \
  --launch-type FARGATE
```

### Azure Container Instances

```bash
# 創建資源群組
az group create --name seanews-rg --location southeastasia

# 創建容器實例
az container create \
  --resource-group seanews-rg \
  --name seanews-container \
  --image YOUR_REGISTRY/seanews-system:latest \
  --dns-name-label seanews-app \
  --ports 8501 \
  --environment-variables \
    AGNO_TELEMETRY=false \
  --secure-environment-variables \
    OPENAI_API_KEY=your_key \
    EMAIL_PASSWORD=your_password
```

---

## 環境變數配置

### 必要變數

| 變數名稱 | 說明 | 範例 |
|---------|------|------|
| `OPENAI_API_KEY` | OpenAI API 金鑰 | `sk-proj-...` |
| `EMAIL_ADDRESS` | 發件人郵箱 | `sender@gmail.com` |
| `EMAIL_PASSWORD` | 郵箱應用程式密碼 | `xxxx xxxx xxxx xxxx` |

### 可選變數

| 變數名稱 | 說明 | 預設值 |
|---------|------|--------|
| `SMTP_SERVER` | SMTP 伺服器 | `smtp.gmail.com` |
| `SMTP_PORT` | SMTP 端口 | `587` |
| `DEBUG` | 調試模式 | `false` |
| `AGNO_TELEMETRY` | Agno 遙測 | `false` |

### 雲端密鑰管理

#### Google Cloud Secret Manager
```bash
# 創建密鑰
echo -n "your_api_key" | gcloud secrets create openai-api-key --data-file=-

# 授予權限
gcloud secrets add-iam-policy-binding openai-api-key \
  --member=serviceAccount:YOUR_SERVICE_ACCOUNT \
  --role=roles/secretmanager.secretAccessor
```

#### AWS Secrets Manager
```bash
# 創建密鑰
aws secretsmanager create-secret \
  --name openai-api-key \
  --secret-string "your_api_key"
```

#### Azure Key Vault
```bash
# 創建密鑰保管庫
az keyvault create --name seanews-vault --resource-group seanews-rg

# 添加密鑰
az keyvault secret set --vault-name seanews-vault \
  --name openai-api-key \
  --value "your_api_key"
```

---

## 監控與維護

### 健康檢查

系統提供健康檢查端點：
- **Streamlit Health**: `http://localhost:8501/_stcore/health`

### 日誌管理

#### 查看 Docker 日誌
```bash
docker logs -f seanews-app --tail 100
```

#### 查看 Cloud Run 日誌
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=seanews-system" \
  --limit 50 --format json
```

### 性能監控

建議使用以下工具：
- **Prometheus**: 收集性能指標
- **Grafana**: 視覺化監控儀表板
- **Sentry**: 錯誤追蹤

### 備份策略

1. **報告備份**: 定期備份 `reports/` 目錄
2. **配置備份**: 備份 `.env` 文件（注意安全）
3. **資料庫備份**: 如有使用資料庫

### 更新部署

#### Docker 更新
```bash
# 重新構建
docker-compose build

# 重啟服務
docker-compose up -d
```

#### Cloud Run 更新
```bash
# 重新構建並推送
gcloud builds submit --tag asia-east1-docker.pkg.dev/YOUR_PROJECT_ID/seanews-repo/seanews-system

# 自動部署新版本
```

### 故障排除

#### 問題 1: 容器無法啟動
```bash
# 檢查日誌
docker logs seanews-app

# 檢查環境變數
docker inspect seanews-app | grep -A 10 "Env"
```

#### 問題 2: API 連接失敗
- 驗證 API Key 是否正確
- 檢查網路連接
- 確認 API 配額未用完

#### 問題 3: 郵件發送失敗
- 檢查 Gmail 應用程式密碼
- 確認 SMTP 端口未被阻擋
- 驗證收件人地址格式

---

## 安全性建議

1. **不要將 `.env` 提交到版本控制**
2. **使用雲端密鑰管理服務**
3. **定期更新依賴套件**
4. **啟用 HTTPS（生產環境）**
5. **實施 API 速率限制**
6. **定期審查存取日誌**

---

## 成本估算

### Google Cloud Run
- 免費額度: 每月 2 百萬請求
- 付費: 約 $0.00002400/請求
- 預估: $30-80/月

### AWS ECS Fargate
- 0.5 vCPU, 1GB 記憶體
- 預估: $50-100/月

### Azure Container Instances
- B2S 等級
- 預估: $40-90/月

---

**最後更新**: 2025-01
**維護團隊**: Development Team
