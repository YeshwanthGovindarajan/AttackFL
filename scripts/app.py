import streamlit as st
import numpy as np
import pandas as pd
import gdown
from tensorflow.keras.models import load_model
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

# Load the trained model from Google Drive
model_url = 'https://drive.google.com/uc?export=download&id=1dS0zUJxy8zEUN5pLhVc1M-xmKh7xRz9H'  # Replace with your file ID
gdown.download(model_url, 'attack_classifier_model.h5', quiet=False)
model = load_model('attack_classifier_model.h5')

# Predefined attack signatures
attack_signatures = {
    "Backdoor": [
        "2021 18:17:22.429613000 192.168.0.128 192.168.0.170 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1453306566 0x00001b38 0 0 0 0 4321 0x00000018 1 304 0101080a2b0052ae3d6a605f c2a66a4b08602247767f200d42fce98bdba8773fc2a66a4ac2a66b53c2a66a4b7b20d4674d2b303fe0abf8d25716b97c338de5241188155a6cecfbf63686590d7b8cba01577690618d858e387973bd84e4383d48fd859b438c6b00247b0b19d4feee3b3d62f78a9c7a9600680b187fdc8a7be2c78341e6688416c3e6e6393b829886bb0ca1ad359d7707095fab6606ad637f5f5848a4fd26c2adf0bccc4f2bf02e8759a1da7f792cc27dc6e4418fbcbd9662715fdecf4353967a469ec695f7868c8301758210ad2d1f2d44a33f25cbb5b3aa4a761f4127e71e852fbbfb90314f9faa2ca048846495e8a6ad4a455d520d0016d88c03885561d46614f86727fe8eddca1e7d2ea97b3c408bacde97f5ed354600d5ccdd3b6821791b58432203a5b30c2fc7fe4fa28ca41abacc7833b0c21c 972225 56322 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 Backdoor"
    ],
    "DDoS_HTTP": [
        "2021 11:35:32.017617000 192.168.0.128 192.168.0.170 0 0 0 0 0 0 0 0 0 0 0 0 0 28 1776784235 0x0000a2a0 0 0 0 0 54562 0x00000010 1 0 0101080a1dd4e8ff0aa48815 0 1 80 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 DDoS_HTTP"
    ],
    "OS_Fingerprinting": [
        "2021 22:25:51.106150000 192.168.0.170 192.168.0.128 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0x00007a27 0 0 1 0 65535 0x00000002 0 0 0 0 0 1388 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 OS_Fingerprinting"
    ],
    "Port_Scanning": [
        "2021 16:25:05.874655000 192.168.0.170 192.168.0.128 0 0 0 0 0 0 0 0 0 0 0 0 0 476195363 476195363 0x0000abe9 0 0 1 0 80 0x00000002 0 0 0 0 0 2682 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 Port_Scanning"
    ]
}

# Initialize encoders and scalers used during training
encoder = LabelEncoder()
scaler = MinMaxScaler()

# Simulate preprocessing (encoding and scaling)
def preprocess_input(data):
    # Encode and scale the input data like during training
    # This is a simplified version, adjust it based on the actual encoding/feature processing
    data_encoded = encoder.transform([data])  # Simulating encoding
    data_scaled = scaler.transform([data_encoded])  # Simulating scaling
    return data_scaled

# Streamlit UI
st.title("Network Attack Signature Classifier")
st.write("Select or input an attack signature to classify.")

# Let users select attack signature from predefined ones
signature_option = st.selectbox("Select an Attack Signature", list(attack_signatures.keys()))

# Alternatively, input custom signature
custom_signature = st.text_area("Or input a custom attack signature", "")

# Determine which input to use
input_signature = custom_signature if custom_signature else attack_signatures[signature_option][0]

st.write(f"Selected Signature: {input_signature}")

# Preprocess and classify
if st.button("Classify Attack Signature"):
    if input_signature:
        preprocessed_input = preprocess_input(input_signature)
        predictions = model.predict(preprocessed_input)
        predicted_class = np.argmax(predictions, axis=1)
        st.write(f"Predicted Attack Type: {list(attack_signatures.keys())[predicted_class[0]]}")
    else:
        st.write("Please select or input a signature.")
