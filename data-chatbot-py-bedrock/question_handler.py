import random
import re

def handle_question(question, content, bedrock_client, history):
    """
    Handles the user's question by verifying its relevance to the provided context.
    Generates a response or suggests random questions if the topic is irrelevant.
    """
    combined_content = " ".join(content.values()).lower()

    if is_question_relevant(question, combined_content):
        context = "\n".join(content.values())
        response = generate_response(question, context, bedrock_client, history)
        return True, response
    else:
        suggested_questions = fetch_random_questions(bedrock_client, history)
        return False, (
            "I can only assist with AWS Cloud Club-related topics. "
            "Please ask something in that scope.\n"
        )

def is_question_relevant(question, combined_content):
    """
    Checks if the question is relevant by identifying keywords and comparing them to the content.
    """
    question_words = re.findall(r'\b\w+\b', question.lower())
    for word in question_words:
        if word in combined_content:
            return True
    return False

def generate_response(question, context, bedrock_client, history):
    """
    Generates a response using AWS Bedrock API.
    """
    previous_questions = "\n".join([entry["question"] for entry in history])
    prompt = (
        f"You are a helpful chatbot specialized in AWS Cloud Club topics. "
        f"Provide an informative and human-like response to the user's query.\n\n"
        f"Context:\n{context}\n\n"
        f"Previous Questions:\n{previous_questions}\n\n"
        f"User's Question: {question}"
    )

    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-v1",
        contentType="text/plain",
        accept="text/plain",
        body=prompt
    )

    response_text = response['body'].read().decode('utf-8')
    return response_text.strip()

def fetch_random_questions(bedrock_client, history):
    """
    Uses AWS Bedrock to suggest random AWS Cloud Club-related questions.
    """
    previous_questions = "\n".join([entry["question"] for entry in history])
    prompt = (
        f"Suggest two questions which are simple and new user-friendly related to AWS Cloud Club topics. "
        f"Avoid repeating these:\n{previous_questions}"
    )

    response = bedrock_client.invoke_model(
        modelId="anthropic.claude-v1",
        contentType="text/plain",
        accept="text/plain",
        body=prompt
    )

    response_text = response['body'].read().decode('utf-8')
    questions = [q.strip() for q in response_text.split("\n") if q.strip()]
    return questions[:2]
