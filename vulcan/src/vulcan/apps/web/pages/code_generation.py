"""
Code generation page for the Vulcan web application.
"""
import json
import time
from typing import Dict, List, Any

import streamlit as st

from vulcan.apps.web.api.client import VulcanAPIClient
from vulcan.apps.web.config import DEFAULT_CONSTRAINTS


def render_code_generation_page(api_client: VulcanAPIClient) -> None:
    """
    Render the code generation page.
    
    Args:
        api_client: API client for interacting with the Vulcan API
    """
    # Header
    st.markdown("<h1 class='main-header'>Code Generation</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='sub-header'>Generate code based on your requirements</p>",
        unsafe_allow_html=True,
    )
    
    # Form for code generation
    with st.form("code_generation_form"):
        # Description
        description = st.text_area(
            "Description",
            placeholder="Describe the code you want to generate...",
            height=150,
        )
        
        # Constraints
        st.markdown("### Constraints")
        constraints = []
        
        # Default constraints with checkboxes
        for constraint in DEFAULT_CONSTRAINTS:
            if st.checkbox(constraint, value=True):
                constraints.append(constraint)
        
        # Custom constraints
        custom_constraints = st.text_area(
            "Custom Constraints (one per line)",
            placeholder="Enter additional constraints...",
            height=100,
        )
        
        if custom_constraints:
            constraints.extend([c.strip() for c in custom_constraints.split("\n") if c.strip()])
        
        # Examples
        examples = st.text_area(
            "Examples (one per line)",
            placeholder="Enter examples of expected behavior...",
            height=100,
        )
        
        examples_list = []
        if examples:
            examples_list = [e.strip() for e in examples.split("\n") if e.strip()]
        
        # Submit button
        submitted = st.form_submit_button("Generate Code")
    
    # Handle form submission
    if submitted and description:
        with st.spinner("Generating code..."):
            # Call API to generate code
            result = api_client.generate_code(
                description=description,
                constraints=constraints,
                examples=examples_list,
            )
            
            # Store result in session state
            st.session_state.code_generation_result = result
    
    # Display result if available
    if st.session_state.code_generation_result:
        result = st.session_state.code_generation_result
        
        if result.get("success"):
            st.markdown("<div class='success-box'>", unsafe_allow_html=True)
            st.markdown("### Code Generated Successfully!")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Display process ID
            st.markdown(f"**Process ID:** {result.get('process_id')}")
            
            # Display artifacts
            st.markdown("### Generated Files")
            
            artifacts = result.get("artifacts", [])
            if artifacts:
                for i, artifact in enumerate(artifacts):
                    with st.expander(f"{artifact.get('file_path')} ({artifact.get('language')})"):
                        st.code(artifact.get("content"), language=artifact.get("language"))
                        
                        # Add button to run tests on this code
                        if st.button(f"Run Tests on {artifact.get('file_path')}", key=f"test_{i}"):
                            st.session_state.page = "testing"
                            # Prepare code content for testing
                            st.session_state.testing_code = {
                                artifact.get("file_path"): artifact.get("content")
                            }
                
                # Add button to run tests on all code
                if st.button("Run Tests on All Files"):
                    st.session_state.page = "testing"
                    # Prepare all code content for testing
                    st.session_state.testing_code = {
                        artifact.get("file_path"): artifact.get("content")
                        for artifact in artifacts
                    }
                
                # Add button to deploy code
                if st.button("Deploy Code"):
                    st.session_state.page = "deployment"
                    # Prepare all code content for deployment
                    st.session_state.deployment_code = {
                        artifact.get("file_path"): artifact.get("content")
                        for artifact in artifacts
                    }
            else:
                st.info("No files were generated.")
        else:
            st.markdown("<div class='error-box'>", unsafe_allow_html=True)
            st.markdown("### Error Generating Code")
            st.markdown(f"Error: {result.get('error_message', 'Unknown error')}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Help section
    with st.expander("Help"):
        st.markdown(
            """
            ### How to Write Good Requirements
            
            1. **Be specific**: Clearly describe what the code should do.
            2. **Provide examples**: Include examples of expected inputs and outputs.
            3. **Specify constraints**: Mention any requirements for error handling, performance, etc.
            4. **Mention the language**: Specify the programming language if you have a preference.
            
            ### Example
            
            **Description:**
            Create a Python function that calculates the factorial of a number. The function should handle negative numbers and return 1 for input 0.
            
            **Constraints:**
            - Must include proper error handling
            - Must include type hints
            - Must include docstrings
            - Must be efficient for large numbers
            
            **Examples:**
            - factorial(5) -> 120
            - factorial(0) -> 1
            - factorial(-1) -> Error
            """
        )