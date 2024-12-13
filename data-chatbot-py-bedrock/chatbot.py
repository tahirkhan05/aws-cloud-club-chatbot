import os
from dotenv import load_dotenv
from pdf_data import pdfContent
from question_handler import handle_question, fetch_random_questions
import boto3

# Load environment variables
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Initialize AWS Bedrock client
bedrock_client = boto3.client('bedrock', region_name=AWS_REGION)

def main():
    print("Welcome to the AWS Cloud Club!")
    print("Type 'exit' or 'quit' to end the conversation.")

    # Store conversation history
    history = []

    while True:
        question = input("\nYou: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("Chatbot: Thank you for using the chatbot. Goodbye!")
            break

        # Handle the question
        is_relevant, response = handle_question(question, pdfContent, bedrock_client, history)
        print("\nChatbot: " + response)

        if not is_relevant:
            # Fetch random suggestions if irrelevant
            suggestions = fetch_random_questions(bedrock_client, history)
            print("Here are some suggestions you can ask:")
            for i, suggestion in enumerate(suggestions, 1):
                print(f"{i}. {suggestion}")

        # Update history
        history.append({"question": question, "response": response})

if __name__ == "__main__":
    main()