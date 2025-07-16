import pandas as pd  # Import pandas for data manipulation and analysis
from sklearn.model_selection import train_test_split  # For splitting data into train and test sets
from sklearn.preprocessing import OneHotEncoder, StandardScaler  # For encoding categorical variables and scaling numerical features
from sklearn.impute import SimpleImputer  # For handling missing values
from sklearn.linear_model import LogisticRegression  # The machine learning model used for classification
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix  # For evaluating model performance
from sklearn.compose import ColumnTransformer  # For applying different preprocessing to different columns
from sklearn.pipeline import Pipeline  # For chaining preprocessing and modeling steps
import joblib  # For saving and loading trained models


def auto_train_model(
    train_path=None,  # Path to the training data CSV file (optional)
    test_path=None,   # Path to the test data CSV file (optional)
    full_path=None,   # Path to a single CSV file containing all data (optional)
    target_column=None,  # Name of the target column to predict (required)
    model_name=None      # Name to use when saving the trained model (optional)
):
    # Load data
    if full_path:  # If a single full dataset is provided
        df = pd.read_csv(full_path)  # Read the CSV file into a DataFrame
        X = df.drop(columns=[target_column])  # Features: all columns except the target
        y = df[target_column]  # Target: the column to predict
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42  # Split data into train/test (80/20 split)
        )
    elif train_path and test_path:  # If separate train and test files are provided
        train_df = pd.read_csv(train_path)  # Read training data
        test_df = pd.read_csv(test_path)    # Read test data
        X_train = train_df.drop(columns=[target_column])  # Training features
        y_train = train_df[target_column]  # Training target
        if target_column in test_df.columns:  # If test data includes target column
            y_test = test_df[target_column]  # Test target
            X_test = test_df.drop(columns=[target_column])  # Test features
        else:  # If test data does not include target column (e.g., for prediction only)
            X_test = test_df  # Test features only
            y_test = None     # No test target available
    else:
        raise ValueError("Need either full_path or both train_path and test_path")  # Require at least one data source

    # Preprocessing
    cat_cols = X_train.select_dtypes(include=["object", "category"]).columns.tolist()  # List of categorical columns
    num_cols = X_train.select_dtypes(include=["number"]).columns.tolist()  # List of numerical columns

    # Pipeline for numerical columns: impute missing values with mean, then scale
    num_pipeline = Pipeline(
        [("imputer", SimpleImputer(strategy="mean")), ("scale", StandardScaler())]
    )
    # Pipeline for categorical columns: impute missing values with most frequent, then one-hot encode
    cat_pipeline = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("onehot", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    # Combine numerical and categorical pipelines into a single preprocessor
    preprocessor = ColumnTransformer(
        [("num", num_pipeline, num_cols), ("cat", cat_pipeline, cat_cols)]
    )

    # Full pipeline: preprocessing followed by logistic regression classifier
    pipeline = Pipeline(
        [
            ("prep", preprocessor),  # Preprocessing step
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),  # Classifier with balanced class weights and increased max iterations
        ]
    )

    # Train
    pipeline.fit(X_train, y_train)  # Fit the pipeline on the training data

    # Evaluate
    metrics = {}  # Dictionary to store evaluation metrics
    if y_test is not None:  # If test labels are available
        y_pred = pipeline.predict(X_test)  # Predict on the test set
        metrics["accuracy"] = accuracy_score(y_test, y_pred)  # Accuracy score
        metrics["classification_report"] = classification_report(
            y_test, y_pred, output_dict=True  # Detailed classification metrics as a dictionary
        )
        metrics["confusion_matrix"] = confusion_matrix(y_test, y_pred).tolist()  # Confusion matrix as a list
    else:  # If no test labels are available
        metrics["accuracy"] = None
        metrics["classification_report"] = None
        metrics["confusion_matrix"] = None

    # Save model
    if model_name:  # If a model name is provided
        joblib.dump(pipeline, f"{model_name}.pkl")  # Save the trained pipeline to a file
        metrics["model_path"] = f"{model_name}.pkl"  # Store the model path in metrics

    return pipeline, metrics  # Return the trained pipeline and