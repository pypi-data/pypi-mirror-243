import streamlit as st
from dp.launching.workbench.utils.session import is_iphone_access

IPHONE_MAGIC_TYPES = {"pdb", "sdf", "mol", "pdbqt"}


def file_uploader(
    label,
    type=None,
    accept_multiple_files=False,
    key=None,
    help=None,
    on_change=None,
    args=None,
    kwargs=None,
    *,
    disabled=False,
    label_visibility="visible"
):
    if type and is_iphone_access():
        if isinstance(type, (list, tuple)) and any(
            i.lower() in IPHONE_MAGIC_TYPES for i in type
        ):
            type = None
        elif isinstance(type, str) and type.lower() in IPHONE_MAGIC_TYPES:
            type = None
    return st.file_uploader(
        label,
        type,
        accept_multiple_files,
        key,
        help,
        on_change,
        args,
        kwargs,
        disabled=disabled,
        label_visibility=label_visibility,
    )
