import os
import streamlit as st
from groq import Groq

# Set page configuration
st.set_page_config(
    page_title="AI Mentor Pro Dashboard",
    page_icon="🧠",
    layout="wide"
)

# Fetch API key securely from Streamlit Secrets or Environment Variables
GROQ_API_KEY = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

# Helper function to call Groq API
def call_groq_mentor(prompt, model_choice):
    if not GROQ_API_KEY:
        st.error("⚠️ **API Key Missing**: Please set `GROQ_API_KEY` in Streamlit Secrets.")
        return ""
    
    try:
        client = Groq(api_key=GROQ_API_KEY.strip())
        completion = client.chat.completions.create(
            model=model_choice,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a world-class, practical AI Learning Mentor built on the philosophy: "
                        "'Learn -> Apply -> Think'. Your goal is to guide students with clear, structured output."
                    )
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_completion_tokens=2048,
        )
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"❌ **API Error**: {str(e)}")
        return ""

# Sidebar Profile Controls
with st.sidebar:
    st.header("👤 Learner Profile")
    global_skill = st.text_input("Target Skill / Technology", value="Python")
    global_level = st.selectbox("Skill Level", ["Absolute Beginner", "Intermediate Learner", "Advanced Developer"])
    global_model = st.selectbox("Groq AI Engine", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    st.divider()
    st.caption("💡 Settings in this sidebar apply dynamically to all dashboard tabs.")

# Main App Header
st.title("🧠 AI Learning Mentor Dashboard")
st.subheader("Learn ➔ Apply ➔ Think")
st.caption("An all-in-one personalized platform to master coding, debug programs, practice problems, and build real-world software.")

# Dashboard Navigation Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📖 Learn Concept", 
    "🎯 Practice Problems", 
    "🚀 Guided Projects", 
    "🐞 Code Debugger", 
    "⚡ Code Optimizer", 
    "🗺️ Learning Roadmap"
])

# TAB 1: LEARN CONCEPT
with tab1:
    st.header("📖 Concept Breakdown & Industry Examples")
    col1, col2 = st.columns([1, 2])
    with col1:
        learn_topic = st.text_input("Topic or Concept", placeholder="e.g., Dictionaries, Decorators")
        learn_depth = st.radio("Explanation Depth", ["Brief Overview", "Detailed Explanation", "Deep Dive"])
        btn_learn = st.button("📚 Teach Me Concept", type="primary")
    with col2:
        if btn_learn:
            if not global_skill:
                st.warning("Please specify a Target Skill in the sidebar.")
            else:
                prompt = f"""
                Act as an AI Learning Mentor teaching '{global_skill}' at the '{global_level}' level.
                Topic: {learn_topic if learn_topic else 'Core fundamentals'}
                Depth: {learn_depth}
                Structure output as:
                1. 📖 **Concept Breakdown**
                2. 💡 **Real-World Analogy & Industry Scenario**
                3. 🛠️ **Annotated Code Example**
                4. 🧠 **Reflection Question**
                """
                with st.spinner("Generating lesson..."):
                    res = call_groq_mentor(prompt, global_model)
                    if res:
                        st.markdown(res)

# TAB 2: PRACTICE PROBLEMS
with tab2:
    st.header("🎯 LeetCode-Style Problem Generator")
    col1, col2 = st.columns([1, 2])
    with col1:
        prob_topic = st.text_input("Focus Topic", placeholder="e.g., String manipulation, Recursion")
        prob_cat = st.selectbox("Problem Category", ["Algorithm Challenge", "Real-World Business Logic", "Optimization Problem"])
        btn_prob = st.button("🎯 Generate Problem", type="primary")
    with col2:
        if btn_prob:
            prompt = f"""
            Create a LeetCode-style problem for learning '{global_skill}' at '{global_level}' level.
            Focus Topic: {prob_topic if prob_topic else 'General problem solving'}
            Category: {prob_cat}
            Structure output as:
            1. 🎯 **Problem Statement**
            2. 📥 **Sample Test Cases**
            3. 💡 **Hints & Thinking Strategy**
            4. 🧪 **Starter Code Template**
            """
            with st.spinner("Generating problem..."):
                res = call_groq_mentor(prompt, global_model)
                if res:
                    st.markdown(res)

