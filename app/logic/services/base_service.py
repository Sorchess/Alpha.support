from dataclasses import dataclass

from infra.database.manager import DatabaseManager


@dataclass(eq=False, frozen=True)
class BaseService:
    db: DatabaseManager
