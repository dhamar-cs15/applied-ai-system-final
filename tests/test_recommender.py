from src.recommender import (
    load_songs,
    recommend_songs,
    score_song,
)


def test_load_songs_converts_numeric_fields(tmp_path):
    csv_path = tmp_path / "songs.csv"
    csv_path.write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,Test Song,Test Artist,pop,happy,0.8,120,0.9,0.7,0.2\n",
        encoding="utf-8",
    )

    songs = load_songs(str(csv_path))

    assert len(songs) == 1
    song = songs[0]
    assert song["title"] == "Test Song"
    assert song["id"] == 1
    assert isinstance(song["id"], int)
    assert song["tempo_bpm"] == 120
    assert isinstance(song["tempo_bpm"], int)
    for field in ("energy", "valence", "danceability", "acousticness"):
        assert isinstance(song[field], float)


def test_score_song_returns_score_and_reasons():
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    song = {"genre": "pop", "mood": "happy", "energy": 0.6}

    score, reasons = score_song(user_prefs, song)

    assert score == 88.0
    assert reasons == [
        "genre match (+10.0)",
        "mood match (+30.0)",
        "energy similarity (+48.0)",
    ]


def test_recommend_songs_ranks_top_k_without_mutating_catalog():
    songs = [
        {"title": "Low Match", "genre": "rock", "mood": "sad", "energy": 0.2},
        {"title": "Best Match", "genre": "pop", "mood": "happy", "energy": 0.8},
        {"title": "Partial Match", "genre": "pop", "mood": "sad", "energy": 0.7},
    ]
    original_order = list(songs)

    results = recommend_songs(
        {"genre": "pop", "mood": "happy", "energy": 0.8}, songs, k=2
    )

    assert [result[0]["title"] for result in results] == ["Best Match", "Partial Match"]
    assert len(results) == 2
    assert all(isinstance(result[1], float) for result in results)
    assert all(result[2] for result in results)
    assert songs == original_order
