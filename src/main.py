"""
Command line runner for the Music Recommender Simulation.

Pass a natural-language request as an argument, or run interactively.
"""

import argparse
import logging
from typing import List, Optional

from .agent import run_agent
from .recommender import load_songs

logger = logging.getLogger(__name__)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description="Get Taylor Swift song recommendations.")
    parser.add_argument("request", nargs="?", help="What kind of songs you want to hear")
    parser.add_argument("--top-k", type=int, default=5, help="Number of songs to recommend")
    args = parser.parse_args(argv)
    if args.top_k < 1:
        parser.error("--top-k must be at least 1")

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    request = args.request
    if request is None:
        try:
            request = input("What would you like to hear? ")
        except EOFError:
            parser.error("Provide a request argument when running without an interactive terminal.")

    songs = load_songs("data/songs.csv")
    result = run_agent(request, songs, k=args.top_k)

    for entry in result["trace"]:
        logger.info("%s", entry)

    print(f"\nRequest: {result['request']}")
    print(f"Preferences: {result['profile'] or 'none identified'}")
    print(
        f"Preference match score: {result['match_score']:.2f} "
        f"(checks: {result['match_checks']})"
    )
    if result["warnings"]:
        print(f"Warnings: {', '.join(result['warnings'])}")

    for rank, (song, score, explanation) in enumerate(result["results"], start=1):
        print(f"\n{rank}. {song['title']} — {song['artist']}")
        print(f"   Score: {score:.1f}")
        print(f"   Reasons: {explanation}")

    if result["needs_human_review"]:
        logger.warning("%s", result["message"])
    else:
        print(f"\n{result['message']}")


if __name__ == "__main__":
    main()
