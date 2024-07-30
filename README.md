# mass-miner

This is an official MassCoin miner developed by [us](https://github.com/starlight-apps/). Keep in mind we only provide help for the parts of the ecosystem that we develop.

# ❗ Disclaimer: MassCoin is not a real cryptocurrency ❗

This "miner" only sends requests via the internet (WebSockets specifically), no actual system strain/harm is done.<br>
**You can verify that by checking the used resources in Task Manager or the respective program for your OS.
Alternatively you can just check the code.**

MassCoin is a hobby project which uses chance instead of computer power to generate its coins.

Furthermore, you shouldn't take it too seriously, at the end of the day, most of this is just for fun/code excercise/time burning purposes.

# Setup

To setup the miner, you need to install Python.
After you've done that, navigate to the root directory of the miner, open a terminal and run the following command to install the required libraries:

```
python -m pip install -r requirements.txt
```

After that, go to [the MassCoin settings](https://masscoin.xyz/settings) and copy your token, then paste it into the value string of the "token" key in the config.toml file. Your config should look like this:

```toml
[miner]
token = "[your-token-here]"
```

It's worth mentioning once again that this token should **never** be shared.

To start mining, you can run the following command in the terminal:

```
python main.py
```
