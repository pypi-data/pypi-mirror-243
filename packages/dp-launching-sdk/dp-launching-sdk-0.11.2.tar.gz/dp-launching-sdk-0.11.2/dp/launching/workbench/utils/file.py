import uuid
import os.path
from pathlib import Path

from loguru import logger
from streamlit.runtime.uploaded_file_manager import UploadedFile

from dp.launching.workbench.config import LAUNCHING_UPLOADED_FILE_TMPDIR

__all__ = ["save_upload_file"]


def save_upload_file(user: str, uploaded_file: UploadedFile):
    user_upload_path: Path = LAUNCHING_UPLOADED_FILE_TMPDIR / user
    user_upload_path.mkdir(parents=True, exist_ok=True)
    basename = os.path.basename(uploaded_file.name)
    fname, ext = tuple(os.path.splitext(basename))
    random_str = uuid.uuid4().hex
    fullpath = user_upload_path / f"{fname}-{random_str}{ext}"
    fullpath.write_bytes(uploaded_file.getvalue())
    logger.info(f"save_upload_file: {user}/{uploaded_file.name} -> {fullpath}")
    return fullpath
