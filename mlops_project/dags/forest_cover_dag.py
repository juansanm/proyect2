import airflow
from airflow.decorators import dag, task
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import pandas as pd
import mlflow
import mlflow.sklearn
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 28),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

@dag(
    dag_id='forest_cover_mlops',
    default_args=default_args,
    schedule_interval='*/5 * * * *',  # Every 5 minutes
    catchup=False
)
def forest_cover_dag():
    @task
    def fetch_data(group_number=1):
        """Fetch data from the external API"""
        url = f"http://10.43.101.108:80/data/{group_number}"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to fetch data: {response.status_code}")

    @task
    def prepare_data(raw_data):
        """Prepare data for model training"""
        df = pd.DataFrame(raw_data)
        X = df.drop('Cover Type', axis=1)
        y = df['Cover Type']
        
        return X, y

    @task
    def train_model(X, y):
        """Train a Random Forest Classifier"""
        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        mlflow.set_tracking_uri("http://mlflow:5000")
        with mlflow.start_run():
            rf_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
            rf_classifier.fit(X_train, y_train)
            y_pred = rf_classifier.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            mlflow.log_metric("accuracy", accuracy)
            report = classification_report(y_test, y_pred, output_dict=True)
            for key, value in report.items():
                if isinstance(value, dict):
                    for metric, score in value.items():
                        mlflow.log_metric(f"{key}_{metric}", score)
                        mlflow.sklearn.log_model(rf_classifier, "forest_cover_model")
            
            return rf_classifier
    data = fetch_data()
    X, y = prepare_data(data)
    model = train_model(X, y)
forest_cover_dag()
