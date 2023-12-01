from user_agents import parse

from streamlit.runtime import Runtime
from streamlit.runtime.scriptrunner import get_script_run_ctx


def _get_session_id():
    context = get_script_run_ctx()
    if not context:
        return
    return context.session_id


def _get_current_request():
    session_id = _get_session_id()
    if not session_id:
        return None
    runtime = Runtime._instance
    if not runtime:
        return
    client = runtime.get_client(session_id)
    if not client:
        return
    return client.request


def get_web_origin():
    request = _get_current_request()
    return request.headers["Origin"] if request else None


def get_request_headers():
    request = _get_current_request()
    return request.headers if request else None


def get_ua() -> str:
    headers = get_request_headers()
    if headers:
        return headers.get("User-Agent")
    return None


def is_on_mac_chrome():
    # Windows Chrome: Mozilla/5.0 (Windows NT 10.0; Win64; x64)       AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
    # Mac Chrome:     Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36
    # Mac Safari:     Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15
    ua = get_ua()
    return ua.find("Mac OS") > -1 and ua.find("Chrome") > -1


def get_remote_ip():
    headers = get_request_headers()
    if not headers:
        return
    client_ips = (
        headers.get("X-Original-Forwarded-For")
        or headers.get("X-Forwarded-For")
        or headers.get("X-Real-Ip")
    )
    if not client_ips:
        return
    return client_ips.split(",")[0]


def get_user_agent():
    ua_string = get_ua() or ""
    return parse(ua_string)


def is_iphone_access():
    ua = get_user_agent()
    return ua.is_mobile and ua.os.family == "iOS"


def is_mobile_access():
    user_agent = get_user_agent()
    return user_agent.is_mobile if user_agent else False
