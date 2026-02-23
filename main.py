import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles # 导入静态文件支持
from fastapi.responses import FileResponse   # 导入文件响应
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

# 引入我们刚才写的逻辑
from logic import generate_rename_plan, execute_rename_file

app = FastAPI(title="Anime Renamer API")

# --- 关键修改：让 FastAPI 托管你的网页 ---
# 1. 挂载静态资源目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. 定义根目录访问 index.html
@app.get("/")
async def read_index():
    return FileResponse('static/index.html')

# 解决跨域问题（如果是前后端分离开发需要这个）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# --- 定义数据模型（规定浏览器发过来的数据长什么样） ---

class ScanRequest(BaseModel):
    path: str
    show_name: str
    season: int = 1
    format: str = "{n} S{s}E{e}"


class RenameItem(BaseModel):
    old_name: str
    new_name: str


class RenameRequest(BaseModel):
    path: str
    tasks: List[RenameItem]


# --- 接口 API 部分 ---

@app.get("/")
async def index():
    return {"message": "Anime Renamer API 运行中。请访问 /docs 查看接口文档。"}


@app.post("/api/scan")
async def api_scan(req: ScanRequest):
    """
    扫描文件夹并生成预览计划
    """
    plan = generate_rename_plan(req.path, req.show_name, req.season, req.format)

    # 如果 logic 返回的是字典且包含 error，抛出 HTTP 错误
    if isinstance(plan, dict) and "error" in plan:
        raise HTTPException(status_code=400, detail=plan["error"])

    return {"plan": plan}


@app.post("/api/rename")
async def api_rename(req: RenameRequest):
    """
    执行批量重命名
    """
    results = []
    success_count = 0

    for item in req.tasks:
        success, msg = execute_rename_file(req.path, item.old_name, item.new_name)
        if success:
            success_count += 1
        results.append({
            "old_name": item.old_name,
            "success": success,
            "message": msg
        })

    return {
        "total": len(req.tasks),
        "success_count": success_count,
        "details": results
    }


if __name__ == "__main__":
    # 启动服务器，监听 8000 端口
    # 在 NAS 部署时，uvicorn 会负责处理并发请求
    uvicorn.run(app, host="0.0.0.0", port=8000)