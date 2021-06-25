import jsonlines
from sortedcontainers import SortedDict


def read_score_db_for_specific_player(score_db_path, refid):
    scores = SortedDict()
    with jsonlines.open(score_db_path) as reader:
        for obj in reader:
            if obj.get("collection") == "music" and obj.get("__refid") == refid:
                music_id = obj["mid"]
                difficulty = obj["type"]
                score = obj["score"]
                if music_id not in scores:
                    scores[music_id] = {k:0 for k in range(5)}
                scores[music_id][difficulty] = max(scores[music_id][difficulty], score)
    return scores

