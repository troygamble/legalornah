import os
import openai
import json
import re
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# (Optional) Your Amazon Affiliate ID
AMAZON_AFFILIATE_ID = "YOURAFFILIATEID-20"

def get_seo_friendly_questions(num_questions=10):
    """
    Generate a list of highly searched, SEO-friendly 'Is it legal to ...' questions in the United States.
    The focus is on maximizing organic search traffic by using common Google search queries.
    """
    prompt = (
        f"Generate {num_questions} SEO-optimized 'Is it legal to ...' questions that people frequently search for on Google in the United States. "
        "Use specific state names and common activities to make them more relevant. "
        "Ensure the questions are highly searched legal concerns. "
        "Return your output as a JSON list, for example: [\"Is it legal to drive barefoot in Texas?\", \"Is it legal to own a raccoon in Florida?\", ...]."
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an SEO and legal expert. Generate legal questions that match high search volume queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        questions_json = response.choices[0].message.content
        questions = json.loads(questions_json)
        return list(set(questions)) if isinstance(questions, list) else []  # Remove duplicates
    except (json.JSONDecodeError, IndexError, AttributeError) as e:
        print("Failed to parse JSON response for questions:", e)
        return []

def generate_answer_content(question, max_retries=3):
    """
    Generate a structured response for a legal question.
    Returns a JSON object with keys: short_answer, explanation, disclaimer, trivia.
    Retries up to max_retries times in case of an empty response.
    """
    prompt = f"""
Answer the question: '{question}' in a structured way.
1) Provide a short Yes/No/Depends answer.
2) Explain relevant laws or regulations in simple terms (2 paragraphs).
3) Include a disclaimer: 'This is not legal advice. Laws may vary by state.'
4) Provide a fun fact or trivia about the topic.
Return your response in valid JSON format with the keys: "short_answer", "explanation", "disclaimer", and "trivia".
"""

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal expert assistant. Always return responses in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )

            # Debug: Print the raw response
            print(f"🔍 Attempt {attempt + 1}: Raw OpenAI Response:", response)

            # Extract the response content
            content = response.choices[0].message.content.strip()

            # Handle empty response case
            if not content:
                print(f"⚠️ Warning: OpenAI returned an empty response on attempt {attempt + 1}!")
                time.sleep(2)  # Wait before retrying
                continue  # Retry the request

            # Attempt to parse the JSON response
            return json.loads(content)

        except (json.JSONDecodeError, IndexError, AttributeError) as e:
            print(f"❌ Failed to parse JSON response on attempt {attempt + 1}: {e}")
            print("Response Content:", content if 'content' in locals() else "No content received.")
            time.sleep(2)  # Wait before retrying

    # If all retries fail, return a default response
    print("🚨 Max retries reached. Returning a default response.")
    return {
        "short_answer": "It depends.",
        "explanation": "Unable to generate explanation.",
        "disclaimer": "This is not legal advice.",
        "trivia": ""
    }

def slugify(text):
    """Create a URL-friendly slug from the given text."""
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

def main():
    os.makedirs("_questions", exist_ok=True)
    existing_files = set(os.listdir("_questions"))  # Track existing files

    questions = get_seo_friendly_questions(num_questions=10)
    if not questions:
        print("No questions were generated. Exiting.")
        return

    for question in questions:
        md_filename = f"{slugify(question)}.md"
        if md_filename in existing_files:
            print(f"⚠️ Skipping duplicate question: {question}")
            continue  # Skip duplicates

        data = generate_answer_content(question)
        markdown_content = f"""---
layout: question
title: "{question}"
short_answer: "{data.get('short_answer', '')}"
disclaimer: "{data.get('disclaimer', '')}"
---

{data.get('explanation', '')}

**Trivia:** {data.get('trivia', '')}
"""
        with open(f"_questions/{md_filename}", "w", encoding="utf-8") as f:
            f.write(markdown_content)

        print(f"✅ Saved: {question}")

if __name__ == "__main__":
    main()
