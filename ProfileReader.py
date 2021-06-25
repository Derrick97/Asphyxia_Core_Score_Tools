import jsonlines


def read_profiles(path):
    cards = {}
    with jsonlines.open(path) as reader:
        for obj in reader:
            if obj.get("__s") == "card":
                refid, info = _reformat_card(obj)
                cards[refid] = info
    return cards


def _reformat_card(item):
    refid = item["__refid"]
    cid = item["cid"]
    id = item["_id"]
    create_date = item["createdAt"]["$$date"]
    return refid, {"refid": refid, "id": id, "cardid": cid, "create_date": create_date}


if __name__ == '__main__':
    profiles = read_profiles(r"E:\EG_Upgrade\Asphyxia\savedata\core.db")
    print(profiles)