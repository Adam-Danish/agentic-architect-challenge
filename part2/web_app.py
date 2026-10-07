import streamlit as st

from web_summarizer import summarize_url


st.title("Web Summarizer")
st.write("Enter a webpage URL to get a summary of no more than 100 words.")

url = st.text_input(
    "Webpage URL",
    placeholder="https://www.python.org/about/",
)
api_key = st.text_input("Gemini API key", type="password")

if st.button("Summarize", type="primary"):
    if not url.strip() or not api_key:
        st.warning("Enter both a webpage URL and your Gemini API key.")
    else:
        try:
            with st.spinner("Reading and summarizing the page..."):
                result = summarize_url(url.strip(), api_key)
        except Exception as error:
            st.error(f"Could not summarize: {error}")
        else:
            st.caption(
                f"Found {result['source_words']} words in "
                f"{result['chunks']} chunk(s)."
            )
            if result["used_browser"]:
                st.info("Browser fallback was used to read this page.")

            st.subheader("Summary")
            st.write(result["summary"])