from django.shortcuts import render
import PyPDF2
import docx
import re
import pandas as pd
from io import BytesIO
import mimetypes
from django.http import HttpResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages

# Create your views here.

def index(request):
    if request.method == 'POST':
        try:
            cv_file = request.FILES['docfile']
        except MultiValueDictKeyError:
            messages.error(request, "Please choose a file.")
            return render(request, 'index.html')
        cv_data = extract_information_from_cv(cv_file)
        excel_data = generate_excel_data(cv_data)
        file_name = cv_file.name.split('.')[0]
        response = HttpResponse(excel_data, content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = f'attachment; filename="{file_name}.xlsx"'
        return response
    return render(request, 'index.html')

def extract_text_from_pdf(cv_file):
    text = ""
    reader = PyPDF2.PdfReader(cv_file)
    for page_num in range(len(reader.pages)):
        text += reader.pages[page_num].extract_text()
    return text

def extract_text_from_docx(cv_file):
    text = ""
    docx_content = BytesIO(cv_file.read())  # Create a file-like object from uploaded file content
    doc = docx.Document(docx_content)
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
    if cv_file.name.endswith('.pdf'):
        text = extract_text_from_pdf(cv_file)
    elif cv_file.name.endswith('.docx'):
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

def generate_excel_data(data):
    emails = pd.Series(data["Emails"], name="Emails")
    ph_no = pd.Series(data["Phone Numbers"], name="Phone Numbers")
    text = pd.Series(data["Text"], name="Text")

    df = pd.concat([emails, ph_no, text], axis=1)
    
    # Write DataFrame to a BytesIO object
    excel_data = BytesIO()
    with pd.ExcelWriter(excel_data, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')
        worksheet = writer.sheets['Sheet1']
        
        # Adjust column widths
        for i, col in enumerate(df.columns):
            max_len = max(df[col].astype(str).apply(len))
            worksheet.set_column(i, i, max_len + 2)  # Add extra padding
            
        # Enable text wrapping
        for i, row in enumerate(df.iterrows()):
            for j, value in enumerate(row[1]):
                worksheet.write(i + 1, j, value, writer.book.add_format({'text_wrap': True}))
    
    # Reset the BytesIO object's position to the beginning
    excel_data.seek(0)
    
    return excel_data