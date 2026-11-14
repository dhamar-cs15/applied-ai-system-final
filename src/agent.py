"""
agent.py — an agentic wrapper.

The loop:
    PLAN     turn a plain-English request into a taste profile
    ACT      run recommend_songs with the current weights
    TEST     check whether the top results actually match the request
    REFLECT  if the match score is low, raise failed preference weights and retry;
             if it remains low, request human review

Every decision writes a line to `trace`, which main.py logs.
An optional parse_request-compatible client can be injected for PLAN;
the CLI uses the offline heuristic parser.
"""

import re
from typing import Dict, List, Optional, Tuple

from .recommender import (
    DEFAULT_WEIGHTS,
    VALID_GENRES,
    VALID_MOODS,
    recommend_songs,
)

# ---------------------------------------------------------------------------
# PLAN: keyword tables for the offline parser.
# Keys are regex patterns (word-boundary matched, case-insensitive).
# ---------------------------------------------------------------------------
GENRE_KEYWORDS = {
    r"folklore|evermore|folk|indie|storytelling": "folk",
    r"fearless|speak now|debut|country|banjo": "country",
    r"\bred\b|rock|band": "pop-rock",
    r"reputation|midnights|synth|dark pop|electro": "synth-pop",
    r"tortured|ttpd|poets": "alt-pop",
    r"1989|lover|\bpop\b": "pop",   # last so album-specific words win first
}

MOOD_KEYWORDS = {
    r"sad|heartbreak|heartbroken|cry|crying|breakup|lonely|grief|melanchol": "sad",
    r"happy|joy|joyful|fun|upbeat|bright|sunny|celebrat": "happy",
    r"hype|workout|gym|angry|rage|intense|pump|revenge|fierce|power": "intense",
    r"chill|calm|mellow|relax|quiet|soft|easy": "chill",
    r"nostalgic|wistful|thoughtful|neutral": "neutral",
}

ENERGY_KEYWORDS = {
    r"slow|chill|calm|quiet|sleep|rainy|soft|mellow|study": 0.3,
    r"upbeat|dance|hype|workout|gym|party|run|energetic|loud": 0.85,
}

VALENCE_KEYWORDS = {
    r"sad|heartbreak|cry|crying|breakup|lonely|grief|dark": 0.2,
    r"happy|joy|joyful|fun|upbeat|bright|sunny|celebrat": 0.75,
}

ACOUSTIC_KEYWORDS = {
    r"\b(?:electronic|synth|dance|club|produced|beat)\b": False,
    r"\b(?:acoustic|guitar|piano|stripped|unplugged|folk)\b": True,
}

AVOID_ACOUSTIC_PATTERN = (
    r"\b(?:not\s+(?:(?:too|very|much|that|anything)\s+)?|no\s+|less\s+|"
    r"without\s+|avoid\s+|skip\s+)(?:acoustic|guitar|piano|stripped|unplugged|folk)\b"
)

# Word groups that contradict each other. If both sides appear, flag it.
CONFLICTS = [
    (r"happy|joy|fun|upbeat", r"sad|heartbreak|cry|grief", "happy vs sad"),
    (r"slow|chill|calm|quiet", r"hype|workout|energetic|loud", "slow vs high-energy"),
]

MATCH_SCORE_THRESHOLD = 0.6


def _first_match(text: str, table: dict):
    """Return the value for the first regex in `table` that appears in `text`."""
    for pattern, value in table.items():
        if re.search(pattern, text, re.IGNORECASE):
            return value
    return None


def parse_request_heuristic(text: str) -> Dict:
    """Offline parser: map keywords to a profile dict. Keys are optional.

    Produces the same keys the recommender already understands:
    genre, mood, energy, valence, likes_acoustic.
    """
    profile: Dict = {}
    genre = _first_match(text, GENRE_KEYWORDS)
    if genre:
        profile["genre"] = genre
    mood = _first_match(text, MOOD_KEYWORDS)
    if mood:
        profile["mood"] = mood
    energy = _first_match(text, ENERGY_KEYWORDS)
    if energy is not None:
        profile["energy"] = energy
    valence = _first_match(text, VALENCE_KEYWORDS)
    if valence is not None:
        profile["valence"] = valence
    if re.search(AVOID_ACOUSTIC_PATTERN, text, re.IGNORECASE):
        acoustic = False
    else:
        acoustic = _first_match(text, ACOUSTIC_KEYWORDS)
    if acoustic is not None:
        profile["likes_acoustic"] = acoustic
    return profile


def detect_conflicts(text: str) -> List[str]:
    """Return a list of contradictions found in the request (empty if none)."""
    found = []
    for left, right, label in CONFLICTS:
        if re.search(left, text, re.IGNORECASE) and re.search(right, text, re.IGNORECASE):
            found.append(label)
    return found


def validate_profile(profile: Dict) -> Dict:
    """Drop any values the dataset can't satisfy. Used on LLM output especially."""
    clean: Dict = {}
    for key, valid_values in (("genre", VALID_GENRES), ("mood", VALID_MOODS)):
        value = profile.get(key)
        if isinstance(value, str):
            normalized = value.strip().casefold()
            match = next(
                (candidate for candidate in valid_values if candidate.casefold() == normalized),
                None,
            )
            if match:
                clean[key] = match
    for key in ("energy", "valence"):
        try:
            v = float(profile[key])
            if 0.0 <= v <= 1.0:
                clean[key] = v
        except (KeyError, TypeError, ValueError):
            pass
    if isinstance(profile.get("likes_acoustic"), bool):
        clean["likes_acoustic"] = profile["likes_acoustic"]
    return clean


