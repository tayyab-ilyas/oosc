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
   4. **Navigate to the `main.py` file** in the repository and replace the example url: 
```python
 if __name__ == "__main__":
    url = 'https://brodierobertson.xyz'
 process_website(url,  max_depth=6)
``` 
  5. Run the command to scrape the URL:
```bash
 python3 main.py  
```
  6.  **A file named `webpage_content.json` will be created.** in the following format:
```json 
[
{"url": "https://brodierobertson.xyz", "content": "Brodie's Soon To Be Blog Home Donate Videos Gear Contact Me Link Tree Brodie's Soon To Be Blog I've been meaning to put this site together for a very long time, and the result is well... make of it as you will. Hey I'm Brodie Robertson To be completely honest, I didn't think I would ever get to the point where some random person like you would want to visit my website but here we are. I don't know if you'd frame it like this but I'm most well known online for showcasing various pieces of Linux software which catch my attention, which you can check out here. If that's not your thing I'll also cover I'll also occasionally various other pieces of Linux or Linux adjacent topics such as \"What is Swap Space\" or \"Linus Torvalds Ponders The Future Of The Linux Kernel\" so if Linux is your jam I'm sure you'll find something to interest you. I'm still fairly new to Linux all things considered It may come across in my videos like I'm someone who's been using Linux for years and has tons of experience with this sort of software but in reality I've only actually been daily driving Linux close to 2 years, so occasionally I'll make some mistakes. Being interested in software for most of my life I've known about Linux for a long time but I didn't really consider trying it out until I discovered Linux content creators like Bryan Lunduke, Luke Smith, Distrotube and many others. I didn't even wait get comfortable with Linux before making videos as you'll see from some of my early content but I feel like in the last couple of months I've finally reached a point where what I know, what I know I can learn and what I can teach people can finally provide some actual value. The software I use is always changing but you can see what I typically use here Along with my video content I'll also chuck together some scripts and config files from time to time and all of this is available on my GitHub. I also have a Podcast!! To be completely honest this podcast is only a tech podcast in name, sure I love tech so it'll come up from time to time but expect anything from news, to anime, to random anecdotes from and anything in between. If you expect to leave this podcast having learned anything useful you're be dissapointed most of the time, but none the less I still try to make it a fun and worthwhile experience if you like some fun banter. If that sounds like fun check out the audio release over on Anchor. There's also a video release of the podcast over on Youtube and Odysee. And even a gaming channel! I like video games, you probably like video games so why not come and watch me play some over on YouTube, Twitch and even Dlive. My tastes are really varied, sometimes I'll play platformers like Celeste or Spyro, sometimes I'll play rogue lites/likes such as Dead Cells or Hades and sometimes I'll even play JRPGs like Kingdom Hearts and Neptunia. If I'm going to be playing some games anyway I might as well stream them so here we are, I'm not the best gamer and I'm pretty awful at talking to chat while also playing but that leads to even more fun. Get more updates about my life than you could ever want RSS Feeds I know a lot of you guys prefer doing stuff through RSS so here's a few of my links. Brodie Robertson YouTube: brodierobertson.xyz/rss Podcast YouTube: techovertea.xyz/rssvideo Podcast Audio: http://techovertea.xyz/rss Gaming YouTube: http://brodierobertson.xyz/gamingrss Note that Brave users can also donate to any of my websites or my YouTube channel through their browser. Get in contact with me here! Return Back To Home"},
{"url": "https://brodierobertson.xyz/index.html", "content": "Brodie's Soon To Be Blog Home Donate Videos Gear Contact Me Link Tree Brodie's Soon To Be Blog I've been meaning to put this site together for a very long time, and the result is well... make of it as you will. Hey I'm Brodie Robertson To be completely honest, I didn't think I would ever get to the point where some random person like you would want to visit my website but here we are. I don't know if you'd frame it like this but I'm most well known online for showcasing various pieces of Linux software which catch my attention, which you can check out here. If that's not your thing I'll also cover I'll also occasionally various other pieces of Linux or Linux adjacent topics such as \"What is Swap Space\" or \"Linus Torvalds Ponders The Future Of The Linux Kernel\" so if Linux is your jam I'm sure you'll find something to interest you. I'm still fairly new to Linux all things considered It may come across in my videos like I'm someone who's been using Linux for years and has tons of experience with this sort of software but in reality I've only actually been daily driving Linux close to 2 years, so occasionally I'll make some mistakes. Being interested in software for most of my life I've known about Linux for a long time but I didn't really consider trying it out until I discovered Linux content creators like Bryan Lunduke, Luke Smith, Distrotube and many others. I didn't even wait get comfortable with Linux before making videos as you'll see from some of my early content but I feel like in the last couple of months I've finally reached a point where what I know, what I know I can learn and what I can teach people can finally provide some actual value. The software I use is always changing but you can see what I typically use here Along with my video content I'll also chuck together some scripts and config files from time to time and all of this is available on my GitHub. I also have a Podcast!! To be completely honest this podcast is only a tech podcast in name, sure I love tech so it'll come up from time to time but expect anything from news, to anime, to random anecdotes from and anything in between. If you expect to leave this podcast having learned anything useful you're be dissapointed most of the time, but none the less I still try to make it a fun and worthwhile experience if you like some fun banter. If that sounds like fun check out the audio release over on Anchor. There's also a video release of the podcast over on Youtube and Odysee. And even a gaming channel! I like video games, you probably like video games so why not come and watch me play some over on YouTube, Twitch and even Dlive. My tastes are really varied, sometimes I'll play platformers like Celeste or Spyro, sometimes I'll play rogue lites/likes such as Dead Cells or Hades and sometimes I'll even play JRPGs like Kingdom Hearts and Neptunia. If I'm going to be playing some games anyway I might as well stream them so here we are, I'm not the best gamer and I'm pretty awful at talking to chat while also playing but that leads to even more fun. Get more updates about my life than you could ever want RSS Feeds I know a lot of you guys prefer doing stuff through RSS so here's a few of my links. Brodie Robertson YouTube: brodierobertson.xyz/rss Podcast YouTube: techovertea.xyz/rssvideo Podcast Audio: http://techovertea.xyz/rss Gaming YouTube: http://brodierobertson.xyz/gamingrss Note that Brave users can also donate to any of my websites or my YouTube channel through their browser. Get in contact with me here! Return Back To Home"},
]
... 
```
Next, run:
```bash
 python3 model.py 
```
  7. A JSON file named **`questions_with_content.json`** will be generated, containing all the relevant data.
