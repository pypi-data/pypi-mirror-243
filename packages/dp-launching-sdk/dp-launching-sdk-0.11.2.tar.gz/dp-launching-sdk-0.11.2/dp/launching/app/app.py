import os
import sh
import json
import uuid
import requests
from typing import Optional, Dict, Tuple, List, Any
from urllib.parse import urljoin
from loguru import logger
from pathlib import Path
from dp.launching.app import config
from dp.launching.utils.tools import lazy_property


class PaymentInfo:
    paid_account: str
    paid_project_id: str

    def __init__(self, paid_account, paid_project_id):
        self.paid_account = paid_account
        self.paid_project_id = paid_project_id


def ensure_path_exists(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


class App:
    app_name: str
    app_secret: str

    def __init__(self, app_name, app_secret):
        self.app_name = app_name
        self.app_secret = app_secret

    @lazy_property
    def get_draft_job_root(self):
        path = config.LAUNCHING_ROOT / self.app_name / "draft-jobs"
        return ensure_path_exists(path)

    @lazy_property
    def get_job_root(self):
        path = config.LAUNCHING_ROOT / self.app_name / "jobs"
        return ensure_path_exists(path)

    def get_job_output_path(self, job_id: str):
        path = self.get_job_root / job_id / "outputs"
        return ensure_path_exists(path)

    def get_job_log_path(self, job_id: str):
        return self.get_job_output_path(job_id) / "STDOUTERR.log"

    @lazy_property
    def get_tmp_root(self):
        path = config.LAUNCHING_ROOT / self.app_name / "uploaded-files"
        return ensure_path_exists(path)

    @lazy_property
    def get_log_path(self):
        return config.LAUNCHING_ROOT / self.app_name / "jobs"

    def submit_job(
        self,
        payment_info: PaymentInfo,
        job_name: str = "",
        files: Dict = {},
        params: Dict = {},
        props: Dict = {},
        version: str = "",
        session_id: str = "",
        submit_params: Dict = {},
    ) -> Optional[str]:
        # TODO check user shortTerm ticket/orderId
        logger.info(f"submit job {job_name}: params {params}, props {props}")
        if config.DRY_RUN_MODE:
            return "fake-dryrun-job-id" + str(uuid.uuid4())

        creator = payment_info.paid_account
        job_id = f"{job_name}-{uuid.uuid4().hex[:8]}"
        draft_job_path = self.get_draft_job_root

        logger.info(f"start prepare inputs for job {job_id}")
        for field_name, origin_file_path in files.items():
            file_path = draft_job_path / field_name
            file_path.mkdir(parents=True, exist_ok=True)
            logger.debug(f"copy {origin_file_path} to {file_path}")
            sh.cp(
                origin_file_path, (file_path / os.path.basename(origin_file_path))
            )  # noqa
        logger.debug(f"end prepare inputs for job {job_id}")
        url = urljoin(config.LAUNCHING_API_BASE, "/api/jobs/")

        props = props or {}
        props.update(
            {
                "paid_account": payment_info.paid_account,
                "paid_project_id": payment_info.paid_project_id,
                # TODO support more login type
                "login_type": "bohrium",
            }
        )
        if session_id:
            props["session"] = session_id

        payload = json.dumps(
            {
                "job_id": job_id,
                "description": "job created from workbench",
                "application": self.app_name,
                "token": self.app_secret,
                "version": version,
                "creator": creator,
                "from_labs": True,  # TODO FIXME both launching & labs can access workbench
                "params": params,
                "properties": props,
                "submit_params": submit_params,
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
            logger.error(data["error"])
            return None
        return job_id

    def get_job_status(self, payment_info: PaymentInfo, job_id: str):
        if config.DRY_RUN_MODE:
            return "success"

        url = urljoin(
            config.LAUNCHING_API_BASE, f"/api/jobs/{self.app_name}/{job_id}/status"
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

    def get_job_logs(
        self, payment_info: PaymentInfo, job_id: str, nlast: int = 1000
    ) -> Optional[str]:
        if config.DRY_RUN_MODE:
            return "fake-dryrun-log"
        log_path = self.get_job_log_path(job_id)
        if log_path.exists():
            return str(sh.tail("-n", nlast, log_path))

    def cancel_job(self, payment_info: PaymentInfo, job_id: str) -> Optional[str]:
        payload = json.dumps(
            {
                "job_id": job_id,
                "application": self.app_name,
                "token": self.app_secret,
            }
        )
        headers = {"Content-Type": "application/json"}
        url = urljoin(config.LAUNCHING_API_BASE, "/api/jobs/stop_job")
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
            logger.error(data["error"])
            return None
        return job_id

    def get_jobs_by_session_id(
        self, payment_info: PaymentInfo, session_id: str
    ) -> Tuple[int, List[Any]]:
        if config.DRY_RUN_MODE:
            return 0, []

        url = urljoin(config.LAUNCHING_API_BASE, f"/api/jobs/{self.app_name}")
        session_id = session_id
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.app_secret}",
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
        if data.get("code") != 200:
            logger.error(data)
            logger.exception(Exception(data.get("error")))
        return data.get("count"), data.get("data")
