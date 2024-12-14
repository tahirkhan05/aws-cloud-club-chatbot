import random
import re
import json

# Function to handle user questions
def handle_question(question, content, bedrock_client, conversation_history):
    """
    Handles the user's question by verifying its relevance to the provided context.
    Generates a response or suggests random questions if the topic is irrelevant.
    """
    # Combine content for context
    combined_content = " ".join(content.values()).lower()

    # Check relevance
    if is_question_relevant(question, combined_content):
        context = "\n".join(content.values())
        response = generate_response(
            question, 
            context, 
            bedrock_client, 
            conversation_history
        )
        return True, response
    else:
        # Always generate random questions when the question is irrelevant
        suggested_questions = fetch_random_questions(
            bedrock_client, 
            conversation_history
        )
        return False, (
            "I can only assist with AWS Cloud Club-related topics. "
            "Please ask something in that scope.\n"
        )

# Function to check relevance of a question (remains the same)
def is_question_relevant(question, combined_content):
    question_words = re.findall(r'\b\w+\b', question.lower())
    for word in question_words:
        if word in combined_content:
            return True
    return False

# Function to generate a response using Bedrock
def generate_response(question, context, bedrock_client, conversation_history):
    """
    Generates a response using Anthropic Claude 3 Haiku model
    """
    # Prepare messages for the API call
    messages = conversation_history + [
        {
            "role": "user", 
            "content": (
                f"You are a helpful chatbot specialized in AWS Cloud Club topics. "
                f"Provide an informative and human-like response to the user's query.\n\n"
                f"Context:\n{context}\n\n"
                f"User's Question: {question}"
            )
        }
    ]

    # Prepare the request payload
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "messages": messages
    })

    # Make the API call
    try:
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            contentType="application/json",
            accept="application/json",
            body=body
        )

        # Parse the response
        response_body = json.loads(response['body'].read())
        generated_text = response_body['content'][0]['text']

        # Additional filtering
        if "code" in generated_text.lower() or "program" in generated_text.lower():
            return "Sorry, I cannot provide technical programming details. Please ask about AWS Cloud Club topics."

        return generated_text.strip()

    except Exception as e:
        return f"An error occurred: {str(e)}"

# Function to fetch random question suggestions
def fetch_random_questions(bedrock_client, conversation_history):
    """
    Uses Anthropic Claude 3 Haiku to suggest random AWS Cloud Club-related questions
    """
    # Prepare messages for the API call
    messages = conversation_history + [
        {
            "role": "user", 
            "content": (
                "Suggest two simple, new user-friendly questions related to AWS Cloud Club topics "
                "regarding goals, milestones, or events. "
                "Provide only the questions, no additional explanation."
            )
        }
    ]

    # Prepare the request payload
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": messages
    })

    # Make the API call
    try:
        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            contentType="application/json",
            accept="application/json",
            body=body
        )

        # Parse the response
        response_body = json.loads(response['body'].read())
        generated_text = response_body['content'][0]['text']

        # Split and clean questions
        questions = [q.strip() for q in generated_text.split("\n") if q.strip()]
        return questions[:2]  # Limit to two suggestions

    except Exception as e:
        return ["What are the goals of AWS Cloud Club?", "What events are planned?"]