import streamlit as st
import matplotlib.pyplot as plt
import main  # Importing functions from main.py

st.title("AI-Powered File Validation System")
st.sidebar.header("User Input")

# User input fields
name = st.sidebar.text_input("Name")
branch = st.sidebar.text_input("Branch")
vendor_code = st.sidebar.text_input("Vendor Code")
account_number = st.sidebar.text_input("Account Number")
date = st.sidebar.text_input("Date")
user_email = st.sidebar.text_input("Email")  # User email input

uploaded_file = st.file_uploader("Upload Vendor PDF", type=["pdf", "csv", "xlsx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]
    
    if file_extension == "pdf":
        with open("temp.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        extracted_text = main.extract_text_from_pdf("temp.pdf")
        extracted_data = main.extract_fields(extracted_text)
    else:
        extracted_data = main.extract_fields_from_csv_excel(uploaded_file)
    
    # Compare with user input
    user_data = {
        "Name": name.strip(),
        "Branch": branch.strip(),
        "Vendor Code": vendor_code.strip(),
        "Account Number": account_number.strip(),
        "Date": date.strip()
    }
    errors = main.validate_data(user_data, extracted_data)

    # Check for missing values in the extracted data
    missing_fields = [key for key, value in extracted_data.items() if value == "Blank"]

    # Submit Button to validate and send email
    if st.button("Submit"):
        if errors or missing_fields:
            st.error("Errors detected! Please check the details below.")
            
            if missing_fields:
                st.warning(f"⚠️ Missing values in file: {', '.join(missing_fields)}")
                errors.append(f"Missing values: {', '.join(missing_fields)}")

            for error in errors:
                st.warning(error)

            st.toast("Validation errors detected! Check the description below.", icon="⚠️")

            # Send error notification email
            main.send_email_notification(
                user_email, 
                "Validation Errors Detected", 
                "Errors found: " + "\n".join(errors)
            )
        else:
            st.success("File validated successfully! ✅")
            main.store_final_file(uploaded_file)

            # Send success email
            main.send_email_notification(
                user_email, 
                "File Validated Successfully", 
                "Your file has been successfully validated and stored!"
            )

        # Visualization of errors
        error_counts = {"Total Fields": 5, "Errors": len(errors)}
        fig, ax = plt.subplots()
        ax.bar(error_counts.keys(), error_counts.values(), color=['green', 'red'])
        ax.set_ylabel("Count")
        ax.set_title("Validation Summary")
        st.pyplot(fig)
