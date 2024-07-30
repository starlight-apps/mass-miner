from time import sleep
from websockets import connect
from websockets.exceptions import InvalidStatusCode
from typing import TypedDict
from json import loads
from colorama import Fore, Style
from toml import load
import asyncio

class Response(TypedDict):
    coin: float

class Miner(TypedDict):
    token: str

class Config(TypedDict):
    miner: Miner

print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Loading config file...")

config: Config = load("config.toml")
miner_config = config["miner"]

print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Connecting...")

async def main():
    async with connect("wss://m1.masscoin.xyz", close_timeout=2, extra_headers={
        "Cookie": f"token={miner_config["token"]}"
    }) as websocket:
        print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Connected, starting to mine.\n")

        while True:
            await websocket.send("")

            message = await websocket.recv()
            response: Response = loads(message)
            coin = response["coin"]

            if response["coin"] > 0:
                print(Fore.GREEN + "[+]" + Style.RESET_ALL + " " + f"Got {coin} MSC$.")
            else:
                print(Fore.RED + "[-]" + Style.RESET_ALL + " " + "Didn't find any coins.")

            sleep(1.1)

try:
    asyncio.run(main())
except TimeoutError as e:
    print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Connection took too long. Try asking on the MassCoin Discord server @ https://discord.gg/rn5nAVmTBk")
except KeyboardInterrupt as e:
    print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Interrupted. Closing...")
except InvalidStatusCode as e:
    if e.status_code == 401:
        print(Fore.RED + "[e]" + Style.RESET_ALL + " " + f"Incorrect credentials.")
        exit(0)

    # shouldn't happen but maybe some cloudflare issue, regardless I'll leave it in
    print(Fore.RED + "[e]" + Style.RESET_ALL + " " + f"Server returned an unusual code. Try asking on the MassCoin Discord server @ https://discord.gg/rn5nAVmTBk")
    exit(1)