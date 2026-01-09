import streamlit as st

st.set_page_config(page_title="Connection Test")
st.title("✅ Streamlit is Working!")
st.write("If you can see this page, your Cloud Shell web preview is successfully connected to the Streamlit server.")

if st.button("Click Me"):
    st.balloons()
    st.success("Interactive elements are also working!")
