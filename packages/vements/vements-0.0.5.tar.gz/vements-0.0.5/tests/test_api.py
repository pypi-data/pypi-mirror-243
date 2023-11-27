#!/usr/bin/env python

# Copyright 2023 Monster Street Systems LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# NB: This is a generated file; any changes will be lost.

from datetime import datetime
from random import choice

from faker import Faker
from requests import post

from vements import api, client, config, types


class Setup:
    def __init__(self):
        tags = {"development", "host", "substitute"}

        cc = client.ClientConfig(api_key="has to be something to skip env check", tags=tags)
        print("server url:", cc.server_url)

        try:
            self.db = post(cc.server_url + "-/database").json()
        except Exception as e:
            import sys

            print("could not read test db:", e, file=sys.stderr)
            sys.exit(1)

        api_key = [k for k in self.db["api_key"] if k["capability"] == "rw"][0]
        api_key_v = f"{api_key['project_id']}:{api_key['api_key_id']}"
        print("api key:", api_key_v)

        self.client = client.Client(
            client_config=client.ClientConfig(api_key=api_key_v, tags=tags)
        )
        self.api = api.API(client=self.client, output=api.Output.OBJECT)
        self.fake = Faker()

    def get_value(self, key):
        if key == "recorded":
            return f"{datetime.utcnow().isoformat()}"
        project_id = self.client.api_key.split(":")[0]
        if key == "project_id":
            return project_id
        resource = key.split("_")[0]
        resources = [r for r in self.db[resource] if r["project_id"] == project_id]
        return choice(resources)[f"{resource}_id"] if resources else None

    def get_random(self, key):
        if key == "display":
            return self.fake.name()
        if key == "rank_dir":
            return choice(["asc", "desc"])
        if key == "public":
            return choice([False, True])
        if key == "external_id":
            return self.fake.bban()
        if key == "image":
            return ""
        if key == "extra":
            return dict()
        return None


def test_achievement_leaderboard():
    setup = Setup()

    params = {}
    params["achievement_id"] = setup.get_value("achievement_id")
    print("params:", params)

    call = setup.api.achievement.leaderboard
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.AchievementLeaderboardResponse)


def test_achievement_record():
    setup = Setup()

    params = {}
    params["achievement_id"] = setup.get_value("achievement_id")
    params["participant_id"] = setup.get_random("participant_id")
    params["value"] = setup.get_random("value")
    params["recorded"] = setup.get_random("recorded")
    print("params:", params)

    call = setup.api.achievement.record
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.AchievementProgressResponse)


def test_participant_progress():
    setup = Setup()

    params = {}
    params["participant_id"] = setup.get_value("participant_id")
    print("params:", params)

    call = setup.api.participant.progress
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ParticipantProgressResponse)


def test_participant_scores():
    setup = Setup()

    params = {}
    params["participant_id"] = setup.get_value("participant_id")
    print("params:", params)

    call = setup.api.participant.scores
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ParticipantScoresResponse)


def test_scoreboard_record():
    setup = Setup()

    params = {}
    params["scoreboard_id"] = setup.get_value("scoreboard_id")
    params["participant_id"] = setup.get_random("participant_id")
    params["value"] = setup.get_random("value")
    params["recorded"] = setup.get_random("recorded")
    print("params:", params)

    call = setup.api.scoreboard.record
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ScoreboardScoreResponse)


def test_scoreboard_scores():
    setup = Setup()

    params = {}
    params["scoreboard_id"] = setup.get_value("scoreboard_id")
    params["from_"] = None
    params["to"] = None
    print("params:", params)

    call = setup.api.scoreboard.scores
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ScoreboardScoresResponse)


def test_achievement_list():
    setup = Setup()

    params = {}
    params["project_id"] = setup.get_value("project_id")
    params["limit"] = None
    params["offset"] = None
    print("params:", params)

    call = setup.api.achievement.list
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.AchievementListResponse)


def test_achievement_create():
    setup = Setup()

    params = {}
    params["project_id"] = setup.get_value("project_id")
    params["display"] = setup.get_random("display")
    params["goal"] = setup.get_random("goal")
    params["repeats"] = setup.get_random("repeats")
    params["locked_image"] = setup.get_random("locked_image")
    params["unlocked_image"] = setup.get_random("unlocked_image")
    params["position"] = setup.get_random("position")
    params["public"] = setup.get_random("public")
    params["extra"] = setup.get_random("extra")
    print("params:", params)

    call = setup.api.achievement.create
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.AchievementCreateResponse)


