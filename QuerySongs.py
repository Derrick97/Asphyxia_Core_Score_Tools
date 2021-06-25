from functools import lru_cache
from MusicDBXMLReader import get_songs_info
import pprint

diff_names = {0:'NOV', 1:'ADV', 2:'EXH', 31:'INF', 32:'GRV', 33:'HVN', 34:'VVD', 4:'MXM'}


class SongsDB:
    def __init__(self, db_path):
        self.db_path = db_path
        self.songs_info = get_songs_info(db_path)
        self.default_response = {}
        self.current_query_response = {}
        self.current_query_response_size = 0
        self.load_default()
        self.current_queries = {}

    # Query Response Form: {song_id: [diffs]}

    # Exposed API 1: Query songs from specific level range.
    def filter_levels(self, lowerbound, upperbound):
        assert 1 <= lowerbound <= upperbound <= 20
        should_del_ids = set()
        for song_id, diffs in self.current_query_response.items():
            should_del = set()
            for diff in diffs:
                diff_num = int(self.songs_info[song_id][1][int(str(diff)[0])].get('difnum', 0))
                if lowerbound <= diff_num <= upperbound:
                    continue
                else:
                    should_del.add(diff)
            if len(should_del) == len(diffs):
                should_del_ids.add(song_id)
            self.current_query_response[song_id] = set(diffs).difference(should_del)
            self.current_query_response_size -= len(should_del)
        for id in should_del_ids:
            del self.current_query_response[id]
        self.__merge_queries("FILTER_LEVEL", [lowerbound, upperbound])

    # Exposed API 2: Query songs from specific generation range.
    def filter_generations(self, lowerbound, upperbound):
        assert 1 <= lowerbound <= upperbound <= 6
        should_del_songs = set()
        for song_id, diffs in self.current_query_response.items():
            should_del = set()
            if lowerbound <= int(self.songs_info[song_id][0]['version']) <= upperbound:
                for diff in diffs:
                    if diff > 30:
                        inf_gen = diff - 30 + 1
                        if lowerbound <= inf_gen <= upperbound:
                            continue
                        should_del.add(diff)
                self.current_query_response[song_id] = set(diffs).difference(should_del)
                self.current_query_response_size -= len(should_del)
                if len(should_del) == len(diffs):
                    should_del_songs.add(song_id)
            else:
                should_del_this = True
                self.current_query_response_size -= len(diffs)
                inf_diff = max(diffs)
                if inf_diff > 30:
                    inf_gen = inf_diff - 30 + 1
                    if lowerbound <= inf_gen <= upperbound:
                        should_del_this = False
                        self.current_query_response[song_id] = {inf_diff}
                        self.current_query_response_size += 1
                if should_del_this:
                    should_del_songs.add(song_id)
        for song_id in should_del_songs:
            self.current_query_response_size -= len(self.current_query_response[song_id])
            del self.current_query_response[song_id]
        self.__merge_queries("FILTER_GENERATION", [lowerbound, upperbound])

    # Exposed API: Query songs from specific diff range.
    def filter_diff(self, diff_range):
        raise NotImplementedError

    def load_default(self):
        size = 0
        for song_id, (meta, diffs) in self.songs_info.items():
            self.default_response[song_id] = [0, 1, 2]
            inf_ver = int(meta['inf_ver'])
            size += 3
            if inf_ver:
                diff = (inf_ver - 1) + 30
                self.default_response[song_id].append(diff)
                size += 1
            if len(diffs) == 5:
                self.default_response[song_id].append(4)
                size += 1
        self.current_query_response = dict(self.default_response)
        self.current_queries = {}
        self.current_query_response_size = size

    # Score list form: {song_id: {diffnum: score}}

    # Map any dictionary with song id as keys to readable lines.
    def __map_id_to_songs(self):
        res = {}
        for k, v in self.current_query_response.items():
            new_v = []
            for diff in v:
                new_v.append(diff_names[diff])
            res[self.songs_info[k][0]['title_name']] = new_v
        return res

    def get_song_list(self):
        return self.__map_id_to_songs().keys()


    def __str__(self):
        return pprint.pformat(self.__map_id_to_songs())

    def __merge_queries(self, query_name, query_param):
        def merge_range(r1, r2):
            s1, e1 = r1
            s2, e2 = r2
            if e1 < s2 or e2 < s1:
                return [-1, -1]
            if s1 <= s2:
                return [s2, e1]
            else:
                return [e2, s1]

        if query_name in self.current_queries:
            self.current_queries[query_name] = merge_range(self.current_queries[query_name], query_param)
        else:
            self.current_queries[query_name] = query_param

    def force_refresh(self):
        self.songs_info = get_songs_info(self.db_path)
        self.load_default()


if __name__ == '__main__':
    pass
    # path = r"E:\EG_Upgrade\data\others\music_db.xml"
    # db = read_music_db(path)
    # all_info = get_songs_info(db)
    # print(all_info[1516])
