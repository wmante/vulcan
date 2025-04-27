"""
Deployment page for the Vulcan web application.
"""
import json
from typing import Dict, List, Any

import streamlit as st

from vulcan.apps.web.api.client import VulcanAPIClient
from vulcan.apps.web.config import DEFAULT_BRANCH, DEFAULT_COMMIT_MESSAGE, ENABLE_DEPLOYMENT


def render_deployment_page(api_client: VulcanAPIClient) -> None:
    """
    Render the deployment page.
    
    Args:
        api_client: API client for interacting with the Vulcan API
    """
    # Header
    st.markdown("<h1 class='main-header'>Deployment</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='sub-header'>Deploy your code to GitHub</p>",
        unsafe_allow_html=True,
    )
    
    # Check if deployment is enabled
    if not ENABLE_DEPLOYMENT:
        st.warning(
            "Deployment is currently disabled. Please contact your administrator to enable it."
        )
        return
    
    # Check if code is available from code generation or testing
    has_code = False
    code_content = {}
    
    if hasattr(st.session_state, "deployment_code") and st.session_state.deployment_code:
        has_code = True
        code_content = st.session_state.deployment_code
    
    # Form for deployment
    with st.form("deployment_form"):
        if not has_code:
            # Code input
            st.markdown("### Code to Deploy")
            
            # File path input
            file_path = st.text_input(
                "File Path",
                placeholder="e.g., factorial.py",
            )
            
            # Code content input
            code = st.text_area(
                "Code Content",
                placeholder="Enter your code here...",
                height=300,
            )
            
            if file_path and code:
                code_content = {file_path: code}
        else:
            # Display code from code generation or testing
            st.markdown("### Code from Previous Step")
            
            for file_path, content in code_content.items():
                with st.expander(file_path, expanded=True):
                    st.code(content, language="python")
        
        # Deployment options
        st.markdown("### Deployment Options")
        
        # Repository URL
        repository_url = st.text_input(
            "Repository URL",
            placeholder="https://github.com/username/repo.git",
        )
        
        # Branch
        branch = st.text_input(
            "Branch",
            value=DEFAULT_BRANCH,
        )
        
        # Commit message
        commit_message = st.text_area(
            "Commit Message",
            value=DEFAULT_COMMIT_MESSAGE,
            height=100,
        )
        
        # Submit button
        submitted = st.form_submit_button("Deploy Code")
    
    # Handle form submission
    if submitted and code_content and repository_url:
        with st.spinner("Deploying code..."):
            # Call API to deploy code
            result = api_client.deploy_code(
                code_content=code_content,
                repository_url=repository_url,
                branch=branch,
                commit_message=commit_message,
            )
            
            # Store result in session state
            st.session_state.deployment_result = result
    
    # Display result if available
    if hasattr(st.session_state, "deployment_result") and st.session_state.deployment_result:
        result = st.session_state.deployment_result
        
        if result.get("success"):
            st.markdown("<div class='success-box'>", unsafe_allow_html=True)
            st.markdown("### Deployment Completed Successfully!")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Display process ID
            st.markdown(f"**Process ID:** {result.get('process_id')}")
            
            # Display deployment URL if available
            deployment_url = result.get("deployment_url")
            if deployment_url:
                st.markdown(f"**Deployment URL:** [{deployment_url}]({deployment_url})")
            
            # Display logs
            logs = result.get("logs", [])
            if logs:
                st.markdown("### Deployment Logs")
                
                for log in logs:
                    st.text(log)
        else:
            st.markdown("<div class='error-box'>", unsafe_allow_html=True)
            st.markdown("### Error Deploying Code")
            st.markdown(f"Error: {result.get('error_message', 'Unknown error')}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Help section
    with st.expander("Help"):
        st.markdown(
            """
            ### How Deployment Works
            
            1. **Repository Setup**: The system connects to the specified GitHub repository.
            2. **Branch Creation**: If the branch doesn't exist, it will be created.
            3. **Code Commit**: The code is committed to the repository.
            4. **Pull Request**: Optionally, a pull request can be created.
            
            ### Tips for Successful Deployment
            
            1. **Use HTTPS URLs**: Make sure to use HTTPS URLs for the repository.
            2. **Provide Access**: Ensure the system has access to the repository.
            3. **Choose Appropriate Branch**: Use a feature branch for development.
            4. **Write Clear Commit Messages**: Describe the changes in the commit message.
            """
        )