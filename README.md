# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

<!-- The catalog in `data/songs.csv` is adapted from the [Taylor Swift Spotify Dataset on Kaggle](https://www.kaggle.com/datasets/jarredpriester/taylor-swift-spotify-dataset). The source does not provide genre or mood labels, so genres are assigned by album: Taylor Swift, Fearless, and Speak Now are `country`; Red is `pop-rock`; 1989 and Lover are `pop`; reputation and Midnights are `synth-pop`; folklore and evermore are `folk`; and The Tortured Poets Department is `alt-pop`. Album editions and live variants use their parent album's genre. Mood is derived from Spotify valence and energy: valence ≥ 0.65 is `happy`, valence ≤ 0.35 is `sad`, otherwise energy ≥ 0.70 is `intense`, energy ≤ 0.40 is `chill`, and the remaining tracks are `neutral`. Tempo is rounded to whole BPM. -->


This version of the song recommender


---

## How The System Works

Explain your design in plain language.

System diagram: [Recommendation system architecture](diagrams/recommendation_system.mmd)

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Write a short paragraph explaining your understanding of how real-world recommendations work and what your version will prioritize.
List the specific features your Song and UserProfile objects will use in your simulation.



---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app with a natural-language request:

   ```bash
   python -m src.main "happy energetic pop" --top-k 5
   ```

   Omit the request to enter one interactively. The CLI uses the offline
   keyword parser; no model API key or network connection is required.

### Running Tests

Run the automated tests with:

```bash
pytest -q
```

Agent and recommendation tests are in `tests/`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```
```
Top recommendations
========================================

1. Sunrise City
   Final score: 79.4 points
   Reasons:
     - genre match (+20.0)
     - mood match (+30.0)
     - energy similarity (+29.4)

2. Rooftop Lights
   Final score: 58.8 points
   Reasons:
     - genre mismatch (+0.0)
     - mood match (+30.0)
     - energy similarity (+28.8)

3. Gym Hero
   Final score: 46.1 points
   Reasons:
     - genre match (+20.0)
     - mood mismatch (+0.0)
     - energy similarity (+26.1)

4. Gold on the Floor
   Final score: 29.7 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+29.7)

5. Night Drive Loop
   Final score: 28.5 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+28.5)

```


**TESTING FOR 3 DIFFERENT PROFILES**
```
Top recommendations for High-Energy Pop
==================================================

1. Sunrise City
   Final score: 92.5 points
   Reasons:
     - genre match (+20.0)
     - mood match (+30.0)
     - energy similarity (+26.1)
     - acoustic preference (+16.4)

2. Gym Hero
   Final score: 68.4 points
   Reasons:
     - genre match (+20.0)
     - mood mismatch (+0.0)
     - energy similarity (+29.4)
     - acoustic preference (+19.0)

3. Rooftop Lights
   Final score: 67.3 points
   Reasons:
     - genre mismatch (+0.0)
     - mood match (+30.0)
     - energy similarity (+24.3)
     - acoustic preference (+13.0)

4. Iron Horizon
   Final score: 48.6 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+29.4)
     - acoustic preference (+19.2)

5. Storm Runner
   Final score: 46.8 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+28.8)
     - acoustic preference (+18.0)

Top recommendations for Chill Lofi
==================================================

1. Library Rain
   Final score: 95.7 points
   Reasons:
     - genre match (+20.0)
     - mood match (+30.0)
     - energy similarity (+28.5)
     - acoustic preference (+17.2)

2. Midnight Coding
   Final score: 93.6 points
   Reasons:
     - genre match (+20.0)
     - mood match (+30.0)
     - energy similarity (+29.4)
     - acoustic preference (+14.2)

3. Spacewalk Thoughts
   Final score: 74.8 points
   Reasons:
     - genre mismatch (+0.0)
     - mood match (+30.0)
     - energy similarity (+26.4)
     - acoustic preference (+18.4)

4. Focus Flow
   Final score: 65.6 points
   Reasons:
     - genre match (+20.0)
     - mood mismatch (+0.0)
     - energy similarity (+30.0)
     - acoustic preference (+15.6)

5. Coffee Shop Stories
   Final score: 46.9 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+29.1)
     - acoustic preference (+17.8)

Top recommendations for Deep Intense Rock
==================================================

1. Storm Runner
   Final score: 97.7 points
   Reasons:
     - genre match (+20.0)
     - mood match (+30.0)
     - energy similarity (+29.7)
     - acoustic preference (+18.0)

2. Gym Hero
   Final score: 78.1 points
   Reasons:
     - genre mismatch (+0.0)
     - mood match (+30.0)
     - energy similarity (+29.1)
     - acoustic preference (+19.0)

3. Afterglow Circuit
   Final score: 47.5 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+29.1)
     - acoustic preference (+18.4)

4. Iron Horizon
   Final score: 47.1 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+27.9)
     - acoustic preference (+19.2)

5. Sunrise City
   Final score: 44.0 points
   Reasons:
     - genre mismatch (+0.0)
     - mood mismatch (+0.0)
     - energy similarity (+27.6)
     - acoustic preference (+16.4)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I tested what happened when I made energy more important and genre less important. I brought down the genre-match points from 20 to 10 and doubled the maximum energy points from 30 to 60. This made songs with energy close to a user’s target more likely to rank highly, even when their genre didn’t match. Unfortunately, this also created some overlap in profiles. 

---

## Reliability and Evaluation

Run the automated tests with `pytest -q`. The current suite completed with **14 of 14 tests passing**:

| Test suite | What it checks | Result |
|---|---|---|
| `tests/test_recommender.py` | Numeric CSV loading, score/explanation details, top-k ranking without catalog mutation, and the object-based recommender. | 5 passed |
| `tests/test_agent.py` | Preference parsing and validation, acoustic alignment, weight-adjustment retries, low-information and invalid-input handling, optional-client fallback, and CLI integration/logging. | 9 passed |

The reported match score is a heuristic average of preference-alignment checks, **not** a calibrated probability that a recommendation is correct. The CLI currently uses deterministic keyword parsing; no Gemini or other model API client is configured. The optional `client.parse_request` interface has a fallback test, but these results do not measure LLM quality or include human-review outcomes.

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.


There are many limitations with this recommender. For example, it doesn't have a vast variety of songs, just a limited dataset. A major limitation I can think of is that sometimes the song's energy doesn't match the mood. For example, angry rock songs can be high in energy but the recommender might think that this energy level matches the profile of a user who likes "happy pop." I can think of songwriters who will also write songs that sound upbeat and happy but are actually sad or distressing. 
Another limitation is that the user's profile right now is static. The user is described very one-dimensionally, such as "happy pop." But people's moods shift throughout the day and across periods of time; the recommender at the moment does not adjust the user's profile based on what they have actually been feeling and listening to lately. 

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



