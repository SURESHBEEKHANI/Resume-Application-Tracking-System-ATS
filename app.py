# Import necessary libraries
from dotenv import load_dotenv  # type: ignore # For loading environment variables from a .env file
import base64  # For encoding binary data to base64 format
import streamlit as st  # type: ignore # For creating the web app interface
import os  # For interacting with the operating system (e.g., getting environment variables)
import io  # For handling byte streams
from PIL import Image  # type: ignore # For working with images
import pdf2image  # type: ignore # For converting PDF pages to images
import google.generativeai as genai  # type: ignore # For interacting with Google's Generative AI API

# Load environment variables from a .env file
load_dotenv()

# Configure the Generative AI API with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define a function to get a response from the Generative AI model
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')  # Create a Generative Model instance
    # Generate content using the provided input, PDF content, and prompt
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text  # Return the generated response text

# Define a function to handle PDF file uploads and convert the first page to an image
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to images (one image per page)
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        
        # Get the first page image
        first_page = images[0]
        
        # Convert the image to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        # Encode the image bytes to base64 format
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64 and decode to string
            }
        ]
        return pdf_parts  # Return the base64-encoded image data
    else:
        raise FileNotFoundError("No file uploaded")  # Raise an error if no file is uploaded

# Streamlit app setup
# Streamlit app setup with sidebar
# Streamlit app setup
# Streamlit app setup
st.set_page_config(page_title="ATS Resume Expert")  # Set the title of the web page
st.header("ATS Tracking System")  # Display a header

# Sidebar setup
# Add the logo in the sidebar and center it using HTML
logo_path = "img/ATS_LOGO.jpg"  # Replace with your logo file path

# Use markdown with HTML to center the image
st.sidebar.markdown(
    f"""
    <div style="text-align: center;">
        <img src="data:image/jpeg;base64,{base64.b64encode(open(logo_path, "rb").read()).decode()}" alt="ATS Logo" width="50">
    </div>
    """,
    unsafe_allow_html=True
)

# Add a description or caption below the logo, centered
st.sidebar.markdown("<h3 style='text-align: center;'>ATS Resume Expert</h3>", unsafe_allow_html=True)
st.sidebar.markdown("<p style='text-align: center;'>Your AI-powered tool for resume and job application analysis.</p>", unsafe_allow_html=True)



# Create a text area for the job description input in the sidebar
input_text = st.sidebar.text_area("Job Description: ", key="input")

# Create a file uploader for the resume (PDF file) in the sidebar
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# Notify the user if the file was uploaded successfully
if uploaded_file is not None:
    st.sidebar.write("PDF Uploaded Successfully")

# Create buttons for different actions in the sidebar
submit1 = st.sidebar.button("Tell Me About the Resume")
submit3 = st.sidebar.button("Percentage match")
# Define prompts for the Generative AI model
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

# Handle the "Tell Me About the Resume" button click
if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)  # Prepare the PDF content
        response = get_gemini_response(input_prompt1, pdf_content, input_text)  # Get the response from the model
        st.subheader("The Response is")  # Display the response header
        st.write(response)  # Show the response text
    else:
        st.write("Please upload the resume")  # Prompt to upload a resume if not done already

# Handle the "Percentage match" button click
elif submit3:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)  # Prepare the PDF content
        response = get_gemini_response(input_prompt3, pdf_content, input_text)  # Get the response from the model
        st.subheader("The Response is")  # Display the response header
        st.write(response)  # Show the response text
    else:
        st.write("Please upload the resume")  # Prompt to upload a resume if not done already
