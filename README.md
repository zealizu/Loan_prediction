# Loan Approval Prediction & AutoML Dashboard

This project provides a complete solution for predicting loan approval using machine learning, with a user-friendly web interface for both model training (AutoML) and prediction. It also includes an analytics dashboard for exploring loan approval data.

## Features

- **AutoML Model Trainer**: Upload your own CSV data, select the target column, and train a logistic regression model with automatic preprocessing.
- **Loan Approval Predictor**: Enter applicant details in a web form and get instant loan approval predictions using a trained model.
- **Analytics Dashboard**: Visualize approval rates and loan statistics interactively.
- **Model Download**: Download trained models for reuse or deployment.

## Project Structure

```
.
├── auto_ml.py                # Core AutoML logic (training, preprocessing, evaluation)
├── streamlit_app.py          # Streamlit app for loan approval prediction
├── model.pkl                 # Example trained model (binary file)
├── my_model_1.pkl            # Example trained model (binary file)
├── predicted_data.csv        # CSV log of predictions made by the app
├── requirements.txt          # Python dependencies
├── test.csv                  # Example test dataset
├── train.csv                 # Example training dataset
├── pages/
│   ├── dashboard.py          # Streamlit dashboard for analytics
│   └── model.py              # Streamlit page for AutoML model training
└── bank_Loan_Prediction.ipynb # Jupyter notebook for data exploration and model development
```

## Getting Started

### 1. Install Dependencies

Install the required Python packages:

```sh
pip install -r requirements.txt
```

### 2. Run the Streamlit App

To launch the main app (prediction interface):

```sh
streamlit run streamlit_app.py
```

To access the dashboard and AutoML trainer, use Streamlit's multipage feature:

```sh
streamlit run streamlit_app.py
```

Then navigate to the sidebar to access:
- **Loan AutoML Model Trainer** (pages/model.py)
- **Loan Approval Analytics Dashboard** (pages/dashboard.py)

### 3. Model Training (AutoML)

- Go to the **Loan AutoML Model Trainer** page.
- Upload your training (and optionally test) CSV files.
- Select the target column and enter a model name.
- Click "Train Model" to train and download your model.

### 4. Loan Approval Prediction

- Use the main app interface to input applicant details.
- Click "Submit" to get a prediction.
- Each prediction is logged in `predicted_data.csv`.

### 5. Analytics Dashboard

- Go to the **Loan Approval Analytics Dashboard** page.
- Upload a CSV file (e.g., `predicted_data.csv` or your own data).
- Explore approval rates and loan statistics with interactive charts.

## Data Format

Your CSV files should have columns similar to:

- `Gender` (0=Female, 1=Male)
- `Married` (0=No, 1=Yes)
- `Dependents` (0, 1, 2, 3)
- `Education` (0=Not Graduate, 1=Graduate)
- `Self_Employed` (0=No, 1=Yes)
- `ApplicantIncome`
- `CoapplicantIncome`
- `LoanAmount`
- `Loan_Amount_Term`
- `Credit_History` (0=No, 1=Yes)
- `Property_Area` (0=Rural, 1=Semi-Urban, 2=Urban)
- `Loan_Status` (0=Not Approved, 1=Approved) — for supervised training

## Model Details

- Uses a [`LogisticRegression`](auto_ml.py) classifier with balanced class weights.
- Preprocessing includes imputation, scaling, and one-hot encoding as appropriate.
- All preprocessing is included in the saved model pipeline.

## Customization

- You can modify the model or preprocessing steps in [`auto_ml.py`](auto_ml.py).
- The Streamlit UI can be customized in [`streamlit_app.py`](streamlit_app.py), [`pages/model.py`](pages/model.py), and [`pages/dashboard.py`](pages/dashboard.py).

## Example Usage

**Using a trained model in Python:**
```python
import pickle
import pandas as pd

with open("my_model.pkl", "rb") as f:
    model = pickle.load(f)

# input_data must be a pandas DataFrame with the same features as used in training
# prediction = model.predict(input_data)
```

## License

This project is for educational and demonstration purposes.

---

**Author:** Your Name Here