# 🚀 部署與生產環境建議

## ⚠️ 當前版本限制

目前的實作適合**開發和測試環境**，使用了以下簡化方案：

### 任務管理
- ❌ 使用內存字典儲存任務狀態
- ❌ 伺服器重啟後任務狀態會遺失
- ❌ 無法跨多個 worker 共享狀態

### 背景任務
- ❌ 使用 FastAPI BackgroundTasks（單進程）
- ❌ 無任務優先級
- ❌ 無任務重試機制
- ❌ 並發能力有限

### 安全性
- ❌ 無身份驗證
- ❌ 無 API 金鑰驗證
- ❌ 無速率限制
- ❌ CORS 開放過於寬鬆

### 檔案管理
- ❌ 檔案存放在本地目錄
- ❌ 無檔案清理機制
- ❌ 無檔案大小限制

---

## 🏗️ 生產環境改進建議

### 1. 任務狀態管理 - 使用 Redis

#### 為什麼需要 Redis?
- ✅ 持久化儲存（伺服器重啟後任務狀態不遺失）
- ✅ 跨多個 worker 共享狀態
- ✅ 支援 TTL（自動過期）
- ✅ 高效能讀寫

#### 實作範例

**安裝依賴**:
```bash
pip install redis
```

**修改 `app/services/progress.py`**:
```python
import redis
import json
from typing import Dict, Any, Optional

class TaskProgress:
    """使用 Redis 的任務進度管理"""
    
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
        self.ttl = 86400  # 任務保留 24 小時
    
    def create_task(self, user_prompt: str, email: str, **kwargs) -> str:
        task_id = str(uuid.uuid4())
        
        task_data = {
            "task_id": task_id,
            "status": "queued",
            "progress": 0,
            "user_prompt": user_prompt,
            "email": email,
            "created_at": datetime.now().isoformat(),
            **kwargs
        }
        
        # 儲存到 Redis
        self.redis_client.setex(
            f"task:{task_id}",
            self.ttl,
            json.dumps(task_data)
        )
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        data = self.redis_client.get(f"task:{task_id}")
        if data:
            return json.loads(data)
        return None
    
    def update_task(self, task_id: str, **kwargs):
        task = self.get_task(task_id)
        if task:
            task.update(kwargs)
            task["updated_at"] = datetime.now().isoformat()
            self.redis_client.setex(
                f"task:{task_id}",
                self.ttl,
                json.dumps(task)
            )
```

**Docker Compose 配置**:
```yaml
version: '3.8'

services:
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
```

---

### 2. 背景任務 - 使用 Celery

#### 為什麼需要 Celery?
- ✅ 分散式任務佇列
- ✅ 支援任務優先級
- ✅ 支援任務重試
- ✅ 支援定時任務
- ✅ 可擴展到多個 worker

#### 實作範例

**安裝依賴**:
```bash
pip install celery[redis]
```

**建立 `app/celery_app.py`**:
```python
from celery import Celery
from config import Config

celery_app = Celery(
    'sea_news_alert',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=3600,  # 1 小時超時
)
```

**建立 `app/tasks.py`**:
```python
from app.celery_app import celery_app
from app.services.workflow import workflow

@celery_app.task(bind=True, max_retries=3)
def execute_news_report_task(self, task_id: str):
    """Celery 任務: 執行新聞報告生成"""
    try:
        # 使用 async_to_sync 如果需要
        workflow.execute_task(task_id)
    except Exception as e:
        # 重試機制
        raise self.retry(exc=e, countdown=60)
```

**修改 `app/routers/tasks.py`**:
```python
from app.tasks import execute_news_report_task

@router.post("/news-report", response_model=TaskResponse, status_code=201)
async def create_news_report_task(request: NewsReportRequest):
    # 創建任務
    task_id = task_manager.create_task(...)
    
    # 使用 Celery 執行
    execute_news_report_task.delay(task_id)
    
    return TaskResponse(task_id=task_id, message="Task started")
```

**啟動 Celery Worker**:
```bash
celery -A app.celery_app worker --loglevel=info
```

---

### 3. 身份驗證 - 使用 JWT

#### 實作範例

**安裝依賴**:
```bash
pip install python-jose[cryptography] passlib[bcrypt]
```

**建立 `app/auth.py`**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta

security = HTTPBearer()

SECRET_KEY = "your-secret-key-here"  # 應從環境變數讀取
ALGORITHM = "HS256"

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
```

**保護 API 端點**:
```python
from app.auth import verify_token

@router.post("/news-report", dependencies=[Depends(verify_token)])
async def create_news_report_task(request: NewsReportRequest):
    # ... 原有邏輯
    pass
```

---

### 4. 速率限制

**安裝依賴**:
```bash
pip install slowapi
```

**配置速率限制**:
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@router.post("/news-report")
@limiter.limit("10/hour")  # 每小時 10 次
async def create_news_report_task(request: Request, ...):
    pass
```

---

### 5. 檔案管理 - 使用雲端儲存

#### 使用 AWS S3

**安裝依賴**:
```bash
pip install boto3
```

