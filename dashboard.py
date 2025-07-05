import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(layout="wide")
st.title("Loan Approval Analytics Dashboard")

@st.cache_data
def load_data():
    return pd.read_csv("predicted_data.csv")

df = load_data()

# Map encoded values back to readable labels
df['Gender'] = df['Gender'].map({0: "Female", 1: "Male"})
df['Married'] = df['Married'].map({0: "No", 1: "Yes"})
df['Dependents'] = df['Dependents'].map({0: "0", 1: "1", 2: "2", 3: "3+"})
df['Education'] = df['Education'].map({0: "Not Graduate", 1: "Graduate"})
df['Self_Employed'] = df['Self_Employed'].map({0: "No", 1: "Yes"})
df['Loan_Status'] = df['Loan_Status'].map({0: "N", 1: "Y"})

# Helper function: approval rates by category
def approval_rate(df, col):
    return (
        df.groupby(col)['Loan_Status']
        .apply(lambda x: (x == 'Y').mean() * 100)
        .reset_index(name='Approval Rate (%)')
    )

# Calculate approval rates
gender_rates = approval_rate(df, 'Gender')
married_rates = approval_rate(df, 'Married')
dependents_rates = approval_rate(df, 'Dependents')
education_rates = approval_rate(df, 'Education')
self_emp_rates = approval_rate(df, 'Self_Employed')

# Prepare Loan Amount sums grouped by Loan_Status for pie chart
loan_amount_sums = df.groupby('Loan_Status')['LoanAmount'].sum().reset_index()

cols = st.columns(2)

# 1. Approval Rate by Gender — Donut Chart
with cols[0]:
    fig1 = px.pie(
        gender_rates,
        values='Approval Rate (%)',
        names='Gender',
        hole=0.4,
        title='Approval Rate by Gender (Donut Chart)',
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig1, use_container_width=True)

# 2. Approval Rate by Marital Status — Sunburst Chart
with cols[1]:
    mar_status_counts = df.groupby(['Married', 'Loan_Status']).size().reset_index(name='count')
    fig2 = px.sunburst(
        mar_status_counts,
        path=['Married', 'Loan_Status'],
        values='count',
        title='Marital Status and Loan Approval Distribution (Sunburst)'
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3. Approval Rate by Dependents — Pie Chart (replacing Barpolar)
with cols[0]:
    fig3 = px.pie(
        dependents_rates,
        values='Approval Rate (%)',
        names='Dependents',
        title='Approval Rate by Number of Dependents (Pie Chart)',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig3, use_container_width=True)

# 4. Approval Rate by Education — Pie Chart
with cols[1]:
    fig4 = px.pie(
        education_rates,
        values='Approval Rate (%)',
        names='Education',
        title='Approval Rate by Education Level (Pie Chart)',
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    st.plotly_chart(fig4, use_container_width=True)

# 5. Approval Rate by Self-Employment — Funnel Area Chart
with cols[0]:
    fig5 = px.funnel_area(
        self_emp_rates,
        names='Self_Employed',
        values='Approval Rate (%)',
        title='Approval Rate by Self-Employment Status (Funnel Area Chart)'
    )
    st.plotly_chart(fig5, use_container_width=True)

# 6. Loan Amount Distribution by Approval Status — Pie Chart (replacing Violin)
with cols[1]:
    fig6 = px.pie(
        loan_amount_sums,
        values='LoanAmount',
        names='Loan_Status',
        title='Total Loan Amount Distribution by Approval Status (Pie Chart)',
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    st.plotly_chart(fig6, use_container_width=True)
