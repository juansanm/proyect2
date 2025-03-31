import streamlit as st
import requests
import pandas as pd
st.title("Forest Cover Type Prediction")
st.sidebar.header("Input Features")
def get_user_input():
    inputs = {}
    feature_mapping = {
        "Elevation": (0, 4000),
        "Aspect": (0, 360),
        "Slope": (0, 90),
        "Horizontal Distance To Hydrology": (0, 10000),
        "Vertical Distance To Hydrology": (-500, 500),
        "Horizontal Distance To Roadways": (0, 10000),
        "Hillshade 9am": (0, 255),
        "Hillshade Noon": (0, 255),
        "Hillshade 3pm": (0, 255),
        "Horizontal Distance To Fire Points": (0, 10000)
    }
    
    for feature, (min_val, max_val) in feature_mapping.items():
        inputs[feature] = st.sidebar.slider(
            feature, 
            min_value=min_val, 
            max_value=max_val, 
            value=(min_val + max_val) // 2
        )
    
    return inputs
user_inputs = get_user_input()
if st.sidebar.button("Predict Forest Cover Type"):
    try:
        response = requests.post("http://inference-api:8000/predict", json=user_inputs)
        
        if response.status_code == 200:
            prediction = response.json()['prediction']
            
            cover_types = {
                1: "Spruce/Fir",
                2: "Lodgepole Pine",
                3: "Ponderosa Pine",
                4: "Cottonwood/Willow",
                5: "Aspen",
                6: "Douglas-fir",
                7: "Krummholz"
            }
            
            st.success(f"Predicted Forest Cover Type: {cover_types.get(prediction, 'Unknown')}")
        else:
            st.error(f"Prediction failed: {response.text}")
    
    except Exception as e:
        st.error(f"Error making prediction: {e}")

st.subheader("Current Input Features")
st.write(user_inputs)
