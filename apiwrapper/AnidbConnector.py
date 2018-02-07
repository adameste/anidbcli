import socket
import encryptors
import hashlib

API_ADDRESS = "api.anidb.net"
API_PORT = 9000
SOCKET_TIMEOUT = 5
MAX_RECEIVE_SIZE = 65536

API_ENDPOINT_ENCRYPT = "ENCRYPT user=%s&type=1"

ENCRYPTION_ENABLED = 209


class AnidbConnector:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET socket.SOCK_DGRAM)
        self.socket.connect((socket.gethostbyname_ex(API_ADDRESS)[2][0], API_PORT))
        self.socket.settimeout(SOCKET_TIMEOUT)
        self.crypto = encryptors.PlainTextCrypto()

    def _set_crypto(self, crypto):
        self.crypto = crypto

    @classmethod
    def create_plain(username, password):
        instance = AnidbConnector()
        instance._login(username, password)
        return instance

    @classmethod
    def create_secure(username, password, api_key):
        intance = AnidbConnector()
        enc_res = instance.send_request(API_ENDPOINT_ENCRYPT % username, False)
        if enc_res["code"] != ENCRYPTION_ENABLED:
            raise Exception(enc_res["data"])
        salt = enc_res["data"].split(" ")[0]
        md5 = hashlib.md5(bytes(api_key + salt, "ascii"))
        instance._set_crypto(encryptors.Aes128TextEncryptor(md5.digest()))
        instance._login(username, password)
        return instance


    def _login(self, username, password):
        pass

    def send_request(self, content, appendSession = True):
        if appendSession:
            if not self.session:
                raise Exception("No session was set")
            content += "&s=%s" % self.session
        self.socket.send(content)
        res = self.socket.recv(MAX_RECEIVE_SIZE)
        response  = dict()
        response["code"] = int(res[:3])
        response["data"] = res[4:]
        return response

        