import streamlit as st
import joblib

# Load the trained machine learning model from the file
model = joblib.load("model.pkl")

def run():
    # Set up the app title and header using custom HTML and Streamlit markdown
    new_title = '<p style="font-family:sans-serif; color:Orange; font-size: 20px;">Loan Approval Predictor </p>'
    st.markdown(new_title, unsafe_allow_html=True)
    title = '<p style="font-family:sans-serif; color:orange; font-size: 30px;">💸 Loan Approval Prediction App</p>'
    st.markdown(title,unsafe_allow_html=True)

    # Input field for user's full name
    fn = st.text_input('Full Name')

    # Gender selection (Male/Female)
    gen_display = ('Male','Female')
    gen_options = list(range(len(gen_display)))
    gen = st.selectbox("Gender",gen_options, format_func=lambda x: gen_display[x])

    # Education selection (Not Graduate/Graduate)
    edu_display = ('Not Graduate', 'Graduate')
    edu_options = list(range(len(edu_display)))
    edu = st.selectbox("Education", edu_options, format_func=lambda x: edu_display[x])
    
    # Marital status selection (No/Yes)
    mar_display = ('No', 'Yes')
    mar_options = list(range(len(mar_display)))
    mar = st.selectbox("Marital Status", mar_options, format_func=lambda x: mar_display[x])

    # Dependents selection (No/One/Two/More than Two)
    dep_display = ('No', 'One', 'Two', 'More than Two')
    dep_options = list(range(len(dep_display)))
    dep = st.selectbox("Dependents", dep_options, format_func=lambda x: dep_display[x])

    # Self Employed selection (No/Yes)
    emp_display = ('No', 'Yes')
    emp_options = list(range(len(emp_display)))
    emp = st.selectbox("Self Employed", emp_options, format_func=lambda x: emp_display[x])

    # Property Area selection (Rural/Semi-Urban/Urban)
    prop_display = ('Rural', 'Semi-Urban', 'Urban')
    prop_options = list(range(len(prop_display)))
    prop = st.selectbox("Property Area", prop_options, format_func=lambda x: prop_display[x])

    # Credit History selection (No/Yes)
    cred_history = ('No', 'Yes')
    cred_options = list(range(len(cred_history)))
    cred = st.selectbox("Do you Have a Credit History", cred_options, format_func=lambda x: cred_history[x])
    
    # Applicant's monthly income input
    mon_income = st.number_input("Applicant's Monthly Income($)", value=10000)

    # Co-applicant's monthly income input
    co_mon_income = st.number_input("Co-Applicant's Monthly Income($)", value=10000)

    # Loan amount input
    loan_amt = st.number_input("Loan Amount", value=500)

    # Loan duration selection with mapping to number of days
    dur_display = ['2 Month', '6 Month', '8 Month', '1 Year', '16 Month']
    dur_options = range(len(dur_display))
    dur = st.selectbox("Loan Duration", dur_options, format_func=lambda x: dur_display[x])

    # When the user clicks the Submit button, process the input and make a prediction
    if st.button("Submit"):
        # Map the selected duration to the corresponding number of days
        duration = 0
        if dur == 0:
            duration = 60
        if dur == 1:
            duration = 180
        if dur == 2:
            duration = 240
        if dur == 3:
            duration = 360
        if dur == 4:
            duration = 480

        # Prepare the features in the order expected by the model
        features = [[gen, mar, dep, edu, emp, mon_income, co_mon_income, loan_amt, duration, cred, prop]]
        print(features)  # For debugging: print the features to the console

        # Make a prediction using the loaded model
        prediction = model.predict(features)
        # Convert prediction output to integer
        lc = [str(i) for i in prediction]
        ans = int("".join(lc))

        # Display the result to the user based on the prediction
        if ans == 0:
            st.error(
                "Hello " + fn +' you will not get a loan as per the calculations of the bank.'
            )
        else:
            st.success(
                "Hello " + fn + ' '+' Congratulations!! you will get the loan from Bank'
            )

# Run the Streamlit app
run()