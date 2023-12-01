import os
from pathlib import Path
from tempfile import gettempdir

NOT_SYNCED_PREFIX = "$NOT_SYNCED$"

DEBUG_MODE = True if os.getenv("DEBUG_MODE") in ("True", "true", "1") else False

DRY_RUN_MODE = True if os.getenv("DRY_RUN_MODE") in ("True", "true", "1") else False

LAUNCHING_API_BASE = os.getenv("LAUNCHING_API_BASE", "https://launching.local.dp.tech")

LAUNCHING_APPLICATION_NAME = os.getenv("LAUNCHING_APPLICATION_NAME")
LAUNCHING_APPLICATION_TOKEN = os.getenv("LAUNCHING_APPLICATION_TOKEN")
LAUNCHING_APPLICATION_OWNER = os.getenv("LAUNCHING_APPLICATION_OWNER")
LAUNCHING_APPLICATION_VERSION = os.getenv("LAUNCHING_APPLICATION_VERSION")

LAUNCHING_ROOT = Path(os.getenv("LAUNCHING_ROOT") or "var").absolute()
LAUNCHING_ROOT.mkdir(parents=True, exist_ok=True)

LAUNCHING_SESSIONS_ROOT = (
    Path(os.getenv("LAUNCHING_SESSIONS_ROOT"))
    if os.getenv("LAUNCHING_SESSIONS_ROOT")
    else LAUNCHING_ROOT / "sessions"
)
LAUNCHING_SESSIONS_ROOT.mkdir(parents=True, exist_ok=True)
LAUNCHING_JOBS_ROOT = LAUNCHING_ROOT / "jobs"
LAUNCHING_JOBS_ROOT.mkdir(parents=True, exist_ok=True)
LAUNCHING_JOBS_DRAFT_ROOT = LAUNCHING_ROOT / "draft-jobs"
LAUNCHING_JOBS_DRAFT_ROOT.mkdir(parents=True, exist_ok=True)

LAUNCHING_UPLOADED_FILE_TMPDIR = Path(gettempdir()) / "uploaded-files"
LAUNCHING_UPLOADED_FILE_TMPDIR.mkdir(parents=True, exist_ok=True)

FAKE_USER = os.getenv("FAKE_USER", "fake@dp.tech")


def get_not_synced_key(user_key: str) -> str:
    return NOT_SYNCED_PREFIX + "_" + user_key


WORKSPACE_INFO_SESSION_KEY = get_not_synced_key("current_workspace_info")
