import random, tls_client, tls_client.response
from charlogger import Logger

class AbsoluteBase():

    def __init__(self, taskId: int) -> None:
        self.taskId = taskId
        prefixStr = f"{taskId}"
        if taskId < 100:
            if taskId < 10:prefixStr = f"00{taskId}"
            else: prefixStr = f"0{taskId}"
        self.logger = Logger(False, defaultPrefix=f"<TIME> WORKER-{prefixStr}")
        self.session = self.getClient()

        proxies = [x.strip() for x in open("data/proxies.txt", "r", encoding="utf8").readlines()]
        self.proxy = f"http://{random.choice(proxies)}"
        self.session.proxies = { "http": self.proxy, "https": self.proxy }

        self.userAgent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"

        self.session.headers = {
            # "User-Agent": self.userAgent['user_agent']
            "User-Agent": self.userAgent
        }
        pass

    def post(self, url, *args, **kwargs) -> tls_client.response.Response:
        return self.session.post(url, *args, **kwargs)

    def get(self, url, *args, **kwargs) -> tls_client.response.Response:
        return self.session.get(url, *args, **kwargs)

    def put(self, url, *args, **kwargs) -> tls_client.response.Response:
        return self.session.put(url, *args, **kwargs)
    
    def patch(self, url, *args, **kwargs) -> tls_client.response.Response:
        return self.session.patch(url, *args, **kwargs)

    def getOptions(self, headers: dict = None):
        if headers is None:
            headers = {}
        headers.update(self.session.headers)
    
    def getClient(self) -> tls_client.Session:
        return tls_client.Session(
            client_identifier="chrome_111"
        )
