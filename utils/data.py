# utils/data.py
import streamlit as st
from datetime import datetime, date

def collect_user_data():
    """Collect all user data for CV generation"""

    # Basic Information
    st.subheader("Basic Information")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Full Name *", placeholder="Enter your full name")
        phone = st.text_input("Phone Number *", placeholder="Enter your phone number")

    with col2:
        dob = st.date_input("Date of Birth *", max_value=date(2007,1,1), min_value=date(1999, 1, 1))
        is_married = st.selectbox("Marital Status *", ["Single", "Married"])

    # Address Information
    address = st.text_area("Current Address *", placeholder="Enter your current address")

    # Family Information based on marital status
    father_name = ""
    husband_name = ""
    if is_married == "Single":
        father_name = st.text_input("Father's Name *", placeholder="Enter father's name")
    elif is_married == "Married":
        husband_name = st.text_input("Husband's Name *", placeholder="Enter husband's name")

    # Education Information
    st.subheader("Education Information")

    # Determine highest qualification
    qualification_levels = ["10th", "12th", "Diploma", "UG (Bachelor's)", "PG (Master's)"]
    highest_qualification = st.selectbox("Highest Qualification *", qualification_levels)

    # Ask about ITI and diploma based on highest qualification
    has_iti = False
    iti_timing = None
    has_diploma = False

    if highest_qualification in ["12th", "Diploma", "UG (Bachelor's)", "PG (Master's)"]:
        has_iti = st.checkbox("Do you have an ITI Certificate?", value=False)
        if has_iti:
            iti_timing = st.radio("When did you complete ITI?", ["Before 12th", "After 12th"])

    if highest_qualification in ["UG (Bachelor's)", "PG (Master's)"]:
        has_diploma = st.checkbox("Do you have a Diploma?", value=False)

    # Collect education details based on highest qualification
    education_details = collect_education_details(highest_qualification, has_iti, iti_timing, has_diploma)

    # Certification Courses (Optional)
    st.subheader("Certification Courses (Optional)")
    has_certifications = st.radio("Do you have any certification courses?", ["No", "Yes"])

    certifications = []
    if has_certifications == "Yes":
        num_certifications = st.number_input("Number of Certifications", min_value=1, max_value=10, value=1)

        for i in range(int(num_certifications)):
            st.write(f"**Certification {i+1}:**")
            col1, col2 = st.columns(2)

            with col1:
                cert_name = st.text_input(f"Certification Name *", key=f"cert_name_{i}")
                institution = st.text_input(f"Institution/Organization *", key=f"cert_inst_{i}")

            with col2:
                cert_year = st.number_input(f"Year of Completion *",
                                          min_value=2015,
                                          max_value=datetime.now().year,
                                          key=f"cert_year_{i}")
                duration = st.text_input(f"Duration (Optional)", key=f"cert_duration_{i}", placeholder="e.g., 6 months")

            if cert_name and institution:
                certifications.append({
                    'name': cert_name,
                    'institution': institution,
                    'year': cert_year,
                    'duration': duration if duration else None
                })

    # Work Experience
    st.subheader("Work Experience")
    has_experience = st.radio("Do you have work experience?", ["No", "Yes"])

    work_experience = []
    if has_experience == "Yes":
        num_employers = st.number_input("Number of Previous Employers", min_value=1, max_value=10, value=1)

        for i in range(int(num_employers)):
            st.write(f"**Employer {i+1}:**")
            col1, col2 = st.columns(2)

            with col1:
                company = st.text_input(f"Company Name *", key=f"company_{i}")
                position = st.text_input(f"Position *", key=f"position_{i}")

            with col2:
                start_date = st.date_input(f"Start Date *", key=f"start_{i}")
                is_current = st.checkbox(f"Currently working here", key=f"current_{i}")
                end_date = None
                if not is_current:
                    end_date = st.date_input(f"End Date *", key=f"end_{i}")

            if company and position:
                work_experience.append({
                    'company': company,
                    'position': position,
                    'start_date': start_date,
                    'end_date': end_date,
                    'is_current': is_current
                })

    # Validation
    if not all([name, phone, address]):
        st.warning("Please fill in all required fields marked with *")
        return None

    if is_married == "Single" and not father_name:
        st.warning("Please enter father's name")
        return None

    if is_married == "Married" and not husband_name:
        st.warning("Please enter husband's name")
        return None

    if not education_details:
        st.warning("Please fill in education details")
        return None

    # Validate that all chosen education levels are properly filled
    validation_errors = validate_education_completeness(education_details, highest_qualification, has_iti, has_diploma)
    if validation_errors:
        for error in validation_errors:
            st.warning(error)
        return None

    # Validate certifications if chosen
    if has_certifications == "Yes" and not certifications:
        st.warning("Please add at least one certification or select 'No' for certification courses")
        return None

    # Validate work experience if chosen
    if has_experience == "Yes" and not work_experience:
        st.warning("Please add at least one work experience or select 'No' for work experience")
        return None

    # Compile all data
    user_data = {
        'name': name,
        'phone': phone,
        'dob': dob,
        'address': address,
        'is_married': is_married,
        'father_name': father_name,
        'husband_name': husband_name,
        'highest_qualification': highest_qualification,
        'education': education_details,
        'certifications': certifications,
        'work_experience': work_experience
    }

    return user_data

