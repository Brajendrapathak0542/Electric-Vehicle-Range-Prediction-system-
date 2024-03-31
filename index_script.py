import numpy as np
import pickle
import pandas as pd
from PIL import Image
import tensorflow as tf
import sklearn
import streamlit as st

import os

def get_scaler(out_path_parent):
    # load saved model
    with open(out_path_parent+'scaler_X_r.pkl', 'rb') as f:
        scaler_X = pickle.load(f)
    with open(out_path_parent+'scaler_y_r.pkl' , 'rb') as f:
        scaler_y = pickle.load(f)
    return scaler_X,scaler_y

def get_scaler_c(out_path_parent):
    # load saved model
    with open(out_path_parent+'scaler_X_c.pkl', 'rb') as f:
        scaler_X_c = pickle.load(f)
    return scaler_X_c


def get_model_r(out_path_parent):
    # Get a list of all files in the directory
    file_list = os.listdir(out_path_parent)

    # Check if any .pickle or .keras files exist
    pickle_files = [file for file in file_list if file.endswith("model_r.pkl")]
    keras_files = [file for file in file_list if file.endswith("_r.keras")]

    is_deep = True

    if pickle_files:
        print("Found .pickle files:", pickle_files)
        with open(out_path_parent+'model_r.pkl' , 'rb') as f:
            model_r = pickle.load(f)
        is_deep = False
    else:
        print("Found .keras files:", keras_files)
        model_r = tf.keras.models.load_model(out_path_parent+"model_r.keras")
    return model_r,is_deep

def get_model_c(out_path_parent):
    # Get a list of all files in the directory
    file_list = os.listdir(out_path_parent)

    # Check if any .pickle or .keras files exist
    pickle_files = [file for file in file_list if file.endswith("model_c.pkl")]
    keras_files = [file for file in file_list if file.endswith("_c.keras")]

    is_deep = True

    if pickle_files:
        print("Found .pickle files:", pickle_files)
        with open(out_path_parent+'model_c.pkl' , 'rb') as f:
            model_c = pickle.load(f)
        is_deep = False
    else:
        print("Found .keras files:", keras_files)
        model_c = tf.keras.models.load_model(out_path_parent+"model_c.keras")
    return model_c,is_deep

def get_predictions_r(input_vals,out_path_parent):
    
    scaler_X,scaler_y = get_scaler(out_path_parent)
    model_r,is_deep = get_model_r(out_path_parent)

    if is_deep:
        input_data = np.array([input_vals])

        # Apply input data transformation
        input_data_scaled = scaler_X.transform(input_data)

        # Reshape input data to match model's expected shape
        input_data_reshaped = input_data_scaled.reshape(1, -1)

        # Make prediction
        prediction_scaled = model_r.predict(input_data_reshaped)

        # Apply inverse transformation to the prediction
        prediction = scaler_y.inverse_transform(prediction_scaled)

        # print("Predicted values:", prediction)
        return prediction[0][0]
    else:
        prediction = model_r.predict([input_vals])
        return prediction[0]


def get_predictions_c(input_vals,out_path_parent):
    
    scaler_X_c = get_scaler_c(out_path_parent)
    model_c,is_deep = get_model_c(out_path_parent)

    if is_deep:
        input_data = np.array([input_vals])

        # Apply input data transformation
        input_data_scaled = scaler_X_c.transform(input_data)

        # Reshape input data to match model's expected shape
        input_data_reshaped = input_data_scaled.reshape(1, -1)

        # Make prediction
        prediction_scaled = model_c.predict(input_data_reshaped)

        # Apply inverse transformation to the prediction
        prediction = tf.where(prediction_scaled > 0.7, tf.ones_like(prediction_scaled), tf.zeros_like(prediction_scaled) )

        # print("Predicted values:", prediction)
        return prediction[0][0]
    else:
        prediction = model_c.predict([input_vals])
        return prediction[0]


