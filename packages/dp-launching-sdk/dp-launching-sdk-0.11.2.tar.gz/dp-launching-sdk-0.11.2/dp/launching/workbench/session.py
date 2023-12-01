import uuid
import os
import os.path
import json
from pathlib import Path
from urllib.parse import urljoin
from typing import Optional, Dict, Tuple, Any, List

import sh
import requests
from loguru import logger
import streamlit as st

from dp.launching.workbench.config import (
    DRY_RUN_MODE,
    LAUNCHING_API_BASE,
    LAUNCHING_APPLICATION_NAME,
    LAUNCHING_APPLICATION_VERSION,
    LAUNCHING_APPLICATION_OWNER,
    LAUNCHING_APPLICATION_TOKEN,
    LAUNCHING_JOBS_ROOT,
    LAUNCHING_JOBS_DRAFT_ROOT,
)

from dp.launching.workbench.user import (
    get_current_user,
    get_current_session,
)

__all__ = ["get_session_saved_data", "save_session_data"]

LAUNCHING_SESSION_KEY = "launching_saved_data"


def get_session_saved_data(key, default=""):
    data = _get_session_saved_data()
    if not data:
        return default
    return data.get(key, default)


def _get_session_saved_data():
    data = st.session_state.get(LAUNCHING_SESSION_KEY)

    if not data:
        if DRY_RUN_MODE:
            return {
                "target_molecule": "CCO",
                "options": {
                    "retro_system": "unimol0621_bart0702_similarity",
                    "check_system": "unimol0717",
                    "optional_retro_system": "",
                },
                "current_step": 2,
            }
        data = _get_session_saved_data_from_remote() or {}
        st.session_state[LAUNCHING_SESSION_KEY] = data
    return data


def _get_session_saved_data_from_remote():
    session_id = get_current_session()
    params = {
        "session_id": session_id,
        "user": get_current_user(),
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LAUNCHING_APPLICATION_TOKEN}",
    }
    url = urljoin(
        LAUNCHING_API_BASE,
        f"/api/jobs/{LAUNCHING_APPLICATION_NAME}/session/{session_id}",
    )
    response = requests.request("GET", url, headers=headers, params=params)
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(
            f"get session data {session_id} failed, status code: {response.status_code} {e}"
        )  # noqa
    data = response.json()
    if data.get("code") != 200:
        logger.error(data)
        logger.exception(Exception(data.get("error")))
    return data.get("data")


def save_session_data(data: dict):
    if os.getenv("DRY_RUN_MODE"):
        session_data = _get_session_saved_data()
        session_data.update(data)
        st.session_state[LAUNCHING_SESSION_KEY] = session_data
        return data

    session_id = get_current_session()
    req_data = {
        "session_id": int(session_id),
        "application_name": LAUNCHING_APPLICATION_NAME,
        "application_token": LAUNCHING_APPLICATION_TOKEN,
        "user": get_current_user(),
        "data": data,
    }
    url = urljoin(
        LAUNCHING_API_BASE,
        f"/api/jobs/{LAUNCHING_APPLICATION_NAME}/session/{session_id}",
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, json=req_data)
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(
            f"save session {session_id} failed, status code: {response.status_code} {e}"
        )  # noqa
    resp = response.json()
    if resp.get("code") != 200:
        logger.error(data)
        logger.exception(Exception(resp.get("error")))

    # save to session state
    session_data = _get_session_saved_data()
    session_data.update(data)
    st.session_state[LAUNCHING_SESSION_KEY] = session_data

    return session_data
