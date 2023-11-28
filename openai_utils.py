import streamlit as st
from openai import OpenAI

def get_quiz_data(text, openai_api_key):

    client = OpenAI(
    api_key=openai_api_key,
    )

    template = f"""
    You are a helpful assistant programmed to generate questions based on any text provided. For every chunk of text you receive, you're tasked with designing 5 distinct questions. Each of these questions will be accompanied by 3 possible answers: one correct answer and two incorrect ones. 

    For clarity and ease of processing, structure your response in a way that emulates a Python list of lists. 

    Your output should be shaped as follows:

    1. An outer list that contains 5 inner lists.
    2. Each inner list represents a set of question and answers, and contains exactly 4 strings in this order:
    - The generated question.
    - The correct answer.
    - The first incorrect answer.
    - The second incorrect answer.

    Your output should mirror this structure:
    [
        ["Generated Question 1", "Correct Answer 1", "Incorrect Answer 1.1", "Incorrect Answer 1.2"],
        ["Generated Question 2", "Correct Answer 2", "Incorrect Answer 2.1", "Incorrect Answer 2.2"],
        ...
    ]

    It is crucial that you adhere to this format as it's optimized for further Python processing.

    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages = [
                {"role": "system", "content": template},
                {"role": "user", "content": f"Generate 5 questions based on the following text:\n{text}\n\n"},
            ],
            max_tokens=1000,
            n=5,
            stop=None,
            temperature=0.2
        )

        quiz_data = response.choices[0].message.content
        return quiz_data

    except Exception as e:
        if "AuthenticationError" in str(e):
            st.error("Incorrect API key provided. Please check and update your API key.")
            st.stop()
        else:
            st.error(f"An error occurred: {str(e)}")
            st.stop()