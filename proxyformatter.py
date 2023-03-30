def formatProxies():
    proxies = [x.strip() for x in open("data/proxies.txt", "r", encoding="utf8").readlines()]
    newProxies = []

    while len(proxies) > 0:
        host, port, user, password = proxies.pop().split(":")
        newProxies.append(f"{user}:{password}@{host}:{port}")

    with open("data/proxies.txt", "w", encoding="utf8") as file:
        for proxy in newProxies:
            file.write(f"{str(proxy)}\n")
        file.close()

if __name__ == "__main__":
    formatProxies()