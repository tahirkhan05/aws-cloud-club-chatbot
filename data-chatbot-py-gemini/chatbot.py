import os
from dotenv import load_dotenv
from pdf_data import pdfContent  # Import content
from question_handler import handle_question, fetch_random_questions  # Logic for questions
import google.generativeai as genai  # Gemini API

# Load API key from environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=API_KEY)

def main():
    print("Welcome to the AWS Cloud Club!")
    print("Type 'exit' or 'quit' to end the conversation.")

    # Initialize a chat instance with Gemini
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    chat = model.start_chat(history=[])

    # Store conversation history
    history = []

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Chatbot: Thank you for using the chatbot. Goodbye!")
            break

        # Handle the question
        is_relevant, response = handle_question(question, pdfContent, chat, history)
        print("\nChatbot: " + response)

        if not is_relevant:
            # Fetch random suggestions if irrelevant
            suggestions = fetch_random_questions(chat, history)
            print("Here are some suggestions you can ask:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")

        # Update history
        history.append({"question": question, "response": response})

if __name__ == "__main__":
    main()