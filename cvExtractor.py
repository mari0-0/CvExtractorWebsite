import PyPDF2
import docx
import re
import pandas as pd

def extract_text_from_pdf(pdf_file):
    text = ""
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page_num in range(len(reader.pages)):
            text += reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(docx_file):
    text = ""
    doc = docx.Document(docx_file)
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text

def extract_emails(text):
    return re.findall(r'\b[A-Za-z0-9._%+-]+ ?@ ?[A-Za-z0-9.-]+ ?\.[A-Za-z]{2,}\b', text)


def extract_phone_numbers(text):
    phone_numbers = re.findall(r'\b(?:\+?(\d{1,3}))?[-. (]*(\d{3})[-. )]*(\d{3})[-. ]*(\d{4})(?: *x(\d+))?\b', text)
    phone_numbers += re.findall(r'\b\d{5} \d{5}\b', text)
    formatted_phone_numbers = []
    for number in phone_numbers:
        formatted_number = ''.join(number)
        formatted_phone_numbers.append(formatted_number)
    return formatted_phone_numbers


def extract_information_from_cv(cv_file):
    if cv_file.endswith('.pdf'):
        text = extract_text_from_pdf(cv_file)
    elif cv_file.endswith('.docx'):
        text = extract_text_from_docx(cv_file)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")

    emails = extract_emails(text)
    phone_numbers = extract_phone_numbers(text)
    return {
        "Emails": emails,
        "Phone Numbers": phone_numbers,
        "Text": text
    }

def save_to_excel(data, output_file):
    emails = pd.Series(data["Emails"], name="Emails")
    ph_no = pd.Series(data["Phone Numbers"], name="Phone Numbers")
    text = pd.Series(data["Text"], name="Text")

    df = pd.concat([emails, ph_no, text], axis=1)
    df.to_excel(output_file, index=False)

# Example usage
cv_file = "sample2/AnanyaDas.pdf"  # Replace with the path to your CV file
output_file = "cv_data.xlsx"
cv_data = extract_information_from_cv(cv_file)
save_to_excel(cv_data, output_file)
print("CV data has been extracted and saved to", output_file)
