import os
import json
import boto3
from dotenv import load_dotenv
from pdf_data import pdfContent  # Import content
from question_handler import handle_question, fetch_random_questions  # Logic for questions

# Load environment variables
load_dotenv()

# Initialize AWS Bedrock client
bedrock_runtime = boto3.client(
    'bedrock-runtime', 
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def main():
    print("Welcome to the AWS Cloud Club!")
    print("Type 'exit' or 'quit' to end the conversation.")

    # Store conversation history
    history = []
    conversation_history = []

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Chatbot: Thank you for using the chatbot. Goodbye!")
            break

        # Handle the question
        is_relevant, response = handle_question(
            question, 
            pdfContent, 
            bedrock_runtime, 
            conversation_history
        )
        print("\nChatbot: " + response)

        if not is_relevant:
            # Fetch random suggestions if irrelevant
            suggestions = fetch_random_questions(
                bedrock_runtime, 
                conversation_history
            )
            print("Here are some suggestions you can ask:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")

        # Update history
        history.append({"question": question, "response": response})
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": response})

if __name__ == "__main__":
    main()