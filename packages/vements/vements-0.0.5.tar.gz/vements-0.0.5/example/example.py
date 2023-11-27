#!/usr/bin/env python

API_KEY = ""
PROJECT_ID = ""
SCOREBOARD_ID = ""

import datetime
import os
import random
import sys

try:
    from vements.api import API
except ImportError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
    try:
        from vements.api import API
    except ImportError:
        raise ImportError("Module vements not found on sys path, nor in parent directory.")


def main():
    player = random.randint(0, 10000)
    api = API(api_key=API_KEY)

    participant = api.participant.create(
        project_id=PROJECT_ID,
        display=f"Example Player {player}",
        external_id=f"example player {player}",
        image=None,
        extra=None,
    )

    print("Participant Created: " + participant["participant_id"])

    for _ in range(5):
        api.scoreboard.record(
            scoreboard_id=SCOREBOARD_ID,
            participant_id=participant["participant_id"],
            value=random.randint(1, 1000),
            recorded=datetime.datetime.now().isoformat(),
        )

    scores = api.scoreboard.scores(scoreboard_id=SCOREBOARD_ID)
    for score in scores:
        print(
            f"Rank: {score['rank']} Player: {score['participant']['display']} Total: {score['total']}"
        )


if __name__ == "__main__":
    main()
