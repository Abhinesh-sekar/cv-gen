# utils/cv_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
from datetime import datetime

def capitalize_name(name):
    """Capitalize names properly"""
    if not name or name == 'N/A':
        return name
    return ' '.join(word.capitalize() for word in str(name).split())

def generate_cv_pdf(user_data):
    """Generate a professional CV PDF from user data following the format of the first CV generator"""
    
    # Create temp directory if it doesn't exist
    temp_dir = "temp"
    os.makedirs(temp_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"cv_temp_{timestamp}.pdf"
    filepath = os.path.join(temp_dir, filename)
    
    # Create PDF document
    doc = SimpleDocTemplate(
        filepath,
        pagesize=A4,
        rightMargin=0.75*inch,
        leftMargin=0.75*inch,
        topMargin=0.75*inch,
        bottomMargin=0.75*inch
    )
    
    # Define styles matching the first CV format
    styles = getSampleStyleSheet()
    
    # Title style for "CURRICULUM-VITAE"
    title_style = ParagraphStyle(
        'CVTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    # Name style
    name_style = ParagraphStyle(
        'NameStyle',
        parent=styles['Normal'],
        fontSize=14,
        spaceAfter=10,
        fontName='Helvetica-Bold',
        alignment=TA_LEFT
    )
    
    # Section header style with colored background
    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=8,
        spaceBefore=15,
        fontName='Helvetica-Bold',
        textColor=colors.white,
        backColor=colors.darkblue,
        borderPadding=5,
        alignment=TA_LEFT
    )
    
    # Normal text style
    normal_style = ParagraphStyle(
        'CVNormal',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        alignment=TA_LEFT,
        fontName='Helvetica'
    )
    
    # Build story (content)
    story = []
    
    # Title - "CURRICULUM-VITAE"
    story.append(Paragraph("<b>CURRICULUM-VITAE</b>", title_style))
    story.append(Spacer(1, 12))
    
    # Name
    story.append(Paragraph(f"<b>{capitalize_name(user_data['name'])}</b>", name_style))
    
    # Personal Information (following the first CV format)
    # Father's Name and Husband's Name based on marital status
    if user_data.get('father_name'):
        story.append(Paragraph(f"Father's Name: {capitalize_name(user_data['father_name'])}", normal_style))
    
    if user_data.get('is_married') == "Married" and user_data.get('husband_name'):
        story.append(Paragraph(f"Husband's Name: {capitalize_name(user_data['husband_name'])}", normal_style))
    
    # Age (calculated from DOB if available)
    if user_data.get('dob'):
        age = datetime.now().year - user_data['dob'].year
        date = user_data['dob']
        story.append(Paragraph(f"Age: {age} years", normal_style))
        story.append(Paragraph(f"Date Of Birth : {date}", normal_style))
    
    # Address
    if user_data.get('address'):
        story.append(Paragraph(f"Address: {user_data['address']}", normal_style))
    
    # Phone Number
    if user_data.get('phone'):
        story.append(Paragraph(f"Phone Number: {user_data['phone']}", normal_style))
    
    story.append(Spacer(1, 15))
    
    # EDUCATIONAL QUALIFICATIONS Section
    story.append(Paragraph("EDUCATIONAL QUALIFICATIONS", section_header_style))
    
    if user_data.get('education'):
        # Order education from lowest to highest (like the first CV)
        education_order = ["10th", "12th", "ITI", "Diploma", "UG (Bachelor's)", "PG (Master's)"]
        
        for level in education_order:
            if level in user_data['education']:
                edu = user_data['education'][level]
                
                if level == "10th":
                    if edu.get('institution') and edu.get('year'):
                        story.append(Paragraph(f"• 10th Standard, {edu['institution']}, {edu['year']}", normal_style))
                
                elif level == "12th":
                    if edu.get('institution') and edu.get('year'):
                        story.append(Paragraph(f"• 12th Standard, {edu['institution']}, {edu['year']}", normal_style))
                
                elif level == "ITI":
                    if edu.get('specialization') and edu.get('year'):
                        story.append(Paragraph(f"• ITI, {edu['specialization']}, {edu['year']}", normal_style))
                
                elif level == "Diploma":
                    if edu.get('institution') and edu.get('year'):
                        course_title = edu.get('specialization', 'Diploma')
                        story.append(Paragraph(f"• {course_title}, {edu['institution']}, {edu['year']}", normal_style))
                
                elif level == "UG (Bachelor's)":
                    if edu.get('institution') and edu.get('year'):
                        course_title = edu.get('specialization', 'Graduation')
                        story.append(Paragraph(f"• {course_title}, {edu['institution']}, {edu['year']}", normal_style))
                
                elif level == "PG (Master's)":
                    if edu.get('institution') and edu.get('year'):
                        course_title = edu.get('specialization', 'Post Graduation')
                        story.append(Paragraph(f"• {course_title}, {edu['institution']}, {edu['year']}", normal_style))
    
    story.append(Spacer(1, 15))
    
    # VOCATIONAL TRAINING Section (if applicable)
    if user_data.get('vocational_training'):
        story.append(Paragraph("VOCATIONAL TRAINING", section_header_style))
        for training in user_data['vocational_training']:
            story.append(Paragraph(f"• {training}", normal_style))
        story.append(Spacer(1, 15))
    
    # WORK EXPERIENCE Section
    story.append(Paragraph("WORK EXPERIENCE", section_header_style))
    
    if user_data.get('work_experience') and len(user_data['work_experience']) > 0:
        for i, exp in enumerate(user_data['work_experience'], 1):
            # Format similar to the first CV
            exp_text = f"{i}. "
            story.append(Paragraph(exp_text, normal_style))
            
            # Role/Designation
            if exp.get('position'):
                story.append(Paragraph(f"    Designation: {capitalize_name(exp['position'])}", normal_style))
            
            # Company
            if exp.get('company'):
                story.append(Paragraph(f"    Company: {capitalize_name(exp['company'])}", normal_style))
            
            # Department
            if exp.get('department'):
                story.append(Paragraph(f"    Department: {exp['department']}", normal_style))
                        
            # Start Year
            if exp.get('start_date'):
                start_year = exp['start_date'].year if hasattr(exp['start_date'], 'year') else exp['start_date']
                story.append(Paragraph(f"    Start Year: {start_year}", normal_style))
            
            # End Year
            if exp.get('end_date'):
                end_year = exp['end_date'].year if hasattr(exp['end_date'], 'year') else exp['end_date']
                story.append(Paragraph(f"    End Year: {end_year}", normal_style))
            
            story.append(Spacer(1, 8))
    else:
        story.append(Paragraph("• Fresher - No prior work experience", normal_style))
    
    # Build PDF
    doc.build(story)
    
    return filepath

def add_colored_header_pdf(story, text, section_header_style):
    """Add a colored header section to the PDF story"""
    story.append(Paragraph(text, section_header_style))

def format_year(year_value):
    """Format year value similar to the first CV generator"""
    if year_value is None or year_value == "" or str(year_value).strip() == "":
        return "N/A"
    
    try:
        if isinstance(year_value, float):
            return str(int(year_value))
        return str(year_value)
    except:
        return "N/A"
