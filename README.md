# 🎵 Feeling Swift - A Taylor Swift Song Recommender

## Project Summary

This project recommends Taylor Swift songs from a natural-language request. A keyword parser extracts preferences, a weighted ranker scores the song catalog, and an evaluation loop retries with adjusted weights or flags results for human review. The recommender evaluates various user preferences in regards to song characteristics, such as genre, mood, and energy to suggest the best-fitted tracks. The catalog is adapted from the Taylor Swift Spotify Dataset on Kaggle, which includes 582 tracks (https://www.kaggle.com/datasets/jarredpriester/taylor-swift-spotify-dataset).

This final project is based on Module 3's project, which implemented a simple song recommender based on a catalog of 18 songs and 3 pre-determined user profiles. The original project did not incorporate an agentic workflow and was not flexible in its user input. This updated project allows a user to express how they are feeling and what type of music they'd like to listen to, as well as how many song recommendations they would like to receive. This allows the user to receive a personalized playlist that best fits their preferences. 

---

## Architecture: How The System Works

System diagram: [Recommendation system architecture](diagrams/recommendation_system.mmd)

The CLI passes the request to the agent in `src/agent.py`. The agent extracts
available preferences, ranks songs using genre, mood, energy, valence, and
acousticness in `src/recommender.py`, then checks how well the results match
those preferences. It logs its trace and requests human review if it cannot
understand the request or the results remain a poor match. The current parser
is rule-based; no model API is configured.


[NEED_EXPLANATION]

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

Run a real request with:

```bash
python -m src.main "happy energetic pop" --top-k 1
```

```
INFO: REFLECT: match score 1.0 ≥ 0.6 — accepting results.

Request: happy energetic pop
Preferences: {'genre': 'pop', 'mood': 'happy', 'energy': 0.85, 'valence': 0.75}
Preference match score: 1.00 (checks: {'genre': 1.0, 'mood': 1.0, 'energy': 1.0, 'valence': 1.0})

1. New Romantics (Taylor's Version) — Taylor Swift
   Score: 119.4
   Reasons: genre match (+10.0), mood match (+30.0), energy similarity (+59.9), valence similarity (+19.5)

Recommendations accepted.
```

``` bash
python -m src.main "sad country" --top-k 5
```

```
INFO: PLAN: request = 'sad country'
INFO: PLAN: heuristic parser produced {'genre': 'country', 'mood': 'sad', 'valence': 0.2}
INFO: ACT  (pass 1): ranked 582 songs with weights {'genre': 10.0, 'mood': 30.0, 'energy': 60.0, 'valence': 20.0, 'acoustic': 20.0}
INFO: TEST (pass 1): match_score=1.0 checks={'genre': 1.0, 'mood': 1.0, 'valence': 1.0}
INFO: REFLECT: match score 1.0 ≥ 0.6 — accepting results.

Request: sad country
Preferences: {'genre': 'country', 'mood': 'sad', 'valence': 0.2}
Preference match score: 1.00 (checks: {'genre': 1.0, 'mood': 1.0, 'valence': 1.0})

1. Long Live - Live/2011 — Taylor Swift
   Score: 59.9
   Reasons: genre match (+10.0), mood match (+30.0), valence similarity (+19.9)

2. White Horse — Taylor Swift
   Score: 59.9
   Reasons: genre match (+10.0), mood match (+30.0), valence similarity (+19.9)

3. Fifteen — Taylor Swift
   Score: 59.9
   Reasons: genre match (+10.0), mood match (+30.0), valence similarity (+19.9)

4. Last Kiss - Live/2011 — Taylor Swift
   Score: 59.8
   Reasons: genre match (+10.0), mood match (+30.0), valence similarity (+19.8)

5. Last Kiss — Taylor Swift
   Score: 59.8
   Reasons: genre match (+10.0), mood match (+30.0), valence similarity (+19.8)

Recommendations accepted.
```


```bash
python -m src.main "really sad but slightly upbeat" --top-k 10                 
```

```
INFO: PLAN: request = 'really sad but slightly upbeat'
INFO: PLAN: conflicting cues found (happy vs sad); will proceed but flag it.
INFO: PLAN: heuristic parser produced {'mood': 'sad', 'energy': 0.85, 'valence': 0.2}
INFO: ACT  (pass 1): ranked 582 songs with weights {'genre': 10.0, 'mood': 30.0, 'energy': 60.0, 'valence': 20.0, 'acoustic': 20.0}
INFO: TEST (pass 1): match_score=1.0 checks={'mood': 1.0, 'energy': 1.0, 'valence': 1.0}
INFO: REFLECT: match score 1.0 ≥ 0.6 — accepting results.

Request: really sad but slightly upbeat
Preferences: {'mood': 'sad', 'energy': 0.85, 'valence': 0.2}
Preference match score: 1.00 (checks: {'mood': 1.0, 'energy': 1.0, 'valence': 1.0})
Warnings: happy vs sad

1. Electric Touch (feat. Fall Out Boy) (Taylor’s Version) (From The Vault) — Taylor Swift
   Score: 108.6
   Reasons: mood match (+30.0), energy similarity (+59.8), valence similarity (+18.8)

2. Out Of The Woods (Taylor's Version) — Taylor Swift
   Score: 107.7
   Reasons: mood match (+30.0), energy similarity (+58.0), valence similarity (+19.7)

3. Out Of The Woods (Taylor's Version) — Taylor Swift
   Score: 107.7
   Reasons: mood match (+30.0), energy similarity (+58.0), valence similarity (+19.7)

4. Haunted - Live/2011 — Taylor Swift
   Score: 107.6
   Reasons: mood match (+30.0), energy similarity (+58.1), valence similarity (+19.5)

5. Out Of The Woods — Taylor Swift
   Score: 106.7
   Reasons: mood match (+30.0), energy similarity (+59.5), valence similarity (+17.2)

6. Out Of The Woods — Taylor Swift
   Score: 106.7
   Reasons: mood match (+30.0), energy similarity (+59.5), valence similarity (+17.2)

7. Out Of The Woods — Taylor Swift
   Score: 106.7
   Reasons: mood match (+30.0), energy similarity (+59.5), valence similarity (+17.2)

8. Style (Taylor's Version) — Taylor Swift
   Score: 106.3
   Reasons: mood match (+30.0), energy similarity (+58.3), valence similarity (+18.0)

9. Bad Blood — Taylor Swift
   Score: 105.2
   Reasons: mood match (+30.0), energy similarity (+57.1), valence similarity (+18.1)

10. Hits Different — Taylor Swift
   Score: 105.0
   Reasons: mood match (+30.0), energy similarity (+56.2), valence similarity (+18.8)

Recommendations accepted.
```

```bash 
python -m src.main "anything you want to recommend me" --top-k 5 
```
```
INFO: PLAN: request = 'anything you want to recommend me'
INFO: PLAN: heuristic parser produced {}
INFO: PLAN: could not extract any preference — stopping instead of recommending blindly.

Request: anything you want to recommend me
Preferences: none identified
Preference match score: 0.00 (checks: {})
WARNING: I couldn't tell what you're in the mood for. Try naming an album, a mood, or an energy level.
```

---

## Design Decisions
For this project, I decidied to go with a Taylor Swift catalogue - she is known for having a music catalogue that spans from country to pop to folk and alternative. Her diversity makes it ideal for a project like this where mood and genre factors used to put together a playlist based on the user's preferences. This was also a decision made for the human review aspect, since I'm very familiar with Swift's music and would be able to verify if the agent was accurately recommending songs when give prompts such as "sad but slightly upbeat."

One tradeoff is that while Swift's catalogue is diverse, using only her discography provides a limited variety of genres and moods. There are many genres she has not covered and moods that aren't the primary ones represented in her songs. 

Another decision made was to have the program go based off known words like "sad," "pop," or "acoustic" so that it would be able to accurately map requests to the songs' characteristics. The program is able to understand words like "melancholy" which aren't directly associated with any song, and still produce accurate recommendations, such as sad songs in this case. However, the program doesn't understand other non-standard ways of describing a mood, such as "feeling a bit down." Therefore, there are some design choices such as this one that were made for simplicity and so that the agent would be able to understand synonyms related to the songs' characteristics in order to provide an accurate playlist, rather than return irrelevant results in an attempt to figure out what "feeling a bit down" meant.

This design decision also led to the implementation of guardrails and human review. Rather than continue with irrelevant results, the agent makes sure that it understands the request clearly. It evaluates what the request could mean and explains why it is matching it to songs that meet a particular criteria. If it is not able to find songs that match accurately, it displays that transparently to the user, with CLI messages such as "INFO: PLAN: could not extract any preference — stopping instead of recommending blindly."

---

## Testing Summary

Run the automated tests with `python -m pytest -q`. The current suite completed with **12 of 12 tests passing**:

| Test suite | What it checks | Result |
|---|---|---|
| `tests/test_recommender.py` | Numeric CSV loading, score/explanation details, and top-k ranking without catalog mutation. | 3 passed |
| `tests/test_agent.py` | Preference parsing and validation, acoustic alignment, weight-adjustment retries, low-information and invalid-input handling, optional-client fallback, and CLI integration/logging. | 9 passed |

This agent is efficient at recommending songs for a variety of moods and genres. It uses the scoring rubric in order to rank songs that match closely to these two particular factors. Based on my own knowledge of Taylor Swift's songs, I would say that the program is accurate most of the time in its recommendations. 

Through multiple rounds of testing, I kept seeing that the agent would recommend the same song multiple times in the same response. This was for a few reasons: the first is that the dataset included duplicates for each time that Swift has released a track on a "new" record. This would include each time that she has released songs on both a standard version and deluxe version. Particularly in the case of Taylor Swift, she released rerecordings of 4 of her previous albums as "Taylor's Version"s -- therefore all of these songs will have their original released tracks and their newer rerecorded ones. This can be confusing for a user that does not know much about Swift's catalogue. In a more optimized edition, the agent would be ale to differentiate between these repeated tracks and evaluate which to recommend. 

I also learned that the agent does not understand very nuanced expressions or anything that is too vague. For example, "sad but happy" returns a list of songs that I would personally agree are sad, but in no way happy. The agent understands that this is a conflict, noting: "INFO: PLAN: conflicting cues found (happy vs sad); will proceed but flag it." Yet, it proceeds to make a recommendation that is inaccurate. The program is not able to separate what the user would consider to be sad in a song versus happy. 

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



