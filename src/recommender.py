import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

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

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a song against user preferences and return the score with reasons."""
    score = 0.0
    reasons = []

    genre = user_prefs.get("genre")
    if genre:
        if str(genre).strip().casefold() == str(song.get("genre", "")).strip().casefold():
            score += 10
            reasons.append("genre match (+10.0)")
        else:
            reasons.append("genre mismatch (+0.0)")

    mood = user_prefs.get("mood")
    if mood:
        if str(mood).strip().casefold() == str(song.get("mood", "")).strip().casefold():
            score += 30
            reasons.append("mood match (+30.0)")
        else:
            reasons.append("mood mismatch (+0.0)")

    if "energy" in user_prefs and "energy" in song:
        energy_points = round(
            60 * max(
                0.0, 1.0 - abs(float(user_prefs["energy"]) - float(song["energy"]))
            ),
            1,
        )
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.1f})")

    if "likes_acoustic" in user_prefs and "acousticness" in song:
        acousticness = min(1.0, max(0.0, float(song["acousticness"])))
        acoustic_points = 20 * (
            acousticness if user_prefs["likes_acoustic"] else 1.0 - acousticness
        )
        score += acoustic_points
        reasons.append(f"acoustic preference (+{acoustic_points:.1f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Return the top-k songs ranked by score with explanations."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons) or "No matching preferences were provided."
        scored_songs.append((song, score, explanation))

    return sorted(scored_songs, key=lambda result: result[1], reverse=True)[: max(0, k)]
