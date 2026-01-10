from infra.database.models import File
from infra.database.repositories.base_repository import BaseRepository
from schemas.file import FileResponse


class FilesRepository(BaseRepository):
    model = File
    schema = FileResponse