# def predict_range(quantity,city,motor_way,country_roads,ac,park_heating,avg_speed,driving_style,tire_type):
#     prediction=lr.predict([[quantity,city,motor_way,country_roads,ac,park_heating,avg_speed,driving_style,tire_type]])
#     return prediction

# def predict_ecr(quantity,result,city,motor_way,country_roads,ac,park_heating,avg_speed,driving_style,tire_type):
#     ecr_predict=ec.predict([[quantity,result,city,motor_way,country_roads,ac,park_heating,avg_speed,driving_style,tire_type]])
#     return ecr_predict

def main():
    car_names = ["ev_golf", "tesla_s", "renault_zoe", "mitsubishi_imiev"]
    selected_car = st.sidebar.selectbox("Select a car:", car_names)
    st.title("EV Range Predictor")

     # Display selected car name
    st.write(f"You selected: {selected_car}")
    
    # Input boxes for car details
    st.write(f"Enter details for {selected_car}:")


    quantity = st.number_input("Quantity(kWh)")
    # city = st.text_input("City(0 or 1)",placeholder = "Type Here")
    city = int(st.checkbox("City Road"))
    motor_way = int(st.checkbox("Highway Road"))
    country_roads = int(st.checkbox("Country Road"))
    # motor_way = st.text_input("Motor Way(0 or 1)",placeholder = "Type Here")
    # country_roads  = st.text_input("Country Roads(0 or 1)",placeholder = "Type Here")
    ac = int(st.checkbox("A/C On/Off"))
    # ac = st.text_input("A/C",placeholder = "Type Here")
    park_heating = int(st.checkbox("Park Heating On/Off"))
    # park_heating = st.text_input("Park Heating (0 or 1)",placeholder = "Type Here")
    avg_speed = st.number_input("Average Speed(km/h")
    
    driving_styles = {"Normal": 0, "Moderate": 1, "Fast": 2}
    selected_style = st.selectbox("Driving Style:", list(driving_styles.keys()))

    # Display selected driving style and its corresponding value
    # st.write(f"Selected Driving Style: {selected_style}")
    # st.write(f"Backend Format: {driving_styles[selected_style]}")
    
    driving_style = driving_styles[selected_style]
    # driving_style = st.text_input("Driving Style(Normal, Moderate or Fast)",placeholder = "Type Here")
    tire_types = {"Summer": 0, "Winter": 1}
    selected_tire = st.selectbox("Tire Type:", list(tire_types.keys()))
    tire_type = tire_types[selected_tire]

    # tire_type = st.text_input("Tire Type(0 or 1)",placeholder = "Type Here")
    car_name = selected_car
    result=0

    out_path_parent = f"C:/Users/shubh/OneDrive/Desktop/ev-app - Copy/cars/{car_name}/"
    if st.button("Get Predictions"):
        input_vals_r = [quantity,city,motor_way,country_roads,ac,park_heating,avg_speed,driving_style,tire_type]
        # st.write(input_vals_r)
        result = get_predictions_r(input_vals_r,out_path_parent)
        result = np.round(result, 2)
        # st.write(type(result))
        
        # ecr = predict_ecr(quantity,result,city,motor_way,country_roads,ac,park_heating,avg_speed,driving_style,tire_type)
        # st.success('Predicted Range: {}\n'.format(result) + "\n" + "Consumption is likely to be higher" if ecr > 0 else "Consumption is likely to be lower")
        df = pd.read_csv(out_path_parent+'model_details.csv')
        tolerance = df.iloc[0,0]
        tolerance = np.round(tolerance,2)
        st.success(f"Estimated Driving Range is {result} Kms with tolerance level of +- {tolerance} Kms")
        input_vals_c = [quantity,result,city,motor_way,country_roads,ac,park_heating,avg_speed,driving_style,tire_type]
        ecr_val = get_predictions_c(input_vals_c,out_path_parent)
        ecr = "Energy Consumption likely to be higher than maker." if ecr_val ==1 else "Energy Consumption likely to be lesser than maker."
        st.success(ecr)
if __name__=='__main__':
    main()

