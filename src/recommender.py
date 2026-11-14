import csv
from typing import List, Dict, Tuple, Optional

DEFAULT_WEIGHTS: Dict[str, float] = {
    "genre": 10.0,      # flat bonus for an era/genre match
    "mood": 30.0,       # flat bonus for a mood match
    "energy": 60.0,     # scaled by closeness to the user's target energy
    "valence": 20.0,    # scaled by closeness to the user's target valence (NEW)
    "acoustic": 20.0,   # scaled by acousticness, direction set by likes_acoustic
}
 
# The values the dataset actually uses. The agent's parser must stay inside these.
VALID_GENRES = {"country", "pop-rock", "pop", "synth-pop", "folk", "alt-pop"}
VALID_MOODS = {"happy", "sad", "neutral", "intense", "chill"}

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file, converting numeric fields to numbers."""
    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        songs = []
        for row in csv.DictReader(csv_file):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = int(row["tempo_bpm"])
            for field in ("energy", "valence", "danceability", "acousticness"):
                row[field] = float(row[field])
            songs.append(row)
    return songs

def _closeness(a: float, b: float) -> float:
    """1.0 when identical, 0.0 when a full unit apart."""
    return max(0.0, 1.0 - abs(float(a) - float(b)))

def score_song(user_prefs: Dict, song: Dict, weights:Optional[Dict[str, float]] = None) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return the score with reasons."""
    w = {**DEFAULT_WEIGHTS, **(weights or {})}
    score = 0.0
    reasons = []

    genre = user_prefs.get("genre")
    if genre:
        if str(genre).strip().casefold() == str(song.get("genre", "")).strip().casefold():
            score += w["genre"]
            reasons.append(f"genre match (+{w['genre']:.1f})")
        else:
            reasons.append("genre mismatch (+0.0)")

    mood = user_prefs.get("mood")
    if mood:
        if str(mood).strip().casefold() == str(song.get("mood", "")).strip().casefold():
            score += w["mood"]
            reasons.append(f"mood match (+{w['mood']:.1f})")
        else:
            reasons.append("mood mismatch (+0.0)")

    if "energy" in user_prefs and "energy" in song:
        energy_points = round(w["energy"] * _closeness(user_prefs["energy"], song["energy"]), 1)
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.1f})")

    if "valence" in user_prefs and "valence" in song:
        valence_points = round(w["valence"] * _closeness(user_prefs["valence"], song["valence"]), 1)
        score += valence_points
        reasons.append(f"valence similarity (+{valence_points:.1f})")
 
    if "likes_acoustic" in user_prefs and "acousticness" in song:
        acousticness = min(1.0, max(0.0, float(song["acousticness"])))
        acoustic_points = round(
            w["acoustic"] * (acousticness if user_prefs["likes_acoustic"] else 1.0 - acousticness), 1
        )
        score += acoustic_points
        reasons.append(f"acoustic preference (+{acoustic_points:.1f})")
 
    return round(score, 1), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Optional[Dict[str, float]] = None) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs ranked by score with explanations."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = ", ".join(reasons) or "No matching preferences were provided."
        scored_songs.append((song, score, explanation))

    return sorted(scored_songs, key=lambda result: result[1], reverse=True)[: max(0, k)]
