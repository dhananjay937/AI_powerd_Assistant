
# 📂 AI-Powered File Validation System

This Streamlit-based web app automates the validation of vendor files (PDF, CSV, Excel) by extracting key fields, comparing them with user inputs, highlighting mismatches or missing fields, and notifying users via email.

---

## 🚀 Features

- Upload and extract data from PDF, CSV, or Excel files.
- Validate extracted data against manually entered fields.
- Detect missing or incorrect information.
- Real-time email notifications for success or error.
- Visual error summary chart using Matplotlib.
- Stores validated files locally for records.

---

## 🧠 Technologies Used

- **Python 3.7+**
- **Streamlit** – GUI Interface
- **PyMuPDF (fitz)** – PDF Text Extraction
- **Pandas** – CSV/Excel handling
- **Regex (re)** – Data extraction
- **smtplib** – Email Notifications
- **matplotlib** – Error visualization

---

## 📁 Project Structure

```
├── main.py                  # Backend logic: extraction, validation, email
├── GUI.py                   # Streamlit GUI
├── validated_files/         # Folder where validated files are stored
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## 🔧 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ai-file-validator.git
cd ai-file-validator
```

### 2. Create and Activate Virtual Environment (Optional)

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

---

## 💌 Gmail SMTP Email Setup

### Step 1: Enable 2-Step Verification

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** for your Gmail.

### Step 2: Generate an App Password

1. Visit [App Passwords](https://myaccount.google.com/apppasswords)
2. Generate an app password for "Mail" and select "Other" device (e.g., File Validator).
3. Copy the 16-character app password shown.

### Step 3: Set Email Credentials

Edit the `main.py` file or create environment variables for secure usage.

**Option A - Quick Hardcoding (Not secure for production)**

```python
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
```

**Option B - Use Environment Variables (Recommended)**

1. Install `python-dotenv`:

```bash
pip install python-dotenv
```

2. Create a `.env` file in your project root:

```env
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
```

3. Modify `main.py`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🧪 Running the App

```bash
streamlit run GUI.py
```

Then open in your browser at: `http://localhost:8501`

---

## 📦 Requirements

Your `requirements.txt` should include:

```
streamlit
PyMuPDF
pandas
matplotlib
openpyxl
```

Generate it with:

```bash
pip freeze > requirements.txt
```

---

## 📸 Demo Screenshot

![Demo](Screenshot (141).png)  

---

## 📬 Contact

Made with ❤️ by [Your Name]  
📧 Email: patildhananjay1307@gmail.com 
🔗 LinkedIn: [www.linkedin.com/in/dhananjay-patil-b25423315

]

---


