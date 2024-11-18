使用 FastAPI 构建接口时，可以通过定义一个脚手架来快速启动项目，提供统一的目录结构和基础功能。以下是一个适用于 FastAPI 项目的脚手架示例，它涵盖了常见的项目需求，例如路由管理、依赖注入、配置管理和错误处理。

---

### **FastAPI 脚手架示例**

#### **1. 目录结构**
```plaintext
fastapi_project/
├── app/
│   ├── api/                    # 路由管理
│   │   ├── v1/                 # API 的版本管理
│   │   │   ├── endpoints/      # 具体的业务逻辑
│   │   │   │   ├── user.py     # 用户相关接口
│   │   │   │   └── item.py     # 商品相关接口
│   │   │   └── __init__.py
│   │   └── __init__.py
│   ├── core/                   # 核心功能
│   │   ├── config.py           # 配置管理
│   │   └── security.py         # 安全模块 (如 JWT)
│   ├── db/                     # 数据库模块
│   │   ├── base.py             # 数据库基础配置
│   │   ├── models.py           # 数据库模型
│   │   └── session.py          # 数据库会话管理
│   ├── services/               # 业务逻辑
│   │   └── user_service.py     # 用户服务
│   ├── utils/                  # 工具函数
│   │   ├── logger.py           # 日志管理
│   │   └── common.py           # 通用工具
│   ├── main.py                 # 入口文件
│   └── __init__.py
├── tests/                      # 测试
│   ├── test_user.py            # 用户模块的测试
│   └── test_item.py            # 商品模块的测试
├── requirements.txt            # 依赖列表
├── Dockerfile                  # Docker 配置
└── README.md                   # 项目说明文档
```

---

#### **2. 核心代码示例**

##### **`main.py`** (项目入口)
```python
from fastapi import FastAPI
from app.api.v1 import endpoints

# 初始化 FastAPI 应用
app = FastAPI(title="FastAPI 项目脚手架", version="1.0.0")

# 注册路由
app.include_router(endpoints.router, prefix="/api/v1")

# 根路径
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Project"}
```

---

##### **`config.py`** (配置管理)
```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "FastAPI 项目脚手架"
    DEBUG: bool = True
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = "your_secret_key"

    class Config:
        env_file = ".env"

settings = Settings()
```

---

##### **`user.py`** (用户相关接口)
```python
from fastapi import APIRouter, Depends
from app.services.user_service import get_user_by_id

router = APIRouter()

@router.get("/users/{user_id}")
def read_user(user_id: int):
    """获取用户信息"""
    user = get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}
    return {"user": user}
```

---

##### **`user_service.py`** (用户服务)
```python
def get_user_by_id(user_id: int):
    """模拟从数据库获取用户"""
    mock_users = {1: {"id": 1, "name": "John Doe"}, 2: {"id": 2, "name": "Jane Smith"}}
    return mock_users.get(user_id)
```

---

##### **`base.py`** (数据库基础配置)
```python
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
```

##### **`session.py`** (数据库会话)
```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

##### **`logger.py`** (日志管理)
```python
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

logger = logging.getLogger("FastAPI Project")
```

---

#### **3. 运行项目**
1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 启动项目：
   ```bash
   uvicorn app.main:app --reload
   ```

3. 访问文档：
   - 自动生成的 Swagger 文档：`http://127.0.0.1:8000/docs`
   - Redoc 文档：`http://127.0.0.1:8000/redoc`

---

#### **4. 依赖文件示例**
`requirements.txt`：
```plaintext
fastapi==0.95.2
uvicorn==0.23.2
pydantic==1.10.2
sqlalchemy==1.4.46
```

---

### **总结**
该脚手架设计清晰，适合小型到中型的 FastAPI 项目。它包含：
- 路由模块化管理
- 配置管理
- 数据库支持
- 业务逻辑分离
- 单元测试框架

你可以在此基础上进一步扩展，例如添加认证、缓存、消息队列等功能。