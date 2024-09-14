# ATS Resume Expert

**ATS Resume Expert** is a Streamlit web application designed to analyze resumes against job descriptions using Google's Generative AI model. It offers two primary functionalities: detailed professional feedback on a resume and a percentage match score indicating how closely the resume aligns with the job requirements.

## Features

- **Resume Analysis:** Provides a professional evaluation of a resume against a job description, identifying strengths and areas for improvement.
- **Percentage Match:** Calculates a percentage indicating the alignment between the resume and job description, highlighting missing keywords and offering insights.
- **User-Friendly Interface:** Utilizes Streamlit for a simple, interactive web interface.

## Prerequisites

Make sure you have the following libraries installed:

- `streamlit`
- `python-dotenv`
- `Pillow`
- `pdf2image`
- `google-generativeai`

Install the required libraries using pip:

```bash
pip install streamlit python-dotenv Pillow pdf2image google-generativeai
Setup
1. Environment Variables
Create a .env file in the root directory of your project with the following content:

env
Copy code
GOOGLE_API_KEY=your_api_key_here
Replace your_api_key_here with your actual Google Generative AI API key.

2. Logo Image
Ensure you have your logo image file (e.g., ATS_LOGO.jpg) placed in the img directory. This logo will be displayed in the sidebar of the Streamlit app.

Running the Application
To run the application, navigate to the directory containing your app.py file and use the following command:

bash
Copy code
streamlit run app.py
This will start a local server and open the application in your default web browser.

Usage
Upload Resume:

In the sidebar, click on "Upload your resume (PDF)..." to upload a resume file in PDF format.
Enter Job Description:

Enter the job description text in the "Job Description:" text area located in the sidebar.
Analyze Resume:

Click the "Tell Me About the Resume" button to receive a detailed analysis of how well the resume matches the job description.
Click the "Percentage match" button to get a percentage match score along with insights on missing keywords and an overall evaluation.
Code Explanation
Libraries
dotenv: Loads environment variables from a .env file for securely managing API keys.
base64: Encodes binary data to base64 format for embedding images in the web app.
streamlit: Creates the web interface for the application.
os: Interacts with the operating system to retrieve environment variables.
io: Handles byte streams for image processing.
PIL (Pillow): Processes images, including converting PDF pages to images.
pdf2image: Converts PDF files to images for display in the web app.
google.generativeai: Interacts with Google's Generative AI model to analyze resumes.
Key Functions
get_gemini_response(input, pdf_content, prompt): Communicates with the Google Generative AI model to generate content based on the provided input, PDF content, and prompt. Returns the generated response text.

input_pdf_setup(uploaded_file): Handles PDF file uploads, converts the first page of the PDF to an image, and encodes it in base64 format for embedding in the web app.

Streamlit Configuration
App Header: Sets the title and header of the web page.
Sidebar Setup: Displays the logo and description, along with input fields for the job description and resume upload.
Buttons: Provides functionality for analyzing the resume and calculating the percentage match.
Contributing
Contributions are welcome! If you have suggestions or improvements, feel free to fork the repository and submit pull requests.

License
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
For any questions or feedback, please contact your-email@example.com.

