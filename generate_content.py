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

def generate_seo_friendly_questions(batch_size=5):
    """
    Generate a batch of hyper-targeted, SEO-optimized 'Is it legal to ...' questions.
    Each question should:
      - Be highly specific with both a legal concern and a hyper-local reference (e.g., city, county, region).
      - Use long-tail keywords known for high search volume.
      - Address trending or evergreen legal topics.
    
    Expected JSON output format:
    [
      {"question": "Is it legal to ride an e-scooter without a license in downtown Los Angeles?"},
      {"question": "Is it legal to operate a drone without registration in central London?"},
      ...
    ]
    """
    # Choose a random region and then specify a location within it.
    TARGET_REGIONS = {
        "USA": ["Los Angeles", "New York", "Chicago", "Houston"],
        "UK": ["London", "Manchester", "Birmingham", "Glasgow"],
        "Canada": ["Toronto", "Vancouver", "Montreal", "Calgary"],
        "Australia": ["Sydney", "Melbourne", "Brisbane", "Perth"],
        "Germany": ["Berlin", "Munich", "Frankfurt", "Hamburg"],
        "France": ["Paris", "Lyon", "Marseille", "Nice"],
        "India": ["Mumbai", "Delhi", "Bangalore", "Chennai"]
    }
    region = random.choice(list(TARGET_REGIONS.keys()))
    location = random.choice(TARGET_REGIONS[region])
    
    prompt = (
        f"Generate {batch_size} highly SEO-optimized 'Is it legal to ...' questions that target high search volume keywords globally. "
        f"Each question should include a specific legal concern (such as driving without insurance, operating without a license, "
        f"or using unregistered vehicles) and incorporate a hyper-local reference by mentioning a specific city or region, for example '{location}' in {region}. "
        "The questions should use actionable verbs and long-tail keywords that align with high search volume queries. "
        "Make sure each question is unique, compelling, and designed to attract significant organic traffic for global audiences. "
        "Return the output in a valid JSON array exactly in this format: "
        '[{"question": "Is it legal to ride an e-scooter without a license in downtown Los Angeles?"}, '
        '{"question": "Is it legal to operate a drone without registration in central London?"}]'
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert SEO strategist and legal content creator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        
        questions_json = response.choices[0].message.content.strip()
        data = json.loads(questions_json)
        if isinstance(data, list) and all("question" in item for item in data):
            print(f"Generated a batch of {len(data)} questions targeting {location}, {region}.")
            return [item["question"].strip() for item in data]
        else:
            print("❌ JSON output did not match expected format.")
            return []
    except (json.JSONDecodeError, IndexError, AttributeError) as e:
        print("❌ Failed to generate or parse questions:", e)
        return []

def generate_answer_content(question, max_retries=3):
    """
    Generate a detailed and structured answer for a legal question.
    The JSON response includes:
      - "short_answer": A concise answer (Yes/No/Depends).
      - "explanation": Two paragraphs explaining the legal background.
      - "disclaimer": A disclaimer note.
      - "trivia": A fun fact related to the topic.
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
    os.makedirs("_questions", exist_ok=True)
    existing_files = set(os.listdir("_questions"))
    
    target_entries = 5000
    unique_count = 0
    max_batches = target_entries // 5 + 10  # extra batches in case some questions are duplicates

    for batch_num in range(max_batches):
        print(f"\nProcessing batch {batch_num + 1}")
        questions = generate_seo_friendly_questions(batch_size=5)
        if not questions:
            print("⚠️ No questions generated in this batch, retrying next batch...")
            continue

        for question in questions:
            md_filename = f"{slugify(question)}.md"
            # If the file exists, we consider it already processed
            if md_filename in existing_files:
                print(f"⚠️ Duplicate file detected for question: {question}")
                continue

            # Generate answer content for the question
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
            existing_files.add(md_filename)
            unique_count += 1
            print(f"✅ Saved: {question}")

            if unique_count >= target_entries:
                break
        if unique_count >= target_entries:
            break
        time.sleep(1)

    print(f"Finished with {unique_count} unique entries.")

if __name__ == "__main__":
    main()