```json
 {
    "url": "https://brodierobertson.xyz/videos.html",
    "content": "Watch My Videos! Home Donate Videos Gear Contact Me Link Tree Watch My Videos! I've seen so many creators get burnt by making the stupid mistake of uploading their content onto YouTube, even just having you content somewhere else as a backup is a good idea. All of the the videos I upload get synched across multiple platforms to ensure that as many people as possible can see them, obviously losing some would hurt but it would hurt much more to dissapear after losing just one platform. Video On De",
    "questions": [
        "1. Why is it important to have a backup for your video content?",
        "2. On how many platforms does the creator upload their videos?",
        "3. How often does the creator upload videos on weekdays?",
        "4. On which day of the week does the creator stream on the main channel?",
        "5. What type of games are streamed on the main channel?",
        "6. What is the purpose of the \"Video On Demand\" section?",
        "7. Which platforms are available for streaming?",
        "8. How can Brave users support the creator?",
        "9. What is the creator's preferred method of communication?",
        "10. What is the primary platform mentioned in the content?"
    ],
    "relevant_links": [
        "https://brodierobertson.xyz/videos.html",
        "https://brodierobertson.xyz/donate.html",
        "https://brodierobertson.xyz/contact.html",
        "https://brodierobertson.xyz/link_tree.html",
        "https://brodierobertson.xyz/gear.html"
    ],
    "topics": [
        "Watch",
        "My",
        "Home",
        "Donate",
        "Videos"
    ],
    "question_relevance_score": 0.6612800359725952,
    "link_relevance_score": 0.5508520098284784
} 
```  
    
## License
[GNU GENERAL PUBLIC LICENSE
Version 2, June 1991](https://www.gnu.org/licenses/old-licenses/gpl-2.0.txt)
