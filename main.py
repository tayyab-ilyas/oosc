import requests
from bs4 import BeautifulSoup
import re
import json
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, urljoin

def scrape_website(url, max_depth, current_depth=0, visited=None):
    if visited is None:
        visited = set()
    
    if current_depth > max_depth or url in visited:
        return []

    visited.add(url)
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
        hostname = urlparse(url).hostname
        valid_links = []
        
        for link in links:
            if link.startswith('http'):
                if urlparse(link).hostname == hostname:
                    valid_links.append(link)
            else:
                valid_links.append(urljoin(url, link))
        
        # Process the current page
        process_link(url)
        
        # Recursively scrape valid links
        for link in valid_links:
            if link not in visited:
                valid_links.extend(scrape_website(link, max_depth, current_depth + 1, visited))
        
        return valid_links
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

def save_links(links, filename='links.json'):
    with open(filename, 'w') as f:
        json.dump(links, f)

def save_links_csv(links, filename='links.csv'):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['URL'])
        for link in links:
            writer.writerow([link])

def get_webpage_content(url):
    try:
        headers = {'Accept-Encoding': 'identity'} 
        response = requests.get(url, headers=headers)
        response.raise_for_status()  
        
        return response.text
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None

def clean_text(content):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()
    text = re.sub(r'\s+', ' ', text)
    
    # Remove non-ASCII characters and most special characters
    text = re.sub(r'[^\x20-\x7E]+', '', text)
    
    return text.strip()

def save_content_to_json(data, filename='webpage_content.json'):
    with open(filename, 'a', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
        f.write('\n')  # Write each JSON object on a new line

def format_json_file(filename='webpage_content.json'):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Remove any trailing commas and newlines
    lines = [line.strip().rstrip(',') for line in lines if line.strip()]

    # Wrap the content in square brackets to make it a valid JSON array
    formatted_content = '[\n' + ',\n'.join(lines) + '\n]'

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(formatted_content)

    print(f"Formatted {filename} as a valid JSON array")

def process_link(link):
    content = get_webpage_content(link)
   
    if content:
        cleaned_content = clean_text(content)
        data = {
            "url": link,
            "content": cleaned_content
        }
        save_content_to_json(data)
        print(f"Processed and saved content from {link}")
    else:
        print(f"Failed to process {link}")

def process_website(url, max_depth):
    # Clear the content file before starting
    open('webpage_content.json', 'w').close()

    links = scrape_website(url, max_depth)
    
    save_links(links)
    save_links_csv(links)

    # Format the JSON file after all content has been saved
    format_json_file()

if __name__ == "__main__":
    process_website('https://rajuljha.github.io', max_depth=6)