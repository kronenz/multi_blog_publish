from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID
from backend.src.models.blog_post import BlogPost
from backend.src.services.blog_post_service import BlogPostService

router = APIRouter()
blog_post_service = BlogPostService()

@router.post("/blog_posts", response_model=BlogPost, status_code=201)
def create_blog_post(blog_post: BlogPost):
    return blog_post_service.create_blog_post(blog_post)

@router.get("/blog_posts/{blog_post_id}", response_model=BlogPost)
def get_blog_post(blog_post_id: UUID):
    blog_post = blog_post_service.get_blog_post_by_id(blog_post_id)
    if blog_post is None:
        raise HTTPException(status_code=404, detail="Blog post not found")
    return blog_post
