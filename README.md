# CV Generator App Setup Instructions

## Folder Structure
Create the following folder structure:

```
cv_generator/
├── main.py                 # Main Streamlit app
├── requirements.txt        # Python dependencies
├── utils/                  # Utility modules
│   ├── __init__.py
│   ├── data_collection.py  # Data collection functions
│   ├── cv_generator.py     # PDF generation functions
│   ├── encryption.py       # PDF encryption functions
│   └── dropbox_handler.py  # Dropbox integration functions
└── temp/                   # Temporary files (auto-created)
```

## Setup Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Create Utils Package
Create an empty `__init__.py` file in the `utils` folder to make it a Python package:

```bash
touch utils/__init__.py
```

### 3. Dropbox Setup
1. Go to [Dropbox App Console](https://www.dropbox.com/developers/apps)
2. Click "Create app"
3. Choose "Scoped access"
4. Choose "Full Dropbox" or "App folder" based on your needs
5. Give your app a name
6. Generate an access token from the app settings
7. Copy the access token (you'll need this in the app)

### 4. Run the Application
```bash
streamlit run main.py
```

## Usage Instructions

1. **Configure Dropbox** (Optional):
   - Enter your Dropbox access token in the sidebar
   - Specify the folder path where CVs should be saved
   - Test the connection

2. **Fill Personal Information**:
   - Enter all required fields marked with *
   - The form adapts based on marital status

3. **Education Details**:
   - Select your highest qualification
   - Fill details for each education level (from 10th up to your highest)

4. **Work Experience**:
   - Choose if you have work experience
   - If yes, specify number of employers and fill details for each

5. **Generate CV**:
   - Click "Generate CV" to create the PDF
   - Download the generated CV
   - If Dropbox is configured, it will be automatically uploaded

## Security Features

- **PDF Password Protection**: Each CV is encrypted with the user's date of birth in DDMMYYYY format
- **Temporary File Cleanup**: All temporary files are automatically deleted after processing
- **Secure Token Handling**: Dropbox tokens are handled securely and not stored

## Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   # Make sure all dependencies are installed
   pip install -r requirements.txt
   ```

2. **Dropbox Upload Fails**:
   - Check your access token
   - Ensure the folder path exists or has proper permissions
   - Test the connection using the sidebar button

3. **PDF Generation Fails**:
   - Ensure all required fields are filled
   - Check that the temp directory has write permissions

4. **Module Not Found Errors**:
   - Ensure the `utils/__init__.py` file exists
   - Run the app from the correct directory

### File Permissions
Make sure the application has:
- Read/write permissions in the application directory
- Permission to create the `temp/` folder
- Network access for Dropbox uploads

## Customization Options

### CV Template
You can modify the CV template in `utils/cv_generator.py`:
- Change colors, fonts, and styling
- Add new sections (skills, certifications, etc.)
- Modify the layout and formatting

### Data Collection
Extend `utils/data_collection.py` to collect additional information:
- Skills and certifications
- Languages known
- Hobbies and interests
- References

### Encryption
Modify `utils/encryption.py` to:
- Change password format
- Add additional security measures
- Implement different encryption methods

## Security Considerations

1. **Access Tokens**: Never commit Dropbox access tokens to version control
2. **Temporary Files**: The app automatically cleans up temporary files
3. **Password Format**: Default uses DDMMYYYY format - consider if this meets your security requirements
4. **File Permissions**: Ensure proper file system permissions are set

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify all dependencies are correctly installed
3. Ensure proper folder structure and permissions
4. Test Dropbox connection separately if upload issues occur
