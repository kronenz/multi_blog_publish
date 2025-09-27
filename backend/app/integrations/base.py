from abc import ABC, abstractmethod
from typing import Dict, Any
from app.models import PostCreate, PostUpdate

class BlogAdapter(ABC):
    """
    Abstract base class for blog integration adapters.
    Defines the common interface for all blog platforms.
    """

    @abstractmethod
    def authenticate(self, credentials: Dict[str, Any]) -> None:
        """Authenticates with the blog service."""
        raise NotImplementedError

    @abstractmethod
    def create_post(self, post_data: PostCreate) -> str:
        """
        Creates a new post on the blog platform.
        Returns the URL or ID of the newly created post.
        """
        raise NotImplementedError

    @abstractmethod
    def update_post(self, post_id: str, post_data: PostUpdate) -> str:
        """
        Updates an existing post on the blog platform.
        Returns the URL or ID of the updated post.
        """
        raise NotImplementedError

    @abstractmethod
    def delete_post(self, post_id: str) -> bool:
        """
        Deletes a post from the blog platform.
        Returns True if successful, False otherwise.
        """
        raise NotImplementedError