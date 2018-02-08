from abc import ABC, abstractmethod
import os
import datetime

import anidbcli.libed2k as libed2k 

API_ENDPOINT_FILE = "FILE size=%d&ed2k=%s"
API_ENDPOINT_EPISODE = "EPISODE eid=%d"
API_ENDPOINT_GROUP = "GROUP gid=%d"
API_ENDPOINT_ANIME = "ANIME aid=%d"


RESULT_FILE = 220

class Operation:
    @abstractmethod
    def Process(self, file): pass

class MylistAddOperation(Operation):
    def __init__(self, connector, output):
        self.connector = connector
        self.output = output
    def Process(self, file):
        pass

class HashOperation(Operation):
    def __init__(self, output):
        self.output = output
    def Process(self, file):
        try:
            link = libed2k.get_ed2k_link(file["path"])
        except Exception as e:
            self.output.error(f"Failed to generate hash: {e}.")
            return False
        file["ed2k"] = link
        file["size"] = os.path.getsize(file["path"])
        self.output.success("Generated ed2k link.")
        return True

class GetEpisodeInfoOperation(Operation):
    def __init__(self, connector, output):
        self.connector = connector
        self.output = output
    def Process(self, file):
        try:
            res = self.connector.send_request(API_ENDPOINT_EPISODE % file["fileinfo"]["eid"])
        except Exception as e:
            self.output.error(f"Failed to get episode info: {e}")
            return False
        if res["code"] != RESULT_FILE:
            self.output.error(f"Failed to get episode info: {res["data"]}")
            return False
        parsed = parse_data(res["data"])
        episodeinfo = {}
        episodeinfo["epno"] = parsed[5]
        episodeinfo["eng"] = parsed[6]
        episodeinfo["romanji"] = parsed[7]
        episodeinfo["kanji"] = parsed[8]
        episodeinfo["aired"] = datetime.datetime.fromtimestamp(int(parsed[9]))

        file["episodeinfo"] = episodeinfo
        self.output.success("Successfully grabbed episode info.")
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
            self.output.error(f"Failed to get file info: {res["data"]}")
            return False
        parsed = parse_data(res["data"])
        fileinfo = {}
        fileinfo["fid"] = int(parsed[0])
        fileinfo["aid"] = int(parsed[1])
        fileinfo["eid"] = int(parsed[2])
        fileinfo["gid"] = int(parsed[3])
        file["fileinfo"] = fileinfo
        self.output.success("Successfully grabbed file info.")
        return True

class GetGroupInfo(Operation):
    def __init__(self, connector, output):
        self.connector = connector
        self.output = output
        self.cache = {}
    def Process(self, file):
        if file["fileinfo"]["gid"] in self.cache:
            groupinfo = self.cache[file["fileinfo"]["gid"]]
        else:
            try:
                res = self.connector.send_request(API_ENDPOINT_GROUP % file["fileinfo"]["gid"])
            except Exception as e:
                self.output.error(f"Failed to get group info: {e}")
                return False
            if res["code"] != RESULT_FILE:
                self.output.error(f"Failed to get group info: {res["data"]}")
                return False
            parsed = parse_data(res["data"])
            groupinfo = {}
            groupinfo["name"] = parsed[5]
            groupinfo["shortname"] = parsed[6]
            self.cache[file["fileinfo"]["gid"]] = groupinfo
            self.output.success("Successfully grabbed group info.")
        file["groupinfo"] = groupinfo       
        return True

class GetAnimeInfo(Operation):
    def __init__(self, connector, output):
        self.connector = connector
        self.output = output
        self.cache = {}
    def Process(self, file):
        if file["fileinfo"]["aid"] in self.cache:
            animeinfo = self.cache[file["fileinfo"]["aid"]]
        else:
            try:
                res = self.connector.send_request(API_ENDPOINT_ANIME % file["fileinfo"]["aid"])
            except Exception as e:
                self.output.error(f"Failed to get anime info: {e}")
                return False
            if res["code"] != RESULT_FILE:
                self.output.error(f"Failed to get anime info: {res["data"]}")
                return False
            parsed = parse_data(res["data"])
            animeinfo = {}
            animeinfo["episodecount"] = int(parsed[2])
            animeinfo["year"] = parsed[10]
            animeinfo["romanji"] = parsed[12]
            animeinfo["kanji"] = parsed[13]
            animeinfo["english"] = parsed[14]          
            self.cache[file["fileinfo"]["aid"]] = animeinfo
            self.output.success("Successfully grabbed anime info.")
        file["animeinfo"] = animeinfo
        return True


def parse_data(raw_data):
    res = raw_data.split("|")
    for idx, item in res:
        item = item.replace("/", "|")
        item = item.replace("`", "'")
        item = item.replace("<br />", "\n")
    return res