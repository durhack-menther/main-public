import streamlit as st
import module.matchmaker as mm

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
    offers_val = st.text_area("What I Offer?", placeholder="Enter 50 words to get +1000XP")
    help_val = st.text_area("How I Can Help", placeholder="Enter 50 words to get +1000XP")
    mbti_val = st.selectbox(
    "What is Your MBTI?",
    ("ENFJ", "ENFP", "ENTP", "ENTJ", "ESFJ", "ESFP", "ESTP", "ESTJ",
     "INFJ", "INFP", "INTP", "INTJ", "ISFJ", "ISFP", "ISTP", "ISTJ", "I don't know"),
    index=None,
    placeholder = "Choose one option",)

    cv_val = st.file_uploader("Upload your CV")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Submit")
    if submitted:
        cv_mentor = mm.read_pdf('dummy-data/CV2024_DivanyHarryndira_DS.pdf')
        sum_cv_mentee = mm.analyse_cv(cv_mentor)

        mm.mentors_data.append({"name": name_val, "work experiences":sum_cv_mentee[1][2]})
        mm.sum_mentors.append(sum_cv_mentee[0])
        mm.mentor_offers.append(f"""
                                What I Offer: {offers_val}
                                
                                How I Can Help: {help_val}""")
        mm.mbti_mentors.append(mbti_val)

        st.success('Your submission was saved!', icon='😍')
        