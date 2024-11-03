import streamlit as st
import module.matchmaker as mm

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")
st.title('Match Found!')

for mentor_data in mm.mentors_data:
    with st.container():
        st.html(f"""<div style='background-color: white; border-radius: 10px; padding: 10px 5px 2px 20px; display: flex; flex-direction:row; justify-content:space-between'>
                <div>
                <h3 style='margin-bottom: 0px; color:black'>{mentor_data["name"]}</h3>
                <p style='color:black;'>{mentor_data["work experiences"]}</p>
                </div>
                <div style='display: flex; flex-direction:column; padding-left: 10px'>
                <p style='color:black;'>CV Score: {st.session_state.scores[0][0]}</p>
                <p style='color:black;'>Purpose & Goal: {st.session_state.scores[0][1]}</p>
                <p style='color:black;'>MBTI: {st.session_state.scores[0][2]}</p>
                </div>
                <div style='display: flex; flex-direction:column; padding-left: 10px; text-align: center'>
                <p style='color:black; font-weight:bold;'>Overall Score</p>
                <h2 style='color:black;'>{st.session_state.scores[0][3]}</h2>
                </div>
                </div>""")