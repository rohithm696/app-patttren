import streamlit as st
import sqlite3

st.set_page_config(page_title="Custom Pattern App")  # Change browser window title

# Database setup
conn = sqlite3.connect("user_data.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT)")
conn.commit()

def generate_pattern(n):
    size = 2 * n - 1
    pattern = []
    for i in range(size):
        row = []
        for j in range(size):
            distance_i = abs(n - 1 - i)
            distance_j = abs(n - 1 - j)
            max_distance = max(distance_i, distance_j)
            computed_value = max_distance + 1
            row.append(str(computed_value))
        row_string = " ".join(row)  # Add space between numbers
        pattern.append(row_string)
    return pattern

st.title("Pattern Generator")
n = st.number_input("Enter a number:", min_value=1, step=1, value=3)
if st.button("Generate Pattern"):
    pattern = generate_pattern(n)
    for row in pattern:
        st.markdown(f'<p style="color:green; font-family:monospace;">{row}</p>', unsafe_allow_html=True)

# Form to collect user messages
st.header("Send a Message")
with st.form("message_form"):
    user_message = st.text_area("Enter your message:")
    submitted = st.form_submit_button("Send")
    if submitted and user_message:
        c.execute("INSERT INTO messages (message) VALUES (?)", (user_message,))
        conn.commit()
        st.success("Text sent to the owner successfully!")

conn.close()
