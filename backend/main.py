from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from backend.src.api import users, knowledge_vaults, blog_posts

app = FastAPI(
    title="Multi-Blog Publishing Platform API",
    description="AI 기반 지식 관리 및 멀티 플랫폼 블로그 퍼블리싱 서비스",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Multi-Blog Publishing Platform API"
    }

app.include_router(users.router)
app.include_router(knowledge_vaults.router)
app.include_router(blog_posts.router)
