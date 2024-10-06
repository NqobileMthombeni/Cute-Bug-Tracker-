import streamlit as st
import requests

# Set the title of the Streamlit app
st.title("Cute Bug Tracker")

# Form to add a new bug
with st.form(key='add_bug_form'):
    title = st.text_input("Title")
    description = st.text_area("Description")
    severity = st.selectbox("Severity", ["Low", "Medium", "High"])
    reported_by = st.text_input("Reported By")
    
    submit_button = st.form_submit_button(label='Report Bug')
    
    if submit_button:
        # Send a POST request to the Flask app to add the bug
        response = requests.post('http://127.0.0.1:5000/add_bug', data={
            'title': title,
            'description': description,
            'severity': severity,
            'reported_by': reported_by
        })
        if response.ok:
            st.success("Bug reported successfully! 🐛")
        else:
            st.error("Failed to report the bug.")

## Display all reported bugs
st.subheader("Reported Bugs")

# Get the bugs from the Flask API
response = requests.get('http://127.0.0.1:5000/api/bugs')
if response.ok:
    bugs = response.json().get('bugs', [])  # Use .get() to avoid KeyError
    for bug in bugs:
        st.write(f"**{bug['title']}** - {bug['status']} - Reported by: {bug['reported_by']}")
else:
    st.error("Failed to load bugs.")
