import random
import re

def handle_question(question, content, chat, history):
    """
    Handles the user question by checking its relevance to the provided content
    and querying Gemini for relevant responses.
    """
    # Combine all content into a single string for context
    combined_content = " ".join(content.values())

    # Check if the question can be answered based on the content
    if is_question_relevant(question, combined_content):
        # If relevant, send context to Gemini for response generation
        context = "\n".join(content.values())
        previous_questions = "\n".join([h["question"] for h in history])
        response = chat.send_message(
            f"Context: {context}\n\nPrevious Questions:\n{previous_questions}\n\nUser 's Question: {question}"
        )
        # Ensure no programming-related responses
        if "code" in response.text.lower() or "program" in response.text.lower():
            suggestions = fetch_random_questions(chat, history)  # Fetch suggestions
            return True, "Sorry, I cannot provide this response. Here are some questions you might consider asking:\n" + "\n".join(suggestions)
        return True, response.text
    else:
        # If irrelevant, prepare a response to indicate irrelevance
        return False, (
            "Your question seems to be unrelated to the AWS Cloud Club or its topics.\n"
            "This chatbot is dedicated to AWS Cloud Club-related information."
        )

def is_question_relevant(question, combined_content):
    """
    Determine if the question is relevant to the provided content.
    This can be done by checking if key concepts from the question are present
    in the content.
    """
    # Clean and prepare the question for comparison
    question_words = re.findall(r'\b\w+\b', question.lower())

    # Check for the presence of significant words from the question in the combined content
    for word in question_words:
        if word in combined_content.lower():
            return True

    # If no relevant words are found, return False
    return False

def fetch_random_questions(chat, history):
    """
    Uses the Gemini API to fetch random relevant suggestions related to AWS Cloud Club.
    """
    previous_questions = "\n".join([h["question"] for h in history])
    prompt = (
        f"Generate three simple and user-friendly questions about AWS Cloud Club, excluding these:\n{previous_questions}.\n"
        "Focus on topics like overview, goals, and milestones."
    )
    response = chat.send_message(prompt)
    questions = [q.strip() for q in response.text.split("\n") if q.strip()]  # Clean and split lines
    return questions[:2]  # Limit to 2 suggestions