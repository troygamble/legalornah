import os
import openai
import json
import re
import time
import random
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

# (Optional) Your Amazon Affiliate ID
AMAZON_AFFILIATE_ID = "YOURAFFILIATEID-20"

# List of regions to target for global SEO.
TARGET_REGIONS = ["USA", "UK", "Canada", "Australia", "Germany", "France", "India"]

def generate_seo_friendly_question():
    """
    Generate one SEO-optimized 'Is it legal to ...' question.
    The question should be highly specific, include a regional reference (state, province, or country),
    and target a high search volume query.
    
    Expected JSON output:
    {"question": "Is it legal to drive without insurance in Texas?"}
    """
    # Randomly choose a target region
    region = random.choice(TARGET_REGIONS)
    prompt = (
        f"Generate 1 highly SEO-optimized 'Is it legal to ...' question that has a high search volume on Google for {region}. "
        "The question should mention a specific state, province, or region name and a common activity or legal concern. "
        "Ensure it is unique, clear, and directly answerable. "
        "Return the output in valid JSON format exactly like: "
        "{\"question\": \"Is it legal to drive without insurance in Texas?\"}"
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an SEO and legal content expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        # Extract and parse the JSON response
        questions_json = response.choices[0].message.content.strip()
        data = json.loads(questions_json)
        question = data.get("question", "").strip()
        if question:
            print(f"Generated question for {region}: {question}")
            return question
        else:
            print("❌ No question found in the API response.")
            return None
    except (json.JSONDecodeError, IndexError, AttributeError) as e:
        print("❌ Failed to generate or parse question:", e)
        return None

def generate_answer_content(question, max_retries=3):
    """
    Generate a detailed and structured answer for a legal question.
    The JSON response should include:
      - "short_answer": A concise answer (Yes/No/Depends).
      - "explanation": Two paragraphs explaining the legal background.
      - "disclaimer": A disclaimer note.
      - "trivia": A fun fact related to the topic.
    
    Returns the JSON as a Python dict.
    """
    prompt = f"""
Answer the following legal question in a clear, concise, and structured manner:
"{question}"

Instructions:
1. Provide a brief answer (Yes/No/Depends) as "short_answer".
2. Write two well-structured paragraphs explaining the relevant laws or regulations in simple terms as "explanation".
3. Include a disclaimer that says: "This is not legal advice. Laws may vary by region." as "disclaimer".
4. Provide an interesting trivia or fun fact related to the topic as "trivia".

Return your answer in valid JSON format with the keys exactly as: "short_answer", "explanation", "disclaimer", and "trivia".
"""
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "system", "content": "You are a legal expert assistant who provides clear, accurate, and structured answers in JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )

            # Debug: Log the raw response for troubleshooting
            print(f"🔍 Answer Attempt {attempt + 1}: Raw API Response:", response)

            content = response.choices[0].message.content.strip()

            if not content:
                print(f"⚠️ Warning: Empty response on attempt {attempt + 1}. Retrying...")
                time.sleep(2)
                continue

            return json.loads(content)

        except (json.JSONDecodeError, IndexError, AttributeError) as e:
            print(f"❌ Failed to parse JSON response on attempt {attempt + 1}: {e}")
            print("Response Content:", content if 'content' in locals() else "No content received.")
            time.sleep(2)

    print("🚨 Max retries reached. Returning a default answer response.")
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
    # Create the output directory if it doesn't exist
    os.makedirs("_questions", exist_ok=True)
    existing_files = set(os.listdir("_questions"))  # To prevent duplicates

    # Set the desired number of iterations (each iteration creates one page)
    target_entries = 10
    iterations = 0

    while iterations < target_entries:
        print(f"\nIteration {iterations + 1} of {target_entries}")

        # Generate a new SEO-friendly question
        question = generate_seo_friendly_question()
        if not question:
            print("⚠️ No question generated, retrying this iteration...")
            continue  # Skip this iteration if question generation failed

        md_filename = f"{slugify(question)}.md"
        if md_filename in existing_files:
            print(f"⚠️ Duplicate question detected, skipping: {question}")
            iterations += 1  # Count iteration even if duplicate to avoid an infinite loop
            continue

        # Generate the answer content for the question
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
        # Save the generated content as a markdown file
        with open(f"_questions/{md_filename}", "w", encoding="utf-8") as f:
            f.write(markdown_content)
        existing_files.add(md_filename)
        print(f"✅ Saved: {question}")

        iterations += 1
        # Optional pause to avoid hitting rate limits
        time.sleep(1)

if __name__ == "__main__":
    main()
