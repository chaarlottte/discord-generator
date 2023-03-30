import json, random, requests, time, charlogger
from dort.captcha import HCaptchaEnterpriseTask

config = json.loads(open("data/config.json").read())
captchaService = config.get("captcha").get("solving_service")
key = config.get("captcha").get("service_key")

class solver():
    def solveCaptcha(logger: charlogger.Logger, session: requests.Session) -> str:
        publicKey = "4c672d35-0701-42b2-88c3-78380b0db560"
        siteUrl = "https://discord.com"

        match captchaService:
            case "DORT":
                return solver.solveDortCaptcha(publicKey, siteUrl, logger=logger, session=session)
            case "CAPSOLVER":
                return solver.solveGeneric(publicKey, siteUrl, domain="https://api.capsolver.com", logger=logger, session=session)
            case "ANTICAPTCHA":
                return solver.solveGeneric(publicKey, siteUrl, domain="https://api.anti-captcha.com", logger=logger, session=session)
            case "CAPMONSTER":
                return solver.solveGeneric(publicKey, siteUrl, domain="https://api.capmonster.cloud", logger=logger, session=session)

    def solveDortCaptcha(publicKey: str, siteUrl: str, logger: charlogger.Logger, session: requests.Session) -> str:
        return HCaptchaEnterpriseTask(
            apiKey=key, 
            publicKey=publicKey,
            siteUrl=siteUrl,
            proxy=session.proxies.get("http")
        ).solve()
    
    def solveGeneric(publicKey: str, siteUrl: str, logger: charlogger.Logger, session: requests.Session, domain: str = "https://api.capsolver.com") -> str:
        taskType = "HCaptchaEnterpriseTask" if "capsolver" in domain else "HCaptchaTask"
        data1 = {
            "clientKey": key,
            "appId": "5C4B67D5-D8E9-485D-AF57-4F427464F0CF",
            "task": {
                "type": taskType,
                "websiteURL": siteUrl,
                "websiteKey": publicKey,
                "userAgent": session.headers.get("User-Agent"),
                "proxy": solver.getProxyFromSession(session)
            }
        }
        resp1 = requests.post(f"{domain}/createTask", json=data1)
        if resp1.json().get("errorId") == 0:
            # print(resp1.text)
            taskId = resp1.json().get("taskId")
            logger.debug(title="CAPTCHA", data=f"Got task ID. {taskId}")
            data = {
                "clientKey": key,
                "taskId": taskId
            }
            resp = requests.post(f"{domain}/getTaskResult", json=data)
            status = resp.json().get("status")
            logger.debug(title="CAPTCHA", data=f"{resp.status_code}, {resp.text}")

            while status == "processing":
                logger.debug(title="CAPTCHA", data=f"{resp.status_code}, {resp.text}")
                time.sleep(1)
                resp = requests.post(f"{domain}/getTaskResult", json=data)
                status = resp.json().get("status")

            if status == "ready":
                captchaToken = resp.json().get("solution").get("gRecaptchaResponse")
                logger.info(title="CAPTCHA", data=f"Solved captcha. {captchaToken.split('.')[0]}")
                return resp.json().get("solution").get("gRecaptchaResponse")
            else:
                logger.debug(title="CAPTCHA", data=f"Solving error! {resp.text}")
                return solver.solveCaptcha(logger=logger, session=session)
        else:
            return solver.solveGeneric(publicKey, siteUrl, logger, session, domain)
    
    def getProxyFromSession(session: requests.Session) -> str:
        protocol, sessionProxy = session.proxies.get("http").split("://")
        sessionProxy = sessionProxy.replace(":", "big juicy fat cock").replace("@", "big juicy fat cock")
        if len(sessionProxy.split("big juicy fat cock")) == 4:
            user, password, host, port = sessionProxy.split("big juicy fat cock")
            return f"{protocol}:{host}:{port}:{user}:{password}"
        else:
            host, port = sessionProxy.split("big juicy fat cock")
            return f"{protocol}:{host}:{port}"