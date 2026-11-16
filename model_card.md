# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

**Feeling Swift - A Taylor Swift Song Recommender**


---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  


This recommender is designed to create a short playlist of songs that match a user's mood. Based on the user's music taste preferences, this simulator determines which songs the user is most likely to enjoy at the moment. The recommender will take the user's preferred genre, mood, energy level, and favorability towards acousticness -- using these factors, it calculates how similar a song is to the user preference levels of the factors. If the song's attributes align well with the user's taste, it recommends that song to the user.

The music catablogue used in the project is based off Taylor Swift's discography, which ranges across ranges from country to pop to indie folk. The catalogue features various moods such as sad, happy, neutral, intense, chill, and more. 

Right now, this recommender is for classroom exploration only. The program implements an agent that considers the user's description of what type of music they would like to listen to. The agent is limited in which kind of statements it can interpret but it is able to understand those with synonyms to the keywords in the catalogue, allowing it to be flexible enough to interact with users. 

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

The system will first look for known keywords in the request and maps them to a small set of preferences. Based on its closeness to a song's characteristics, it then scores each song -- giving most weight to the similarity in energy, mood, and genre to the user's preferences. Once each song has received its score, it is sorted in a ranking (best matched songs first). 

Afyter ranking, the agent checks whether the results align with the extracted preferences. If the user's request is unclear or the songs don't really align with it, the agent flags the result for human review, explaining its reasoning for the warning. This makes sure that the agent is transparent about what it can and cannot produce. The score that it gives each song is simply an indication of preferene alignment but can't guarantee that the user will actually agree with the recommended songs or enjoy them.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

The final catalog contains 582 rows and is adapted from the Taylor Swift Spotify dataset on Kaggle. The earlier Module 3 version used 18 songs and three predetermined user profiles; this version lets users enter requests directly -- providing for a more flexible and personalized experience for the user.

The current system supports various genres, including country, pop-rock, pop, synth-pop, folk, and alt-pop, and the moods happy, sad, neutral, intense, and chill. The data includes numeric audio attributes such as energy, valence, tempo, danceability, and acousticness, although not all of them affect the current score. The catalog is limited to one artist, Taylor Swift, and repeated track titles or versions can appear, so 582 rows doesn't necessarily mean 582 distinct songs. One arist's catalogue might be diverse but it will inevitably leave out a variety of genres and moods that the user might be looking for but not find fulfilled within this catalogue of music used. 


---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

The recommender works best when the user’s request uses cues the parser recognizes and the catalog contains tracks with matching attributes. For example, “happy energetic pop” produces preferences for pop, happy mood, high energy, and positive valence; “sad country” produces country, sad mood, and low valence.

I think the score reasons make it possible to see which attributes contributed to a recommendation. The evaluation loop also checks the results instead of simply returning a ranked list without qualification.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users 

Examples of inaccurate/limited suggestions:
```bash
python -m src.main "not too acoustic chill folk" --top-k 3
```
```
1. I Think He Knows — Taylor Swift
   Score: 105.8
   Reasons: genre mismatch (+0.0), mood match (+30.0), energy similarity (+56.0), acoustic preference (+19.8)
```

```bash 
python -m src.main "sad country" --top-k 5
```
```
1. Long Live - Live/2011 — Taylor Swift
   Score: 59.9
   Reasons: genre match (+10.0), mood match (+30.0), valence similarity (+19.9)
```

The system only recommends from a Taylor Swift catalogue, so it cannot serve listeners seeking other artists or music outside its supported categories. Its keyword parser can also miss context, handle mixed preferences poorly, or assign a fixed mood even when a request is more nuanced. For example, a user can prefer several genres at once, but the current profile supports only one genre due to the need to use one for scoring decisions. Another example is how the agent might interpret a mood such as "sad," which can mean different things -- one of the prompts above demonstrate this, where the user asked for "sad country" and was recommended the song "Long Live", which depending on the context, can be associated with different moods that are usually not aligned with sadness. 

The scoring relies on audio attributes and category labels, not lyrics or a listener’s personal interpretation of a song. Energy and valence are imperfect proxies for how a song feels, and the high energy weight can outweigh other preferences. Catalogue imbalances and repeated tracks can also make some recommendations more likely to appear than others. This was seen in one of my output examples detailed in the README, where a single song (Out of the Woods) was recommended 5 times in a playlist of 10 songs, due to the different versions that exist of it. 


---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

I checked the system with natural-language requests, including “happy energetic pop,” “sad country,” a request with conflicting mood cues, and a request with no recognizable preferences. I also ran the automated test suite and all 12 tests passed.

One observation was that the system can flag contradictory cues and still report a high preference-match score. the score measures alignment with the preferences the parser extracted but it does not prove that the parser interpreted the original request correctly. I also saw repeated tracks in some top-k results several times, which shows that ranking rows does not necessarily produce a playlist of distinct songs.

One thing I tested from the original Module 3 assignment was contradictory moods such as "sad but upbeat", which the original program was not able to figure out. This updated program was able to interpret this request much better, recommending songs that were classified as sad in terms of their lyrics or theme, but energetic/upbeat sonically. 

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  


I would first decide whether to clean the data to remove duplicated songs so that they're not suggested multiple times in a single recommendation. This would involve investigating which versions are in the catalogue, since Taylor Swift has often done remixes that change the mood/characteristics of the song, or emphasized a certain emotion more in her newer Taylor's Version tracks. I would also add better support for mixed or multiple preferences, more diverse tracks and categories, and a way to tune the relative importance of preferences. A stronger evaluation could include human ratings of recommendation usefulness rather than relying only on attribute alignment, which would allow the system to learn more about what is working and what is not. This would be helpful for the duplicates issue, especially to determine whether it makes a difference if the system recommends one version of the song over another. 



---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  


I learned that recommender systems are a lot more complicated and data-driven than they may seem. At the same time, this final project taught me more about how important context is, especially when attempting to understand what the user is asking for. For example, a user might want songs that are "nostalgic" but what does being nostalgic really mean? The songs could be either happy or sad, and there's not a standard set of attributes that could accurtely capture what nostalgic music is. The original program didn't allow much flexibility for nuance; this updated version does allow for more nuance from the user's inputs but in doing so it has to tackle the dilemma of figuring out what that nuance actually means. 

Something I thought was interesting is that sometimes the agent can recommend songs seemingly confidently but still give warnings about conflicts. This is interesting because it makes me wonder to what extent would an agent present information it has reservations about and continue forward with its task. 


## 10. AI Reflection
I used Co-Pilot as an AI assistant to help me review the project from Module 3 again and understand its design and where it could be improved upon by an agent. I accepted its suggestions to make guardrail behavior transparent so that the user could see in the commandline the reasoning for the ranking given and if there were any warnings issued. I thought this was helpful becuase it provided an opportunity for human review. 

The AI also pointed out that there were multiple repeated recommendations in some of the outputs -- I decided to leave the code and dataset unchanged in this case and treated those duplicates as a limitation instead. I thought that to remove the duplicates, it would involve an expansion in scope and creating a rubric for how to deal with songs that had different versions that expressed different moods. Thus, I decided to leave the duplicates as they were for this project version.

