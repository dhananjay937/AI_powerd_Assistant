import fitz  # PyMuPDF for PDF extraction
import re
import smtplib
import os
import pandas as pd
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extracts text from a given PDF file."""
    try:
        doc = fitz.open(pdf_file)
        text = "\n".join([page.get_text() for page in doc])
        return text
    except Exception as e:
        print(f"❌ Error extracting text from PDF: {e}")
        return ""

# Function to manually extract fields from text
def extract_fields(text):
    """Extracts specific fields from text using regex patterns."""
    extracted_data = {}

    name_match = re.search(r"Name:\s*(.+)", text)
    branch_match = re.search(r"Branch:\s*(.+)", text)
    vendor_code_match = re.search(r"Vendor Code:\s*([A-Za-z0-9]{6})", text)
    account_number_match = re.search(r"Account Number:\s*(\d{10})", text)
    date_match = re.search(r"Date:\s*(\d{4}-\d{2}-\d{2})", text)

    extracted_data["Name"] = name_match.group(1).strip().title() if name_match else "Blank"
    extracted_data["Branch"] = branch_match.group(1).strip() if branch_match else "Blank"
    extracted_data["Vendor Code"] = vendor_code_match.group(1).strip() if vendor_code_match else "Blank"
    extracted_data["Account Number"] = account_number_match.group(1).strip() if account_number_match else "Blank"
    extracted_data["Date"] = date_match.group(1).strip() if date_match else "Blank"

    return extracted_data

# Function to extract fields from CSV or Excel
def extract_fields_from_csv_excel(file):
    """Extracts fields from an uploaded CSV or Excel file."""
    try:
        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)
        
        extracted_data = {
            "Name": str(df.iloc[0].get("Name", "Blank")).title(),
            "Branch": df.iloc[0].get("Branch", "Blank"),
            "Vendor Code": df.iloc[0].get("Vendor Code", "Blank"),
            "Account Number": df.iloc[0].get("Account Number", "Blank"),
            "Date": df.iloc[0].get("Date", "Blank")
        }
        return extracted_data
    except Exception as e:
        print(f"❌ Error extracting fields from file: {e}")
        return {}

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587  # TLS port
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "your_email@gmail.com")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD", "your_password")

def send_email_notification(to_email, subject, message, html_message=None):
    """Sends an email notification via SMTP."""
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = to_email
        msg["Subject"] = subject

        msg.attach(MIMEText(message, "plain"))

        if html_message:
            msg.attach(MIMEText(html_message, "html"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Secure connection
        server.login(SENDER_EMAIL, SENDER_PASSWORD)

        server.sendmail(SENDER_EMAIL, to_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent successfully to {to_email}")

    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Function to validate extracted data against user input
def validate_data(user_data, extracted_data):
    """Validates extracted fields against user-provided data."""
    errors = []

    for key, value in user_data.items():
        if extracted_data.get(key, "Blank") == "Blank":
            errors.append(f"{key} is missing in the uploaded file.")
        elif value.strip() != extracted_data[key]:
            errors.append(f"{key} mismatch: Expected '{value}', Found '{extracted_data[key]}'")

    # Validate Account Number (10-digit numeric only)
    if extracted_data["Account Number"] != "Blank" and not re.fullmatch(r"^\d{10}$", extracted_data["Account Number"]):
        errors.append("⚠️ Account Number should be exactly 10 digits.")

    # Validate Vendor Code (6-character alphanumeric only)
    if extracted_data["Vendor Code"] != "Blank" and not re.fullmatch(r"^[A-Za-z0-9]{6}$", extracted_data["Vendor Code"]):
        errors.append("⚠️ Vendor Code should be exactly 6 alphanumeric characters.")

    # Validate Date (YYYY-MM-DD format)
    try:
        if extracted_data["Date"] != "Blank":
            datetime.strptime(extracted_data["Date"], "%Y-%m-%d")
    except ValueError:
        errors.append("⚠️ Date format should be YYYY-MM-DD and must be a valid date.")

    return errors

# Function to store final validated file
def store_final_file(uploaded_file, save_path="validated_files/"):
    """Stores the uploaded file in the validated_files/ directory after ensuring it exists."""
    try:
        os.makedirs(save_path, exist_ok=True)  # Create directory if it doesn’t exist

        file_path = os.path.join(save_path, uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        print(f"✅ File saved successfully at {file_path}")

    except Exception as e:
        print(f"❌ Error saving file: {e}")
