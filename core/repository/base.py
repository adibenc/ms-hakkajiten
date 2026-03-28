"""Base repository class following fa-pidum pattern"""

from typing import Union
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_scoped_session


class BBaseRepository:
    """Base repository class with raw SQL execution support"""

    row_per_page = 20
    page = 1

    def __init__(self, gsess: Union[AsyncSession, async_scoped_session] = None, db_session: AsyncSession = None):
        self.session = db_session
        self.get_session = gsess

    async def rawQuery(self, rawq="select 1"):
        """
        Execute raw SQL query and return results as list of dicts

        Args:
            rawq: Raw SQL query string

        Returns:
            List of dictionaries representing query results
        """
        if self.session:
            stm = text(rawq)
            result = await self.session.execute(stm)
            rows = result.mappings().all()
            return [dict(r) for r in rows]

        # Use scoped session
        async for s in self.get_session():
            stm = text(rawq)
            result = await s.execute(stm)
            rows = result.mappings().all()
            return [dict(r) for r in rows]
