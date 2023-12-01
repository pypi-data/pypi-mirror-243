"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

st.title(f"aagent v{version('aagent')}")  # type: ignore[no-untyped-call]
