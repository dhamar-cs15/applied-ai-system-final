"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    my_user_prefs = {"genre": "folk", "mood": "wistful", "energy": 0.45, "acousticness": "likes_acoustic" }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations")
    print("=" * 40)
    if not recommendations:
        print("No recommendations found.")
        return

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']}")
        print(f"   Final score: {score:.1f} points")
        print("   Reasons:")
        for reason in explanation.split(", "):
            print(f"     - {reason}")


if __name__ == "__main__":
    main()
