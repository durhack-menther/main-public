from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
import streamlit as st
import pandas as pd

import PyPDF2
from tqdm import tqdm

embeddings = OpenAIEmbeddings(openai_api_key=st.secrets['OPENAI_API_KEY'])

mentors_data = [{"name": "Anita Doe", "work experiences": "Data Science; Analytics; Technology; Education; Consulting"}]

sum_mentors = [""" Here is the summary of the CV:
    The person's academic or research background is in Data Science; Technology.
    The person's field of study can be categorized as Computer Science.
    The person's work experiences is in Data Science; Analytics; Technology; Education; Consulting.
    The person's work experiences can be categorized as Business and finance.
    The person's technical or hard skills included: Python; RStudio; SQL; Tableau; Excel; Power BI; Looker; RShiny; Google Data Studio; TensorFlow; Keras.
    The person's soft skills included: Data Analysis; Business Analysis; Product Development; Market Research; Project Management; Communication; Critical Thinking; Team Management; Leadership; Community Development; Public Relation; Event Planning; Time Management; Strategic Planning; Brand Marketing; Content Creation; Social Media Management."""]

mentor_offers = ["""
What I Offer: In our mentoring sessions, I can help you deepen your understanding of complex academic topics in data science and computer science. With my background in research and teaching, I can guide you through the essential theories, methodologies, and best practices in this field. Additionally, I can help you develop effective study techniques and strategies for academic success.

How I Can Help: If you’re struggling with specific subjects or assignments, we can work together to break down these concepts and tackle them step-by-step. I’m also here to support you in setting clear academic goals, like publishing your research or preparing for exams, and in finding resources that align with your long-term goals. My aim is to build your confidence and independence as a student, so you feel equipped to tackle academic challenges on your own.
"""]

mbti_mentors = ["ENFJ"]

def read_pdf(filename):
    reader = PyPDF2.PdfReader(filename)
    cv_docs = ""
    for i in range(len(reader.pages)):
        cv_docs += reader.pages[i].extract_text()
        if i != len(reader.pages)-1:
            cv_docs += "\n"
    return cv_docs

