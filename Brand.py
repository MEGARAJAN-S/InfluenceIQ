import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("C:\\Users\\Devar\\\Downloads\\influencerai-efb20-firebase-adminsdk-fbsvc-9d7c63e15d.json")  # Save your JSON file as serviceAccountKey.json
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Firestore Database

# Streamlit UI
st.set_page_config(page_title="Brand Registration", layout="centered")
st.title("Brand Registration Portal")
st.markdown("---")

# Brand Registration Form
st.header("Register Your Brand")
brand_name = st.text_input("Brand Name")
followers = st.number_input("Number of Followers", min_value=0, step=100)
views_likes = st.number_input("Average Views & Likes", min_value=0, step=100)
domain = st.selectbox("Domain", ["Fashion", "Tech", "Fitness", "Food", "Travel", "Other"])
budget = st.number_input("Budget ($)", min_value=0, step=50)
target_audience = st.text_area("Target Audience Description")

# Submit Button
if st.button("Register Brand"):
    brand_data = {
        "Brand Name": brand_name,
        "Followers": followers,
        "Views & Likes": views_likes,
        "Domain": domain,
        "Budget": budget,
        "Target Audience": target_audience
    }
    db.collection("brands").add(brand_data)  # Save to Firestore
    st.success("Brand Registered Successfully!")
    st.write(pd.DataFrame([brand_data]))

# Influencer Suggestion Section
st.markdown("---")
st.header("Suggested Influencers")

if brand_name:
    st.info("Influencers are suggested based on rating and relevance to your domain.")

    # Fetch Influencers from Firestore (Assumes 'influencers' collection exists)
    influencers_ref = db.collection("influencers").where("Domain", "==", domain)
    docs = influencers_ref.stream()
    
    influencer_list = []
    for doc in docs:
        influencer_list.append(doc.to_dict())

    if influencer_list:
        influencer_df = pd.DataFrame(influencer_list)
        st.dataframe(influencer_df)
    else:
        st.warning("No influencers found for this domain.")
else:
    st.warning("Please register your brand to see influencer suggestions.")
