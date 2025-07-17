# utils/dropbox_handler.py

import os
import requests
import dropbox
from dropbox.exceptions import AuthError, ApiError
import streamlit as st

# ---------------------
# 🔁 Refresh Access Token
# ---------------------
def refresh_access_token():
    try:
        creds = st.secrets["dropbox"]
        data = {
            "grant_type": "refresh_token",
            "refresh_token": creds["refresh_token"],
            "client_id": creds["client_id"] if "client_id" in creds else st.secrets["DROPBOX_APP_KEY"],
            "client_secret": creds["client_secret"] if "client_secret" in creds else st.secrets["DROPBOX_APP_SECRET"]
        }

        response = requests.post("https://api.dropboxapi.com/oauth2/token", data=data)
        response.raise_for_status()
        token = response.json().get("access_token")
        return token
    except Exception as e:
        st.error(f"Error refreshing access token: {e}")
        return None

# ---------------------
# 📦 Dropbox Client
# ---------------------
def get_dbx_client():
    access_token = refresh_access_token()
    if access_token:
        return dropbox.Dropbox(access_token)
    else:
        st.error("Failed to refresh Dropbox token.")
        st.stop()

# ---------------------
# ✅ Test Connection
# ---------------------
def test_connection():
    try:
        dbx = get_dbx_client()
        dbx.users_get_current_account()
        return True
    except Exception:
        return False

# ---------------------
# ⬆️ Upload File
# ---------------------
def upload_to_dropbox(local_file_path, dropbox_folder, filename):
    try:
        dbx = get_dbx_client()

        # Normalize path
        if not dropbox_folder.startswith("/"):
            dropbox_folder = "/" + dropbox_folder
        if not dropbox_folder.endswith("/"):
            dropbox_folder += "/"

        dropbox_path = dropbox_folder + filename
        file_size = os.path.getsize(local_file_path)

        with open(local_file_path, "rb") as file:
            if file_size <= 150 * 1024 * 1024:
                dbx.files_upload(file.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)
            else:
                upload_session_start_result = dbx.files_upload_session_start(file.read(4 * 1024 * 1024))
                cursor = dropbox.files.UploadSessionCursor(
                    session_id=upload_session_start_result.session_id,
                    offset=file.tell()
                )
                while file.tell() < file_size:
                    chunk = file.read(4 * 1024 * 1024)
                    if len(chunk) < 4 * 1024 * 1024:
                        dbx.files_upload_session_finish(
                            chunk, cursor, dropbox.files.CommitInfo(path=dropbox_path)
                        )
                        break
                    else:
                        dbx.files_upload_session_append_v2(chunk, cursor)
                        cursor.offset = file.tell()

        return True
    except Exception as e:
        st.error(f"Upload failed: {e}")
        return False

# ---------------------
# 📁 Create Folder
# ---------------------
def create_folder(folder_path):
    try:
        dbx = get_dbx_client()
        if not folder_path.startswith("/"):
            folder_path = "/" + folder_path
        dbx.files_create_folder_v2(folder_path)
        return True
    except ApiError as e:
        if e.error.is_path() and e.error.get_path().is_conflict():
            return True  # Already exists
        else:
            st.error(f"API error creating folder: {e}")
            return False
    except Exception as e:
        st.error(f"Error creating folder: {e}")
        return False

# ---------------------
# 📄 List Files
# ---------------------
def list_files(folder_path=""):
    try:
        dbx = get_dbx_client()
        if folder_path and not folder_path.startswith("/"):
            folder_path = "/" + folder_path
        result = dbx.files_list_folder(folder_path)
        return [entry.name for entry in result.entries if isinstance(entry, dropbox.files.FileMetadata)]
    except Exception as e:
        st.error(f"Error listing files: {e}")
        return []

# ---------------------
# 🔗 Get Download Link
# ---------------------
def get_download_link(file_path):
    try:
        dbx = get_dbx_client()
        if not file_path.startswith("/"):
            file_path = "/" + file_path
        link = dbx.files_get_temporary_link(file_path)
        return link.link
    except Exception as e:
        st.error(f"Error getting download link: {e}")
        return None
