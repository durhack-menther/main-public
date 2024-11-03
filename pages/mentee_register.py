import streamlit as st
import module.matchmaker as mm

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

st.page_link("main_page.py", label = "< Home")
st.title('Ready to meet your Mentor?')
with st.form("my_form"):
    name_val = st.text_input("Name")
    challenges_val = st.text_area("What challenges are you currently facing?")
    purpose_option_val = st.selectbox(
    "For what purpose do you require a mentor?",
    ("Academic/Study", "Business Advisor", "Work-related", "Social & Lifestyle"),
    index=None,
    placeholder = "Choose one option",
)
    aspiration_val = st.text_area("What do you want to achieve through the mentoring? What are your goals?")
    dream_val = st.text_area("Do you have any long-term goals? What is your ultimate dream?")
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
        cv_mentee = mm.read_pdf(cv_val)
        sum_cv_mentee = mm.analyse_cv(cv_mentee)
        cv_compare_score = []
        for sum_cv_mentor in mm.sum_mentors:
            cv_compare_score.append(mm.compare_cv(sum_cv_mentor, sum_cv_mentee, mm.cv_criteria))
        
        problem_goal = f"""
{mm.mentee_questions[0]}
Answer: {challenges_val}

{mm.mentee_questions[1]}
Answer: {aspiration_val}

{mm.mentee_questions[2]}
Answer: {dream_val}
"""
        sum_pg = mm.sum_mentee_pg(problem_goal)

        pg_compare_score = []
        for mentor_offer in mm.mentor_offers:
            pg_compare_score.append(mm.compare_pgo(sum_pg, sum_cv_mentor, mentor_offer, mm.pg_criteria))

        mbti_score = []
        for mbti_mentor in mm.mbti_mentors:
            mbti_score.append(mm.mbti_comp_df[mbti_val][mbti_mentor])
        
        scores = []
        for i in range(len(mbti_score)):
            scores.append(mm.count_score(cv_compare_score[i], pg_compare_score[i], mbti_score[i]))

        print(scores)

