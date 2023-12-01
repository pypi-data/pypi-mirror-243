import os

import jwt
import base64
from pathlib import Path

from loguru import logger
import streamlit as st
import extra_streamlit_components as stx

from dp.launching.workbench.config import (
    LAUNCHING_SESSIONS_ROOT,
    FAKE_USER,
    WORKSPACE_INFO_SESSION_KEY,
    LAUNCHING_APPLICATION_VERSION,
)


LAUNCHING_JWT_PUBLIC_KEY = os.getenv("LAUNCHING_JWT_PUBLIC_KEY")

cookie_manager = stx.CookieManager()

__all__ = [
    "get_current_session",
    "get_current_session_name",
    "get_current_user",
    "get_current_paid_account",
    "get_current_bohrium_project",
    "get_user_session_root",
    "is_anonymous_user",
]


def get_current_session():
    if os.getenv("DRY_RUN_MODE"):
        return 1
    info = _get_current_workbench_info()
    return info["payload"]["session"]


def get_current_session_name():
    if os.getenv("DRY_RUN_MODE"):
        return "fake-session"
    info = _get_current_workbench_info()
    return info["payload"]["session-name"]


def get_current_user():
    if os.getenv("DRY_RUN_MODE"):
        return FAKE_USER
    info = _get_current_workbench_info()
    return info["name"] if info else None


def get_current_bohrium_project_available():
    if os.getenv("DRY_RUN_MODE"):
        return True
    info = _get_current_workbench_info()
    return info["payload"]["paid_project_available"]


def get_current_bohrium_project():
    if os.getenv("DRY_RUN_MODE"):
        return "fake-project"
    info = _get_current_workbench_info()
    return info["payload"]["paid_project_id"]


def get_current_paid_account():
    if os.getenv("DRY_RUN_MODE"):
        return "fake-account"
    info = _get_current_workbench_info()
    return info["payload"]["paid_account"]


def get_current_job_version():
    if os.getenv("DRY_RUN_MODE"):
        return "fake-project"
    info = _get_current_workbench_info()
    return info["payload"].get("job_version", LAUNCHING_APPLICATION_VERSION)


def _get_current_workbench_info():
    if st.session_state.get(WORKSPACE_INFO_SESSION_KEY):
        return st.session_state.get(WORKSPACE_INFO_SESSION_KEY)
    query_string = st.experimental_get_query_params()
    token = query_string.get("dp_token")
    if not token:
        return None
    info = None
    try:
        public_key = base64.b64decode(LAUNCHING_JWT_PUBLIC_KEY)
        info = jwt.decode(
            jwt=token[0],
            key=public_key,
            algorithms=[
                "RS256",
            ],
        )
    except Exception as e:
        logger.error(f"failed get_session_from_token: {e}")
    if info:
        st.session_state[WORKSPACE_INFO_SESSION_KEY] = info
    return info


def get_user_session_root(user: str) -> Path:
    root = LAUNCHING_SESSIONS_ROOT / user
    if not root.exists():
        root.mkdir(parents=True, exist_ok=True)
    return root


def is_anonymous_user(user: str) -> bool:
    return user == "anonymous@anonymous.tech"
