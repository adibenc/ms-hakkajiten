"""Article repository (placeholder for future expansion)"""

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.repository import BBaseRepository
from app.models.article import Article
from typing import List, Optional


class ArticleRepository(BBaseRepository):
    """Article repository (placeholder for future expansion)"""

    def __init__(self):
        super().__init__()

    async def get_all(self, db: AsyncSession) -> List[Article]:
        """
        Get all articles

        Args:
            db: Database session

        Returns:
            List of articles
        """
        query = select(Article)
        result = await db.execute(query)
        return result.scalars().all()
