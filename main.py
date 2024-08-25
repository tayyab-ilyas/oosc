import requests
from bs4 import BeautifulSoup
import re
import json
import csv

def scrape_website(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        links = [a.get('href') for a in soup.find_all('a', href=True)]
        
       
        valid_links = [link for link in links if link.startswith('http')]
        
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
    return text.strip()

def save_content_to_json(data, filename='webpage_content.json'):
    with open(filename, 'a') as f:
        json.dump(data, f)
        f.write('\n')

def process_website(url):
    links = scrape_website(url)
    
    save_links(links)
    save_links_csv(links)
    
    for link in links:
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

if __name__ == "__main__":
    process_website('https://amu.ac.in')
