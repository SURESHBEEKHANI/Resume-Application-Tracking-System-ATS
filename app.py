# Import necessary libraries
from dotenv import load_dotenv  # For loading environment variables from a .env file
import base64  # For encoding binary data to base64 format
import streamlit as st  # For creating the web app interface
import os  # For interacting with the operating system (e.g., getting environment variables)
import io  # For handling byte streams
from PIL import Image  # For working with images
import pdf2image  # For converting PDF pages to images
import google.generativeai as genai  # For interacting with Google's Generative AI API
from langchain.schema import AIMessage, HumanMessage  # For storing chat history

# Load environment variables from a .env file
load_dotenv()

# Configure the Generative AI API with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get a response from the Generative AI model
def get_gemini_response(input_text, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input_text, pdf_content[0], prompt])
    return response.text

# Function to handle PDF file uploads and convert the first page to an image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Function to handle AI and user chat display
def display_chat():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []  # Initialize chat history

    # Display chat history
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.markdown(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.markdown(message.content)

    # User input field
    user_query = st.chat_input("Type a message...")
    if user_query and user_query.strip():
        st.session_state.chat_history.append(HumanMessage(content=user_query))

        with st.chat_message("Human"):
            st.markdown(user_query)

        if st.session_state.vectorstore:
            response = get_response(user_query, st.session_state.vectorstore, st.session_state.chat_history, llm)
        else:
            response = "Please process a URL first before asking questions."

        with st.chat_message("AI"):
            st.markdown(response)

        st.session_state.chat_history.append(AIMessage(content=response))

# Streamlit app setup
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Sidebar setup for file upload, job description input, and logo display
logo_path = r"C:\Users\SURESH BEEKHANI\Desktop\Resume Application Tracking System(ATS)\img\ATS_LOGO.jpg"
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}" alt="ATS Logo" width="150">
    </div>
    """, unsafe_allow_html=True
)
st.sidebar.markdown("<h3 style='text-align: center;'>ATS Resume Expert</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>Your AI-powered tool for resume and job application analysis.</p>", unsafe_allow_html=True)

input_text = st.sidebar.text_area("Job Description: ", key="input")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF)...", type=["pdf"])

if uploaded_file is not None:
    st.sidebar.write("PDF Uploaded Successfully")

submit1 = st.sidebar.button("Tell Me About the Resume")
submit3 = st.sidebar.button("Percentage match")

input_prompt1 = """
You are a seasoned Technical Human Resource Manager. Your task is to carefully assess the provided resume against the specific job description. 
Provide a detailed professional evaluation on the candidate's suitability for the role, clearly outlining how well their skills, experience, and qualifications align with the job requirements. 
Additionally, identify both the strengths and areas for improvement in the applicant's profile relative to the job criteria.
"""

input_prompt3 = """
You are a highly specialized ATS (Applicant Tracking System) scanner with expertise in data science and ATS algorithms. 
Your task is to analyze the resume in comparison to the provided job description. 
First, provide a percentage match that reflects how closely the resume aligns with the job requirements. 
Next, list any missing or insufficient keywords, and conclude with a brief summary of your overall evaluation, including any key insights or concerns about the candidate's fit for the role.
"""

# Handle button clicks for generating responses based on the resume
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("The Response is")
        st.write(response)
    else:
        st.write("Please upload the resume")

# Display chat interaction
display_chat()

