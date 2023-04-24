from src.base import AbsoluteBase
from src.utils import utils
from src.solver import solver
from charlogger import Logger
import time, threading, websocket, json, random, os

class creator(AbsoluteBase):
    def __init__(self, taskId: int, invite: str) -> None:
        super().__init__(taskId)
        self.invite = invite
        self.username = utils.getUsername()
        pass

    def start(self) -> None:
        self.session.headers = self.getHeaders()
        self.captchaToken = solver.solveCaptcha(self.logger, self.session)
        self.fingerprint = self.getFingerprint()
        self.session.headers["X-Fingerprint"] = self.fingerprint
        self.getCookies()
        self.register()

    def register(self) -> None:
        body = {
            "fingerprint": self.fingerprint,
            "username": self.username,
            "invite": self.invite,
            "consent": True,
            "date_of_birth": f"{random.randint(1980, 2000)}-0{random.randint(1, 9)}-{random.randint(10, 28)}",
            "gift_code_sku_id": None,
            "captcha_key": self.captchaToken
        }
        resp = self.post("https://discord.com/api/v9/auth/register", json=body)
        if "token" in resp.text:
            self.token = resp.json()["token"]
            self.logger.valid(title="CREATED", data=f"{self.token.split('.')[0]}.{'*'*24}")
            with open("output/tokens.txt", "a") as f:
                f.write(f"{self.token}\n")
                f.close()
            threading.Thread(target=self.websocketHandler, args=(self.token,)).start()
            self.session.headers["authorization"] = self.token
        elif "retry_after" in resp.text:
            delay = resp.json()["retry_after"]
            self.logger.warn(title="RATELIMIT", data=f"Waiting for {delay}s...")
            time.sleep(delay)
        elif "invalid-response" or "invalid-input-response" in resp.text:
            self.logger.warn(title="ERROR", data=f"Captcha error: {self.captchaSolution.split('.')[0]}")

    def getHeaders(self) -> dict:
        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "Host": "discord.com",
            "Origin": "https://discord.com",
            "Referer": "https://discord.com/register",
            "Sec-ch-ua": '"Chromium";v="111", "Not A(Brand";v="24", "Google Chrome";v="111"',
            "Sec-ch-ua-mobile": "?0",
            "Sec-ch-ua-platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": self.userAgent,
            "X-Super-Properties": utils.getChromeXPROP(userAgent=self.userAgent, buildNumber=str(utils.getBuildNumber())),
            "X-Discord-Locale": "en-US"
        }
        return headers
    
    def websocketHandler(self, token: str):
        while True:
            try:
                ws = websocket.WebSocket()
                ws.connect("wss://gateway.discord.gg/?encoding=json&v=6")
                websocketData = utils.getWebsocketData()
                websocketData["d"]["token"] = token
                thing = json.dumps(websocketData)
                ws.send(thing)
                heartbeat = json.loads(ws.recv()).get("d").get("heartbeat_interval")
                time.sleep(heartbeat / 1000)
                ws.send(json.dumps({"op": 1, "d": None}))
            except Exception as e:
                continue

    def getCookies(self) -> None:
        self.get("https://discord.com/register")
        self.logger.debug(f"Got cookies.")

    def getFingerprint(self) -> str:
        return self.get("https://discord.com/api/v9/experiments").json()["fingerprint"]


config = json.loads(open("data/config.json").read())
invite = config.get("general").get("invite")
threads = config.get("general").get("threads")

if invite.startswith("https://discord.gg/"):
    invite = invite.split("https://discord.gg/")[1]

def runThread(threadNum: int):
    while True:
        creator(threadNum, invite).start()

def main():
    logger = Logger(True, default_prefix=f"<TIME> | GENERATOR")
    os.system("cls")
    if not os.path.exists("output"): os.mkdir("output")
    logger.info(f"Starting generator...")
    for x in range(threads):
        thread = threading.Thread(target=runThread, args=(x + 1,))
        thread.start()

if __name__ == "__main__":
    main()
