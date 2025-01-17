# 项目说明
- 本项目实现了一个基于FastAPI的AI对话后端，
## 项目结构
- app/
  - \_\_init__.py
  - main.py              # FastAPI 应用入口
  - models/              # 数据库模型
  - schemas/             # Pydantic 数据模型
  - services/            # 业务实现
  - core/                # 核心配置（如数据库、认证）
  - utils/               # 工具函数
- requirements.txt         # 依赖列表 
- .env                     # 环境变量
## 使用说明
### 环境准备与运行
- 安装依赖：`pip install -r requirements.txt`
- 安装数据库 自行下载PostgreSQL数据库，新建一个数据库，我使用的用户名、密码、端口和数据库名在.env里可以看到。
- 需要自行修改的代码 services/message.py 中的AI_API_URL需要自行填上，具体请求的方式需要自己修改，我给的是vllm部署的借口请求方式。
- 运行：`uvicorn app.main:app --reload`
### 接口文档
- 项目运行后访问 `http://127.0.0.1:8000/docs` 即可查看接口文档。