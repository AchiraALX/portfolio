#!/usr/bin/env python3
"""Script for deleting models
"""

from db_storage import DBStorage
from models.user import User
from models.blog import Blog, BlogComment
from models.repo import Repo
from models.ghub import Ghub
from models.heat import Heat, HeatComment
from models.task import Task, TaskComment

class Delete:
    """Delete class
    """

    def __init__(self) -> None:
        """Initialize
        """
        self.storage = DBStorage().n_session()

    def delete_user(self, user_id: int) -> None:
        """Delete user

        Args:
            user_id (int): user id
        """
        user = self.storage.get(User, user_id)

        if user:
            try:
                self.storage.delete(user)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle blog deletion
    def delete_blog(self, blog_id: int) -> None:
        """Delete blog

        Args:
            blog_id (int): blog id
        """

        blog = self.storage.get(Blog, blog_id)

        if blog:
            try:
                self.storage.delete(blog)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle blog comment deletion
    def delete_blog_comment(self, blog_comment_id: int) -> None:
        """Delete blog comment

        Args:
            blog_comment_id (int): blog comment id
        """

        blog_comment = self.storage.get(BlogComment, blog_comment_id)

        if blog_comment:
            try:
                self.storage.delete(blog_comment)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle repo deletion
    def delete_repo(self, repo_id: int) -> None:
        """Delete repo

        Args:
            repo_id (int): repo id
        """

        repo = self.storage.get(Repo, repo_id)

        if repo:
            try:
                self.storage.delete(repo)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle ghub deletion
    def delete_ghub(self, ghub_id: int) -> None:
        """Delete ghub

        Args:
            ghub_id (int): ghub id
        """

        ghub = self.storage.get(Ghub, ghub_id)

        if ghub:
            try:
                self.storage.delete(ghub)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle heat deletion
    def delete_heat(self, heat_id: int) -> None:
        """Delete heat

        Args:
            heat_id (int): heat id
        """

        heat = self.storage.get(Heat, heat_id)

        if heat:
            try:
                self.storage.delete(heat)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle heat comment deletion
    def delete_heat_comment(self, heat_comment_id: int) -> None:
        """Delete heat comment

        Args:
            heat_comment_id (int): heat comment id
        """

        heat_comment = self.storage.get(HeatComment, heat_comment_id)

        if heat_comment:
            try:
                self.storage.delete(heat_comment)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle task deletion
    def delete_task(self, task_id: int) -> None:
        """Delete task

        Args:
            task_id (int): task id
        """

        task = self.storage.get(Task, task_id)

        if task:
            try:
                self.storage.delete(task)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Handle task comment deletion
    def delete_task_comment(self, task_comment_id: int) -> None:
        """Delete task comment

        Args:
            task_comment_id (int): task comment id
        """

        task_comment = self.storage.get(TaskComment, task_comment_id)

        if task_comment:
            try:
                self.storage.delete(task_comment)
                self.storage.commit()

            except Exception as e:
                self.storage.rollback()
                raise e

        else:
            return None

    # Representation
    def __repr__(self) -> str:
        """String representation of the class.

        Returns:
            str: String representation of the class
        """
        return f'<Delete>'


delete = Delete()

if __name__ == '__main__':
    print(delete.delete_blog(18))