import sys
import os
import json
import time
import requests
import random
from base64 import b64decode
from urllib.parse import unquote
from telethon import TelegramClient, sync, events
from telethon.tl.functions.messages import RequestWebViewRequest
from telethon.errors import SessionPasswordNeededError
from phonenumbers import is_valid_number as valid_number, parse as pp
from colorama import *

init(autoreset=True)

merah = Fore.LIGHTRED_EX
putih = Fore.LIGHTWHITE_EX
hijau = Fore.LIGHTGREEN_EX
kuning = Fore.LIGHTYELLOW_EX
biru = Fore.LIGHTBLUE_EX
reset = Style.RESET_ALL

peer = "onchaincoin_bot"


class OnchainBot:
    def __init__(self):
        self.tg_data = None
        self.bearer = None
        self.peer = "onchaincoin_bot"

    def log(self, message):
        year, mon, day, hour, minute, second, a, b, c = time.localtime()
        mon = str(mon).zfill(2)
        hour = str(hour).zfill(2)
        minute = str(minute).zfill(2)
        second = str(second).zfill(2)
        print(f"{biru}[{year}-{mon}-{day} {hour}:{minute}:{second}] {message}")

    def countdown(self, t):
        while t:
            menit, detik = divmod(t, 60)
            jam, menit = divmod(menit, 60)
            jam = str(jam).zfill(2)
            menit = str(menit).zfill(2)
            detik = str(detik).zfill(2)
            print(f"waiting until {jam}:{menit}:{detik} ", flush=True, end="\r")
            t -= 1
            time.sleep(1)
        print("                          ", flush=True, end="\r")

    def login(self, phone):
        session_folder = "session"
        api_id = 2040
        api_hash = "b18441a1ff607e10a989891a5462e627"

        if not os.path.exists(session_folder):
            os.makedirs(session_folder)

        if not valid_number(pp(phone)):
            self.log(f"{merah}phone number invalid !")
            sys.exit()

        client = TelegramClient(
            f"{session_folder}/{phone}", api_id=api_id, api_hash=api_hash
        )
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
                code = input(f"{putih}input login code : ")
                client.sign_in(phone=phone, code=code)
            except SessionPasswordNeededError:
                pw2fa = input(f"{putih}input password 2fa : ")
                client.sign_in(phone=phone, password=pw2fa)

        me = client.get_me()
        first_name = me.first_name
        last_name = me.last_name
        username = me.username
        self.log(f"{putih}Login as {hijau}{first_name} {last_name}")
        res = client(
            RequestWebViewRequest(
                peer=self.peer,
                bot=self.peer,
                platform="Android",
                url="https://db4.onchaincoin.io/",
                from_bot_menu=False,
            )
        )
        self.tg_data = unquote(res.url.split("#tgWebAppData=")[1]).split(
            "&tgWebAppVersion="
        )[0]
        # print(self.tg_data)
        return self.tg_data

    def get_info(self,bearer):
        _url = "https://db4.onchaincoin.io/api/info"
        _headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.5",
            "authorization": f"Bearer {bearer}",
            "referer": "https://db4.onchaincoin.io/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "te": "trailers",
            "content-length": "0",
        }
        res = requests.get(_url, headers=_headers, timeout=100)
        if res.status_code != 200:
            if "Invalid token" in res.text:
                return "need_reauth"

        name = res.json()["user"]["fullName"]
        energy = res.json()["user"]["energy"]
        max_energy = res.json()["user"]["maxEnergy"]
        league = res.json()["user"]["league"]
        clicks = res.json()["user"]["clicks"]
        coins = res.json()["user"]["coins"]
        self.log(f"{hijau}full name : {putih}:{name}")
        self.log(f"{putih}total coins : {hijau}{coins}")
        self.log(f"{putih}total clicks : {hijau}{clicks}")
        self.log(f"{putih}total energy : {hijau}{energy}")
        print("~" * 50)

    def on_login(self,tg_data):
        _url = "https://db4.onchaincoin.io/api/validate"
        _data = {"hash": tg_data}
        _headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "content-length": str(len(json.dumps(_data))),
            "origin": "https://db4.onchaincoin.io",
            "referer": "https://db4.onchaincoin.io/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "te": "trailers",
        }
        res = requests.post(_url, json=_data, headers=_headers, timeout=100)
        if res.status_code != 200:
            print(res.text)
            sys.exit()

        if res.json()["success"] is False:
            print(res.text)
            sys.exit()

        open('token','w').write(res.json()['token'])
        token = res.json()['token']
        header,payload,sign = token.split('.')
        decode = b64decode(payload + '==').decode('utf-8')
        gelo = json.loads(decode)
        gelo["token"] = token
        open('token.json','w').write(json.dumps(gelo,indent=4))
        return True
        
    def click(self,bearer,click,min_energy):
        url = "https://db4.onchaincoin.io/api/klick/myself/click"
        _headers = {
            "user-agent": "Mozilla/5.0 (Linux; Android 11; SAMSUNG SM-G973U) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/14.2 Chrome/87.0.4280.141 Mobile Safari/537.36",
            "accept": "application/json, text/plain, */*",
            "accept-language": "en-US,en;q=0.5",
            "content-type": "application/json",
            "authorization": f"Bearer {bearer}",
            "content-length": "12",
            "origin": "https://db4.onchaincoin.io",
            "referer": "https://db4.onchaincoin.io/",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "te": "trailers",
        }

        try:
            _data = {"clicks": click}
            res = requests.post(url, json=_data, headers=_headers, timeout=10)

            if "Insufficient energy" in res.text:
                self.log(merah + "Insufficient energy")
                return "insufficient_energy"

            clicks = res.json()["clicks"]
            coins = res.json()["coins"]
            energy = res.json()["energy"]
            self.log(f"{hijau}click : {putih}{click}")
            self.log(f"{hijau}total clicks : {putih}{clicks}")
            self.log(f"{hijau}total coins : {putih}{coins}")
            self.log(f"{hijau}remaining energy : {putih}{energy}")
            if int(energy) < min_energy:
                return 'energy_limit'

            return True

        except (
            requests.exceptions.ReadTimeout,
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout,
        ) as e:
            self.log(f"{merah} {e}")
            return False
    
    def refresh_token(self):
        data = json.loads(open('token.json','r').read())
        return data
            
    def main(self):
        banner = f"""
    {hijau}Auto tap-tap @onchaincoin_bot
    
    {biru}By t.me/AkasakaID
    github : @AkasakaiD{reset}

    {kuning}Warning
    All risks are borne by the user
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner) 

        if not os.path.exists("tg_data"):
            print(f"{putih}example input : +628169696969")
            phone = input(f"{hijau}input telegram phone number : {putih}")
            print()
            data = self.login(phone)
            open("tg_data", "w").write(data)
        
        if not os.path.exists('token.json'):
            open('token.json','w').write(json.dumps({
                "username":"",
                "id":"",
                "iat": "1600000000",
                "exp": "1600000000"
            }))

        tg_data = open("tg_data", "r").read()
        read_config = open("config.json", "r").read()
        load_config = json.loads(read_config)
        interval = load_config["interval"]
        sleep = load_config["sleep"]
        min_energy = load_config["min_energy"]
        click_range = load_config["click_range"]
        start = click_range["start"]
        end = click_range["end"]
        if int(start) > int(end):
            self.log(f'{merah}the value of click range end must be higher than start value !')
            sys.exit()

        token = self.refresh_token()
        if int(time.time()) > int(token['exp']):
            self.on_login(tg_data)
            token = self.refresh_token()
        
        self.get_info(token['token'])

        while True:
            click = random.randint(int(start),int(end))
            now = int(time.time())
            if now > int(token["exp"]):
                self.on_login(tg_data)
                token = self.refresh_token()
            res = self.click(token['token'],click,min_energy)
            print('~' * 50)
            if res == 'energy_limit':
                self.log(f'{kuning}limit energy reacted !')
                self.log(f'{kuning}active sleepzz mode zzzzzzz.... !')
                print('~' * 50)
                self.countdown(int(sleep))
                continue

            if res == 'insufficient_energy':
                self.log(f'{kuning}insufficient energy reacted !')
                self.log(f'{kuning}active sleepzz mode zzzzzzz.... !')
                print('~' * 50)
                self.countdown(int(sleep))
                continue
            
            if isinstance(res,bool):
                self.countdown(int(interval))
                continue

            
if __name__ == "__main__":
    try:
        app = OnchainBot()
        app.main()
    except KeyboardInterrupt:
        sys.exit()
