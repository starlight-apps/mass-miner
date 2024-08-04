from websockets import connect
from websockets.exceptions import InvalidStatusCode
from typing import TypedDict
from json import loads
from colorama import Fore, Style, init
from toml import load
import asyncio

class Response(TypedDict):
    coin: float

class Miner(TypedDict):
    server: str
    token: str

class Config(TypedDict):
    miner: Miner

init(convert=True)

print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Loading config file...")

config: Config = load("config.toml")
miner_config = config["miner"]

print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Connecting...")

async def main():
    async with connect(miner_config["server"], close_timeout=2, extra_headers={
        "Cookie": f"token={miner_config["token"]}"
    }) as websocket:
        print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Connected, starting to mine.\n")

        # to recatch the miner's pace on reconnects
        await asyncio.sleep(1.1)

        while True:
            await websocket.send("")

            message = await websocket.recv()
            response: Response = loads(message)
            coin = response["coin"]

            if response["coin"] > 0:
                print(Fore.GREEN + "[+]" + Style.RESET_ALL + " " + f"Got {coin} MSC$.")
            else:
                print(Fore.RED + "[-]" + Style.RESET_ALL + " " + "Didn't find any coins.")

            await asyncio.sleep(1.1)

runner = asyncio.Runner()

while True:
    try:
        runner.run(main())
    
    # initial connection failures
    except TimeoutError as e:
        print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Connection took too long. Try asking on the MassCoin Discord server @ https://discord.gg/rn5nAVmTBk")
        exit(1)
    except InvalidStatusCode as e:
        if e.status_code == 401:
            print(Fore.RED + "[e]" + Style.RESET_ALL + " " + f"Incorrect credentials.")
            exit(1)
            
        # shouldn't happen but maybe some cloudflare issue, regardless I'll leave it in
        print(Fore.RED + "[e]" + Style.RESET_ALL + " " + f"Server returned an unusual code. Try asking on the MassCoin Discord server @ https://discord.gg/rn5nAVmTBk")
        exit(1)
    
    # ctrl+c
    except KeyboardInterrupt as e:
        print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"KeyboardInterrupted. Closing...")
        exit(0)
    
    # anything else that can close the connection
    except Exception:
        print(Fore.BLUE + "[i]" + Style.RESET_ALL + " " + f"Connection interrupted, reconnecting...")