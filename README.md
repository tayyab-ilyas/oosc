# QuesGen
This project was developed by **Team ByteClub** during the **OOSC 2024 Hackathon at IIT Kanpur**.

## About the Project
This project develops a system to automatically generate relevant questions from website content. The system scrapes links from a given website, retrieves the content, and creates concise questions related to each webpage. It also selects relevant links from the website and ensures each entry is validated for quality and accuracy. The results are saved in a structured JSON file for easy access and analysis.

![QuesGen](/static/QuesGen.png)

## Technologies Used

- Python
- Pytorch
- BeatifulSoup
- Google Gemini
- Sentence-Transformer
- Bert Transformer


## Getting Started
### Setting up on your local machine 
To set up the project on a local system, follow these steps:
 1. Clone the repository:
```bash
 git clone https://github.com/tayyab-ilyas/quesgen.git
```
 2. Obtain an API key:
 Visit [this link](https://aistudio.google.com/app/apikey) to get an API key. Set it up in a `.env` file and in `model.py`:
```python
  api_key = os.getenv("API_KEY")
  genai.configure(api_key=api_key)
 ```
 4. Install all dependencies:
```bash
 pip install -r requirements.txt
```
   4. **Navigate to the `main.py` file** in the repository and replace the example URL: 
```python
 if __name__ == "__main__":
 process_website('https://rajuljha.github.io/',  max_depth=6)
``` 
  5. Run the command to scrape the URL:
```bash
 python3 main.py  
```
  6.  **A file named `webpage_content.json` will be created.** in the following format:
```json 
 [
{"url": "https://rajuljha.github.io", "content": "The Knight Blog The Knight BlogAbout Contacttwitter github instagram linkedinRajul JhaSoftware DeveloperGSoC 2024 Final Project ReportAug 24, 2024 GSoC 2024 Final Project ReportFirst phase of GSoCJul 5, 2024 First phase of GSoCThe Night of My GSoC ResultMay 2, 2024 The Night of My GSoC ResultNext Page  2024 The Knight BlogPowered by Hugo  Paper"},
{"url": "https://rajuljha.github.io/", "content": "The Knight Blog The Knight BlogAbout Contacttwitter github instagram linkedinRajul JhaSoftware DeveloperGSoC 2024 Final Project ReportAug 24, 2024 GSoC 2024 Final Project ReportFirst phase of GSoCJul 5, 2024 First phase of GSoCThe Night of My GSoC ResultMay 2, 2024 The Night of My GSoC ResultNext Page  2024 The Knight BlogPowered by Hugo  Paper"},
{"url": "https://rajuljha.github.io/about/", "content": "About Me - The Knight Blog The Knight BlogAbout Contacttwitter github instagram linkedinAbout MeHi I am Rajulaka (@rajuljha)Backend Developer | Open Source EnthusiastI am a passionate backend developer from India. Im currently studying Computer Engineering at Aligarh Muslim University. My love for technology and innovation drives me to constantly learn and create, especially in the realm of open source software.Current EndeavorsGSoC 24 with FOSSology: Im thrilled to have been selected for Google Summer of Code 2024 with FOSSology. My project focuses on integrating FOSSology scanners into CI pipelines, enhancing the software compliance process. Checkout my project hereInterests and ActivitiesBackend Development: Backend development is my forte. I enjoy building robust and scalable systems that solve real-world problems. My core tech stack is Python. Nowadays, I am learning Go because of its fast nature and built in concurrency.Open Source Software: I actively create and contribute to open source projects. I believe in the power of collaborative development and the freedom it brings to software creation.Hackathons and Conferences: I love participating in hackathons and attending conferences and talks about programming and software. Recently, I attended PyDelhi, which was an incredible experience.Community Building: I co-founded an open source community at my college called ZHCET Code Oasis. Our mission is to foster a culture of open source contribution and collaboration among students.ProjectsFeel free to check out my projects on GitHub.Thank you for visiting my page! If you share similar interests or have exciting projects to discuss, dont hesitate to connect with me.Contact Me | LinkedIn 2024 The Knight BlogPowered by Hugo  Paper"},
... 
```
Next, run:
```bash
 python3 model.py 
```
  7. A JSON file named **`questions_with_content.json`** will be generated, containing all the relevant data.
```json
 {
    "url": "https://rajuljha.github.io",
    "content": "The Knight Blog The Knight BlogAbout Contacttwitter github instagram linkedinRajul JhaSoftware DeveloperGSoC 2024 Final Project ReportAug 24, 2024 GSoC 2024 Final Project ReportFirst phase of GSoCJul 5, 2024 First phase of GSoCThe Night of My GSoC ResultMay 2, 2024 The Night of My GSoC ResultNext Page  2024 The Knight BlogPowered by Hugo  Paper",
    "questions": [
        "1. What is the purpose of The Knight Blog?",
        "2. Who is the author of the blog?",
        "3. What is the main topic of the first phase of GSoC?",
        "4. When did the author receive the results of their GSoC application?",
        "5. What is the date of the final GSoC 2024 project report?",
        "6. What platform hosts The Knight Blog?",
        "7. What is the primary focus of the blog posts?",
        "8. What programming language is used for the blog?",
        "9. What does GSoC stand for?",
        "10. What is the author's role in the GSoC program?"
    ],
    "relevant_links": [
        "https://rajuljha.github.io",
        "https://rajuljha.github.io/",
        "https://rajuljha.github.io/tags/github",
        "https://rajuljha.github.io/tags/gsoc",
        "https://rajuljha.github.io/tags/open-source"
    ],
    "topics": [
        "The",
        "Knight",
        "Blog",
        "The",
        "Knight"
    ],
    "question_relevance_score": 0.6722960472106934,
    "link_relevance_score": 0.4685312142911073
},
{
    "url": "https://rajuljha.github.io/",
    "content": "The Knight Blog The Knight BlogAbout Contacttwitter github instagram linkedinRajul JhaSoftware DeveloperGSoC 2024 Final Project ReportAug 24, 2024 GSoC 2024 Final Project ReportFirst phase of GSoCJul 5, 2024 First phase of GSoCThe Night of My GSoC ResultMay 2, 2024 The Night of My GSoC ResultNext Page  2024 The Knight BlogPowered by Hugo  Paper",
    "questions": [
        "1. What is the topic of the blog post?",
        "2. Who is the author of the blog post?",
        "3. What is the date of the blog post?",
        "4. What is the name of the author's GSoC project?",
        "5. What is the GSoC program?",
        "6. What phase of GSoC is the author reporting on?",
        "7. What did the author achieve during the first phase of GSoC?",
        "8. When did the author receive their GSoC result?",
        "9. What was the author's reaction to receiving their GSoC result?",
        "10. What other topics has the author written about on their blog?"
    ],
    "relevant_links": [
        "https://rajuljha.github.io",
        "https://rajuljha.github.io/",
        "https://rajuljha.github.io/tags/github",
        "https://rajuljha.github.io/tags/gsoc",
        "https://rajuljha.github.io/tags/open-source"
    ],
    "topics": [
        "The",
        "Knight",
        "Blog",
        "The",
        "Knight"
    ],
    "question_relevance_score": 0.6853605508804321,
    "link_relevance_score": 0.4685312142911073
}, 
```  
    
## License
[GNU GENERAL PUBLIC LICENSE
Version 2, June 1991](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)
