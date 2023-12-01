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
    get_current_bohrium_project,
    get_current_paid_account,
)

from dp.launching.workbench.session import get_current_session


__all__ = ["submit_job", "get_job_status", "get_job_logs", "get_job_output_root"]


def submit_job(
        job_name: str,
        files: Dict,
        params: Dict,
        props: Dict,
        version: str = "",
) -> Optional[str]:
    logger.info(f"submit job {job_name}: params {params}, props {props}")

    if DRY_RUN_MODE:
        return "fake-dryrun-job-id" + str(uuid.uuid4())

    creator = getattr(st.session_state, "user", "")

    job_id = f"{job_name}-{uuid.uuid4().hex[:8]}"
    job_path = LAUNCHING_JOBS_DRAFT_ROOT / job_id / "inputs"
    job_path.mkdir(parents=True, exist_ok=True)

    logger.debug(f"start prepare inputs for job {job_id}")
    for field_name, origin_file_path in files.items():
        file_path = job_path / field_name
        file_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"copy {origin_file_path} to {file_path}")
        sh.cp(
            origin_file_path, (file_path / os.path.basename(origin_file_path))
        )  # noqa
    logger.debug(f"end prepare inputs for job {job_id}")

    url = urljoin(LAUNCHING_API_BASE, "/api/jobs/")

    props = props or {}
    props.update(
        {
            "paid_account": get_current_paid_account(),
            "paid_project_id": get_current_bohrium_project(),
            "session": int(get_current_session())
        }
    )

    # TODO support more login type
    props["login_type"] = "bohrium"
    payload = json.dumps(
        {
            "job_id": job_id,
            "description": "job created from workbench",
            "application": LAUNCHING_APPLICATION_NAME,
            "token": LAUNCHING_APPLICATION_TOKEN,
            "version": version or LAUNCHING_APPLICATION_VERSION,
            "creator": creator or LAUNCHING_APPLICATION_OWNER,
            "from_labs": True,  # FIXME both launching & labs can access workbench
            "params": params,
            "properties": props,
        }
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(
            f"submit job {job_id} to launching failed, status code: {response.status_code}"
        )  # noqa
        logger.exception(e)
        return None
    logger.info(
        f"submit job {job_id} to launching success, status code: {response.status_code}"
    )  # noqa
    data = response.json()
    if data["code"] != 200:
        st.error(data["error"])
        logger.error(data["error"])
        return None
    return job_id


def get_job_status(job_id: str):
    if DRY_RUN_MODE:
        return "success"

    url = urljoin(
        LAUNCHING_API_BASE, f"/api/jobs/{LAUNCHING_APPLICATION_NAME}/{job_id}/status"
    )
    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers)
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(
            f"get job {job_id} status failed, status code: {response.status_code}"
        )  # noqa
        logger.exception(e)
        return "unknown"
    data = response.json()
    return data["status"]


def get_job_logs(job_id: str, nlast: int = 1000) -> Optional[str]:
    if DRY_RUN_MODE:
        return "fake-dryrun-logs"
    log_path = get_job_output_root(job_id) / "STDOUTERR.log"
    if log_path.exists():
        return str(sh.tail("-n", nlast, log_path))


def get_job_output_root(job_id: str) -> Path:
    return LAUNCHING_JOBS_ROOT / job_id / "outputs"


def cancel_job(job_id: str) -> Optional[str]:
    payload = json.dumps(
        {
            "job_id": job_id,
            "application": LAUNCHING_APPLICATION_NAME,
            "token": LAUNCHING_APPLICATION_TOKEN,
        }
    )
    headers = {"Content-Type": "application/json"}
    url = urljoin(LAUNCHING_API_BASE, "/api/jobs/stop_job")
    response = requests.request("POST", url, headers=headers, json=payload)
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(
            f"cancel job {job_id} failed, status code: {response.status_code}"
        )  # noqa
        logger.exception(e)
        return None
    logger.info(
        f"cancel job {job_id} success, status code: {response.status_code}"
    )  # noqa
    data = response.json()
    if data["code"] != 200:
        st.error(data["error"])
        logger.error(data["error"])
        return None
    return job_id


def get_jobs_by_session_id() -> Tuple[int, List[Any]]:
    if DRY_RUN_MODE:
        return 0, []

    url = urljoin(
        LAUNCHING_API_BASE, f"/api/jobs/{LAUNCHING_APPLICATION_NAME}"
    )
    session_id = get_current_session()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {LAUNCHING_APPLICATION_TOKEN}"
    }
    params = {"session_id": session_id}
    response = requests.request("GET", url, headers=headers, params=params)
    try:
        response.raise_for_status()
    except Exception as e:
        logger.error(
            f"get jobs for session {session_id} failed, status code: {response.status_code} {e}"
        )  # noqa
    data = response.json()
    if data.get('code') != 200:
        logger.error(data)
        logger.exception(Exception(data.get('error')))
    return data.get('count'), data.get('data')
