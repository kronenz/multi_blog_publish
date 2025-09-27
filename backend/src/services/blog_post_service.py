from typing import Dict, List
from uuid import UUID
from backend.src.models.blog_post import BlogPost

class BlogPostService:
    def __init__(self):
        self.blog_posts: Dict[UUID, BlogPost] = {}

    def create_blog_post(self, blog_post: BlogPost) -> BlogPost:
        self.blog_posts[blog_post.id] = blog_post
        return blog_post

    def get_blog_post_by_id(self, blog_post_id: UUID) -> BlogPost | None:
        return self.blog_posts.get(blog_post_id)
