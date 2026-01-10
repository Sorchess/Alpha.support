import mimetypes
import unicodedata
from pathlib import Path
from urllib.parse import quote
from fastapi import UploadFile


def get_ext_from_upload(file: UploadFile) -> str:
    ext = ""
    if file.content_type:
        ext = mimetypes.guess_extension(file.content_type, strict=False)
        if ext == ".jpe":
            ext = ".jpg"
    if not ext and file.filename:
        ext = Path(file.filename).suffix
    return ext or ".bin"


def sanitize_filename(name: str, default: str) -> str:
    normalized = unicodedata.normalize("NFKD", name)
    ascii_only = normalized.encode("ascii", "ignore").decode("ascii").strip()
    ascii_only = ascii_only.replace("/", "_").replace("\\", "_").replace(" ", "_")
    return ascii_only[:180] if ascii_only else default


def build_content_disposition(original_name: str | None, default_name: str) -> str:
    safe_ascii = sanitize_filename(original_name or "", default=default_name)
    utf8_name = original_name or default_name
    quoted_ascii = safe_ascii.replace('"', '\\"')
    filename_star = quote(utf8_name, safe="!#$&+-.^_`|~")
    return f"attachment; filename=\"{quoted_ascii}\"; filename*=UTF-8''{filename_star}"
