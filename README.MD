# 新闻项目
一个新闻项目，点击查看相关新闻详情
# 技术栈

- 前端：vue
- 后端：fastapi ＋ uvicorn

# 1. 在根目录创建并激活虚拟环境
- python -m venv .venv
- .venv\Scripts\activate   # Windows
- source .venv/bin/activate # Mac/Linux

# 2. 安装后端依赖
- pip install -r news_backend/requirements.txt

# 3. 启动后端 (注意要进入后端目录)
- cd news_backend
- uvicorn main:app --reload