# filepath: gpt-streamlit-app/src/gemini.py

import streamlit as st
from api.gpt_client import GPTClient
from utils.config import load_config
from ui.components import create_input_box, create_output_area

def main():
    st.title("GPT Streamlit App")
    
    # Load API key from configuration
    api_key = load_config()
    gpt_client = GPTClient(api_key)

    user_input = create_input_box("Enter your query:")
    if st.button("Submit"):
        response = gpt_client.get_response(user_input)
        create_output_area(response)

if __name__ == "__main__":
    main()