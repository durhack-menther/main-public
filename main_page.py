import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

# st.html("<nav>Menther</nav>")
st.image('images/header_landingpage2.jpg')
st.html("<h1 style='text-align: center; margin-bottom: 0px;'>Unlock Your Potential: Find the Perfect Mentor or Mentee Today</h1><p style='text-align: center;'>Whether you're here to share wisdom or to learn, we make it easy to find the right match and achieve your goals.</p>")
left, right = st.columns(2)

if left.button("Become a Mentor", use_container_width=True):
    st.switch_page("pages/mentor_register.py")
if right.button("Find a Mentor", use_container_width=True):
    st.switch_page("pages/mentee_register.py")

st.markdown('#')

with st.container():
    col1, col2 = st.columns(2, vertical_alignment="center")

    with col1:
        st.header('Why Join? Elevate Your Mentorship Experience')
        st.html("<p>Explore benefits that make connecting with mentors or mentees meaningful,<br>impactful, and tailored to your growth journey.</p>")
    
    with col2:
        st.html("<div style='background-color: white; border-radius: 10px; padding: 10px 5px 2px 15px;'><p style='color:black; font-weight:bold; margin-bottom: 0px;'>1. Match with Confidence</p><p style='color:black;'>Our matching algorithm connects you with mentors or mentees who align with your skills, goals, and personality, making it easy to build a meaningful partnership.</p></div>")
        st.html("<div style='background-color: white; border-radius: 10px; padding: 10px 5px 2px 15px; margin-top: 10px;'><p style='color:black; font-weight:bold; margin-bottom: 0px;'>2. Learn and Grow Together</p><p style='color:black;'>With mentorship at your fingertips, gain insights, guidance, and support for your personal and professional journey.</p></div>")
        st.html("<div style='background-color: white; border-radius: 10px; padding: 10px 5px 2px 15px; margin-top: 10px;'><p style='color:black; font-weight:bold; margin-bottom: 0px;'>3. Flexible Connections</p><p style='color:black;'>Connect with people in your field or from diverse backgrounds for a unique learning experience. Browse profiles, swipe, and match at your own pace!</p></div>")

st.markdown('##')

with st.container():
    st.html("<h1 style='text-align: center; margin-bottom: 0px;'>How it Works?</h1>")
    col1, col2, col3 = st.columns(3, vertical_alignment="bottom")

    with col1:
        st.html("<div style='background-color: white; border-radius: 10px; padding: 10px 5px 2px 15px;'><p style='color:black; font-weight:bold; margin-bottom: 0px;'>Step 1: Create Your Profile</p><p style='color:black;'>Tell us about your expertise or goals to help us make the best connections for you.</p></div>")
    
    with col2:
        st.html("<div style='background-color: white; border-radius: 10px; padding: 10px 5px 2px 15px; margin-top: 10px;'><p style='color:black; font-weight:bold; margin-bottom: 0px;'>Step 2: Browse and Match</p><p style='color:black;'>Browse curated profiles of mentors or mentees, and find the people who resonate with you.</p></div>")
        
    with col3:
        st.html("<div style='background-color: white; border-radius: 10px; padding: 10px 5px 2px 15px; margin-top: 10px;'><p style='color:black; font-weight:bold; margin-bottom: 0px;'>Step 3: Start Your Journey</p><p style='color:black;'>Message your match, set up a meeting, and begin an inspiring mentorship journey!</p></div>")

st.markdown('#')

with st.container():
    st.html("<h1 style='text-align: center; margin-bottom: 0px;'>Hear from Them</h1>")
    col1, col2 = st.columns(2, vertical_alignment="center")

    with col1:
        st.html(f"""<div style='background-color: white; 
                border-radius: 10px; padding: 10px 5px 2px 15px; max-width: 80%; margin-left: 18%;'>
                <p style='color:black; margin-bottom:2px;'>“Connecting with a mentor here was so easy and impactful. 
                I’m gaining insights that I couldn’t find anywhere else!”</p>
                <p style='color:black; font-weight:bold;'>-- Jane Doe</p></div>""")
    
    with col2:
        st.html(f"""<div style='background-color: white; 
                border-radius: 10px; padding: 10px 5px 2px 15px; max-width: 80%;'>
                <p style='color:black; margin-bottom:2px;'>“Mentoring on this platform has been a rewarding experience.
                I’m glad to support the next generation in my industry.”</p>
                <p style='color:black; font-weight:bold;'>-- Anita Doe</p></div>""")