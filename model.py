from transformers import pipeline
from sentence_transformers import SentenceTransformer, util
import json

def load_content(filename='webpage_content.json'):
    with open(filename, 'r') as f:
        content_list = [json.loads(line) for line in f]
    return content_list

def generate_questions(content):
    question_generator = pipeline("text2text-generation", model="t5-base")
    questions = []
    
    prompt = f"Generate questions: {content[:500]}" 
    generated_questions = question_generator(prompt, max_length=80, num_beams=10, num_return_sequences=10)
    
    for q in generated_questions:
        questions.append(q['generated_text'].strip())
    
    return questions

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
    if len(data['questions']) == 10 and all(len(q) <= 80 for q in data['questions']):
        with open(filename, 'a') as f:
            json.dump(data, f, indent=4) 
            f.write('\n')
    else:
        print(f"Validation failed for {data['url']}: Questions={len(data['questions'])}, Max Length={max(len(q) for q in data['questions']) if data['questions'] else 'N/A'}")

def process_content_for_questions(content_list, scraped_content_dict, num_urls=5):
    links = list(scraped_content_dict.keys())

    for entry in content_list[:num_urls]:
        content = entry['content']
        url = entry['url']
        
        questions = generate_questions(content)
        relevant_links = find_relevant_links(content, links, scraped_content_dict)
        topics = extract_topics(content)
        
        data = {
            "url": url,
            "content": content[:500],  
            "questions": questions,
            "relevant_links": relevant_links,
            "topics": topics
        }
        
        print(f"Generated data for {url}: {data}")  
        save_questions_to_json(data)
        print(f"Saved data for {url}")

if __name__ == "__main__":
    content_list = load_content()

    scraped_content_dict = {entry['url']: entry['content'] for entry in content_list}
    
    process_content_for_questions(content_list, scraped_content_dict, num_urls=5)
