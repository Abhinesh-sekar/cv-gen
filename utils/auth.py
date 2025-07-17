# utils/auth.py
import hashlib
import streamlit as st

def hash_key(key):
    """
    Generate SHA-256 hash of the key
    
    Args:
        key (str): The key to hash
    
    Returns:
        str: SHA-256 hash of the key
    """
    return hashlib.sha256(key.encode()).hexdigest()

def verify_access_key(input_key):
    """
    Verify if the input key matches the stored hash
    
    Args:
        input_key (str): The key entered by user
    
    Returns:
        bool: True if key is correct, False otherwise
    """
    try:
        # Get the stored hash from Streamlit secrets
        stored_hash = st.secrets["auth"]["access_key_hash"]
        
        # Hash the input key
        input_hash = hash_key(input_key)
        
        # Compare hashes
        return input_hash == stored_hash
        
    except KeyError:
        st.error("❌ Authentication configuration not found. Please contact administrator.")
        return False
    except Exception as e:
        st.error(f"❌ Authentication error: {str(e)}")
        return False

def check_authentication():
    """
    Handle authentication flow
    
    Returns:
        bool: True if authenticated, False otherwise
    """
    
    # Check if already authenticated in session
    if 'authenticated' in st.session_state and st.session_state.authenticated:
        return True
    
    # Show authentication form
    st.title("🔐 CV Generator - Authentication Required")
    st.markdown("---")
    
    with st.container():
        st.info("🔑 Please enter the access key to use the CV Generator")
        
        # Create input form
        with st.form("auth_form"):
            access_key = st.text_input(
                "Access Key", 
                type="password",
                placeholder="Enter your access key",
                help="Contact administrator if you don't have the access key"
            )
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                submit_button = st.form_submit_button("🚀 Access Application", use_container_width=True)
        
        if submit_button:
            if access_key:
                if verify_access_key(access_key):
                    st.session_state.authenticated = True
                    st.success("✅ Authentication successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid access key. Please try again.")
                    # Add a small delay to prevent brute force attempts
                    st.session_state.failed_attempts = st.session_state.get('failed_attempts', 0) + 1
                    
                    if st.session_state.failed_attempts >= 3:
                        st.warning("⚠️ Multiple failed attempts detected. Please wait before trying again.")
            else:
                st.warning("⚠️ Please enter an access key")
    
    # Show instructions for admin
    with st.expander("🔧 For Administrators"):
        st.markdown("""
        **To set up authentication:**
        
        1. **Generate hash for your key:**
        ```python
        import hashlib
        key = "your_secret_key_here"
        hash_value = hashlib.sha256(key.encode()).hexdigest()
        print(hash_value)
        ```
        
        2. **Add to Streamlit secrets:**
        In your `.streamlit/secrets.toml` file or Streamlit Cloud secrets:
        ```toml
        [auth]
        access_key_hash = "your_generated_hash_here"
        ```
        
        3. **Share the original key** (not the hash) with authorized users.
        """)
    
    return False

def logout():
    """Clear authentication from session"""
    if 'authenticated' in st.session_state:
        del st.session_state.authenticated
    if 'failed_attempts' in st.session_state:
        del st.session_state.failed_attempts

def generate_hash_for_key(key):
    """
    Helper function to generate hash for a given key
    Used for initial setup
    
    Args:
        key (str): The key to hash
    
    Returns:
        str: The hash value
    """
    return hash_key(key)