# TAB 3: GUIDED PROJECTS
with tab3:
    st.header("🚀 Step-by-Step Project Blueprint Builder")
    col1, col2 = st.columns([1, 2])
    with col1:
        project_idea = st.text_area("Project Idea (Optional)", placeholder="e.g., Expense Tracker, Web Scraper")
        btn_proj = st.button("🛠️ Generate Project Plan", type="primary")
    with col2:
        if btn_proj:
            prompt = f"""
            Design a project blueprint for '{global_skill}' at '{global_level}' level.
            Concept: {project_idea if project_idea else 'Practical application'}
            Structure output as:
            1. 🚀 **Project Goal & Value**
            2. 📋 **Tech Stack & Architecture**
            3. 🛠️ **Step-by-Step Milestones**
            4. 🔥 **Bonus Extension Feature**
            """
            with st.spinner("Building project blueprint..."):
                res = call_groq_mentor(prompt, global_model)
                if res:
                    st.markdown(res)

# TAB 4: CODE DEBUGGER
with tab4:
    st.header("🐞 Instant Code Fixer & Error Explainer")
    col1, col2 = st.columns([1, 2])
    with col1:
        debug_code = st.text_area("Paste Broken Code Here", height=200)
        debug_err = st.text_input("Error Message / Behavior Issue")
        btn_debug = st.button("🔍 Fix My Code", type="primary")
    with col2:
        if btn_debug:
            if not debug_code:
                st.warning("Please paste code to debug.")
            else:
                prompt = f"""
                Act as a Code Debugger for '{global_skill}' ({global_level} level).
                Code: ```python\n{debug_code}\n```
                Error/Issue: {debug_err}
                Structure output as:
                1. 🔍 **Bug Root Cause**
                2. ✏️ **Corrected Code Solution**
                3. 💡 **Best Practice Tip**
                """
                with st.spinner("Analyzing code..."):
                    res = call_groq_mentor(prompt, global_model)
                    if res:
                        st.markdown(res)

# TAB 5: CODE OPTIMIZER
with tab5:
    st.header("⚡ Code Refactoring & Performance Improvement")
    col1, col2 = st.columns([1, 2])
    with col1:
        opt_code = st.text_area("Paste Working Code to Refactor", height=200)
        btn_opt = st.button("⚡ Refactor Code", type="primary")
    with col2:
        if btn_opt:
            if not opt_code:
                st.warning("Please paste code to refactor.")
            else:
                prompt = f"""
                Refactor code written in '{global_skill}' ({global_level} level).
                Code: ```python\n{opt_code}\n```
                Structure output as:
                1. ⚡ **Performance & Readability Analysis**
                2. 🚀 **Refactored Code**
                3. 📊 **Key Improvements Made**
                """
                with st.spinner("Optimizing code..."):
                    res = call_groq_mentor(prompt, global_model)
                    if res:
                        st.markdown(res)

# TAB 6: LEARNING ROADMAP
with tab6:
    st.header("🗺️ Personalized Skill Roadmap")
    col1, col2 = st.columns([1, 2])
    with col1:
        road_time = st.radio("Duration", ["2 Weeks (Express)", "4 Weeks (Standard)", "8 Weeks (Mastery)"])
        btn_road = st.button("🗺️ Build My Roadmap", type="primary")
    with col2:
        if btn_road:
            prompt = f"""
            Create a roadmap for mastering '{global_skill}' from '{global_level}' level over '{road_time}'.
            Structure output as:
            1. 🗺️ **Roadmap Overview**
            2. 📅 **Weekly Phase Breakdown**
            3. 🎯 **Final Capstone Goal**
            """
            with st.spinner("Generating roadmap..."):
                res = call_groq_mentor(prompt, global_model)
                if res:
                    st.markdown(res)
      
