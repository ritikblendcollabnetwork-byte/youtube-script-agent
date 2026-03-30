import streamlit as st
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

st.set_page_config(page_title="YouTube Script AI", page_icon="🎥", layout="wide")

st.title("🎥 YouTube Script Generator")
st.markdown("**Simple & Fast - Hinglish Script + SEO**")

with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GOOGLE_API_KEY"))
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key

keyword = st.text_input("Keyword / Topic Daalo:", placeholder="Chomu Jaipur history")

if st.button("🚀 Script Generate Karo", type="primary", use_container_width=True):
    if not keyword:
        st.error("Keyword daal do!")
    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("API Key daalo!")
    else:
        with st.spinner("Script bana raha hoon... (20-40 seconds)"):
            llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.75)
            
            prompt = f"""Ek bahut engaging YouTube video script likho topic pe: {keyword}
            Hinglish mein likhna. 
            Structure yeh ho:
            - Strong Hook
            - Introduction
            - 4-5 main sections with facts aur storytelling
            - Conclusion + CTA
            
            Script natural aur bolne layak ho."""

            response = llm.invoke(prompt)
            script = response.content
            
            st.success("✅ Script Ban Gaya!")
            st.markdown(script)
            
            st.download_button("📥 Download Script", script, file_name=f"{keyword}.md")
