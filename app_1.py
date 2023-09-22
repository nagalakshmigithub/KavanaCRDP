import streamlit as st
import pickle
import numpy as np
import bz2 as bz2
import webbrowser as wb

# Loading the saved Model

def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data

# Function use to open link which will download the demo excel file
def open_link(str):
    wb.open(str)

# Unpacking Scaler pkl file
model = decompress_pickle(r'C:\Users\vacha\ccdp.pbz2')

def predict_default(features):

    features = np.array(features).astype(np.float64).reshape(1,-1)
    
    prediction = model.predict(features)
    probability = model.predict_proba(features)

    return prediction, probability

def main():

    html_temp = """
        <div style = "background-color: powderblue; padding: 10px;">
            <center><h1>CREDIT CARD DEFAULT PREDICTION</h1></center>
        </div><br>
    """
    
    st.markdown(html_temp, unsafe_allow_html=True)
    
    LIMIT_BAL = st.text_input("Limited Balance (in New Taiwanese (NT) dollar)")
    sex_status=["male","female"]
    education_status = ["graduate school", "university", "high school", "others"]
    marital_status = ["Married","single", "others"]

    payment_status = ["No delay in payment",
        "payment delay for 1 month",
        "payment delay for 2 month",
        "payment delay for 3 month",
        "payment delay for 4 month",
        "payment delay for 5 month",
        "payment delay for 6 month",
        "payment delay for 7 month",
        "payment delay for 8 month",   
    ]
    
    SEX = sex_status.index(st.selectbox("Select Gender", tuple(sex_status))) + 1
    EDUCATION = education_status.index(st.selectbox("Select Education", tuple(education_status))) + 1
    MARRIAGE = marital_status.index(st.selectbox("Marital Status", tuple(marital_status))) + 1
    AGE = st.text_input("Age (in Years)")

    PAY_1 = payment_status.index(st.selectbox("Repayment Status of last month", tuple(payment_status))) - 2
    PAY_2 = payment_status.index(st.selectbox("Repayment Status of last 2nd month", tuple(payment_status))) - 2
    PAY_3 = payment_status.index(st.selectbox("Repayment Status of last 3rd month", tuple(payment_status))) - 2
    PAY_4 = payment_status.index(st.selectbox("Repayment Status of last 4th month", tuple(payment_status))) - 2
    PAY_5 = payment_status.index(st.selectbox("Repayment Status of last 5th month", tuple(payment_status))) - 2
    PAY_6 = payment_status.index(st.selectbox("Repayment Status of last 6th month", tuple(payment_status))) - 2
     
    BILL_AMT1 = st.text_input("Last month Bill Amount (in NT dollar)")
    BILL_AMT2 = st.text_input("Last 2nd month Bill Amount (in dollar)")
    BILL_AMT3 = st.text_input("Last 3rd month Bill Amount (in NT dollar)")
    BILL_AMT4 = st.text_input("Last 4th month Bill Amount (in NT dollar)")
    BILL_AMT5 = st.text_input("Last 5th month Bill Amount (in NT dollar)")
    BILL_AMT6 = st.text_input("Last 6th month Bill Amount (in Nt dollar)")

    PAY_AMT1 = st.text_input("Amount paid in Last Month (in NT dollar)")
    PAY_AMT2 = st.text_input("Amount paid in Last 2nd month (in NT dollar)")
    PAY_AMT3 = st.text_input("Amount paid in Last 3rd month (in NT) dollar)")
    PAY_AMT4 = st.text_input("Amount paid in Last 4th month (in NT dollar)")
    PAY_AMT5 = st.text_input("Amount paid in Last 5th month (in NT dollar)")
    PAY_AMT6 = st.text_input("Amount paid in Last 6th month (in NT dollar)")

    if st.button("Predict"):
        pay_avg=(PAY_1+PAY_2+PAY_3+PAY_4+PAY_5+PAY_6)/6
        features = [LIMIT_BAL,SEX,EDUCATION,MARRIAGE,AGE,PAY_1,PAY_2,PAY_3,PAY_4,PAY_5,PAY_6,BILL_AMT1,BILL_AMT2,BILL_AMT3,BILL_AMT4,BILL_AMT5,BILL_AMT6,PAY_AMT1,PAY_AMT2,PAY_AMT3,PAY_AMT4,PAY_AMT5,PAY_AMT6,pay_avg]
        prediction, probability = predict_default(features)
        if prediction[0] == 1:
            st.success("This account will be defaulted with a probability of {}%.".format(round(np.max(probability)*100, 2)))
        else:
            st.success("This account will not be defaulted with a probability of {}%.".format(round(np.max(probability)*100, 2)))

if __name__ == '__main__':
    main()
