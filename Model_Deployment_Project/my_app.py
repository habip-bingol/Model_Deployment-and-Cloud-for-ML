import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
from sklearn.linear_model import Lasso
from sklearn.model_selection import train_test_split
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.pipeline import Pipeline



def add_bg_from_url():
    st.markdown(
         f"""
         <style>
         .stApp {{
             background-image: url("https://wallpaperaccess.com/full/239032.jpg");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )

add_bg_from_url() 

st.title("Selling Price Predictor🚗")
st.markdown("**Are you planning to sell your car ?** ")
st.markdown("**Let's try evaluating the price** :grinning:")
    
# read Dataset
df = pd.read_csv("without_outliers_autoscout.csv")    


features = ["make_model", "body_type", "km", "age", "gearing_type", "gears","price_€"]
df = df[features]
 
if st.button("See Dataset Sample"):
    st.write(df.sample(5))

# Creating side bar 
st.sidebar.title("Select the features")
    
make_model = st.sidebar.selectbox("Make_Model", df.make_model.unique())

gearing_Type = st.sidebar.selectbox("Gearing_Type", df.gearing_type.unique())

age = st.sidebar.number_input("Age:",min_value=0, max_value=4)

# age = st.sidebar.selectbox("age", ("0","1", "2", "3"))

km = st.sidebar.slider("Km", 0.0, 317000.0)

Gears = st.sidebar.number_input("Gears",min_value=5, max_value=8)


X = df.drop(columns = ["price_€"])
y = df["price_€"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

cat = X.select_dtypes("object").columns
cat = list(cat)

column_trans = make_column_transformer((OneHotEncoder(handle_unknown="ignore", sparse=False), cat), 
                                       remainder=MinMaxScaler())

X_train=column_trans.fit_transform(X_train)

X_test=column_trans.transform(X_test)


pipe_model = Pipeline([("OneHotEncoder", column_trans), ("Lasso", Lasso(alpha = 0.01))])
pipe_model.fit(X, y)


import pickle
pickle.dump(pipe_model, open('autoscout_deployment_project', 'wb'))

pickle.dump(column_trans, open('transformer', 'wb'))


model = pickle.load(open('autoscout_deployment_project', 'rb'))

transformer = pickle.load(open('transformer', 'rb'))

   
if st.button("Predict"):
    prediction = model.predict(df)
    st.success("Price of your car is €{}. ".format(int(prediction[0])))




    
    
    
    
    