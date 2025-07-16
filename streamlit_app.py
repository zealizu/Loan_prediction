import streamlit as st  # Import Streamlit for building the web app interface
import joblib  # Import joblib for loading the trained machine learning model
import pandas as pd  # Import pandas for data manipulation and saving predictions

# Load the trained machine learning model from the file "model.pkl"
model = joblib.load("model.pkl")

def run():
    # Set up the app title and header using custom HTML and Streamlit markdown
    new_title = '<p style="font-family:sans-serif; color:Orange; font-size: 20px;">Loan Approval Predictor </p>'  # Custom HTML for small title
    st.markdown(new_title, unsafe_allow_html=True)  # Render the small title with custom style
    title = '<p style="font-family:sans-serif; color:orange; font-size: 30px;">💸 Loan Approval Prediction App</p>'  # Custom HTML for main title
    st.markdown(title,unsafe_allow_html=True)  # Render the main title with custom style

    # Input field for user's full name (for personalized messages)
    fn = st.text_input('Full Name')

    # Gender selection (Male/Female) using a dropdown
    gen_display = ('Female','Male')  # Display options for gender
    gen_options = list(range(len(gen_display)))  # Numeric options for gender (0, 1)
    gen = st.selectbox("Gender",gen_options, format_func=lambda x: gen_display[x])  # Dropdown for gender, stores index

    # Education selection (Not Graduate/Graduate) using a dropdown
    edu_display = ('Not Graduate', 'Graduate')  # Display options for education
    edu_options = list(range(len(edu_display)))  # Numeric options for education (0, 1)
    edu = st.selectbox("Education", edu_options, format_func=lambda x: edu_display[x])  # Dropdown for education

    # Marital status selection (No/Yes) using a dropdown
    mar_display = ('No', 'Yes')  # Display options for marital status
    mar_options = list(range(len(mar_display)))  # Numeric options for marital status (0, 1)
    mar = st.selectbox("Marital Status", mar_options, format_func=lambda x: mar_display[x])  # Dropdown for marital status

    # Dependents selection (No/One/Two/More than Two) using a dropdown
    dep_display = ('No', 'One', 'Two', 'More than Two')  # Display options for dependents
    dep_options = list(range(len(dep_display)))  # Numeric options for dependents (0, 1, 2, 3)
    dep = st.selectbox("Dependents", dep_options, format_func=lambda x: dep_display[x])  # Dropdown for dependents

    # Self Employed selection (No/Yes) using a dropdown
    emp_display = ('No', 'Yes')  # Display options for self-employed
    emp_options = list(range(len(emp_display)))  # Numeric options for self-employed (0, 1)
    emp = st.selectbox("Self Employed", emp_options, format_func=lambda x: emp_display[x])  # Dropdown for self-employed

    # Property Area selection (Rural/Semi-Urban/Urban) using a dropdown
    prop_display = ('Rural', 'Semi-Urban', 'Urban')  # Display options for property area
    prop_options = list(range(len(prop_display)))  # Numeric options for property area (0, 1, 2)
    prop = st.selectbox("Property Area", prop_options, format_func=lambda x: prop_display[x])  # Dropdown for property area

    # Credit History selection (No/Yes) using a dropdown
    cred_history = ('No', 'Yes')  # Display options for credit history
    cred_options = list(range(len(cred_history)))  # Numeric options for credit history (0, 1)
    cred = st.selectbox("Do you Have a Credit History", cred_options, format_func=lambda x: cred_history[x])  # Dropdown for credit history

    # Applicant's monthly income input (numeric field)
    mon_income = st.number_input("Applicant's Monthly Income($)", value=10000)  # Default value is 10000

    # Co-applicant's monthly income input (numeric field)
    co_mon_income = st.number_input("Co-Applicant's Monthly Income($)", value=10000)  # Default value is 10000

    # Loan amount input (numeric field)
    loan_amt = st.number_input("Loan Amount", value=500)  # Default value is 500

    # Loan duration selection with mapping to number of days
    dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']  # Display options for loan duration
    dur_options = range(len(dur_display))  # Numeric options for duration (0, 1, 2, 3, 4)
    dur = st.selectbox("Loan Duration", dur_options, format_func=lambda x: dur_display[x])  # Dropdown for loan duration

    # When the user clicks the Submit button, process the input and make a prediction
    if st.button("Submit"):
        # Map the selected duration to the corresponding number of days
        duration = 0  # Initialize duration variable
        if dur == 0:
            duration = 60  # 2 months = 60 days
        if dur == 1:
            duration = 180  # 6 months = 180 days
        if dur == 2:
            duration = 240  # 8 months = 240 days
        if dur == 3:
            duration = 360  # 1 year = 360 days
        if dur == 4:
            duration = 480  # 16 months = 480 days

        # Prepare the features in the order expected by the model
        features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]  # List of features for prediction
        print(features)  # For debugging: print the features to the console

        # Make a prediction using the loaded model
        prediction = model.predict(features)  # Predict loan approval (0 or 1)
        print(prediction)# For debugging
        
        # Extract the predicted class (0 or 1) from the model's single-item output
        ans = int(prediction[0])


        # Save the input and prediction to CSV for record-keeping or analytics
        new_row = {
            "Gender": gen,  # Gender (numeric)
            "Married": mar,  # Marital status (numeric)
            "Dependents": dep,  # Dependents (numeric)
            "Education": edu,  # Education (numeric)
            "Self_Employed": emp,  # Self-employed (numeric)
            "ApplicantIncome": mon_income,  # Applicant's income
            "CoapplicantIncome": co_mon_income,  # Co-applicant's income
            "LoanAmount": loan_amt,  # Loan amount
            "Loan_Amount_Term": duration,  # Loan duration in days
            "Credit_History": cred,  # Credit history (numeric)
            "Property_Area": prop,  # Property area (numeric)
            "Loan_Status": ans  # Prediction result (0 or 1)
        }
        df_new = pd.DataFrame([new_row])  # Create a DataFrame from the new row
        df_new.to_csv("predicted_data.csv", mode='a', header=False, index=False)  # Append the new row to CSV file

        # Display the result to the user based on the prediction
        if ans == 0:
            st.error(
                "Hello " + fn +' you will not get a loan as per the calculations of the bank.'  # Show error message if not approved
            )
        else:
            st.success(
                "Hello " + fn + ' '+' Congratulations!! you will get the loan from Bank'  # Show success message if approved
            )

# Run the Streamlit app by calling the run() function
run()