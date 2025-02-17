import os
import openai
import json
import re
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load OpenAI API Key from .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Your Amazon Affiliate ID (optional)
AMAZON_AFFILIATE_ID = "YOURAFFILIATEID-20"

def generate_questions(num_questions=10):

    """Generate a list of unique 'Is it legal…?' questions using GPT."""
    prompt = f"Generate {num_questions} unique and interesting 'Is it legal to...' questions in the United States. Focus on weird, obscure, or surprising activities."
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    try:
        questions_json = response["choices"][0]["message"]["content"]
        questions = json.loads(questions_json)
        return questions if isinstance(questions, list) else []
    except:
        return []

def generate_answer_content(question):
    """Generate a structured response for each legal question."""
    prompt = f"""
    Answer the question: '{question}' in a structured way.
    1) Provide a short Yes/No/Depends answer.
    2) Explain relevant laws or regulations in simple terms (2 paragraphs).
    3) Include a disclaimer: 'This is not legal advice. Laws may vary by state.'
    4) Provide a fun fact or trivia about the topic.
    Return in JSON format: short_answer, explanation, disclaimer, trivia.
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    
    try:
        return json.loads(response["choices"][0]["message"]["content"])
    except:
        return {
            "short_answer": "It depends.",
            "explanation": "Unable to generate explanation.",
            "disclaimer": "This is not legal advice.",
            "trivia": ""
        }

def slugify(text):
    """Create a URL-friendly slug from a question."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def main():
    os.makedirs("_questions", exist_ok=True)

    questions = generate_questions(num_questions=10)

    for question in questions:
        data = generate_answer_content(question)

        md_filename = f"_questions/{slugify(question)}.md"

        markdown_content = f"""---
layout: question
title: "{question}"
short_answer: "{data['short_answer']}"
disclaimer: "{data['disclaimer']}"
---

{data['explanation']}

**Trivia:** {data['trivia']}
"""

        with open(md_filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)

    print("✅ AI-generated questions saved in _questions/")

if __name__ == "__main__":
    main()
