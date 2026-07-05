def create_input_box(label):
    import streamlit as st
    return st.text_input(label)

def create_output_area(label):
    import streamlit as st
    return st.text_area(label, height=300)