# ---------------------------------------------------------------------------
# TEST: does the top-k actually look like what was asked for?
# ---------------------------------------------------------------------------
def evaluate(results: List[Tuple[Dict, float, str]], profile: Dict) -> Tuple[float, Dict[str, float]]:
    """Measure preference alignment for the recommendations, not model confidence.

    Returns (match_score, per_check), with each check and their mean in 0..1.
    Only checks the fields the profile actually asked for.
    """
    if not results:
        return 0.0, {}
    songs = [r[0] for r in results]
    checks: Dict[str, float] = {}

    if "genre" in profile:
        checks["genre"] = sum(s["genre"] == profile["genre"] for s in songs) / len(songs)
    if "mood" in profile:
        checks["mood"] = sum(s["mood"] == profile["mood"] for s in songs) / len(songs)
    for feature in ("energy", "valence"):
        if feature in profile:
            avg = sum(s[feature] for s in songs) / len(songs)
            gap = abs(avg - profile[feature])
            checks[feature] = 1.0 if gap <= 0.2 else round(max(0.0, 1.0 - gap), 2)
    if "likes_acoustic" in profile:
        avg_acousticness = sum(s["acousticness"] for s in songs) / len(songs)
        alignment = avg_acousticness if profile["likes_acoustic"] else 1.0 - avg_acousticness
        checks["acoustic"] = round(max(0.0, min(1.0, alignment)), 2)

    if not checks:               # profile had nothing checkable
        return 0.0, checks
    return round(sum(checks.values()) / len(checks), 2), checks


# ---------------------------------------------------------------------------
# The loop
# ---------------------------------------------------------------------------
def run_agent(
    request_text: str,
    songs: List[Dict],
    client=None,
    k: int = 5,
    max_passes: int = 2,
    threshold: float = MATCH_SCORE_THRESHOLD,
) -> Dict:
    if k < 1:
        raise ValueError("k must be at least 1")
    if max_passes < 1:
        raise ValueError("max_passes must be at least 1")
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("threshold must be between 0 and 1")

    trace: List[str] = []
    log = trace.append

    result = {
        "request": request_text,
        "profile": {},
        "results": [],
        "match_score": 0.0,
        "match_checks": {},
        "weights": dict(DEFAULT_WEIGHTS),
        "warnings": [],
        "needs_human_review": False,
        "message": "",
        "trace": trace,
    }

    # ---- Guardrail 1: empty request --------------------------------------
    if not request_text or not request_text.strip():
        log("PLAN: request is empty — refusing to guess.")
        result.update(needs_human_review=True, message="Please describe what you want to hear.")
        return result
    text = request_text.strip()
    log(f"PLAN: request = {text!r}")

    # ---- Guardrail 2: contradictory request -------------------------------
    conflicts = detect_conflicts(text)
    if conflicts:
        result["warnings"].extend(conflicts)
        log(f"PLAN: conflicting cues found ({', '.join(conflicts)}); will proceed but flag it.")

    # ---- PLAN: LLM parser if available, heuristic otherwise ---------------
    profile: Dict = {}
    if client is not None:
        try:
            raw = client.parse_request(text)
            profile = validate_profile(raw)
            dropped = set(raw) - set(profile)
            log(f"PLAN: LLM parser returned {raw}")
            if dropped:
                log(f"PLAN: dropped invalid LLM fields {sorted(dropped)}")
        except Exception as exc:  # any failure → fall back, never crash
            log(f"PLAN: LLM parser failed ({type(exc).__name__}: {exc}); falling back to heuristics.")
            profile = {}
    if not profile:
        profile = parse_request_heuristic(text)
        log(f"PLAN: heuristic parser produced {profile}")

    # ---- Guardrail 3: nothing understood ----------------------------------
    if not profile:
        log("PLAN: could not extract any preference — stopping instead of recommending blindly.")
        result.update(
            needs_human_review=True,
            message="I couldn't tell what you're in the mood for. Try naming an album, a mood, or an energy level.",
        )
        return result
    result["profile"] = profile

    # ---- ACT / TEST / REFLECT ---------------------------------------------
    weights = dict(DEFAULT_WEIGHTS)
    for attempt in range(1, max_passes + 1):
        results = recommend_songs(profile, songs, k=k, weights=weights)
        log(f"ACT  (pass {attempt}): ranked {len(songs)} songs with weights {weights}")

        match_score, checks = evaluate(results, profile)
        log(f"TEST (pass {attempt}): match_score={match_score} checks={checks}")

        result.update(
            results=results,
            match_score=match_score,
            match_checks=checks,
            weights=dict(weights),
        )
        if match_score >= threshold:
            log(f"REFLECT: match score {match_score} ≥ {threshold} — accepting results.")
            result["message"] = "Recommendations accepted."
            return result

        failing = [name for name, score in checks.items() if score < threshold]
        if attempt < max_passes and failing:
            for name in failing:
                weights[name] = weights[name] * 2
            log(f"REFLECT: low match score on {failing}; doubling those weights and retrying.")
        else:
            break

    # ---- Guardrail 4: still unsure after retrying -------------------------
    log(f"REFLECT: match score {result['match_score']} still below {threshold} after {max_passes} passes — flagging for human review.")
    result.update(
        needs_human_review=True,
        message="Low preference match: the catalog may not have songs matching this request. Please review the results manually.",
    )
    return result