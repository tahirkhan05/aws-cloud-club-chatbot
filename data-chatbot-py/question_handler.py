import random
import re

# Function to handle user questions
def handle_question(question, content, chat, history):
    """
    Handles the user's question by verifying its relevance to the provided context.
    Generates a response or suggests random questions if the topic is irrelevant.
    """
    # Combine content for context
    combined_content = " ".join(content.values()).lower()

    # Check relevance
    if is_question_relevant(question, combined_content):
        context = "\n".join(content.values())
        response = generate_response(question, context, chat, history)
        return True, response
    else:
        # Always generate random questions when the question is irrelevant
        suggested_questions = fetch_random_questions(chat, history)
        return False, (
            "I can only assist with AWS Cloud Club-related topics. "
            "Please ask something in that scope.\n" +
            "\n"
        )

# Function to check relevance of a question
def is_question_relevant(question, combined_content):
    """
    Checks if the question is relevant by identifying keywords and comparing them to the content.
    """
    # Extract words from the question
    question_words = re.findall(r'\b\w+\b', question.lower())
    
    # Check if at least one word is present in the content
    for word in question_words:
        if word in combined_content:
            return True

    return False

# Function to generate a response using the Gemini API
def generate_response(question, context, chat, history):
    """
    Generates a response using Gemini API, ensuring it's human-like and adheres to restrictions.
    """
    previous_questions = "\n".join([entry["question"] for entry in history])
    prompt = (
        f"You are a helpful chatbot specialized in AWS Cloud Club topics. "
        f"Provide an informative and human-like response to the user's query.\n\n"
        f"Context:\n{context}\n\n"
        f"Previous Questions:\n{previous_questions}\n\n"
        f"User's Question: {question}"
    )

    response = chat.send_message(prompt)
    
    if "code" in response.text.lower() or "program" in response.text.lower():
        return "Sorry, I cannot provide technical programming details. Please ask about AWS Cloud Club topics."

    return response.text.strip()

# Function to fetch random question suggestions
def fetch_random_questions(chat, history):
    """
    Uses the Gemini API to suggest random AWS Cloud Club-related questions.
    """
    previous_questions = "\n".join([entry["question"] for entry in history])
    prompt = (
        f"Suggest two question which is simple and new user-friendly related to AWS Cloud Club topics regarding goals, milestones, or events. "
        f"Dont give descriptions on what you did.\n\n"
        f"Avoid repeating these:\n{previous_questions}"
    )

    response = chat.send_message(prompt)
    questions = [q.strip() for q in response.text.split("\n") if q.strip()]
    return questions[:2]  # Limit to three suggestions
