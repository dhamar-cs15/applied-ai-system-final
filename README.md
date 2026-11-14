# 🎵 Music Recommender Simulation

## Project Summary

This project recommends Taylor Swift songs from a natural-language request. An
offline keyword parser extracts preferences, a weighted ranker scores the song
catalog, and an evaluation loop retries with adjusted weights or flags results
for human review. The catalog is adapted from the
[Taylor Swift Spotify Dataset on Kaggle](https://www.kaggle.com/datasets/jarredpriester/taylor-swift-spotify-dataset).

---

## How The System Works

System diagram: [Recommendation system architecture](diagrams/recommendation_system.mmd)

The CLI passes the request to the agent in `src/agent.py`. The agent extracts
available preferences, ranks songs using genre, mood, energy, valence, and
acousticness in `src/recommender.py`, then checks how well the results match
those preferences. It logs its trace and requests human review if it cannot
understand the request or the results remain a poor match. The current parser
is rule-based; no model API is configured.

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

The CLI prints the parsed preferences, match score, selected track, score
reasons, and whether the agent accepted the result or requested human review.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

I tested what happened when I made energy more important and genre less important. I brought down the genre-match points from 20 to 10 and doubled the maximum energy points from 30 to 60. This made songs with energy close to a user’s target more likely to rank highly, even when their genre didn’t match. Unfortunately, this also created some overlap in profiles. 

---

## Reliability and Evaluation

Run the automated tests with `python -m pytest -q`. The current suite completed with **12 of 12 tests passing**:

| Test suite | What it checks | Result |
|---|---|---|
| `tests/test_recommender.py` | Numeric CSV loading, score/explanation details, and top-k ranking without catalog mutation. | 3 passed |
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



