import streamlit as st
from openai import OpenAI

# --- CONFIGURATION ---
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=OPENAI_API_KEY)

# --- AI WRITER ---
def generate_blog_post(topic, tone):
    prompt = f"""
    You are an expert Content Marketer for a Recruitment Agency.
    Write a 800-word blog post about: "{topic}"
    Tone: {tone}
    
    FORMATTING RULES:
    1. Output strictly in HTML format (use <h2>, <h3>, <p>, <ul>, <li>, <strong>).
    2. Do NOT use <html>, <head>, or <body> tags. Start directly with the content.
    3. Include a catchy Title in an <h1> tag at the top.
    4. Include a "Key Takeaways" box.
    5. End with a Call to Action to "Contact [Your Agency Name]".
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

def generate_seo_meta(content):
    """Generates the Meta Description and SEO Keywords"""
    prompt = f"""
    Read this blog post HTML and generate:
    1. A Meta Description (max 160 chars).
    2. A URL Slug (e.g. resume-tips-2025).
    3. 5 SEO Keywords.
    
    BLOG CONTENT:
    {content[:3000]}
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except: return ""

# --- UI ---
st.set_page_config(page_title="GHL Auto-Blogger", page_icon="✍️", layout="wide")
st.title("✍️ Recruitment Auto-Blogger")
st.markdown("Generate SEO-optimized blogs formatted for GoHighLevel.")

with st.form("blog_form"):
    topic = st.text_input("Blog Topic", "How to negotiate a salary in 2025")
    tone = st.select_slider("Tone", options=["Professional", "Witty", "Direct/Bold", "Empathetic"], value="Professional")
    submitted = st.form_submit_button("Write Blog")

if submitted and topic:
    with st.spinner("AI is writing your article..."):
        # 1. Write Content
        html_content = generate_blog_post(topic, tone)
        
        # 2. Generate SEO Data
        seo_data = generate_seo_meta(html_content)
        
        # --- DISPLAY RESULTS ---
        st.success("Blog Generated!")
        
        tab1, tab2, tab3 = st.tabs(["📖 Preview", "COPY HTML (For GHL)", "🔍 SEO Data"])
        
        with tab1:
            st.markdown(html_content, unsafe_allow_html=True)
            
        with tab2:
            st.info("Copy this code. In GHL Blog Editor, click the `< >` icon and paste this.")
            st.code(html_content, language="html")
            
        with tab3:
            st.write(seo_data)
