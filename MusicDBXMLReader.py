import pprint
import xml.etree.ElementTree as ET
import SDVX_XML


def __read_music_db(path):
    with open(path, encoding='cp932', errors='ignore') as f:
        text = SDVX_XML.translate(f.read())
    root = ET.fromstring(text)
    return root


def __test_xml_query():
    path = r"E:\EG_Upgrade\data\others\music_db.xml"
    with open(path, encoding='cp932', errors='ignore') as f:
        text = SDVX_XML.translate(f.read())
    root = ET.fromstring(text)
    ans = root.findall("./music[@id='639']/difficulty//effected_by")
    for node in ans:
        print(node.text)
    return root


def get_songs_info(path):
    db_xml_root = __read_music_db(path)
    info_all = {}
    for music in db_xml_root:
        id_ = int(music.attrib['id'])
        info_node, diff_node = music[:2]
        meta = __parse_info_node(info_node)
        diff = __parse_diff_node(diff_node)
        info_all[id_] = [meta, diff]
    return info_all


def __parse_info_node(node):
    info = {}
    for child in node:
        info[child.tag] = child.text
    return info


def __parse_diff_node(node):
    # 0 Novice / 1 Advanced / 2 Exhaust / 3 Special (INF, GRV, HVN, VVD) / 4 Maximum
    diff = {k: {} for k in range(5)}
    for i, diff_info in enumerate(node):
        diff[i] = {}
        for child in diff_info:
            diff[i][child.tag] = child.text
    return diff


if __name__ == '__main__':
    pprint.pprint(get_songs_info(r"E:\EG_Upgrade\data\others\music_db.xml"))
