import streamlit as st
import sqlite3
import datetime
import base64

st.set_page_config(page_title="Custom Pattern App")  # Change browser window title

# Database setup
conn = sqlite3.connect("user_data.db")
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, message TEXT, timestamp TEXT)")
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

def get_download_link(pattern):
    text_content = "\n".join(pattern)
    b64 = base64.b64encode(text_content.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="pattern.txt">Download Pattern</a>'
    return href

st.title("Pattern Generator")
n = st.number_input("Enter a number:", min_value=1, step=1, value=3)
if st.button("Generate Pattern"):
    pattern = generate_pattern(n)
    for row in pattern:
        st.markdown(f'<p style="color:green; font-family:monospace;">{row}</p>', unsafe_allow_html=True)
    st.markdown(get_download_link(pattern), unsafe_allow_html=True)

# Form to collect user messages
st.header("Send a Message")
with st.form("message_form"):
    user_message = st.text_area("Enter your message:")
    submitted = st.form_submit_button("Send")
    if submitted and user_message:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO messages (message, timestamp) VALUES (?, ?)", (user_message, timestamp))
        conn.commit()
        st.success("Text sent to the owner successfully!")
conn.close()

# Secure message display (only accessible with authentication)
st.header("Owner Login")
password = st.text_input("Enter owner password:", type="password")
if st.button("View Messages"):
    if password == "admin123":  # Change this to a secure password
        conn = sqlite3.connect("user_data.db")
        c = conn.cursor()
        c.execute("SELECT * FROM messages")
        messages = c.fetchall()
        conn.close()

        if messages:
            for msg in messages:
                st.write(f"**Message ID {msg[0]} (Received at {msg[2]}):** {msg[1]}")
            if st.button("Clear Messages"):
                conn = sqlite3.connect("user_data.db")
                c = conn.cursor()
                c.execute("DELETE FROM messages")
                conn.commit()
                conn.close()
                st.success("All messages have been deleted.")
        else:
            st.write("No messages received yet.")
    else:
        st.error("Incorrect password! Access denied.")

# Dark Mode Toggle
if st.toggle("Dark Mode"):
    st.markdown("""
        <style>
            body {
                background-color: #121212;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)
