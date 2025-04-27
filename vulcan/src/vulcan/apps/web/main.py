"""
Web application entry point for the Vulcan web interface.
"""
import logging
import os
from typing import Dict, Any

import streamlit as st

from vulcan.apps.web.api.client import VulcanAPIClient
from vulcan.apps.web.pages.home import render_home_page
from vulcan.apps.web.pages.code_generation import render_code_generation_page
from vulcan.apps.web.pages.testing import render_testing_page
from vulcan.apps.web.pages.deployment import render_deployment_page
from vulcan.apps.web.config import (
    APP_TITLE,
    APP_DESCRIPTION,
    APP_VERSION,
    API_URL,
    API_KEY,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("vulcan-web")


def setup_page() -> None:
    """Set up the Streamlit page."""
    st.set_page_config(
        page_title=APP_TITLE,
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Add custom CSS
    st.markdown(
        """
        <style>
        .main-header {
            font-size: 2.5rem;
            margin-bottom: 1rem;
        }
        .sub-header {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .info-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f0f2f6;
            margin-bottom: 1rem;
        }
        .success-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #d1fae5;
            margin-bottom: 1rem;
        }
        .error-box {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #fee2e2;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def initialize_session_state() -> None:
    """Initialize the Streamlit session state."""
    if "page" not in st.session_state:
        st.session_state.page = "home"
    
    if "api_client" not in st.session_state:
        st.session_state.api_client = VulcanAPIClient(API_URL, API_KEY)
    
    if "code_generation_result" not in st.session_state:
        st.session_state.code_generation_result = None
    
    if "testing_result" not in st.session_state:
        st.session_state.testing_result = None
    
    if "deployment_result" not in st.session_state:
        st.session_state.deployment_result = None


def render_sidebar() -> None:
    """Render the sidebar navigation."""
    st.sidebar.title("Vulcan")
    st.sidebar.caption(f"v{APP_VERSION}")
    
    st.sidebar.markdown("---")
    
    # Navigation
    if st.sidebar.button("Home", key="nav_home"):
        st.session_state.page = "home"
    
    if st.sidebar.button("Code Generation", key="nav_code_generation"):
        st.session_state.page = "code_generation"
    
    if st.sidebar.button("Testing", key="nav_testing"):
        st.session_state.page = "testing"
    
    if st.sidebar.button("Deployment", key="nav_deployment"):
        st.session_state.page = "deployment"
    
    st.sidebar.markdown("---")
    
    # API Status
    api_status = st.session_state.api_client.check_health()
    if api_status:
        st.sidebar.success("API Connected")
    else:
        st.sidebar.error("API Disconnected")
    
    # About
    st.sidebar.markdown("---")
    st.sidebar.info(
        """
        **Vulcan** is an autonomous coding agent that can write, test, and deploy code based on user instructions.
        """
    )


def main() -> None:
    """Main entry point for the web application."""
    # Set up the page
    setup_page()
    
    # Initialize session state
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render the selected page
    if st.session_state.page == "home":
        render_home_page()
    elif st.session_state.page == "code_generation":
        render_code_generation_page(st.session_state.api_client)
    elif st.session_state.page == "testing":
        render_testing_page(st.session_state.api_client)
    elif st.session_state.page == "deployment":
        render_deployment_page(st.session_state.api_client)


if __name__ == "__main__":
    main()