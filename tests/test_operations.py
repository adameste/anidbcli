import flexmock
import anidbcli.operations as operations
import tempfile
import datetime
import os
import glob

def test_add_ok():
    conn = flexmock.flexmock(send_request=lambda x: {"code": 210, "data": "MYLIST ENTRY ADDED"})
    conn.should_call("send_request").once().with_args("MYLISTADD size=42&ed2k=ABC1234&viewed=1")
    out = flexmock.flexmock()
    out.should_receive("success").once()
    oper = operations.MylistAddOperation(conn, out)
    f = {"size": 42, "ed2k": "ABC1234"}
    oper.Process(f)

def test_add_already_in_mylist():
    conn = flexmock.flexmock(send_request=lambda x: {"code": 310, "data": "ALREADY IN MYLIST"})
    conn.should_call("send_request").once().with_args("MYLISTADD size=42&ed2k=ABC1234&viewed=1")
    out = flexmock.flexmock()
    out.should_receive("warning").once()
    oper = operations.MylistAddOperation(conn, out)
    f = {"size": 42, "ed2k": "ABC1234"}
    oper.Process(f)

def test_add_send_exception():
    conn = flexmock.flexmock()
    conn.should_receive("send_request").once().with_args("MYLISTADD size=42&ed2k=ABC1234&viewed=1").and_raise(Exception)
    out = flexmock.flexmock()
    out.should_receive("error").once()
    oper = operations.MylistAddOperation(conn, out)
    f = {"size": 42, "ed2k": "ABC1234"}
    oper.Process(f)

def test_parse_file_info():
    data = "FILE\n"\
	"2151394|13485|204354|7172|0|0|1064875798|3448d5bd5c28f352006f24582a091c58|"\
	"28d457964c6c348b5d10bf035d33aea6|72b21799ed147d5874ddc792fe545ea9a84dba74|23d62d71||very high|"\
	"www|AAC|128|H264/AVC|5888|1920x1080|mkv|japanese|english|1415|1535760000|"\
	"Boku no Hero Academia (2018) - 21 - What`s the Big Idea? - [HorribleSubs](23d62d71).mkv|"\
	"25|25|2018|TV Series||Boku no Hero Academia (2018)|僕のヒーローアカデミア (2018)|My Hero Academia Season 3|"\
	"僕のヒーローアカデミア (2018)'My Hero Academia Season 3'My Hero Academia Saison 3'나의 히어로 아카데미아 3|"\
	"heroaca3|Boku no Hero Academia Season 3|21|What`s the Big Idea?|Nani o Shitenda yo|何をしてんだよ|HorribleSubs|HorribleSubs"
    conn = flexmock.flexmock()
    conn.should_receive("send_request").once().with_args("FILE size=42&ed2k=ABC1234&fmask=79FAFFE900&amask=F2FCF0C0").and_return({"code": 220, "data": data})
    out = flexmock.flexmock()
    out.should_receive("success").once()
    f = {"size": 42, "ed2k": "ABC1234"}
    oper = operations.GetFileInfoOperation(conn, out)
    oper.Process(f)
    assert f["info"]["crc32"] == "23d62d71"
    assert f["info"]["year"] == "2018"
    assert f["info"]["a_kanji"] == "僕のヒーローアカデミア (2018)"
    assert f["info"]["a_english"] == "My Hero Academia Season 3"
    assert f["info"]["ep_no"] == "21"
    assert f["info"]["ep_english"] == "What's the Big Idea?"
    assert f["info"]["ep_kanji"] == "何をしてんだよ"
    assert f["info"]["resolution"] == "1920x1080"
    assert f["info"]["g_name"] == "HorribleSubs"

def test_parse_file_info_err():
    conn = flexmock.flexmock()
    conn.should_receive("send_request").once().with_args("FILE size=42&ed2k=ABC1234&fmask=79FAFFE900&amask=F2FCF0C0").and_raise(Exception)
    out = flexmock.flexmock()
    out.should_receive("error").once()
    oper = operations.GetFileInfoOperation(conn, out)
    f = {"size": 42, "ed2k": "ABC1234"}
    oper.Process(f)

def test_hash_operation():
    filename = "file.tmp"
    with open(filename, "wb") as f:
            f.write(b"\x6F" * 31457280)
    f = {"path": filename}
    out = flexmock.flexmock(error=lambda x:print(x))
    out.should_receive("success").once()
    oper = operations.HashOperation(out)
    oper.Process(f)
    os.remove(filename)
    assert f["size"] == 31457280
    assert f["ed2k"] == "7e7611fe2ffc72398124dd3f24c4135e"

def test_hash_error():
    filename = "asdasdasdasoasdjasiasd.tmp"
    out = flexmock.flexmock()
    out.should_receive("error").once()
    oper = operations.HashOperation(out)
    f = {"path": filename}
    assert not oper.Process(f) # pipeline should not continue without valid hash

def test_rename_works_with_subtitles():
    filename = "test/abcd.mkv"
    target = ""
    target_expanded = ""
    f = {"path": filename, "info": {}}
    for tag in ("tag_1","tag_2", "tag_3", "tag_4"):
        target += f"%{tag}%"
        target_expanded += tag
        f["info"][tag] = tag
    f["info"]["aired"] = datetime.datetime(2018,2,9)
    target_expanded=target_expanded.replace("aired", "2018-02-09")
    out = flexmock.flexmock(error=lambda x: print(x), warning=lambda x: None)
    out.should_receive("success")
    os_mock = flexmock.flexmock(os)
    glob_mock = flexmock.flexmock(glob)
    os_mock.should_receive("rename").with_args("test/abcd.mkv", target_expanded + ".mkv").once()
    os_mock.should_receive("rename").with_args("test/abcd.srt", target_expanded + ".srt").once()
    os_mock.should_receive("link").with_args("test/abcd.mkv", "test\\" + target_expanded + ".mkv").once()
    os_mock.should_receive("link").with_args("test/abcd.srt", "test\\" + target_expanded + ".srt").once()
    os_mock.should_receive("makedirs").at_least().once()
    lst = [filename, "test/abcd.srt"]
    glob_mock.should_receive("glob").and_return(lst)
    oper = operations.RenameOperation(out, target, "%Y-%m-%d", False, False, False, False)
    oper2 = operations.RenameOperation(out, target, "%Y-%m-%d", False, True, False, True)
    oper.Process(f)
    assert f["path"] != filename # Should be changed for next elements in pipeline
    f["path"] = filename
    oper2.Process(f)