# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**

**Music to my Mood**


---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  


This recommender is designed to create a short playlist of songs that match your mood. Based on the user's music taste preferences, this simulator determines which songs the user is most likely to enjoy at the moment. The recommender will take the user's preferred genre, mood, energy level, and favorability towards acousticness -- using these factors, it calculates how similar a song is to the user preference levels of the factors. If the song's attributes align well with the user's taste, it recommends that song to the user. 

Right now, this recommender is for classroom exploration only. The current program does not take actual user data or user interactions to create a list of recommendations. It only has 18 songs in its catalog and the user preferences are predetermined based on a few factors only. 
---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

There are only a few main features that are currently used from a song in order to determine its score. The current model takes in a song's genre, energy, mood, and acousticness data, though each song has additional attributes (id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness). 
The model identifies the user's preferences for genre, energy, mood, and acousticness and compares them with each song. It then adds points to make a score. An exact genre match adds 10 points, while an exact mood match adds 30. Energy can add up to 60 points: the closer a song's energy is to the user's target, the more points it earns. Acousticness can add up to 20 points depending on whether the user likes acoustic music. For example, a user who prefers energy 0.85 gets a stronger energy match from a song at 0.75 than from one at 0.20.


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

There are 18 songs in the catalog. There are 15 genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, country, reggae, classical, metal, funk, house, folk, and blues. There are 14 moods: happy, chill, intense, moody, focused, nostalgic, playful, serene, defiant, confident, euphoric, wistful, melancholic, and relaxed.

I added 8 songs to the original dataset of 10 songs. This was the only new data added for the catalog.

I think many of the moods and genres listed could virtually be considered "missing" because they only appear once. If they only appear once, the user won't be getting many recommendations with that kind of song, which is a flaw in the recommender. I also doesn't consider whether the user wants to hear songs that might sound one way sonically, but their meaning in lyrics is the complete opposite. 

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

