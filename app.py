import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(page_title="YouTube Script AI", layout="wide")
st.title("🎥 YouTube Script Generator")
st.markdown("**Simple Hinglish Script + SEO**")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GOOGLE_API_KEY"))
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key

keyword = st.text_input("Keyword Daalo:", placeholder="Best phone under 20000 2026")

if st.button("🚀 Generate Script", type="primary", use_container_width=True):
    if not keyword:
        st.error("Keyword daal do!")
    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("API Key daalo!")
    else:
        with st.spinner("Script bana raha hoon..."):
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.75)
            
            prompt = f"Topic: {keyword}\nEk engaging Hinglish YouTube script likho with strong hook, sections aur CTA."
            
            response = llm.invoke(prompt)
            st.success("✅ Ban Gaya!")
            st.markdown(response.content)
            
            st.download_button("📥 Download", response.content, file_name=f"{keyword}.md")
