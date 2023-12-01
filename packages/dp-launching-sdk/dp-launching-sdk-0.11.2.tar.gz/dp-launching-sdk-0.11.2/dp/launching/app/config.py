import os
from pathlib import Path
from tempfile import gettempdir

DEBUG_MODE = True if os.getenv("DEBUG_MODE") in ("True", "true", "1") else False

DRY_RUN_MODE = True if os.getenv("DRY_RUN_MODE") in ("True", "true", "1") else False

LAUNCHING_API_BASE = os.getenv("LAUNCHING_API_BASE", "https://launching.local.dp.tech")

LAUNCHING_ROOT = Path(os.getenv("LAUNCHING_ROOT") or "var").absolute()
LAUNCHING_ROOT.mkdir(parents=True, exist_ok=True)

# LAUNCHING_JOBS_ROOT = LAUNCHING_ROOT / "jobs"
# LAUNCHING_JOBS_ROOT.mkdir(parents=True, exist_ok=True)
# LAUNCHING_JOBS_DRAFT_ROOT = LAUNCHING_ROOT / "draft-jobs"
# LAUNCHING_JOBS_DRAFT_ROOT.mkdir(parents=True, exist_ok=True)

LAUNCHING_UPLOADED_FILE_TMPDIR = Path(gettempdir()) / "uploaded-files"
LAUNCHING_UPLOADED_FILE_TMPDIR.mkdir(parents=True, exist_ok=True)

FAKE_USER = os.getenv("FAKE_USER", "fake@dp.tech")
