from functools import lru_cache
import numpy as np


# Return {song_id: {diffnum:score}}
def __map_songs_to_scores(query_response, score_list):
    ans = {}
    # print(score_list)
    for song_id, diffs in query_response.items():
        ans[song_id] = {}
        for diff in diffs:
            if diff > 30:
                diff = 3
            if song_id not in score_list:
                ans[song_id][diff] = 0
            else:
                ans[song_id][diff] = score_list[song_id][diff]
    return ans


# Calculate score metrics.
# Lowerbound is a filter of scores. eg. Only calc average for played songs.
# @lru_cache(500)
def __squeeze_score(query_response, score_list, lowerbound=0):
    scores = __map_songs_to_scores(query_response, score_list)
    res = []
    for song_id, score_dict in scores.items():
        for diff, score in score_dict.items():
            if score >= lowerbound:
                res.append(score)
    if len(res) == 0:
        print("WARNING: No songs are queried. Please reset queries.")
        res = [0]
    return np.array(res)


def cal_average(song_db, score_list, lowerbound=0):
    return np.average(__squeeze_score(song_db.current_query_response, score_list, lowerbound))


def cal_median(song_db, score_list, lowerbound=0):
    return np.median(__squeeze_score(song_db.current_query_response, score_list, lowerbound))
