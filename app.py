import streamlit as st
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.llm import LLM

load_dotenv()

st.set_page_config(page_title="YouTube Script AI", page_icon="🎥", layout="wide")

st.title("🎥 YouTube Script + SEO Generator")
st.subheader("Hinglish High Retention Faceless Videos ke liye")

with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Gemini API Key", type="password", value=os.getenv("GOOGLE_API_KEY"))
    if api_key:
        os.environ["GOOGLE_API_KEY"] = api_key
    st.caption("Free tier - Bahut use karne pe thoda slow ho sakta hai")

keyword = st.text_input("🎯 YouTube Keyword / Topic Daalo:", 
                        placeholder="Chomu Jaipur history aur vikas")

if st.button("🚀 Best Script + SEO Generate Karo", type="primary", use_container_width=True):
    if not keyword:
        st.error("Keyword to daal do bhai!")
    elif not os.getenv("GOOGLE_API_KEY"):
        st.error("Sidebar mein Gemini API Key daalo!")
    else:
        with st.spinner("🔄 Researcher → Script Writer → SEO Expert kaam kar rahe hain...\n(50-100 seconds lagenge)"):
            
            llm = LLM(
                model="gemini/gemini-2.5-flash",
                api_key=os.getenv("GOOGLE_API_KEY"),
                temperature=0.75
            )

            # Agents
            researcher = Agent(
                role="Smart Researcher",
                goal="Interesting facts aur angles dhundhna",
                backstory="Tu local history, hidden facts aur viewer curiosity samajhta hai.",
                llm=llm
            )

            writer = Agent(
                role="Master Script Writer",
                goal="Bahut engaging Hinglish script banana",
                backstory="Tu faceless YouTube channels ke liye top-class scripts likhta hai. Strong hook, emotional storytelling, questions aur powerful CTA ke saath.",
                llm=llm
            )

            seo = Agent(
                role="SEO Master",
                goal="High CTR title aur description banana",
                backstory="Tu YouTube videos ko search aur recommendation mein rank karne mein expert hai.",
                llm=llm
            )

            # Tasks
            research_task = Task(
                description=f"Topic: {keyword}. Ispe interesting facts, history, current status, aur viewer ke liye useful angles dhundh.",
                expected_output="Detailed research bullets",
                agent=researcher
            )

            script_task = Task(
                description="""Research ke basis pe ek **bahut engaging Hinglish YouTube script** likh.
                Must include:
                - Powerful Hook (first 15 seconds)
                - Clear Introduction
                - 4-5 well structured sections with storytelling + facts + questions
                - Emotional / Surprising elements
                - Strong Conclusion + CTA (Like, Subscribe, Comment)

                Script natural aur bolne layak ho.""",
                expected_output="Full structured script",
                agent=writer
            )

            seo_task = Task(
                description="Script ke hisaab se ek mast Title, detailed Description with timestamps, aur 15-20 best Tags bana.",
                expected_output="SEO elements",
                agent=seo
            )

            crew = Crew(
                agents=[researcher, writer, seo],
                tasks=[research_task, script_task, seo_task],
                process=Process.sequential,
                verbose=False
            )

            result = crew.kickoff(inputs={"keyword": keyword})

            # Clean Output
            st.success("✅ Best Script aur SEO ban gaya!")
            st.markdown("### 📋 Final Result")

            final_output = str(result)
            st.markdown(final_output)

            st.download_button(
                label="📥 Download Script & SEO",
                data=final_output,
                file_name=f"{keyword.replace(' ', '_')}_best_script.md",
                mime="text/markdown"
            )