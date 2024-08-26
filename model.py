import json
import os
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

def load_content(filename='webpage_content.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        try:
            content_list = json.load(f)
            print(f"Successfully loaded {len(content_list)} items from {filename}")
            return content_list
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            print("Attempting to read file line by line...")
            f.seek(0)  # Reset file pointer to the beginning
            content_list = []
            for line_number, line in enumerate(f, 1):
                try:
                    content = json.loads(line.strip())
                    content_list.append(content)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON on line {line_number}: {e}")
                    print(f"Problematic line: {line[:100]}...")  
            
            print(f"Successfully loaded {len(content_list)} items from {filename}")
            return content_list

def generate_questions(content):
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    Generate 10 relevant questions from the following content:
    
    {content}

    Please ensure the questions are clear, concise, and relevant to the content provided.
    """
    
    response = model.generate_content(prompt)
    questions = response.text.strip().split('\n')
    return [question.strip() for question in questions if question.strip()]

model = SentenceTransformer('all-MiniLM-L6-v2')

def find_relevant_links(content, links, scraped_content_dict):
    content_embedding = model.encode(content, convert_to_tensor=True)
    relevant_links = []

    for link in links:
        linked_content = scraped_content_dict.get(link)
        if linked_content:
            link_embedding = model.encode(linked_content, convert_to_tensor=True)
            similarity = util.pytorch_cos_sim(content_embedding, link_embedding).item()
            relevant_links.append((link, similarity))

    relevant_links.sort(key=lambda x: x[1], reverse=True)
    return [link for link, sim in relevant_links[:5]]

def extract_topics(content):
    keywords = [word for word in content.split() if word.isalpha()][:5]  
    return keywords

def save_questions_to_json(data, filename='questions_with_content.json'):
    try:
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(filename, mode, encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.write('\n')
        print(f"Successfully saved data for {data['url']} to {filename}")
    except Exception as e:
        print(f"Error saving data for {data['url']}: {str(e)}")


def process_content_for_questions(content_list, scraped_content_dict, num_urls=5):
    links = list(scraped_content_dict.keys())

    for entry in content_list[:num_urls]:
        try:
            content = entry['content']
            url = entry['url']
            
            print(f"Processing {url}")
            
            questions = generate_questions(content)
            print(f"Generated {len(questions)} questions for {url}")
            
            relevant_links = find_relevant_links(content, links, scraped_content_dict)
            print(f"Found {len(relevant_links)} relevant links for {url}")
            
            topics = extract_topics(content)
            print(f"Extracted {len(topics)} topics for {url}")
            
            data = {
                "url": url,
                "content": content[:500],  
                "questions": questions,
                "relevant_links": relevant_links,
                "topics": topics
            }
            
            save_questions_to_json(data)
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")

if __name__ == "__main__":
    try:
        content_list = load_content()
        print(f"Loaded {len(content_list)} content entries")

        if not content_list:
            print("Error: No content loaded. Check your input file.")
        else:
            scraped_content_dict = {entry['url']: entry['content'] for entry in content_list}
            print(f"Created scraped_content_dict with {len(scraped_content_dict)} entries")

            process_content_for_questions(content_list, scraped_content_dict, num_urls=5)
            
            if os.path.exists('questions_with_content.json'):
                print(f"Output file 'questions_with_content.json' has been created and its size is {os.path.getsize('questions_with_content.json')} bytes")
            else:
                print("Output file 'questions_with_content.json' was not created")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