def analyse_cv(cv_docs):
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", groq_api_key="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")
    prompt = PromptTemplate(
        input_variables=["docs", "question"],
        template="""
    Resume: {docs}
    Analyse and understand how the structure of the CV above. Read the question below and look through the CV content for the answer! Keep all answer short, concise and without commentary. No need for intro and outro text, such as "Here are...." or "Based on....". 
    {question}
    """
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    responses = []

    question_list = [
        """
    What field of academic or research background does the person into? If the field cannot be classified into one field, list all the fields by separating each field with ;
    """,
    """
    Take a look at these fields of study, each field is separeted with ";" :
    Arts; Geography; History; Literature; Philosophy; Theology; Economics; Law; Political Science; Psychology; Sociology; Biology; Chemistry; Earth Science; Space Science; Mathematics; Physics; Agricultural Science; Computer Science; Engineering and Technology; Medicine and Health Science    
    Classify the person's academic background into just one of the field of study!
    """,
    """
    What field of work or organization experiences does the person into? If the field cannot be classified into one field, list all the fields by separating each field with ;
    """,
    """
    Take a look at these job or organization categories, each category is separeted with ";" :
    Administration; Animal care; Beauty and wellbeing; Business and finance; Computing, technology and digital; Construction and trades; Creative and media; Delivery and storage; Emergency and uniform services; Engineering and maintenance; Environment and land; Government services; Healthcare; Home services; Hospitality and food; Law and legal; Managerial; Manufacturing; Retail and sales; Science and research; Social care; Sports and leisure; Teaching and education; Transport; Travel and tourism
    Classify the person's work or organization experience into just one of the categories!
    """,
    """
    List all technical and/or hard skills that the person have! Separate each skill with ;
    """,
    """
    List all soft skills that the person have! Separate each skill with ;
    """
    ]

    for question in tqdm(question_list):
        response = chain.run(docs=cv_docs, question=question)
        responses.append(response)

    final_response = f"""
    Here is the summary of the resume:
    The person's academic or research background is in {responses[0]}.
    The person's field of study can be categorized as {responses[1]}.
    The person's work experiences is in {responses[2]}.
    The person's work experiences can be categorized as {responses[3]}.
    The person's technical or hard skills included: {responses[4]}.
    The person's soft skills included: {responses[5]}.
    """
    return final_response, responses

cv_criteria = """
RULES/CRITERIA:
1. Academic Background Match – Compares the alignment of academic backgrounds, such as field of study or research interests.
Score 1: No relevant overlap in academic fields or research.
Score 2: Minimal overlap, with some general similarities.
Score 3: Moderate overlap, with similar but not directly matching fields (e.g., Computer Science vs. Information Technology).
Score 4: Strong overlap, with directly relevant academic backgrounds (e.g., both in Data Science).
Score 5: Excellent alignment, with matching fields and possibly similar research focus areas.

2. Professional Experience Match – Measures how well the mentor’s work experience aligns with the mentee’s field or career aspirations.
Score 1: No overlap; the mentor’s professional experience is unrelated to the mentee’s aspirations.
Score 2: Minor overlap; some experience in areas adjacent to the mentee’s interests.
Score 3: Some alignment; the mentor has relevant industry experience but in slightly different roles or focuses.
Score 4: Strong alignment; the mentor’s work experience matches the mentee’s field or career path directly.
Score 5: Excellent match; the mentor has extensive experience in the mentee’s desired field, potentially in roles the mentee is aiming for.

3. Technical Skills Overlap – Evaluates the similarity between the technical skills listed in each resume (e.g., programming languages, tools).
Score 1: No overlap in technical skills; mentor lacks any relevant technical skills.
Score 2: Limited overlap; only one or two technical skills match.
Score 3: Moderate overlap; a few core skills are shared.
Score 4: Strong overlap, with several relevant technical skills in common.
Score 5: Excellent overlap, with most technical skills aligned.

4. Soft Skills Alignment – Compares the soft skills present in both summaries to gauge how well the mentor can support the mentee’s personal and professional development needs.
Score 1: No overlap in soft skills; mentor lacks soft skills relevant to mentee’s development.
Score 2: Minor overlap, with one or two soft skills in common.
Score 3: Some overlap, covering a few essential soft skills.
Score 4: Strong overlap, with several shared soft skills that are relevant to mentorship.
Score 5: Excellent alignment; the mentor’s soft skills closely match those the mentee wishes to develop.

5. Field and Industry Relevance – Assesses how closely the mentor’s industry or field expertise aligns with the mentee’s area of interest or intended career path.
Score 1: No relevance; the mentor’s field is unrelated to the mentee’s area of interest.
Score 2: Minimal relevance, with some tangential relation.
Score 3: Somewhat relevant, with the mentor having exposure to a related industry.
Score 4: Strongly relevant, with the mentor actively working in the mentee’s area of interest.
Score 5: Highly relevant, with the mentor having significant experience in the same industry and field the mentee aspires to enter.
"""

def compare_cv(sum_cv_mentor, sum_cv_mentee, cv_criteria):
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", groq_api_key="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")
    prompt = PromptTemplate(
        input_variables=["sum_cv_mentor", "sum_cv_mentee", "cv_criteria"],
        template="""
    Assume you want to match a student to the best teacher she can have. Here you have the summary of resume of both the student and the teacher.
    You are tasked with giving a score of how compatible/similar/matched between the student and the teacher.
    The scoring comparison system must adhere to the rules below. There will be five aspects to score (Academic Background Match, Professional Experience Match, Technical Skills Overlap, Soft Skills Alignment, Field and Industry Relevance) and you should score each aspect from 1 to 5 based on the rules below.
    Do note that in the end, you should give 5 score output which represents each aspects accordingly. You must not display anything else except the score numbers.
    {cv_criteria}

    Below is the student's resume:
    {sum_cv_mentee}
    
    And below is the teacher's resume:
    {sum_cv_mentor}
    """
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(sum_cv_mentor=sum_cv_mentor, sum_cv_mentee=sum_cv_mentee, cv_criteria=cv_criteria)
    return response

mentee_questions = ["Question 1: What challenges are you currently facing?", "Question 2: What do you want to achieve through the mentoring? What are your goals?",
                    "Question 3: Do you have any long-term goals? What is your ultimate dream?", "Question 4: Do you know your MBTI?",
                    "Question 5: What type or style of mentor do you prefer?"]

def sum_mentee_pg(problem_goal):
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", groq_api_key="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")
    prompt = PromptTemplate(
        input_variables=["problem_goal"],
        template="""
    Keep all answer without commentary. No need for intro and outro text, such as "Here are...." or "Based on....".
    Summarise the questions and answers below without redacting or altering the important information inside.
    {problem_goal}
    """
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(problem_goal=problem_goal)

    return response

pg_criteria = """
RULES/CRITERIA:
1. Relevance of Experience – How closely does the mentor’s experience align with the mentee’s challenges and goals?
Score 1: No relevant experience related to the mentee’s challenges or goals.
Score 2: Some relevant experience, but not directly applicable to the mentee’s specific needs.
Score 3: Relevant experience that aligns with some of the mentee’s challenges and goals.
Score 4: Highly relevant experience that directly addresses the mentee’s challenges and aligns with their goals.

2. Skills Alignment – Do the mentor's skills match what the mentee needs to overcome their challenges?
Score 1: No overlap in skills needed by the mentee.
Score 2: Few overlapping skills; mentor can offer limited help.
Score 3: Several overlapping skills that are applicable to the mentee’s needs.
Score 4: Strong alignment with multiple skills that are directly useful to the mentee.

3. Supportive Offer – How well does the mentor’s offer statement reflect the ability to address the mentee’s challenges?
Score 1: No mention of support related to the mentee’s needs.
Score 2: General offer that may be helpful, but lacks specifics for the mentee’s situation.
Score 3: Specific offers of help that align with some of the mentee’s challenges and goals.
Score 4: Clear, targeted offers that directly address the mentee’s challenges and aspirations.
"""

def compare_pgo(sum_pg, sum_cv_mentor, mentor_offer, pg_criteria):
    llm = ChatGroq(temperature=0, model_name="llama3-70b-8192", groq_api_key="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")
    prompt = PromptTemplate(
        input_variables=["sum_pg", "sum_cv_mentor", "mentor_offer"],
        template="""
    Assume you want to match a student to the best teacher she can have. Here you have the summary of the problems and goals that the student have, the summary of the teacher's resume and a statement made by the teacher explaining what can she offer.
    You are tasked with giving a score of how perfect is the teacher to help the student based on the information given.
    The scoring comparison system must adhere to the rules below. There will be three aspects to score (Relevance of Experience, Skills Alignment, Supportive Offer) and you should score each aspect from 1 to 4 based on the rules below.
    Do note that in the end, you should give 3 score output which represents each aspects accordingly. You must not display anything else except the score numbers.
    {pg_criteria}

    Here's the summary of the student's problems and goals:
    {sum_pg}

    Here's the teacher's resume:
    {sum_cv_mentor}

    Here's the offer statement that the teacher made:
    {mentor_offer}
    """
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(sum_pg=sum_pg, sum_cv_mentor=sum_cv_mentor, mentor_offer=mentor_offer, pg_criteria=pg_criteria)

    return response

# MBTI

# Define MBTI types for rows and columns
mbti_types = ["INFP", "ENFP", "INFJ", "ENFJ", "INTJ", "ENTJ", "INTP", "ENTP",
              "ISFP", "ESFP", "ISTP", "ESTP", "ISFJ", "ESFJ", "ISTJ", "ESTJ"]

# Compatibility chart using descriptions instead of colors
compatibility_data = [
    [4,4,4,5,4,5,4,4,1,1,1,1,1,1,1,1],
    [4,4,5,4,5,4,4,4,1,1,1,1,1,1,1,1],
    [4,5,4,4,4,4,4,5,1,1,1,1,1,1,1,1],
    [5,4,4,4,4,4,4,4,5,1,1,1,1,1,1,1],
    [4,5,4,4,4,4,4,5,3,3,3,3,2,2,2,2],
    [5,4,4,4,4,4,5,4,3,3,3,3,3,3,3,3],
    [4,4,4,4,4,5,4,4,3,3,3,3,2,2,2,5],
    [4,4,5,4,5,4,4,4,3,3,3,3,2,2,2,2],
    [1,1,1,5,3,3,3,3,2,2,2,2,3,5,3,5],
    [1,1,1,1,3,3,3,3,2,2,2,2,5,3,5,3],
    [1,1,1,1,3,3,3,3,2,2,2,2,3,5,3,5],
    [1,1,1,1,3,3,3,3,2,2,2,2,5,3,5,3],
    [1,1,1,1,2,3,2,2,3,5,3,5,4,4,4,4],
    [1,1,1,1,2,3,2,2,5,3,5,3,4,4,4,4],
    [1,1,1,1,2,3,2,2,3,5,3,5,4,4,4,4],
    [1,1,1,1,2,3,5,2,5,3,5,3,4,4,4,4],
]

# Create DataFrame
mbti_comp_df = pd.DataFrame(compatibility_data, index=mbti_types, columns=mbti_types)

def count_score(cv_compare_score, pg_compare_score, mbti_score):
    cv_compare_score = [int(score) for score in cv_compare_score.split()]
    weight_cv = [0.15, 0.3, 0.2, 0.15, 0.2]
    cv_compare_score_final = 0
    for i in range(len(cv_compare_score)):
        cv_compare_score_final += weight_cv[i]*cv_compare_score[i]
    perc_cv_score = round((cv_compare_score_final/5)*100)

    pg_compare_score = [int(score) for score in pg_compare_score.split()]
    weight_pg = [0.4, 0.3, 0.2]
    pg_compare_score_final = 0
    for i in range(len(pg_compare_score)):
        pg_compare_score_final += weight_pg[i]*pg_compare_score[i]
    perc_pg_score = round((pg_compare_score_final/4)*100)

    perc_mbti_score = round((mbti_score/5)*100)

    perc_overall_score = round(((cv_compare_score_final+pg_compare_score_final+mbti_score)/14)*100)

    return perc_cv_score, perc_pg_score, perc_mbti_score, perc_overall_score     