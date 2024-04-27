# CV Data Extraction Website

## Description:
The CV Data Extraction Tool is a web application built using Django, a Python web framework. The purpose of this tool is to extract key information such as email addresses, phone numbers, and text content from resumes (CVs) uploaded by users in either PDF or DOCX format.

## Key Features:
1. Upload CV: Users can upload their CV files in either PDF or DOCX format.
2. Extract Information: The application extracts email addresses, phone numbers, and text content from the uploaded CVs.
3. Download Excel: Users can download an Excel spreadsheet containing the extracted data for further analysis.
4. Error Handling: The application handles errors such as invalid file formats and missing files, providing appropriate feedback to the user.

## Installation:
1. Clone the repository:
`git clone https://github.com/mari0-0/CvExtractorWebsite.git`

2. Install dependencies using pip:
`pip install -r requirements.txt`

## Usage:
1. Run the Django development server:
`python manage.py runserver`

2. Open your web browser and navigate to http://localhost:8000/ to access the application.

3. Upload your CV files, and the application will extract the relevant information for you.

## Dependencies:
- PyPDF2
- python-docx
- pandas
- Django

## Author:
Abhai Matta
