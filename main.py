from ScoreReader import read_score_db_for_specific_player
from ProfileReader import read_profiles
from QuerySongs import SongsDB
from InputParser import input_parser

if __name__ == '__main__':
    profiles = read_profiles(r"E:\EG_Upgrade\Asphyxia\savedata\core.db")
    print("Choose Profiles: ")
    for i, refid in enumerate(profiles):
        print(i, "->", profiles[refid]["cardid"][:8] + "XXXXXXXX")
    index = int(input())
    scores_list = read_score_db_for_specific_player(r"E:\EG_Upgrade\Asphyxia\savedata\sdvx@asphyxia.db", list(profiles.keys())[index])
    songs_db = SongsDB(r"E:\EG_Upgrade\data\others\music_db.xml")
    while True:
        ret = input_parser(songs_db, scores_list)
        if not ret:
            break