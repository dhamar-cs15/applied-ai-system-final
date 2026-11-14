import logging

import pytest

from src.agent import evaluate, parse_request_heuristic, run_agent, validate_profile
from src.main import main
from src.recommender import VALID_MOODS


def make_song(
    song_id,
    title,
    genre,
    mood,
    energy=0.7,
    valence=0.6,
    acousticness=0.2,
):
    return {
        "id": song_id,
        "title": title,
        "artist": "Taylor Swift",
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "tempo_bpm": 120,
        "valence": valence,
        "danceability": 0.5,
        "acousticness": acousticness,
    }


def test_heuristic_parser_extracts_catalog_preferences():
    profile = parse_request_heuristic("happy energetic pop, please")

    assert profile == {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.85,
        "valence": 0.75,
    }


def test_heuristic_parser_understands_acoustic_negation():
    assert parse_request_heuristic("not too acoustic pop")["likes_acoustic"] is False
    assert parse_request_heuristic("acoustic guitar")["likes_acoustic"] is True


def test_validate_profile_accepts_all_catalog_moods_and_normalizes_case():
    for mood in VALID_MOODS:
        assert validate_profile({"mood": mood.upper()}) == {"mood": mood}

    assert validate_profile({"mood": "unknown"}) == {}


def test_evaluate_includes_acoustic_preference_alignment():
    results = [(make_song(1, "Acoustic", "folk", "chill", acousticness=0.8), 1.0, "")]

    acoustic_match, acoustic_checks = evaluate(results, {"likes_acoustic": True})
    non_acoustic_match, non_acoustic_checks = evaluate(
        results, {"likes_acoustic": False}
    )

    assert acoustic_match == 0.8
    assert acoustic_checks == {"acoustic": 0.8}
    assert non_acoustic_match == 0.2
    assert non_acoustic_checks == {"acoustic": 0.2}


def test_agent_retry_applies_updated_weights():
    songs = [
        make_song(1, "Country Happy", "country", "happy"),
        make_song(2, "Pop Sad", "pop", "sad"),
    ]

    result = run_agent(
        "country sad",
        songs,
        k=1,
        max_passes=3,
        threshold=0.6,
    )

    assert result["results"][0][0]["title"] == "Country Happy"
    assert result["weights"]["genre"] == 40.0
    assert result["match_checks"]["genre"] == 1.0
    assert result["match_checks"]["mood"] == 0.0
    assert result["needs_human_review"] is True
    assert any("pass 3" in entry for entry in result["trace"])


def test_agent_flags_empty_and_unrecognized_requests_for_review():
    songs = [make_song(1, "Only Song", "pop", "happy")]

    empty = run_agent("", songs)
    unknown = run_agent("something not in the preference vocabulary", songs)

    assert empty["needs_human_review"] is True
    assert empty["results"] == []
    assert unknown["needs_human_review"] is True
    assert unknown["results"] == []


def test_agent_falls_back_when_optional_parser_fails():
    class BrokenClient:
        def parse_request(self, _text):
            raise RuntimeError("provider unavailable")

    result = run_agent(
        "happy pop",
        [make_song(1, "Happy Pop", "pop", "happy", valence=0.75)],
        client=BrokenClient(),
    )

    assert result["profile"]["genre"] == "pop"
    assert result["profile"]["mood"] == "happy"
    assert any("falling back to heuristics" in entry for entry in result["trace"])


def test_agent_rejects_invalid_runtime_options():
    with pytest.raises(ValueError, match="k must be at least 1"):
        run_agent("happy pop", [], k=0)
    with pytest.raises(ValueError, match="max_passes must be at least 1"):
        run_agent("happy pop", [], max_passes=0)
    with pytest.raises(ValueError, match="threshold must be between 0 and 1"):
        run_agent("happy pop", [], threshold=1.1)


def test_main_runs_agent_and_logs_trace(tmp_path, monkeypatch, capsys, caplog):
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "songs.csv").write_text(
        "id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness\n"
        "1,Happy Pop,Taylor Swift,pop,happy,0.85,120,0.75,0.5,0.1\n",
        encoding="utf-8",
    )
    monkeypatch.chdir(tmp_path)

    with caplog.at_level(logging.INFO, logger="src.main"):
        main(["happy energetic pop", "--top-k", "1"])

    output = capsys.readouterr().out
    assert "Happy Pop" in output
    assert "Preference match score: 1.00" in output
    assert "PLAN: heuristic parser produced" in caplog.text