def test_achievement_read():
    setup = Setup()

    params = {}
    params["achievement_id"] = setup.get_value("achievement_id")
    print("params:", params)

    call = setup.api.achievement.read
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.AchievementReadResponse)


def test_achievement_update():
    setup = Setup()

    params = {}
    params["achievement_id"] = setup.get_value("achievement_id")
    params["display"] = setup.get_random("display")
    params["goal"] = setup.get_random("goal")
    params["repeats"] = setup.get_random("repeats")
    params["locked_image"] = setup.get_random("locked_image")
    params["unlocked_image"] = setup.get_random("unlocked_image")
    params["position"] = setup.get_random("position")
    params["public"] = setup.get_random("public")
    params["extra"] = setup.get_random("extra")
    print("params:", params)

    call = setup.api.achievement.update
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.AchievementUpdateResponse)


def test_achievement_delete():
    setup = Setup()

    params = {}
    params["achievement_id"] = setup.get_value("achievement_id")
    print("params:", params)

    call = setup.api.achievement.delete
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.AchievementDeleteResponse)


def test_participant_list():
    setup = Setup()

    params = {}
    params["project_id"] = setup.get_value("project_id")
    params["limit"] = None
    params["offset"] = None
    print("params:", params)

    call = setup.api.participant.list
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ParticipantListResponse)


def test_participant_create():
    setup = Setup()

    params = {}
    params["project_id"] = setup.get_value("project_id")
    params["display"] = setup.get_random("display")
    params["external_id"] = setup.get_random("external_id")
    params["image"] = setup.get_random("image")
    params["extra"] = setup.get_random("extra")
    print("params:", params)

    call = setup.api.participant.create
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ParticipantCreateResponse)


def test_participant_read():
    setup = Setup()

    params = {}
    params["participant_id"] = setup.get_value("participant_id")
    print("params:", params)

    call = setup.api.participant.read
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ParticipantReadResponse)


def test_participant_update():
    setup = Setup()

    params = {}
    params["participant_id"] = setup.get_value("participant_id")
    params["display"] = setup.get_random("display")
    params["external_id"] = setup.get_random("external_id")
    params["image"] = setup.get_random("image")
    params["extra"] = setup.get_random("extra")
    print("params:", params)

    call = setup.api.participant.update
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ParticipantUpdateResponse)


def test_participant_delete():
    setup = Setup()

    params = {}
    params["participant_id"] = setup.get_value("participant_id")
    print("params:", params)

    call = setup.api.participant.delete
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ParticipantDeleteResponse)


def test_scoreboard_list():
    setup = Setup()

    params = {}
    params["project_id"] = setup.get_value("project_id")
    params["limit"] = None
    params["offset"] = None
    print("params:", params)

    call = setup.api.scoreboard.list
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ScoreboardListResponse)


def test_scoreboard_create():
    setup = Setup()

    params = {}
    params["project_id"] = setup.get_value("project_id")
    params["display"] = setup.get_random("display")
    params["rank_dir"] = setup.get_random("rank_dir")
    params["public"] = setup.get_random("public")
    params["extra"] = setup.get_random("extra")
    print("params:", params)

    call = setup.api.scoreboard.create
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ScoreboardCreateResponse)


def test_scoreboard_read():
    setup = Setup()

    params = {}
    params["scoreboard_id"] = setup.get_value("scoreboard_id")
    print("params:", params)

    call = setup.api.scoreboard.read
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ScoreboardReadResponse)


def test_scoreboard_update():
    setup = Setup()

    params = {}
    params["scoreboard_id"] = setup.get_value("scoreboard_id")
    params["display"] = setup.get_random("display")
    params["rank_dir"] = setup.get_random("rank_dir")
    params["public"] = setup.get_random("public")
    params["extra"] = setup.get_random("extra")
    print("params:", params)

    call = setup.api.scoreboard.update
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ScoreboardUpdateResponse)


def test_scoreboard_delete():
    setup = Setup()

    params = {}
    params["scoreboard_id"] = setup.get_value("scoreboard_id")
    print("params:", params)

    call = setup.api.scoreboard.delete
    result = call(**params)
    print("result:", result)

    assert result
    # assert isinstance(result, types.ScoreboardDeleteResponse)

