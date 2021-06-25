import sys
import os
from QuerySongs import SongsDB
import pprint
import Utils


def input_parser(songs_db: SongsDB, score_list):
    print("Enter your query:")
    print("1. Select Song Level Range (1-20).")
    print("2. Select Generation Range (1-6).")
    print("3. Calculate Average Score For the Current Selected Songs.")
    print("4. Calculate Median Score For the Current Selected Songs.")
    print("5. Reset the Query.")
    print("6. Dump the current selected song list to a file.")
    print("0. See you next time.")
    __prompt()
    choice = input()
    choice = str(choice)
    if str(choice).lower() == "nmsl":
        __easter_egg_NMSL()
        return 1

    # if choice < 0 or choice > 5:
    #     print("Not a valid choice.")
    #     return 1
    if choice == '0':
        return 0
    elif choice == '1' or choice.lower() == 'level':
        print(
            "Enter one or two number. If one number: only query this level. If two number: query songs in this range.")
        lowerbound, upperbound = __read_range()
        while not (1 <= lowerbound <= upperbound <= 20):
            print("Invalid level range: should range from 1-20.")
            lowerbound, upperbound = __read_range()
        songs_db.filter_levels(lowerbound, upperbound)
        print("Query set.")
    elif choice == '2' or choice.lower() == 'generation':
        print(
            "Enter one or two number. If one number: only query this generation. If two number: query songs in this "
            "range.")
        lowerbound, upperbound = __read_range()
        while not (1 <= lowerbound <= upperbound <= 6):
            print("Invalid generation range: should range from 1-6.")
            lowerbound, upperbound = __read_range()
        songs_db.filter_generations(lowerbound, upperbound)
        print("Query set.")
    elif choice == '3' or choice.lower() == 'average':
        score_lowerbound = __read_lowerbound()
        print("Current selected songs:")
        print(songs_db)
        # print("Total:", songs_db.current_query_response_size)
        print("Total:", len(songs_db.current_query_response))
        pprint.pprint(songs_db.current_queries)
        print("Average:", Utils.cal_average(songs_db, score_list, lowerbound=score_lowerbound))
    elif choice == '4' or choice.lower() == 'median':
        print("Current selected songs:")
        # print("Total:", songs_db.current_query_response_size)
        pprint.pprint(songs_db.current_queries)
        print("Median: ", Utils.cal_median(songs_db, score_list))
    elif choice == '5' or choice.lower() == 'reset':
        print("Resetting queries...")
        songs_db.load_default()
        print("Resetting queries Done.")
    elif choice == '6' or choice.lower() == 'dump':
        print("Total selected songs:", len(songs_db.current_queries))
        __dump_music_info(songs_db)
    else:
        print("Invalid choice. Please enter the corresponding number of label.")
    return 1



def __read_range():
    __prompt()
    line = input()
    line = line.strip("\t\n ").split()
    if len(line) == 2:
        lowerbound, upperbound = map(int, line)
    else:
        lowerbound = int(line[0])
        upperbound = lowerbound
    return lowerbound, upperbound


def __read_lowerbound():
    __prompt()
    print("Set lowerbound for calculation: (eg. 9000000 only consider songs with scores over 9000000)")
    while True:
        try:
            lowerbound = int(input())
            if 0 <= lowerbound <= 10000000:
                return lowerbound
        except:
            print("Illegal input score: Not a integer.")


def __dump_music_info(songs_db):
    print("Specify the name of the song list file. If blank, the name with be music_list.txt.")
    __prompt()
    filename = str(input())
    try:
        with open(filename, "w+", encoding='cp932', errors='ignore') as f:
            file_str = songs_db.get_song_list()
            for key in file_str:
                f.writelines(key + '\n')
        print('Music list created at', filename)
    except OSError:
        print('Illegal Filename, please retry.')



def __easter_egg_NMSL():
    print("敢这么跟我说话，你妈是批量生产？")


def __easter_egg_others():
    raise NotImplementedError


def __prompt():
    print("> ", end="")