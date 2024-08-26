import json
import os
from urllib.parse import urlparse
from sentence_transformers import SentenceTransformer, util
import google.generativeai as genai
from dotenv import load_dotenv
from transformers import pipeline
import numpy as np
import spacy
import numpy as np
from sklearn.metrics import precision_score, recall_score, f1_score
import time

def is_webpage_url(url: str) -> bool:
    parsed_url = urlparse(url)

    if parsed_url.fragment:
        return False

    file_extensions = (
        '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
        '.jpg', '.jpeg', '.png', '.gif', '.svg', '.bmp', '.tiff', 
        '.zip', '.rar', '.7z', '.tar', '.gz', '.mp3', '.mp4', '.avi', 
        '.mov', '.mkv', '.wmv', '.exe', '.dmg', '.iso', '.apk'
    )

    if any(parsed_url.path.lower().endswith(ext) for ext in file_extensions):
        return False

    return True

# Load environment variables
load_dotenv()
api_key = os.getenv("API_KEY")
genai.configure(api_key=api_key)

# Load content from JSON file
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

# Generate questions using Generative AI model
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

# Initialize SentenceTransformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Find relevant links based on content similarity
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

# Extract topics from content
def extract_topics(content):
    keywords = [word for word in content.split() if word.isalpha()][:5]  
    return keywords

# Save questions and related data to JSON file
def save_questions_to_json(data, filename='questions_with_content.json'):
    try:
        mode = 'a' if os.path.exists(filename) else 'w'
        with open(filename, mode, encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.write('\n')
        print(f"Successfully saved data for {data['url']} to {filename}")
    except Exception as e:
        print(f"Error saving data for {data['url']}: {str(e)}")

# Verify the generated questions and links
def verify_data(data):
    num_questions = len(data['questions'])
    questions_length_valid = all(len(q) <= 80 for q in data['questions'])
    num_links = len(data['relevant_links'])
    num_topics = len(data['topics'])

    if num_questions == 10 and questions_length_valid and num_links == 5 and num_topics == 5:
        return True
    else:
        print(f"Verification failed for {data['url']}:")
        print(f"Number of questions: {num_questions} (Expected: 10)")
        print(f"All questions under 80 characters: {questions_length_valid}")
        print(f"Number of relevant links: {num_links} (Expected: 5)")
        print(f"Number of topics: {num_topics} (Expected: 5)")
        return False

# Evaluate the relevance of generated questions
def evaluate_question_relevance(generated_questions, content):
    content_embedding = model.encode(content, convert_to_tensor=True)
    relevance_scores = []
    for question in generated_questions:
        question_embedding = model.encode(question, convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(content_embedding, question_embedding).item()
        relevance_scores.append(similarity)
    
    avg_relevance = sum(relevance_scores) / len(relevance_scores) if relevance_scores else 0
    return avg_relevance


def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spaCy model...")
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def evaluate_link_relevance(content, predicted_links, scraped_content_dict):
    content_doc = nlp(content[:1000000])  # Limit to first 1M characters to avoid memory issues
    
    relevance_scores = []
    
    for link in predicted_links:
        link_content = scraped_content_dict.get(link, "")
        link_doc = nlp(link_content[:1000000])  # Limit to first 1M characters
        
        similarity = content_doc.similarity(link_doc)
        relevance_scores.append(similarity)
    
    # Normalize scores
    total_score = sum(relevance_scores)
    normalized_scores = [score / total_score if total_score > 0 else 0 for score in relevance_scores]
    
    # Calculate a weighted relevance score
    weighted_relevance = sum(score * (1 / (i + 1)) for i, score in enumerate(normalized_scores))
    
    return weighted_relevance


def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spaCy model...")
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()

def evaluate_link_relevance(content, predicted_links, scraped_content_dict):
    content_doc = nlp(content[:100000])  # Limit to first 1M characters to avoid memory issues
    
    relevance_scores = []
    
    for link in predicted_links:
        link_content = scraped_content_dict.get(link, "")
        link_doc = nlp(link_content[:100000])  # Limit to first 1M characters
        
        similarity = content_doc.similarity(link_doc)
        relevance_scores.append(similarity)
    
    # Normalize scores
    total_score = sum(relevance_scores)
    normalized_scores = [score / total_score if total_score > 0 else 0 for score in relevance_scores]
    
    # Calculate a weighted relevance score
    weighted_relevance = sum(score * (1 / (i + 1)) for i, score in enumerate(normalized_scores))
    
    return weighted_relevance

# Update the process_content_for_questions function
def process_content_for_questions(content_list, scraped_content_dict, num_urls=5):
    links = list(scraped_content_dict.keys())

    for entry in content_list[:num_urls]:
        try:
            content = entry['content']
            url = entry['url']
            
            print(f"Processing {url}")

            # Truncate content to the first 512 tokens
            truncated_content = ' '.join(content.split()[:512])
            
            questions = generate_questions(truncated_content)
            print(f"Generated {len(questions)} questions for {url}")
            
            relevant_links = find_relevant_links(truncated_content, links, scraped_content_dict)
            print(f"Found {len(relevant_links)} relevant links for {url}")
            
            topics = extract_topics(truncated_content)
            print(f"Extracted {len(topics)} topics for {url}")
            
            question_relevance = evaluate_question_relevance(questions, truncated_content)
            link_relevance = evaluate_link_relevance(truncated_content, relevant_links, scraped_content_dict)
            print("Sleeping for 10 sec to avoid rate limit.")
            time.sleep(10)
            
            data = {
                "url": url,
                "content": truncated_content[:500],  
                "questions": questions,
                "relevant_links": relevant_links,
                "topics": topics,
                "question_relevance_score": question_relevance,
                "link_relevance_score": link_relevance
            }
            
            if verify_data(data):
                save_questions_to_json(data)
            else:
                print(f"Skipping saving data for {url} due to verification failure.")
        except Exception as e:
            print(f"Error processing {url}: {str(e)}")
# Main function to execute the process
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