**上傳到 S3**:
```python
import boto3
from pathlib import Path

s3_client = boto3.client(
    's3',
    aws_access_key_id='YOUR_KEY',
    aws_secret_access_key='YOUR_SECRET'
)

def upload_to_s3(file_path: Path, bucket_name: str):
    """上傳檔案到 S3"""
    object_name = f"reports/{file_path.name}"
    
    s3_client.upload_file(
        str(file_path),
        bucket_name,
        object_name
    )
    
    # 生成預簽名 URL（有效期 1 小時）
    url = s3_client.generate_presigned_url(
        'get_object',
        Params={
            'Bucket': bucket_name,
            'Key': object_name
        },
        ExpiresIn=3600
    )
    
    return url
```

**修改 workflow**:
```python
# 生成報告後
pdf_path = self.report_agent.generate_pdf(markdown_report)
excel_path = self.report_agent.generate_excel(structured_news)

# 上傳到 S3
pdf_url = upload_to_s3(pdf_path, 'your-bucket-name')
excel_url = upload_to_s3(excel_path, 'your-bucket-name')

# 儲存 URL 而非本地路徑
task_manager.set_succeeded(
    task_id,
    pdf_path=pdf_url,
    xlsx_path=excel_url
)

# 刪除本地檔案
pdf_path.unlink()
excel_path.unlink()
```

---

### 6. 日誌與監控

**使用結構化日誌**:
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(log_data)

# 設定
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger("sea_news_alert")
logger.addHandler(handler)
logger.setLevel(logging.INFO)
```

**整合監控工具**:
```bash
# Prometheus
pip install prometheus-fastapi-instrumentator

# 在 main.py 中
from prometheus_fastapi_instrumentator import Instrumentator

Instrumentator().instrument(app).expose(app)
```

---

### 7. 資料庫整合

**使用 PostgreSQL**:
```bash
pip install sqlalchemy psycopg2-binary alembic
```

**定義模型**:
```python
from sqlalchemy import Column, String, Integer, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    progress = Column(Integer, default=0)
    user_prompt = Column(Text)
    email = Column(String)
    error = Column(Text, nullable=True)
    pdf_path = Column(String, nullable=True)
    xlsx_path = Column(String, nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

---

## 📦 Docker 部署

**Dockerfile**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# 安裝依賴
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# 複製程式碼
COPY . .

# 暴露端口
EXPOSE 8000

# 啟動
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**docker-compose.yml**:
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - EMAIL_ADDRESS=${EMAIL_ADDRESS}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./reports:/app/reports

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  celery_worker:
    build: .
    command: celery -A app.celery_app worker --loglevel=info
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - EMAIL_ADDRESS=${EMAIL_ADDRESS}
      - EMAIL_PASSWORD=${EMAIL_PASSWORD}
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - redis
    volumes:
      - ./reports:/app/reports

volumes:
  redis_data:
```

**啟動**:
```bash
docker-compose up -d
```

---

## 🔐 環境變數管理

**生產環境 `.env`**:
```env
# API
SECRET_KEY=your-secret-key-here
DEBUG=false
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# OpenAI
OPENAI_API_KEY=sk-...

# Email
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-app-password

# Redis
REDIS_URL=redis://localhost:6379/0

# Database (如果使用)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# AWS S3 (如果使用)
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET_NAME=your-bucket

# 監控
SENTRY_DSN=https://...
```

---

## 🌐 反向代理 - Nginx

**nginx.conf**:
```nginx
upstream fastapi {
    server localhost:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    # 重定向到 HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # 前端靜態文件
    location /static {
        alias /path/to/public;
    }

    # API 請求
    location /api {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 其他請求
    location / {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📊 性能優化建議

### 1. 使用連線池
```python
# Redis 連線池
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=50
)
redis_client = redis.Redis(connection_pool=redis_pool)
```

### 2. 快取機制
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def get_cached_search_results(query: str):
    # 快取搜尋結果
    pass
```

### 3. 非同步 I/O
```python
import asyncio
import aiohttp

async def async_search(query: str):
    async with aiohttp.ClientSession() as session:
        # 非同步 HTTP 請求
        pass
```

---

## ✅ 生產環境檢查清單

### 基礎設施
- [ ] 使用 Redis 儲存任務狀態
- [ ] 使用 Celery 處理背景任務
- [ ] 使用 PostgreSQL/MySQL 儲存資料
- [ ] 使用 S3/雲端儲存管理檔案
- [ ] 設定 Nginx 反向代理
- [ ] 啟用 HTTPS (Let's Encrypt)

### 安全性
- [ ] 實作身份驗證 (JWT/OAuth)
- [ ] 啟用 API 金鑰驗證
- [ ] 設定速率限制
- [ ] 限制 CORS 來源
- [ ] 隱藏錯誤詳情（生產環境）
- [ ] 定期更新依賴套件

### 監控與日誌
- [ ] 設定結構化日誌
- [ ] 整合錯誤追蹤 (Sentry)
- [ ] 設定 Prometheus/Grafana 監控
- [ ] 設定健康檢查端點
- [ ] 設定告警機制

### 備份與災難恢復
- [ ] 資料庫定期備份
- [ ] Redis 持久化設定
- [ ] 檔案備份策略
- [ ] 災難恢復計畫

### 效能
- [ ] 啟用快取機制
- [ ] 使用連線池
- [ ] 設定適當的超時時間
- [ ] 壓縮 API 響應 (gzip)
- [ ] CDN 設定（靜態文件）

---

**文件版本**: 1.0  
**最後更新**: 2025-01-16
