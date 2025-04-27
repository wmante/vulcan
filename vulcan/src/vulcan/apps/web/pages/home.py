"""
Home page for the Vulcan web application.
"""
import streamlit as st

from vulcan.apps.web.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION


def render_home_page() -> None:
    """Render the home page."""
    # Header
    st.markdown(f"<h1 class='main-header'>{APP_TITLE}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-header'>{APP_DESCRIPTION}</p>", unsafe_allow_html=True)
    
    # Introduction
    st.markdown(
        """
        Welcome to Vulcan, an autonomous coding agent that can write, test, and deploy code based on your instructions.
        
        Vulcan integrates with GitHub for version control and CI/CD pipelines, providing a complete end-to-end solution for autonomous software development.
        """
    )
    
    # Features
    st.markdown("## Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            ### Code Generation
            
            Generate code based on your requirements using advanced language models.
            
            - Type-safe code
            - Proper error handling
            - Well-documented
            - Following best practices
            """
        )
    
    with col2:
        st.markdown(
            """
            ### Testing
            
            Automatically test the generated code to ensure it meets requirements.
            
            - Unit tests
            - Integration tests
            - Coverage reports
            - Mocking external dependencies
            """
        )
    
    with col3:
        st.markdown(
            """
            ### Deployment
            
            Deploy the code to GitHub repositories with proper CI/CD pipelines.
            
            - GitHub integration
            - Branch management
            - Pull requests
            - CI/CD pipelines
            """
        )
    
    # Getting Started
    st.markdown("## Getting Started")
    
    st.markdown(
        """
        1. Navigate to the **Code Generation** page to generate code based on your requirements.
        2. Use the **Testing** page to run tests on the generated code.
        3. Deploy the code to GitHub using the **Deployment** page.
        """
    )
    
    # Call to Action
    st.markdown("## Ready to Get Started?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Generate Code", key="home_generate"):
            st.session_state.page = "code_generation"
    
    with col2:
        if st.button("Run Tests", key="home_test"):
            st.session_state.page = "testing"
    
    with col3:
        if st.button("Deploy Code", key="home_deploy"):
            st.session_state.page = "deployment"
    
    # Footer
    st.markdown("---")
    st.markdown(f"Vulcan v{APP_VERSION} | Built with ❤️ by the Vulcan team")