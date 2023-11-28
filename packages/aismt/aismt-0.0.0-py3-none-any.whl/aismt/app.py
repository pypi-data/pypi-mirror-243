"""Streamlit app."""

from importlib.metadata import version

import streamlit as st

st.title(f"aismt v{version('aismt')}")  # type: ignore[no-untyped-call]
