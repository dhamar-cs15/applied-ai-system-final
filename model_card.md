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
The model identifies what the user's preference levels for genre, energy, mood, and acousticness are and compares this data with the song's data in order to determine how similar the two are. The way the program does this is by calculating a score. For example, genre contributes 20 points if the song's genre matches the user's preferred genre-- otherwise, it gives 0 points. Then mood is weighted heavier, contriibuting 30 points if there is an exact match between the song and the user. Factors such as energy and acousticness are measured by a numeric value, rather than a clear category like "pop" or "happy." Therefore, the amount of points each of these factors contribute to the overall score depends on how close the song's value is to the user's value. For example, if a user prefers an energy level of 0.85, a song with an energy level of 0.75 is more likely to be recommended than one with a level of 0.20. 


---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users 

This system does not consider learning from the user after the initial profile is made for them. The recommender selects songs based on the existing user profile but does not consider that the user's tastes might change over time. 


---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
