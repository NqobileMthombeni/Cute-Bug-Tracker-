import streamlit as st
import requests

# Set the title of the Streamlit app
st.title("🐛 Cute Bug Tracker 🦋")

# Form to add a new bug
with st.form(key='add_bug_form'):
    title = st.text_input("Title")
    description = st.text_area("Description")
    severity = st.selectbox("Severity", ["Low 😊", "Medium 😐", "High 😰"])
    reported_by = st.text_input("Reported By")

    submit_button = st.form_submit_button(label='Report a New Bug 🪲')

    if submit_button:
        # Send a POST request to the Flask app to add the bug
        response = requests.post('http://127.0.0.1:5000/add_bug', data={
            'title': title,
            'description': description,
            'severity': severity,
            'reported_by': reported_by
        })

        # Handle the response
        if response.ok:
            st.success("Bug reported successfully! 🐛")
        else:
            st.error("Failed to report the bug: " + response.text)  # Display error message

# Display all reported bugs
st.subheader("Reported Bugs")

# Get the bugs from the Flask API
response = requests.get('http://127.0.0.1:5000/api/bugs')
if response.ok:
    bugs = response.json().get('bugs', [])
    for bug in bugs:
        st.write(f"**{bug['title']}** - {bug['status']} - Reported by: {bug['reported_by']}")
        
        # Button to delete the bug
        if st.button(f"Delete Bug {bug['id']}"):
            delete_response = requests.delete(f'http://127.0.0.1:5000/delete_bug/{bug["id"]}')
            if delete_response.ok:
                st.success("Bug deleted successfully! 🐛")
                st.rerun()  # Refresh the app
            else:
                st.error("Failed to delete the bug.")
else:
    st.error("Failed to load bugs.")
