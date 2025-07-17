# utils/encryption.py
import PyPDF2
import os

def encrypt_pdf(input_path, password):
    """
    Encrypt a PDF file with a password
    
    Args:
        input_path (str): Path to the input PDF file
        password (str): Password to encrypt the PDF with
    
    Returns:
        str: Path to the encrypted PDF file
    """
    
    # Generate output path
    base_name = os.path.splitext(input_path)[0]
    output_path = f"{base_name}_encrypted.pdf"
    
    try:
        # Read the original PDF
        with open(input_path, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            pdf_writer = PyPDF2.PdfWriter()
            
            # Add all pages to the writer
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                pdf_writer.add_page(page)
            
            # Encrypt the PDF
            pdf_writer.encrypt(password)
            
            # Write the encrypted PDF
            with open(output_path, 'wb') as output_file:
                pdf_writer.write(output_file)
        
        return output_path
        
    except Exception as e:
        raise Exception(f"Error encrypting PDF: {str(e)}")

def decrypt_pdf(input_path, password, output_path):
    """
    Decrypt a PDF file with a password
    
    Args:
        input_path (str): Path to the encrypted PDF file
        password (str): Password to decrypt the PDF with
        output_path (str): Path for the decrypted PDF file
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        with open(input_path, 'rb') as input_file:
            pdf_reader = PyPDF2.PdfReader(input_file)
            
            # Check if PDF is encrypted
            if pdf_reader.is_encrypted:
                # Try to decrypt
                if pdf_reader.decrypt(password):
                    pdf_writer = PyPDF2.PdfWriter()
                    
                    # Add all pages to the writer
                    for page_num in range(len(pdf_reader.pages)):
                        page = pdf_reader.pages[page_num]
                        pdf_writer.add_page(page)
                    
                    # Write the decrypted PDF
                    with open(output_path, 'wb') as output_file:
                        pdf_writer.write(output_file)
                    
                    return True
                else:
                    return False
            else:
                # PDF is not encrypted, just copy it
                with open(output_path, 'wb') as output_file:
                    output_file.write(input_file.read())
                return True
                
    except Exception as e:
        print(f"Error decrypting PDF: {str(e)}")
        return False

def verify_pdf_password(pdf_path, password):
    """
    Verify if a password can decrypt a PDF
    
    Args:
        pdf_path (str): Path to the PDF file
        password (str): Password to verify
    
    Returns:
        bool: True if password is correct, False otherwise
    """
    
    try:
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            if pdf_reader.is_encrypted:
                return pdf_reader.decrypt(password)
            else:
                return True  # PDF is not encrypted
                
    except Exception as e:
        print(f"Error verifying PDF password: {str(e)}")
        return False