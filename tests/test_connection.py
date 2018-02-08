import flexmock
import hashlib
import socket

import anidbcli.encryptors as encryptors
import anidbcli.anidbconnector as anidbconnector

def test_encryption():
    string = "Hello World!"
    key1 = hashlib.md5(b"key1").digest()
    key2 = hashlib.md5(b"key2").digest()
    crypto1 = encryptors.Aes128TextEncryptor(key1)
    crypto2 = encryptors.Aes128TextEncryptor(key2)
    assert bytes(string, "utf-8") != crypto1.Encrypt(string)
    assert crypto1.Encrypt(string) != crypto2.Encrypt(string)
    assert crypto1.Decrypt(crypto1.Encrypt(string)) == string

def test_unecrypted_initialization():
    sock=flexmock.flexmock(send=())
    flexmock.flexmock(socket, socket=sock)
    sock.should_receive("connect").once()
    sock.should_receive("settimeout").once()
    sock.should_receive("send").with_args(b"AUTH user=username&pass=password&protover=3&client=anidbcli&clientver=1&enc=UTF8").once()
    sock.should_receive("send").with_args(b"TEST t=123&s=YXM21").once()
    sock.should_receive("recv").and_return(b"200 YXM21 LOGIN ACCEPTED").and_return(b"200 OK")
    cli = anidbconnector.AnidbConnector.create_plain("username", "password")
    res = cli.send_request("TEST t=123")
    assert res["code"] == 200

def test_encrypted_initialization():
    sock=flexmock.flexmock(send=())
    flexmock.flexmock(socket, socket=sock)
    key = hashlib.md5(bytes("apikey" + "k1XaZIJD", "ascii")).digest()
    crypto = encryptors.Aes128TextEncryptor(key)
    sock.should_receive("connect").once()
    sock.should_receive("settimeout").once()
    sock.should_receive("send").with_args(b"ENCRYPT user=username&type=1").once()    
    sock.should_receive("send").with_args(crypto.Encrypt("AUTH user=username&pass=password&protover=3&client=anidbcli&clientver=1&enc=UTF8")).once()
    sock.should_receive("send").with_args(crypto.Encrypt("TEST t=123&s=YXM21")).once()
    sock.should_receive("recv").and_return(b"209 k1XaZIJD ENCRYPTION ENABLED").and_return(crypto.Encrypt("200 YXM21 LOGIN ACCEPTED")).and_return(crypto.Encrypt("200 OK"))
    cli = anidbconnector.AnidbConnector.create_secure("username", "password", "apikey")
    res = cli.send_request("TEST t=123")
    assert res["code"] == 200

def test_udp_send_retry():
    sock=flexmock.flexmock(send=())
    flexmock.flexmock(socket, socket=sock)
    sock.should_receive("connect").once()
    sock.should_receive("settimeout").once()
    sock.should_receive("send").at_least().times(2)
    sock.should_receive("recv").and_raise(Exception)
    try:
        anidbconnector.AnidbConnector.create_plain("username", "password")
        assert False
    except:
        assert True
    
