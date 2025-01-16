# 项目结构
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 应用入口
│   ├── models/              # 数据库模型
│   ├── schemas/             # Pydantic 数据模型
│   ├── services/            # 业务实现
│   ├── core/                # 核心配置（如数据库、认证）
│   └── utils/               # 工具函数
├── tests/                   # 测试代码
├── requirements.txt         # 依赖列表
└── .env                     # 环境变量