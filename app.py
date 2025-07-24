import streamlit as st
import os
import hashlib
from datetime import datetime
from utils.data import collect_user_data
from utils.cv_generator import generate_cv_pdf
from utils.encryption import encrypt_pdf
from utils.dropbox_handler import upload_to_dropbox, test_connection

def hash_password(password):
    """Generate SHA256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_authentication():
    """Check if user is authenticated using SHA256 hash comparison"""
    # Get stored hash from secrets
    try:
        stored_hash = st.secrets["auth"]["password_hash"]
    except KeyError:
        st.error("❌ Authentication not configured. Please set password_hash in secrets.toml")
        return False
    
    # Check if already authenticated in session
    if st.session_state.get('authenticated', False):
        return True
    
    # Show login form
    st.title("🔐 CV Generator - Authentication")
    st.markdown("---")
    
    with st.form("login_form"):
        password = st.text_input("Enter Password:", type="password")
        submitted = st.form_submit_button("Login", type="primary")
        
        if submitted:
            if password:
                # Hash the entered password
                entered_hash = hash_password(password)
                
                # Compare with stored hash
                if entered_hash == stored_hash:
                    st.session_state.authenticated = True
                    st.success("✅ Authentication successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid password. Please try again.")
            else:
                st.warning("⚠️ Please enter a password.")
    
    return False

def logout():
    """Logout the user"""
    st.session_state.authenticated = False
    st.session_state.step = 1
    st.session_state.user_data = {}
    st.rerun()

def main():
    st.set_page_config(
        page_title="CV Generator",
        page_icon="📄",
        layout="wide"
    )
    
    # Hide sidebar
    st.markdown("""
        <style>
            section[data-testid="stSidebar"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
    
    # Authentication check
    if not check_authentication():
        return
    
    # Main application header with logout button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("ACMA-CV Generator")
    with col2:
        if st.button("🚪 Logout", type="secondary"):
            logout()
    
    st.markdown("---")
    
    # Initialize session state
    if 'step' not in st.session_state:
        st.session_state.step = 1
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {}
    
    # Dropbox: optional folder path override
    dropbox_folder = st.secrets["dropbox"].get("folder_path", "/CVs")
    
    # Test Dropbox on first load
    if 'dropbox_status' not in st.session_state:
        st.session_state.dropbox_status = test_connection()
    
    # Show Dropbox status
    if st.session_state.dropbox_status:
        st.info(f"✅ Dropbox connection verified — folder: `{dropbox_folder}`")
    else:
        st.warning("⚠️ Dropbox not connected — check secrets.toml")

    # Step 1 — Form Input
    if st.session_state.step == 1:
        st.header("📝 Personal Information")
        user_data = collect_user_data()
        
        if user_data and st.button("Generate CV", type="primary"):
            st.session_state.user_data = user_data
            st.session_state.step = 2
            st.rerun()
    
    # Step 2 — PDF Generation
    elif st.session_state.step == 2:
        st.header("🔄 Generating Your CV...")
        
        try:
            with st.spinner("Creating PDF..."):
                pdf_path = generate_cv_pdf(st.session_state.user_data)
            
            with st.spinner("Securing PDF..."):
                dob = st.session_state.user_data['dob']
                password = "gbl"
                encrypted_pdf_path = encrypt_pdf(pdf_path, password)
            
            name = st.session_state.user_data['name'].replace(" ", "-")
            phone = st.session_state.user_data['phone']
            final_filename = f"{name}-{phone}.pdf"
            final_path = os.path.join(os.path.dirname(encrypted_pdf_path), final_filename)
            os.rename(encrypted_pdf_path, final_path)
            
            st.success("✅ CV generated successfully!")
            
            # Download button
            with open(final_path, "rb") as file:
                st.download_button(
                    label="📥 Download CV",
                    data=file.read(),
                    file_name=final_filename,
                    mime="application/pdf"
                )
            
            # Upload to Dropbox
            with st.spinner("Uploading to Dropbox..."):
                uploaded = upload_to_dropbox(final_path, dropbox_folder, final_filename)
                if uploaded:
                    st.success("📤 Uploaded to Dropbox successfully!")
                else:
                    st.error("❌ Upload to Dropbox failed.")
            
            st.info(f"🔐 PDF Password: `{password}`:")
            
            try:
                os.remove(pdf_path)
                os.remove(final_path)
            except:
                pass
            
            if st.button("Generate Another CV"):
                st.session_state.step = 1
                st.session_state.user_data = {}
                st.rerun()
        
        except Exception as e:
            st.error(f"❌ Error generating CV: {str(e)}")
            if st.button("Try Again"):
                st.session_state.step = 1
                st.rerun()

if __name__ == "__main__":
    main()
    st.cache_data.clear()
