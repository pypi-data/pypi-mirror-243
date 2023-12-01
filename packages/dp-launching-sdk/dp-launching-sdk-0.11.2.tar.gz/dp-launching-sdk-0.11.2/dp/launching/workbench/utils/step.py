import streamlit as st

__all__ = ["step_session_prefix", "reset_after_step_session", "clear_step_session"]


def step_session_prefix(step: int):
    return f"step-{step}-"


def reset_after_step_session(keep_step: int, max_step: int):
    for step in range(max_step, keep_step, -1):
        clear_step_session(step)


def clear_step_session(step: int):
    prefix = step_session_prefix(step)
    for key in st.session_state.keys():
        if key.startswith(prefix):
            del st.session_state[key]
