import streamlit as st  # Import Streamlit for building the web dashboard
import pandas as pd  # Import pandas for data manipulation
import plotly.express as px  # Import Plotly Express for interactive charts

st.set_page_config(layout="wide")  # Set the Streamlit page layout to wide for more space
st.title("Loan Approval Analytics Dashboard")  # Set the dashboard title at the top of the page

@st.cache_data  # Cache the function output to avoid reloading data on every interaction
def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)  # Read the uploaded CSV file into a pandas DataFrame

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])  # File uploader widget for CSV files
if uploaded_file is not None:  # If a file has been uploaded by the user
    df = load_data(uploaded_file)  # Load the CSV data into a DataFrame

    # Decode values: convert encoded numerical values to human-readable strings for display
    df['Gender'] = df['Gender'].map({0: "Female", 1: "Male"})  # Map 0/1 to Female/Male
    df['Married'] = df['Married'].map({0: "No", 1: "Yes"})  # Map 0/1 to No/Yes
    df['Dependents'] = df['Dependents'].map({0: "0", 1: "1", 2: "2", 3: "3+"})  # Map 0/1/2/3 to 0/1/2/3+
    df['Education'] = df['Education'].map({0: "Not Graduate", 1: "Graduate"})  # Map 0/1 to Not Graduate/Graduate
    df['Self_Employed'] = df['Self_Employed'].map({0: "No", 1: "Yes"})  # Map 0/1 to No/Yes
    df['Loan_Status'] = df['Loan_Status'].map({0: "N", 1: "Y"})  # Map 0/1 to N/Y (No/Yes)

    # Define a function to calculate approval rate for a given column
    def approval_rate(df, col):
        return (
            df.groupby(col)['Loan_Status']  # Group by the specified column
            .apply(lambda x: (x == 'Y').mean() * 100)  # Calculate percent of 'Y' (approved) in each group
            .reset_index(name='Approval Rate (%)')  # Reset index and name the result column
        )

    # Calculate approval rates for various features
    gender_rates = approval_rate(df, 'Gender')  # Approval rate by gender
    married_rates = approval_rate(df, 'Married')  # Approval rate by marital status
    dependents_rates = approval_rate(df, 'Dependents')  # Approval rate by number of dependents
    education_rates = approval_rate(df, 'Education')  # Approval rate by education level
    self_emp_rates = approval_rate(df, 'Self_Employed')  # Approval rate by self-employment status
    loan_amount_sums = df.groupby('Loan_Status')['LoanAmount'].sum().reset_index()  # Total loan amount by approval status

    # Layout: create two columns for displaying charts side by side
    col1, col2 = st.columns(2)  # Split the page into two columns

    with col1:  # First column for some charts
        st.subheader("1️⃣ Approval Rate by Gender")  # Subheader for gender chart
        fig1 = px.bar(gender_rates, x='Gender', y='Approval Rate (%)', color='Gender')  # Bar chart for gender approval rate
        st.plotly_chart(fig1, use_container_width=True)  # Display the chart

        st.subheader("2️⃣ Approval Rate by Self-Employment")  # Subheader for self-employment chart
        fig2 = px.line(self_emp_rates, x='Self_Employed', y='Approval Rate (%)', markers=True)  # Line chart for self-employment approval rate
        st.plotly_chart(fig2, use_container_width=True)  # Display the chart

        st.subheader("3️⃣ Loan Status Distribution (Pie Chart)")  # Subheader for loan status pie chart
        loan_status_counts = df['Loan_Status'].value_counts().reset_index()  # Count number of each loan status
        loan_status_counts.columns = ['Loan_Status', 'Count']  # Rename columns for clarity
        fig3 = px.pie(loan_status_counts, names='Loan_Status', values='Count', title="Loan Status")  # Pie chart for loan status distribution
        st.plotly_chart(fig3, use_container_width=True)  # Display the chart

    with col2:  # Second column for other charts
        st.subheader("4️⃣ Approval Rate by Number of Dependents")  # Subheader for dependents chart
        fig4 = px.bar(dependents_rates, x='Dependents', y='Approval Rate (%)', color='Dependents')  # Bar chart for dependents approval rate
        st.plotly_chart(fig4, use_container_width=True)  # Display the chart

        st.subheader("5️⃣ Approval Rate by Education")  # Subheader for education chart
        fig5 = px.area(education_rates, x='Education', y='Approval Rate (%)', markers=True)  # Area chart for education approval rate
        st.plotly_chart(fig5, use_container_width=True)  # Display the chart

    # Optional: display a table of total loan amount by approval status
    st.subheader("💰 Total Loan Amount by Status")  # Subheader for loan amount table
    st.dataframe(loan_amount_sums.set_index('Loan_Status'))  # Show the table with loan status as index

else:  # If no file has been uploaded yet
    st.info("📤 Please upload a CSV file to continue.")  # Show an info message prompting the user to upload a file