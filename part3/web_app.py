from pathlib import Path

import streamlit as st
from google import genai
from google.genai import types
from pypdf import PdfReader


def load_document():
    pdf_path = Path(__file__).with_name("sample_document.pdf")
    reader = PdfReader(pdf_path)

    text = ""
    for page in reader.pages:
        text += (page.extract_text(extraction_mode="layout") or "") + "\n"

    return text.replace("\ue092", ":")


def calculate_ticket_total(adults: int, students: int) -> int:
    """Calculate the total cost of adult and student tickets."""
    if adults < 0 or students < 0:
        raise ValueError("Ticket quantities cannot be negative.")

    st.session_state.calculator_used = True
    return adults * 25 + students * 15


st.title("Community Tech Day Assistant")
st.caption("Ask about the event, tickets, and programme.")

try:
    document_text = load_document()
except Exception as error:
    st.error(f"Could not read sample_document.pdf: {error}")
    st.stop()

if not document_text.strip():
    st.error("No readable text found in the PDF.")
    st.stop()

api_key = st.sidebar.text_input("Gemini API key", type="password")

if st.sidebar.button("New conversation"):
    st.session_state.pop("chat", None)
    st.session_state.messages = []

if not api_key:
    st.info("Enter your Gemini API key in the sidebar to start.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat" not in st.session_state:
    instructions = (
        "You are an assistant for Community Tech Day. "
        "Use the document below as your only source for event facts. "
        "If the document does not contain an answer, say that the document does not say. "
        "Remember details the user tells you during this conversation. "
        "Do not invent event information. "
        "For questions asking for a total ticket cost, use calculate_ticket_total. "
        "Do not use the calculator for questions that only ask for facts.\n\n"
        "DOCUMENT:\n" + document_text
    )

    client = genai.Client(api_key=api_key)
    st.session_state.chat = client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(
            system_instruction=instructions,
            tools=[calculate_ticket_total],
        ),
    )

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if question := st.chat_input("Ask about Community Tech Day"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)

    st.session_state.calculator_used = False

    try:
        response = st.session_state.chat.send_message(question)
        answer = response.text or "No answer returned."

        with st.chat_message("assistant"):
            st.write(answer)
            if st.session_state.calculator_used:
                st.caption("Calculator used for this answer")

        st.session_state.messages.append(
            {"role": "assistant", "content": answer}
        )
    except Exception as error:
        st.error(f"Could not get an answer: {error}")