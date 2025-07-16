import streamlit as st  # Import Streamlit for building the web interface
import pandas as pd  # Import pandas for data manipulation
import tempfile  # Import tempfile for creating temporary files
import pickle  # Import pickle for saving/loading Python objects (models)
import plotly.express as px  # Import Plotly Express for charts
import plotly.graph_objects as go  # Import Plotly Graph Objects for advanced charts
from auto_ml import auto_train_model  # Import the auto_train_model function from auto_ml.py

st.title("Loan AutoML Model Trainer")  # Set the page title in Streamlit

# File uploader widget: allows user to upload one or two CSV files
uploaded = st.file_uploader("Upload 1 or 2 CSV files", accept_multiple_files=True, type="csv")

if uploaded:  # If at least one file is uploaded
    if len(uploaded) > 2:  # If more than two files are uploaded
        st.error("Upload at most 2 files.")  # Show error message
        st.stop()  # Stop execution

    file_map = {f.name: f for f in uploaded}  # Create a dictionary mapping file names to file objects

    if len(uploaded) == 2:  # If two files are uploaded (train and test)
        st.info("Specify which file is train and which is test:")  # Prompt user to specify roles
        train_name = st.selectbox("Train file", list(file_map))  # Dropdown to select train file
        test_name = st.selectbox("Test file", list(file_map))  # Dropdown to select test file
        if train_name == test_name:  # If user selects the same file for both
            st.error("Train and test must differ.")  # Show error
            st.stop()  # Stop execution
        df_train = pd.read_csv(file_map[train_name])  # Read the selected train file into a DataFrame
        target = st.selectbox("Select target column (train)", df_train.columns)  # Dropdown to select target column from train file
    else:  # If only one file is uploaded (single dataset)
        file = uploaded[0]  # Get the uploaded file
        df = pd.read_csv(file)  # Read the file into a DataFrame
        target = st.selectbox("Select target column", df.columns)  # Dropdown to select target column

    model_name = st.text_input("Enter model name", value="my_model")  # Text input for model name (default: my_model)

    if st.button("Train Model"):  # If user clicks the Train Model button
        with st.spinner("Training..."):  # Show a spinner while training
            if len(uploaded) == 2:  # If two files (train/test) are used
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")  # Create temp file for train data
                tfile.write(file_map[train_name].getvalue())  # Write train file content to temp file
                tfile.flush()  # Flush to disk
                xfile = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")  # Create temp file for test data
                xfile.write(file_map[test_name].getvalue())  # Write test file content to temp file
                xfile.flush()  # Flush to disk
                pipeline, metrics = auto_train_model(  # Call auto_train_model with train and test paths
                    train_path=tfile.name,
                    test_path=xfile.name,
                    target_column=target,
                    model_name=model_name
                )
            else:  # If only one file is used (full dataset)
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")  # Create temp file for data
                tfile.write(uploaded[0].getvalue())  # Write file content to temp file
                tfile.flush()  # Flush to disk
                pipeline, metrics = auto_train_model(  # Call auto_train_model with full_path
                    full_path=tfile.name,
                    target_column=target,
                    model_name=model_name
                )

        st.success(f"✅ Model '{model_name}' trained successfully!")  # Show success message

        # Save pickle file
        pickle_file = f"{model_name}.pkl"  # Name for the pickle file
        with open(pickle_file, "wb") as f:  # Open file for writing in binary mode
            pickle.dump(pipeline, f)  # Save the trained pipeline to the file

        # Download button for the trained model
        st.download_button("📥 Download Model (.pkl)", data=open(pickle_file, "rb"), file_name=pickle_file)

        # Charts section for model metrics
        st.subheader("📊 Model Metrics")  # Subheader for metrics

        if metrics.get('accuracy') is not None:  # If accuracy is available
            accuracy = metrics['accuracy']  # Get accuracy value
            fig_gauge = go.Figure(go.Indicator(  # Create a gauge chart for accuracy
                mode="gauge+number",
                value=accuracy * 100,
                title={'text': "Accuracy (%)"},
                gauge={'axis': {'range': [None, 100]}}
            ))
            st.plotly_chart(fig_gauge, use_container_width=True)  # Display the gauge chart
        else:  # If accuracy is not available
            st.info("⚠️ Accuracy not available (test set may lack target).")  # Show info message

        if metrics.get('classification_report') is not None:  # If classification report is available
            report_df = pd.DataFrame(metrics['classification_report']).transpose()  # Convert report to DataFrame
            st.subheader("📄 Classification Report")  # Subheader for report
            st.dataframe(report_df)  # Display the report as a table

            # Bar chart for precision, recall, f1-score
            fig_bar = px.bar(
                report_df.reset_index().melt(id_vars="index", value_vars=["precision", "recall", "f1-score"]),
                x="index", y="value", color="variable",
                labels={"index": "Class", "value": "Score", "variable": "Metric"},
                barmode="group",
                title="Classification Metrics"
            )
            st.plotly_chart(fig_bar, use_container_width=True)  # Display the bar chart
        else:  # If classification report is not available
            st.info("⚠️ Classification report not available.")  # Show info message

        # Developer Code Block: show how to use the trained model
        st.subheader("🧠 How to Use the Trained Model")  # Subheader for code block

        code = f"""
import pickle

# Load the model
with open("{pickle_file}", "rb") as f:
    model = pickle.load(f)

# Example prediction
# input_data must be a pandas DataFrame with same features used in training
# prediction = model.predict(input_data)
"""
        st.code(code, language="python")  # Display the code block in Python syntax