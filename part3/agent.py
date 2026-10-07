from getpass import getpass

from google import genai
from google.genai import types
from pypdf import PdfReader


reader = PdfReader("sample_document.pdf")

document_text = ""
for page in reader.pages:
    document_text += (page.extract_text(extraction_mode="layout") or "") + "\n"

document_text = document_text.replace("\ue092", ":")

if not document_text.strip():
    raise ValueError("No readable text found in the PDF.")


def calculate_ticket_total(adults: int, students: int) -> int:
    """Calculate the total cost of adult and student tickets."""
    if adults < 0 or students < 0:
        raise ValueError("Ticket quantities cannot be negative.")

    total = adults * 25 + students * 15
    print(f"[Calculator used] {adults} adult, {students} student = RM{total}")
    return total


instructions = (
    "You are an assistant for Community Tech Day. "
    "Use the document below as your only source for event facts. "
    "If the document does not contain an answer, say that the document does not say. "
    "Remember details the user tells you, such as their name, during this conversation. "
    "Do not invent event information. "
    "For questions asking for a total ticket cost, use calculate_ticket_total. "
    "Do not use the calculator for questions that only ask for facts.\n\n"
    "DOCUMENT:\n" + document_text
)

api_key = getpass("Gemini API key (typing is hidden): ")
client = genai.Client(api_key=api_key)

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=instructions,
        tools=[calculate_ticket_total],
    ),
)

print("\nEvent assistant ready. Type 'exit' to stop.")

while True:
    question = input("\nYou: ").strip()

    if question.lower() in ("exit", "quit"):
        break
    if not question:
        continue

    try:
        response = chat.send_message(question)
        print("Agent:", response.text or "No answer returned.")
    except Exception as error:
        print("Could not get an answer:", error)