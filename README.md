# 🌍 AI Travel Recommender

An interactive Streamlit web app that recommends travel destinations based on user preferences such as age, safety, food, nightlife, nature, family-friendliness, budget, weather, and preferred activities.

The app uses a trained machine learning model to suggest the top 5 countries that best match the user’s travel profile. It also displays tourism sites for each recommended country.

---

## 🚀 Live App

Add your deployed Streamlit link here:

```text
**https://travelapp-recomm.streamlit.app/

**
📌 Features
Personalized country recommendations
Multi-step travel preference form
Machine learning-based prediction
Top 5 recommended countries
Match percentage display
User profile summary
Tourism site cards for recommended countries
Custom CSS styling
Background video support
Streamlit dashboard interface
🛠️ Technologies Used
Python
Streamlit
Pandas
Scikit-learn
Joblib
HTML/CSS


Travel_Trip_Recommender/
│
├── test.py
├── requirements.txt
├── travel_country_model.pkl
├── label_encoder.pkl
├── model_columns.pkl
├── sites_for_all_countries.csv
├── video1.mp4
├── .gitattributes
├── .gitignore
└── README.md
📊 Dataset

The app uses travel preference data to train a machine learning model that predicts suitable travel destinations.

The tourism site data is stored in:

sites_for_all_countries.csv

Expected CSV columns:

country
name
city
description
image

Example:

Chile,Torres del Paine,Patagonia,A national park known for mountains and hiking,image_url
🤖 Machine Learning Model

The app uses a trained classification model saved as:

travel_country_model.pkl

Additional saved files:

label_encoder.pkl
model_columns.pkl

These files are loaded in the Streamlit app using joblib.

The model predicts the most suitable countries based on the user’s answers.

⚙️ Installation

Clone the repository:

git clone https://github.com/your-username/your-repository-name.git

Go into the project folder:

cd your-repository-name

Install the required packages:

pip install -r requirements.txt

Run the Streamlit app:

streamlit run test.py
📦 Requirements

The main dependencies are listed in requirements.txt.

Example:

streamlit
pandas
numpy
joblib
scikit-learn==1.6.1

The model was trained using scikit-learn==1.6.1, so the same version should be used when deploying.

🌐 Deployment

This app can be deployed using Streamlit Community Cloud.

Deployment steps:

Push the project to GitHub.
Go to Streamlit Community Cloud.
Click New app.
Select the GitHub repository.
Set the main file path to:
test.py
Choose Python version:
Python 3.11
Click Deploy.
⚠️ Large File Note

The model file may be large:

travel_country_model.pkl

If the file is larger than GitHub’s normal upload limit, use Git LFS.

Example .gitattributes:

*.pkl filter=lfs diff=lfs merge=lfs -text
*.mp4 filter=lfs diff=lfs merge=lfs -text
*.csv filter=lfs diff=lfs merge=lfs -text
🖼️ Tourism Images

Tourism site images are loaded from the CSV file when available. If an image URL is missing or invalid, the app can generate a fallback image URL using the country, city, and site name.

🧭 How the App Works
The user enters their name and date of birth.
The user rates travel preferences such as safety, food, nightlife, nature, and family-friendliness.
The user selects budget, preferred weather, and activities.
The model predicts the top 5 matching countries.
The dashboard displays:
Recommended countries
Match percentages
User travel profile
Tourism sites for selected countries


AbdulRahman Ludeen

Created by:

AbdulRahman Ludeen


