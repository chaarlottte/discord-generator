import string, random, secrets, base64, time, requests, json
from itertools import accumulate
from bisect import bisect
from random import randrange
from unicodedata import name as unicode_name

config = json.loads(open("data/config.json").read())
nameMode = config.get("tokens").get("name_mode")
customName = config.get("tokens").get("custom_name")
prefix = config.get("tokens").get("prefix_or_suffix")
rndLength = config.get("tokens").get("string_length")

class utils():

    def getUsername():
        match nameMode:
            case "CUSTOM":
                return customName
            case "PREFIX":
                start = f"{prefix} | "
                amount = max(32 - len(start), 0)
                return f"{start}{utils.randomString(amount)}"
            case "SUFFIX":
                end = f"| {prefix}"
                amount = max(32 - len(end), 0)
                return f"{utils.randomString(amount)}{end}"
            case "EMOJI":
                return utils.randomEmojis(rndLength)
            case "RANDOM":
                return utils.randomString(rndLength)
            case "FILE":
                return random.choice(open("data/usernames.txt",encoding = "utf-8").read().splitlines())

    def randomEmoji(unicode_version = 6):
         # Set the unicode version.
        # Your system may not support Unicode 7.0 charecters just yet! So hipster.
        UNICODE_VERSION = 6

        # Sauce: http://www.unicode.org/charts/PDF/U1F300.pdf
        EMOJI_RANGES_UNICODE = {
            6: [
                ('\U0001F300', '\U0001F320'),
                ('\U0001F330', '\U0001F335'),
                ('\U0001F337', '\U0001F37C'),
                ('\U0001F380', '\U0001F393'),
                ('\U0001F3A0', '\U0001F3C4'),
                ('\U0001F3C6', '\U0001F3CA'),
                ('\U0001F3E0', '\U0001F3F0'),
                ('\U0001F400', '\U0001F43E'),
                ('\U0001F440', ),
                ('\U0001F442', '\U0001F4F7'),
                ('\U0001F4F9', '\U0001F4FC'),
                ('\U0001F500', '\U0001F53C'),
                ('\U0001F540', '\U0001F543'),
                ('\U0001F550', '\U0001F567'),
                ('\U0001F5FB', '\U0001F5FF')
            ],
            7: [
                ('\U0001F300', '\U0001F32C'),
                ('\U0001F330', '\U0001F37D'),
                ('\U0001F380', '\U0001F3CE'),
                ('\U0001F3D4', '\U0001F3F7'),
                ('\U0001F400', '\U0001F4FE'),
                ('\U0001F500', '\U0001F54A'),
                ('\U0001F550', '\U0001F579'),
                ('\U0001F57B', '\U0001F5A3'),
                ('\U0001F5A5', '\U0001F5FF')
            ],
            8: [
                ('\U0001F300', '\U0001F579'),
                ('\U0001F57B', '\U0001F5A3'),
                ('\U0001F5A5', '\U0001F5FF')
            ]
        }

        NO_NAME_ERROR = '(No name found for this codepoint)'
        if unicode_version in EMOJI_RANGES_UNICODE:
            emoji_ranges = EMOJI_RANGES_UNICODE[unicode_version]
        else:
            emoji_ranges = EMOJI_RANGES_UNICODE[-1]

        # Weighted distribution
        count = [ord(r[-1]) - ord(r[0]) + 1 for r in emoji_ranges]
        weight_distr = list(accumulate(count))

        # Get one point in the multiple ranges
        point = randrange(weight_distr[-1])

        # Select the correct range
        emoji_range_idx = bisect(weight_distr, point)
        emoji_range = emoji_ranges[emoji_range_idx]

        # Calculate the index in the selected range
        point_in_range = point
        if emoji_range_idx != 0:
            point_in_range = point - weight_distr[emoji_range_idx - 1]

        # Emoji 😄
        emoji = chr(ord(emoji_range[0]) + point_in_range)
        emoji_name = unicode_name(emoji, NO_NAME_ERROR).capitalize()
        emoji_codepoint = "U+{}".format(hex(ord(emoji))[2:].upper())

        return emoji

    def randomEmojis(length: int) -> str:
        return f"{''.join(str(utils.randomEmoji()) for i in range(length))}"

    def randomNumber(min, max) :
        return random.randint(min, max)

    def randomString(len):
        return f"{''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase) for i in range(len))}"

    def generatePassword(x):
        prefix = ""
        x = x - len(prefix)
        return f"{prefix}{''.join(secrets.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for i in range(x))}"

    def getWebsocketData():
        game = "Monsoon"
        return {
            "op": 2,
            "d": {
                "token": "",
                "capabilities": 125,
                "properties": {
                    "$os": "Windows",
                    "$browser": "Chrome",
                    "$device": "Windows Device",
                    "system_locale": "en-US",
                    "browser_user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36",
                    "browser_version": "96.0.4664.45",
                    "os_version": "10",
                    "referrer": "",
                    "referring_domain": "",
                    "referrer_current": "",
                    "referring_domain_current": "",
                    "release_channel": "stable",
                    "client_build_number": 105691,
                    "client_event_source": None
                },
                "presence": {
                    "status": random.choice(["online", "idle", "dnd"]),
                    "game": {"name": game, "type": 0},
                    "since": 0,
                    "activities": [],
                    "afk": False
                },
                "compress": False,
                "client_state": {
                    "guild_hashes": {},
                    "highest_last_message_id": "0",
                    "read_state_version": 0,
                    "user_guild_settings_version": -1,
                    "user_settings_version": -1
                }
            },
            "s": None,
            "t": None
        }
    
    def getChromeXPROP(userAgent, buildNumber):
        browserVer = userAgent.split("Chrome/")[1].split(" ")[0]
        return base64.b64encode(str('''{"os":"Windows","browser":"Chrome","device":"","system_locale":"en-US","browser_user_agent":"'''+userAgent+'''","browser_version":"'''+browserVer+'''","os_version":"10","referrer":"","referring_domain":"","referrer_current":"","referring_domain_current":"","release_channel":"stable","client_build_number":'''+buildNumber+''',"client_event_source":null}''').encode()).decode()
    
    def getLatestJS():
        return (requests.get("https://discord.com/app").text.split('"></script><script src="/assets/')[2].split('" integrity')[0])

    def getAppVersion():
        resp = requests.get("https://discord.com/api/downloads/distributions/app/installers/latest?channel=stable&platform=win&arch=x86").text
        
        return resp.split("/distro/app/stable/win/x86/")[1].split("/DiscordSetup.exe")[0]

    def getBuildNumber():
        resp = requests.get(f"https://discord.com/assets/{utils.getLatestJS()}")

        if resp.status_code == 200:
            buildNum = resp.text.split('(t="')[1].split('")?t:"")')[0]
            
            return int(buildNum)
        else:
            return 9999