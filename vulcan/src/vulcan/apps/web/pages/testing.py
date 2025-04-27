"""
Testing page for the Vulcan web application.
"""
import json
from typing import Dict, List, Any

import streamlit as st

from vulcan.apps.web.api.client import VulcanAPIClient
from vulcan.apps.web.config import DEFAULT_GENERATE_COVERAGE


def render_testing_page(api_client: VulcanAPIClient) -> None:
    """
    Render the testing page.
    
    Args:
        api_client: API client for interacting with the Vulcan API
    """
    # Header
    st.markdown("<h1 class='main-header'>Testing</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p class='sub-header'>Run tests on your code</p>",
        unsafe_allow_html=True,
    )
    
    # Check if code is available from code generation
    has_code = False
    code_content = {}
    
    if hasattr(st.session_state, "testing_code") and st.session_state.testing_code:
        has_code = True
        code_content = st.session_state.testing_code
    
    # Form for testing
    with st.form("testing_form"):
        if not has_code:
            # Code input
            st.markdown("### Code to Test")
            
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
            # Display code from code generation
            st.markdown("### Code from Code Generation")
            
            for file_path, content in code_content.items():
                with st.expander(file_path, expanded=True):
                    st.code(content, language="python")
        
        # Testing options
        st.markdown("### Testing Options")
        
        # Generate coverage report
        generate_coverage = st.checkbox(
            "Generate Coverage Report",
            value=DEFAULT_GENERATE_COVERAGE,
        )
        
        # Submit button
        submitted = st.form_submit_button("Run Tests")
    
    # Handle form submission
    if submitted and code_content:
        with st.spinner("Running tests..."):
            # Call API to run tests
            result = api_client.run_tests(
                code_content=code_content,
                generate_coverage=generate_coverage,
            )
            
            # Store result in session state
            st.session_state.testing_result = result
    
    # Display result if available
    if hasattr(st.session_state, "testing_result") and st.session_state.testing_result:
        result = st.session_state.testing_result
        
        if result.get("success"):
            st.markdown("<div class='success-box'>", unsafe_allow_html=True)
            st.markdown("### Tests Completed Successfully!")
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Display process ID
            st.markdown(f"**Process ID:** {result.get('process_id')}")
            
            # Display test results
            st.markdown("### Test Results")
            
            test_results = result.get("test_results", [])
            if test_results:
                # Create a table of test results
                results_data = []
                for test_result in test_results:
                    status = "✅ Passed" if test_result.get("passed") else "❌ Failed"
                    results_data.append({
                        "Test": test_result.get("name"),
                        "Status": status,
                        "Duration": f"{test_result.get('execution_time', 0):.3f}s",
                        "Error": test_result.get("error_message", ""),
                    })
                
                # Display as a table
                st.table(results_data)
                
                # Summary
                passed = sum(1 for r in test_results if r.get("passed"))
                total = len(test_results)
                st.markdown(f"**Summary:** {passed}/{total} tests passed")
            else:
                st.info("No test results available.")
            
            # Display coverage if available
            coverage = result.get("coverage")
            if coverage:
                st.markdown("### Coverage Report")
                
                # Create a table of coverage data
                coverage_data = [
                    {"Type": "Line Coverage", "Percentage": f"{coverage.get('line', 0):.1f}%"},
                    {"Type": "Branch Coverage", "Percentage": f"{coverage.get('branch', 0):.1f}%"},
                    {"Type": "Function Coverage", "Percentage": f"{coverage.get('function', 0):.1f}%"},
                ]
                
                # Display as a table
                st.table(coverage_data)
            
            # Add button to deploy code
            if st.button("Deploy Code"):
                st.session_state.page = "deployment"
                # Prepare code content for deployment
                st.session_state.deployment_code = code_content
        else:
            st.markdown("<div class='error-box'>", unsafe_allow_html=True)
            st.markdown("### Error Running Tests")
            st.markdown(f"Error: {result.get('error_message', 'Unknown error')}")
            st.markdown("</div>", unsafe_allow_html=True)
    
    # Help section
    with st.expander("Help"):
        st.markdown(
            """
            ### How Testing Works
            
            1. **Code Analysis**: The system analyzes your code to understand its structure.
            2. **Test Generation**: Tests are automatically generated based on the code.
            3. **Test Execution**: The tests are executed against your code.
            4. **Coverage Analysis**: If enabled, a coverage report is generated.
            
            ### Tips for Better Testing
            
            1. **Include docstrings**: Docstrings help the system understand the expected behavior.
            2. **Use type hints**: Type hints make it easier to generate appropriate test cases.
            3. **Handle edge cases**: Make sure your code handles edge cases properly.
            4. **Follow best practices**: Well-structured code is easier to test.
            """
        )