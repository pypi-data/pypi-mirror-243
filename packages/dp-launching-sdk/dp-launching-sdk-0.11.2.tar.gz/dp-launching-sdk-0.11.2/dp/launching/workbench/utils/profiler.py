from typing import Any
import streamlit as st


class LaunchingProfiler:
    def __init__(self, skip=False):
        if not skip:
            from pyinstrument import Profiler

            self.profiler = Profiler()
        else:
            self.profiler = None

    def __enter__(self):
        if self.profiler:
            import inspect

            self.profiler.start(caller_frame=inspect.currentframe().f_back)
        return self

    def __exit__(self, *args: Any):
        if self.profiler:
            from streamlit_embeded import st_embeded

            self.profiler.stop()
            with st.expander("System Profiling"):
                st_embeded(self.profiler.output_html(timeline=False), height=1000)
        return False
