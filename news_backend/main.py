from fastapi import FastAPI
from routers import news
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # 允许的源
    allow_credentials=True, # 允许携带cookie
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
async def root():
    return {"msg":"hello world"}

# 挂载路由/注册路由
app.include_router(news.router)