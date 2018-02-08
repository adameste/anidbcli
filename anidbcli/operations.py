from abc import ABC, abstractmethod
import os
import datetime

import anidbcli.libed2k as libed2k 

# ed2k,md5,sha1,crc32,resolution,aired,year,romanji,kanji,english,epno,epname,epromanji,epkanji,groupname,shortgroupname
API_ENDPOINT_FILE = "FILE size=%d&ed2k=%s&fmask=0078020800&amask=20E0F0C0"

API_ENDPOINT_MYLYST_ADD = "MYLISTADD size=%d&ed2k=%s&viewed=1"

RESULT_FILE = 220
RESULT_MYLIST_ENTRY_ADDED = 210
RESULT_ALREADY_IN_MYLIST = 310
class Operation:
    @abstractmethod
    def Process(self, file): pass

class MylistAddOperation(Operation):
    def __init__(self, connector, output):
        self.connector = connector
        self.output = output
    def Process(self, file):
        try:
            res = self.connector.send_request(API_ENDPOINT_MYLYST_ADD % (file["size"], file["ed2k"]))
            if res["code"] == RESULT_MYLIST_ENTRY_ADDED:
                self.output.success("Mylist entry added.")
            elif res["code"] == RESULT_ALREADY_IN_MYLIST:
                self.output.warning("Already in mylist.")
            else:
                self.output.error("Couldn't add to mylist: %s" % res["data"])
        except Exception as e:
            self.output.error(f"Failed to add file to mylist: {e}")

        return True

class HashOperation(Operation):
    def __init__(self, output):
        self.output = output
    def Process(self, file):
        try:
            link = libed2k.hash_file(file["path"])
        except Exception as e:
            self.output.error(f"Failed to generate hash: {e}.")
            return False
        file["ed2k"] = link
        file["size"] = os.path.getsize(file["path"])
        self.output.success("Generated ed2k link.")
        return True


class GetFileInfoOperation(Operation):
    def __init__(self, connector, output):
        self.connector = connector
        self.output = output
    def Process(self, file):
        try:
            res = self.connector.send_request(API_ENDPOINT_FILE % (file["size"], file["ed2k"]))
        except Exception as e:
            self.output.error(f"Failed to get file info: {e}")
            return False
        if res["code"] != RESULT_FILE:
            self.output.error("Failed to get file info: %s" % res["data"])
            return False
        parsed = parse_data(res["data"].split("\n")[1])
        fileinfo = {}
        fileinfo["ed2k"] = parsed[1]
        fileinfo["md5"] = parsed[2]
        fileinfo["sha1"] = parsed[3]
        fileinfo["crc32"] = parsed[4]
        fileinfo["resolution"] = parsed[5]
        fileinfo["aired"] = datetime.datetime.fromtimestamp(int(parsed[6]))
        fileinfo["year"] = parsed[7]
        fileinfo["a_romaji"] = parsed[8]
        fileinfo["a_kanji"] = parsed[9]
        fileinfo["a_english"] = parsed[10]
        fileinfo["ep_no"] = parsed[11]
        fileinfo["ep_english"] = parsed[12]
        fileinfo["ep_romaji"] = parsed[13]
        fileinfo["ep_kanji"] = parsed[14]
        fileinfo["g_name"] = parsed[15]
        fileinfo["g_sname"] = parsed[16]
        file["info"] = fileinfo
        self.output.success("Successfully grabbed file info.")
        return True

class RenameOperation(Operation):
    def __init__(self, output, target_path, date_format):
        self.output = output
        self.target_path = target_path
    def Process(self, file):
        pass


def parse_data(raw_data):
    res = raw_data.split("|")
    for idx, item in enumerate(res):
        item = item.replace("<br />", "\n")
        item = item.replace("/", "|")
        item = item.replace("`", "'")
        res[idx] = item
    return res