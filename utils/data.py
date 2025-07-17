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
    
    # Family Information
    father_name = st.text_input("Father's Name *", placeholder="Enter father's name")
    husband_name = ""
    if is_married == "Married":
        husband_name = st.text_input("Husband's Name *", placeholder="Enter husband's name")
    
    # Education Information
    st.subheader("Education Information")
    
    # Determine highest qualification
    qualification_levels = ["10th", "12th", "Diploma", "UG (Bachelor's)", "PG (Master's)"]
    highest_qualification = st.selectbox("Highest Qualification *", qualification_levels)
    
    # Ask about diploma only for UG/PG students
    has_diploma = False
    if highest_qualification in ["UG (Bachelor's)", "PG (Master's)"]:
        has_diploma = st.checkbox("Do you have a Diploma?", value=False)
    
    # Collect education details based on highest qualification
    education_details = collect_education_details(highest_qualification, has_diploma)
    
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
                company = st.text_input(f"Company Name", key=f"company_{i}")
                position = st.text_input(f"Position", key=f"position_{i}")
            
            with col2:
                start_date = st.date_input(f"Start Date", key=f"start_{i}")
                end_date = st.date_input(f"End Date", key=f"end_{i}")
            
            responsibilities = st.text_area(f"Key Responsibilities", key=f"resp_{i}")
            
            if company and position:
                work_experience.append({
                    'company': company,
                    'position': position,
                    'start_date': start_date,
                    'end_date': end_date,
                    'responsibilities': responsibilities
                })
    
    # Validation
    if not all([name, phone, father_name]):
        st.warning("Please fill in all required fields marked with *")
        return None
    
    if is_married == "Married" and not husband_name:
        st.warning("Please enter husband's name")
        return None
    
    if not education_details:
        st.warning("Please fill in education details")
        return None
    
    # Compile all data
    user_data = {
        'name': name,
        'phone': phone,
        'dob': dob,
        'is_married': is_married,
        'father_name': father_name,
        'husband_name': husband_name,
        'highest_qualification': highest_qualification,
        'education': education_details,
        'work_experience': work_experience
    }
    
    return user_data

def collect_education_details(highest_qualification, has_diploma=False):
    """Collect education details based on highest qualification"""
    
    education_details = {}
    
    # Define the order and required qualifications
    qualification_order = ["10th", "12th", "Diploma", "UG (Bachelor's)", "PG (Master's)"]
    highest_index = qualification_order.index(highest_qualification)
    
    # Determine which levels to collect based on selection
    levels_to_collect = []
    
    if highest_qualification == "10th":
        levels_to_collect = ["10th"]
    elif highest_qualification == "12th":
        levels_to_collect = ["10th", "12th"]
    elif highest_qualification == "Diploma":
        levels_to_collect = ["10th", "12th", "Diploma"]
    elif highest_qualification == "UG (Bachelor's)":
        levels_to_collect = ["10th", "12th"]
        if has_diploma:
            levels_to_collect.append("Diploma")
        levels_to_collect.append("UG (Bachelor's)")
    elif highest_qualification == "PG (Master's)":
        levels_to_collect = ["10th", "12th"]
        if has_diploma:
            levels_to_collect.append("Diploma")
        levels_to_collect.extend(["UG (Bachelor's)", "PG (Master's)"])
    
    # Collect details for each required level
    for level in levels_to_collect:
        st.write(f"**{level} Details:**")
        col1, col2 = st.columns(2)
        
        with col1:
            if level in ["10th", "12th"]:
                board_name = st.text_input(f"Board Name", key=f"board_{level}")
            else:
                board_name = st.text_input(f"University/Institution Name", key=f"board_{level}")
        
        with col2:
            year = st.number_input(f"Year of Completion", 
                                 min_value=2015,
                                 max_value=datetime.now().year,
                                 key=f"year_{level}")
        
        # Handle specialization/course based on level
        specialization = ""
        if level == "Diploma":
            specialization = st.text_input(f"Course Title (e.g., Diploma in Computer Science)", key=f"spec_{level}")
        elif level in ["UG (Bachelor's)", "PG (Master's)"]:
            if level == "UG (Bachelor's)":
                specialization = st.text_input(f"Course Title (e.g., BSC, BCOM, BTech)", key=f"spec_{level}")
            else:  # PG
                specialization = st.text_input(f"Course Title (e.g., MSC, MCOM, MTech)", key=f"spec_{level}")
        # No specialization/stream for 10th and 12th
        
        if board_name and year:
            education_details[level] = {
                'institution': board_name,
                'year': year,
                'specialization': specialization if specialization else None
            }
    
    return education_details