def collect_education_details(highest_qualification, has_iti=False, iti_timing=None, has_diploma=False):
    """Collect education details based on highest qualification with date validation"""

    education_details = {}
    previous_year = 2014  # Minimum year for validation

    # Define the order and required qualifications
    qualification_order = ["10th", "12th", "ITI", "Diploma", "UG (Bachelor's)", "PG (Master's)"]
    highest_index = qualification_order.index(highest_qualification)

    # Determine which levels to collect based on selection
    levels_to_collect = []

    if highest_qualification == "10th":
        levels_to_collect = ["10th"]
    elif highest_qualification == "12th":
        levels_to_collect = ["10th", "12th"]
        if has_iti and iti_timing == "Before 12th":
            levels_to_collect.insert(-1, "ITI")  # Add ITI before 12th
        elif has_iti and iti_timing == "After 12th":
            levels_to_collect.append("ITI")  # Add ITI after 12th
    elif highest_qualification == "Diploma":
        levels_to_collect = ["10th", "12th", "Diploma"]
        if has_iti and iti_timing == "Before 12th":
            levels_to_collect.insert(-2, "ITI")  # Add ITI before 12th
        elif has_iti and iti_timing == "After 12th":
            levels_to_collect.insert(-1, "ITI")  # Add ITI before Diploma
    elif highest_qualification == "UG (Bachelor's)":
        levels_to_collect = ["10th", "12th"]
        if has_iti and iti_timing == "Before 12th":
            levels_to_collect.insert(-1, "ITI")
        elif has_iti and iti_timing == "After 12th":
            levels_to_collect.append("ITI")
        if has_diploma:
            levels_to_collect.append("Diploma")
        levels_to_collect.append("UG (Bachelor's)")
    elif highest_qualification == "PG (Master's)":
        levels_to_collect = ["10th", "12th"]
        if has_iti and iti_timing == "Before 12th":
            levels_to_collect.insert(-1, "ITI")
        elif has_iti and iti_timing == "After 12th":
            levels_to_collect.append("ITI")
        if has_diploma:
            levels_to_collect.append("Diploma")
        levels_to_collect.extend(["UG (Bachelor's)", "PG (Master's)"])

    # Collect details for each required level
    for level in levels_to_collect:
        st.write(f"**{level} Details:**")
        col1, col2 = st.columns(2)

        with col1:
            if level in ["10th", "12th"]:
                board_name = st.text_input(f"Board Name *", key=f"board_{level}")
            else:
                board_name = st.text_input(f"University/Institution Name *", key=f"board_{level}")

        with col2:
            # Set minimum year based on previous qualification
            min_year = max(2015, previous_year + 1)
            year = st.number_input(f"Year of Completion *",
                                 min_value=min_year,
                                 max_value=datetime.now().year,
                                 key=f"year_{level}",
                                 help=f"Must be {min_year} or later")

        # Handle specialization/course based on level
        specialization = ""
        if level == "ITI":
            specialization = st.text_input(f"ITI Trade/Course Title (e.g., Electrician, Fitter) *", key=f"spec_{level}")
        elif level == "Diploma":
            specialization = st.text_input(f"Course Title (e.g., Diploma in Computer Science) *", key=f"spec_{level}")
        elif level in ["UG (Bachelor's)", "PG (Master's)"]:
            if level == "UG (Bachelor's)":
                specialization = st.text_input(f"Course Title (e.g., BSC, BCOM, BTech) *", key=f"spec_{level}")
            else:  # PG
                specialization = st.text_input(f"Course Title (e.g., MSC, MCOM, MTech) *", key=f"spec_{level}")
        # No specialization/stream for 10th and 12th

        if board_name and year:
            education_details[level] = {
                'institution': board_name,
                'year': year,
                'specialization': specialization if specialization else None
            }
            # Update previous year for validation of next qualification
            previous_year = year

    return education_details

def validate_education_completeness(education_details, highest_qualification, has_iti=False, has_diploma=False):
    """Validate that all chosen education levels are completely filled"""
    errors = []

    # Define expected levels based on choices
    expected_levels = []

    if highest_qualification == "10th":
        expected_levels = ["10th"]
    elif highest_qualification == "12th":
        expected_levels = ["10th", "12th"]
        if has_iti:
            expected_levels.append("ITI")
    elif highest_qualification == "Diploma":
        expected_levels = ["10th", "12th", "Diploma"]
        if has_iti:
            expected_levels.append("ITI")
    elif highest_qualification == "UG (Bachelor's)":
        expected_levels = ["10th", "12th", "UG (Bachelor's)"]
        if has_iti:
            expected_levels.append("ITI")
        if has_diploma:
            expected_levels.append("Diploma")
    elif highest_qualification == "PG (Master's)":
        expected_levels = ["10th", "12th", "UG (Bachelor's)", "PG (Master's)"]
        if has_iti:
            expected_levels.append("ITI")
        if has_diploma:
            expected_levels.append("Diploma")

    # Check each expected level
    for level in expected_levels:
        if level not in education_details:
            errors.append(f"Please complete {level} details")
            continue

        edu = education_details[level]

        # Check required fields for each level
        if not edu.get('institution'):
            if level in ["10th", "12th"]:
                errors.append(f"Please enter Board Name for {level}")
            else:
                errors.append(f"Please enter University/Institution Name for {level}")

        if not edu.get('year'):
            errors.append(f"Please enter Year of Completion for {level}")

        # Check specialization for levels that require it
        if level in ["ITI", "Diploma", "UG (Bachelor's)", "PG (Master's)"]:
            if not edu.get('specialization'):
                if level == "ITI":
                    errors.append(f"Please enter ITI Trade/Course Title for {level}")
                elif level == "Diploma":
                    errors.append(f"Please enter Course Title for {level}")
                elif level == "UG (Bachelor's)":
                    errors.append(f"Please enter Course Title for {level}")
                elif level == "PG (Master's)":
                    errors.append(f"Please enter Course Title for {level}")

    return errors
