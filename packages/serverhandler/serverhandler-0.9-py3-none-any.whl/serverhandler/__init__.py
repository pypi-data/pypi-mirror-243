import urllib.request
import urllib.parse
import random
def open():
    key = random.randint(0, 9999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
    if not f"\n{str(key)}\n" in urllib.request.urlopen("http://advanced.figit.club/serverhandler/servers.txt"):
        urllib.request.urlopen("http://advanced.figit.club/serverhandler/open.php", data=urllib.parse.urlencode({"key": key}).encode())
    return key
def receive(server):
    return urllib.request.urlopen(f"http://advanced.figit.club/serverhandler/{server}/output.txt").read().decode("utf-8")
def send(server, message):
    urllib.request.urlopen("http://advanced.figit.club/serverhandler/alter.php", data=urllib.parse.urlencode({"server": server, "message": message}).encode())
def append(server, message):
    urllib.request.urlopen("http://advanced.figit.club/serverhandler/append.php", data=urllib.parse.urlencode({"server": server, "message": message}).encode())