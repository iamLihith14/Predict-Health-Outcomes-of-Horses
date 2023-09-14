# -*- coding: utf-8 -*-
"""horse_health_prediction

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12r52z-WV4WC_gY5XRq9SHYZFxZAUNOyd
"""

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# Define dataset URLs
train_csv_url = "https://raw.githubusercontent.com/iamLihith14/Predict-Health-Outcomes-of-Horses/abc81bc19cfcc9f48df7d7d20d4669cd4f936064/train.csv"
test_csv_url = "https://raw.githubusercontent.com/iamLihith14/Predict-Health-Outcomes-of-Horses/abc81bc19cfcc9f48df7d7d20d4669cd4f936064/test%20(1).csv"

# Load data
train_df = pd.read_csv(train_csv_url)
test_df = pd.read_csv(test_csv_url)

# Selecting relevant columns
cols = ['surgery', 'age', 'rectal_temp', 'pulse', 'respiratory_rate', 'pain', 'packed_cell_volume', 'total_protein', 'outcome']
train_df = train_df[cols]
test_df = test_df[cols[:-1]]  # Test data does not have the 'outcome' column

# Step 1: Preprocess the data
label_encoder = LabelEncoder()
train_df['surgery'] = label_encoder.fit_transform(train_df['surgery'])
train_df['age'] = label_encoder.fit_transform(train_df['age'])
train_df['pain'] = label_encoder.fit_transform(train_df['pain'])
train_df['outcome'] = label_encoder.fit_transform(train_df['outcome'])

# Replace missing values with the median
train_df.fillna(train_df.median(), inplace=True)

X = train_df.drop('outcome', axis=1)
y = train_df['outcome']

scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 2: Build and train the model
model = keras.Sequential([
    layers.Dense(64, activation='relu', input_dim=X.shape[1]),
    layers.Dense(32, activation='relu'),
    layers.Dense(3, activation='softmax')  # 3 classes for outcomes
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, validation_data=(X_val, y_val), epochs=10, batch_size=32, verbose=1)

# Create a Streamlit app
st.set_page_config(
    page_title="Horse Health Outcome Predictor",
    layout="wide",
)

st.title("Horse Health Outcome Predictor")
st.write("Predict the health outcome of a horse based on its attributes.")

# Create input fields for user input
st.write("Enter horse details:")
surgery = st.selectbox("Surgery", ["no", "yes"])
age = st.selectbox("Age", ["adult", "young"])
rectal_temp = st.number_input("Rectal Temperature")
pulse = st.number_input("Pulse")
respiratory_rate = st.number_input("Respiratory Rate")
pain = st.selectbox("Pain", ["mild_pain", "depressed", "moderate", "severe_pain"])
packed_cell_volume = st.number_input("Packed Cell Volume")
total_protein = st.number_input("Total Protein")

# Predict the outcome when the user clicks the button
if st.button("Predict Outcome"):
    input_data = [label_encoder.transform([surgery])[0], label_encoder.transform([age])[0],
                  rectal_temp, pulse, respiratory_rate, label_encoder.transform([pain])[0],
                  packed_cell_volume, total_protein]
    input_data = scaler.transform([input_data])
    predicted_outcome = model.predict(input_data)
    predicted_class = np.argmax(predicted_outcome)

    classes = ['died', 'euthanized', 'lived']
    predicted_outcome_text = classes[predicted_class]

    st.write(f"Predicted Outcome: {predicted_outcome_text}")

    # Evaluate accuracy on the validation set
    y_pred_val = model.predict(X_val)
    predicted_classes = np.argmax(y_pred_val, axis=1)
    accuracy = accuracy_score(y_val, predicted_classes)
    st.write(f"Accuracy on Validation Set: {accuracy:.4f}")

