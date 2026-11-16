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

The recommender gives reasonable results when a user’s preferences are represented in the catalog. For example, Chill Lofi gets acoustic, lower-energy tracks such as “Library Rain” and “Midnight Coding,” which are sound like very typical lofi songs. Other profiles also seem to match, Deep Intense Rock gets “Storm Runner” at the top which matches well with the user's preferences. 

I think the system works well when there are songs that closely match two or more categories, especially energy and mood, which are now the heaviest weighted categories after the weight modifications made.

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users 

python -m src.main "not too acoustic chill folk" --top-k 3
python -m src.main "sad country" --top-k 5

1. I Think He Knows — Taylor Swift
   Score: 105.8
   Reasons: genre mismatch (+0.0), mood match (+30.0), energy similarity (+56.0), acoustic preference (+19.8)

1. Long Live - Live/2011 — Taylor Swift
   Score: 59.9
   Reasons: genre match (+10.0), mood match (+30.0), valence similarity (+19.9)


Taylor's Version

This system does not consider learning from the user after the initial profile is made for them. The recommender selects songs based on the existing user profile but does not consider that the user's tastes might change over time. The current system also does not consider that the user may have multiple genre preferences at the same time. For example, I enjoy both pop and folk, especially songs that combine the two. The system currently has no way of coonsidering both of these genres simultaneously - if I say I like pop, I'll probably not get folk songs. 
On the same note, I'd likely not get folk songs in my recommendations because at the moment there's only one in the dataset. Therefore, even if I add "folk" as my chosen genre, the other 4 recommendations after the one folk song will be from some other genre, which I may or may not like. 
The scoring thus is more linkely to benefit users who have clear-cut preferences that align with the categories in the dataset. If someone likes "psychedelic folk" or "country-pop", the system won't be able to evaluate their preferences correctly. 


---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

I ran three profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock. I looked at the songs matched the preferences and whether overlapping results made sense. For example, there seemed to be quite some overlap between High-Energy Pop and Deep Intense Rock, primarily because of their similar energy levels (0.9 and 0.95). This makes sense and tells me that the recommender is giving a lot of importance to energy levels.

I also tried conflicting preferences, unknown genre or mood labels, and an empty profile. Unknown labels didn't earn match points but somehow the recommender still outputted recommended songs. This is because we don't have any fall back behavior for the system for these scenarios yet.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  


I could add more songs, especially in underrepresented genres and moods, so the system has better options for more listeners. I could also let users choose multiple genres or set different importance levels for their preferences to address some of the weaknesses I mentioned in the first few sections. Also based on teh overlap between the High-Energy Pop and Deep Intense Rock profiles, I could add a diversity feature so the top results don’t repeatedly favor songs with similar qualities. 
These implementations would allow the program to return a more personalized playlist to the user.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  


I learned that recommender systems are a lot more complicated and data-driven than they may seem. I hadn't really thought much about the weight aspect specifically and I wonder how recommender systems in Spotify and Youtube choose WHICH factors to weigh more and if it depends on the type of content. For example, for pop songs, should energy be more important than valence? How are lyrics taken into account? I think I may have ended up with more questions from this project because I hadn't really considered how much went on under the hood of the systems. 

I was surprised that some songs appeared for both High-Energy Pop and Deep Intense Rock, but it was easy to see that while the songs may have not been the same genre, they matched closely in energy levels, which allowed them to be represented on different profiles. 

