# utils/cv_generator.py
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os
from datetime import datetime, date

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
    # Father's Name or Husband's Name based on marital status
    if user_data.get('is_married') == "Single" and user_data.get('father_name'):
        story.append(Paragraph(f"Father's Name: {capitalize_name(user_data['father_name'])}", normal_style))
    elif user_data.get('is_married') == "Married" and user_data.get('husband_name'):
        story.append(Paragraph(f"Husband's Name: {capitalize_name(user_data['husband_name'])}", normal_style))

    # Age (calculated from DOB if available)
    if user_data.get('dob'):
        age = datetime.now().year - user_data['dob'].year
        date_obj = user_data['dob']
        story.append(Paragraph(f"Age: {age} years", normal_style))
        story.append(Paragraph(f"Date Of Birth : {date_obj}", normal_style))

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
        # Order education from highest to lowest (reverse order)
        education_order = ["PG (Master's)", "UG (Bachelor's)", "Diploma", "ITI", "12th", "10th"]

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
                    if edu.get('institution') and edu.get('year'):
                        trade = edu.get('specialization', 'ITI')
                        story.append(Paragraph(f"• ITI ({trade}), {edu['institution']}, {edu['year']}", normal_style))

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

    # CERTIFICATION COURSES Section (only if certifications exist)
    if user_data.get('certifications') and len(user_data['certifications']) > 0:
        story.append(Paragraph("CERTIFICATION COURSES", section_header_style))

        # Sort certifications by year (most recent first)
        sorted_certifications = sorted(user_data['certifications'], key=lambda x: x.get('year', 0), reverse=True)

        for cert in sorted_certifications:
            cert_text = f"• {cert['name']}"
            if cert.get('institution'):
                cert_text += f", {cert['institution']}"
            if cert.get('year'):
                cert_text += f", {cert['year']}"
            if cert.get('duration'):
                cert_text += f" ({cert['duration']})"

            story.append(Paragraph(cert_text, normal_style))

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
        # Sort work experience by start date (most recent first)
        # Use a default date object for sorting when start_date is missing
        sorted_experience = sorted(
            user_data['work_experience'],
            key=lambda x: x.get('start_date', date(1900, 1, 1)),
            reverse=True
        )

        for i, exp in enumerate(sorted_experience, 1):
            # Format similar to the first CV
            exp_text = f"{i}. "
            story.append(Paragraph(exp_text, normal_style))

            # Role/Designation
            if exp.get('position'):
                story.append(Paragraph(f"    Role/Designation: {capitalize_name(exp['position'])}", normal_style))

            # Department
            if exp.get('department'):
                story.append(Paragraph(f"    Department: {exp['department']}", normal_style))

            # Company
            if exp.get('company'):
                story.append(Paragraph(f"    Company: {capitalize_name(exp['company'])}", normal_style))

            # Start Year
            if exp.get('start_date'):
                start_year = exp['start_date'].year if hasattr(exp['start_date'], 'year') else exp['start_date']
                story.append(Paragraph(f"    Start Year: {start_year}", normal_style))

            # End Year or Current
            if exp.get('is_current'):
                story.append(Paragraph(f"    End Year: Present (Currently Working)", normal_style))
            elif exp.get('end_date'):
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
