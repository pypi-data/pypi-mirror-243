import warnings
warnings.filterwarnings("ignore")

__author__ = 'mr moorgh'
__version__ = 1.0

from sys import version_info
if version_info[0] == 2: # Python 2.x
    from mrai import *
elif version_info[0] == 3: # Python 3.x
    from mrai.mrai import *





import requests
import json

version="1.0.1"


class AIError(Exception):
    pass

class TranslateError(Exception):
    pass

class NoInternet(Exception):
    pass

def getlatest():
    global version
    try:
        latest=requests.get(f"https://mrapi.dachhost.top/pyapi.php?ver={version}")
        ver=json.loads(latest)
        if ver["updated"] == False:
            file=open("pyai.py","w")
            file.write(requests.get(ver["get_update_from"]))
            file.close()
            return "Updated PyAPI To Latest"
    except:
        return "No Need"

class ai():
    def bard(query):
        api=requests.get(f"https://mrapi.dachhost.top/api/apitest/gbard.php?question={query}").text
        try:
            return api
        except Exception as er:
            raise NoInternet("Please Connect To Internet To Use This AI")
    def gpt(query):
        query=query.replace(" ","-")
        api=requests.get(f"https://mrapi.dachhost.top/api/chatbot.php?key=testkey&question={query}").text
        result=json.loads(api)
        try:
            return result["javab"]
        except KeyError:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off")
        except Exception as er:
            raise NoInternet("Please Connect To Internet To Use This AI")
        
    def gpt4(query):
        print("Warning: gpt4 may be slow in most cases")
        api=requests.get(f"https://mrapi.dachhost.top/api/gpt4.php?question={query}").text
        try:
            return api
        except KeyError:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off")

    def evilgpt(query):
        api=requests.get(f"https://mrapi.dachhost.top/api/evilgpt.php?key=testkey&emoji=🗿&soal={query}").text
        result=json.loads(api)
        try:
            return result["javab"]
        except KeyError:
            raise AIError("Failed To Get Answer Make Sure That You Are Connected To Internet & vpn is off")
        except Exception as er:
            raise NoInternet("Please Connect To Internet To Use This AI")

class api():
    def translate(to,text):
        api=requests.get(f"https://mrapi.dachhost.top/api/translate.php?to={to}&text={text}").text
        result=json.loads(api)
        try:
            return result["translate"]
        except KeyError:
            raise TranslateError("Translate Error For Lang {to}")
        
    def ocr(to,url):
        api=requests.get(f"https://mrapi.dachhost.top/api/ocr.php?url={url}&lang={to}").text
        result=json.loads(api)
        try:
            return result["result"]
        except KeyError:
            raise AIError("Error In OCR Lang {to}")
