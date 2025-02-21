import streamlit as st

st.set_page_config(page_title="Pattrern")  

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
        row_string = " ".join(row) 
        pattern.append(row_string)
    return pattern

st.title("Yesterday Pattern")
n = st.number_input("Enter your number:", min_value=1, step=1, value=3)
if st.button("Generate"):
    pattern = generate_pattern(n)
    for row in pattern:
        st.markdown(f'<p style="color:green; font-family:monospace;">{row}</p>', unsafe_allow_html=True)
