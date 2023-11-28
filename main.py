import json
from openai import OpenAI
import streamlit as st

from quiz_utils import get_randomized_options, string_to_list
from openai_utils import get_quiz_data

st.title("#23_01 Automated Quiz Generator", anchor=False)
st.write("""
This application was made as a homework for the subject Applied Artifical Inteligence Models in Practice by Bálint Gáspár - ANNBWP
""")

with st.form("user_input"):
    TOPIC = st.text_input("Topic: ", value="animals")
    OPENAI_API_KEY = st.text_input("OpenAI API Key:", placeholder="sk-XXXX", type='password')
    submitted = st.form_submit_button("Generate quiz")

if submitted or ('quiz_data_list' in st.session_state):
    if not TOPIC:
        st.info("Please write a topic")
        st.stop()
    elif not OPENAI_API_KEY:
        st.info("Please write an OpenAI API key")
        st.stop()
        
    with st.spinner("Please wait while we generate your quiz..."):
        if submitted:
            quiz_data_str = get_quiz_data(TOPIC, OPENAI_API_KEY)
            st.session_state.quiz_data_list = string_to_list(quiz_data_str)

            if 'user_answers' not in st.session_state:
                st.session_state.user_answers = [None for _ in st.session_state.quiz_data_list]
            if 'correct_answers' not in st.session_state:
                st.session_state.correct_answers = []
            if 'randomized_options' not in st.session_state:
                st.session_state.randomized_options = []

            for q in st.session_state.quiz_data_list:
                options, correct_answer = get_randomized_options(q[1:])
                st.session_state.randomized_options.append(options)
                st.session_state.correct_answers.append(correct_answer)

        with st.form(key='quiz_form'):
            st.subheader("Quiz", anchor=False)
            for i, q in enumerate(st.session_state.quiz_data_list):
                options = st.session_state.randomized_options[i]
                default_index = st.session_state.user_answers[i] if st.session_state.user_answers[i] is not None else 0
                response = st.radio(q[0], options, index=default_index)
                user_choice_index = options.index(response)
                st.session_state.user_answers[i] = user_choice_index  # Update the stored answer right after fetching it

            results_submitted = st.form_submit_button(label='Evaluate results')

            if results_submitted:
                score = sum([ua == st.session_state.randomized_options[i].index(ca) for i, (ua, ca) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers))])
                st.success(f"Correct answers: {score}/{len(st.session_state.quiz_data_list)}")

                if score == len(st.session_state.quiz_data_list):  # Check if all answers are correct
                    st.balloons()
                else:
                    incorrect_count = len(st.session_state.quiz_data_list) - score
                    if incorrect_count == 1:
                        st.warning(f"Almost perfect, you had only one incorrect answer:")
                    else:
                        st.warning(f"Better luck next time! You had {incorrect_count} incorrect answers:")

                for i, (ua, ca, q, ro) in enumerate(zip(st.session_state.user_answers, st.session_state.correct_answers, st.session_state.quiz_data_list, st.session_state.randomized_options)):
                    with st.expander(f"Question {i + 1}", expanded=False):
                        if ro[ua] != ca:
                            st.info(f"Question: {q[0]}")
                            st.error(f"Your answer: {ro[ua]}")
                            st.success(f"Correct answer: {ca}")