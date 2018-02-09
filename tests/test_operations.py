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
    data = """FILE
1949545|adffdbb12954b0b7167e38a9ad2bd5b8|37af968c7f079546d9ba0d62f1c1524d|30b1a10f3761258e331baaa61b4c5b9e604c8919|44054144|1920x1080|1499385600|2017`-2017|Made in Abyss|Japanese anime name|Made in Abyss|01<br />|The City of the Great Pit|Oona no Machi|Japanese/ episode name|HorribleSubs|HorribleSubs"""
    conn = flexmock.flexmock()
    conn.should_receive("send_request").once().with_args("FILE size=42&ed2k=ABC1234&fmask=0078020800&amask=20E0F0C0").and_return({"code": 220, "data": data})
    out = flexmock.flexmock()
    out.should_receive("success").once()
    f = {"size": 42, "ed2k": "ABC1234"}
    oper = operations.GetFileInfoOperation(conn, out)
    oper.Process(f)
    assert f["info"]["crc32"] == "44054144"
    assert f["info"]["year"] == "2017'-2017"
    assert f["info"]["a_kanji"] == "Japanese anime name"
    assert f["info"]["a_english"] == "Made in Abyss"
    assert f["info"]["ep_no"] == "01\n"
    assert f["info"]["ep_english"] == "The City of the Great Pit"
    assert f["info"]["ep_kanji"] == "Japanese| episode name"
    assert f["info"]["resolution"] == "1920x1080"
    assert f["info"]["g_name"] == "HorribleSubs"

def test_parse_file_info_err():
    conn = flexmock.flexmock()
    conn.should_receive("send_request").once().with_args("FILE size=42&ed2k=ABC1234&fmask=0078020800&amask=20E0F0C0").and_raise(Exception)
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
    for tag in operations.TAGS:
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
    os_mock.should_receive("rename").with_args("test/abcd.mkv", "test\\" + target_expanded + ".mkv").once()
    os_mock.should_receive("rename").with_args("test/abcd.srt", "test\\" + target_expanded + ".srt").once()
    os_mock.should_receive("makedirs").at_least().once()
    lst = [filename, "test/abcd.srt"]
    glob_mock.should_receive("glob").and_return(lst)
    oper = operations.RenameOperation(out, target, "%Y-%m-%d", False, False)
    oper2 = operations.RenameOperation(out, target, "%Y-%m-%d", False, True)
    oper.Process(f)
    assert f["path"] != filename # Should be changed for next elements in pipeline
    f["path"] = filename
    oper2.Process(f)