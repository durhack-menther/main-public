import streamlit as st

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.page_link("main_page.py", label = "< Home")
st.title('Ready to be a Mentor?')
with st.form("my_form"):
    name_val = st.text_input("Name")
    purpose_option_val = st.selectbox(
    "What do you want to share?",
    ("Academic/Study", "Business Advisor", "Work-related", "Social & Lifestyle"),
    index=None,
    placeholder = "Choose one option",
)
    
    purpose_option_val = st.selectbox(
    "What is Your MBTI?",
    ("ENFJ", "ENFP", "ENTP", "ENTJ", "ESFJ", "ESFP", "ESTP", "ESTJ",
     "INFJ", "INFP", "INTP", "INTJ", "ISFJ", "ISFP", "ISTP", "ISTJ", "I don't know"),
    index=None,
    placeholder = "Choose one option",)

    cv_val = st.file_uploader("Upload your CV")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")