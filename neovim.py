#!/bin/python3
import subprocess
import re
import requests
from packaging import version
import os

owner = "neovim"
repo = "neovim"


def existNvim():
    try:
        subprocess.check_call(
            ["/opt/nvim-linux64/bin/nvim", "-v"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except FileNotFoundError:
        return False


def checkLocalNvim():
    text = subprocess.check_output(["/opt/nvim-linux64/bin/nvim", "-v"])
    convertText = text.decode("utf-8")
    versionText = convertText.splitlines()
    versionPattern = re.compile(r"NVIM v\d+\.\d+\.\d+")
    if versionPattern.fullmatch(versionText[0]):
        _, versionNum = versionText[0].split(" ")
        return versionNum.replace("v", "")


def checkRemoteNvim():
    api = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(api)
    return response.json()["tag_name"][1:]


file = "nvim-linux64.tar.gz"
link = f"https://github.com/{owner}/{repo}/releases/latest/download/{file}"  # noqa:E501
print("➡️ Let's see current state of neovim 👀")
if existNvim() is False or version.parse(
    checkLocalNvim()  # type: ignore
) < version.parse(checkRemoteNvim()):
    os.system(
        "notify-send 'Update Neovim' 'Looks like Your neovim either old or does not exist'"
    )
    print(" 󱞩❕Looks like Your neovim either old or does not exist")
    if os.path.isfile(f"/home/nahian/Downloads/{file}") is True:
        print(f"  󱞩Removing {file} from 'Download' folder")
        os.remove(f"/home/nahian/Downloads/{file}")
    if os.path.isdir("/home/nahian/Downloads/nvim-linux64") is True:
        print(f"  󱞩Removing {file[:-7]} folder from 'Download' folder")
        os.system("rm -rf /home/nahian/Downloads/nvim-linux64")
    if os.path.isdir("/opt/nvim-linux64") is True:
        print(f"  󱞩Removing {file[:-7]} folder from 'opt' folder")
        os.system("rm -rf /opt/nvim-linux64")
    print("\n⬇️ Downloading latest neovim in 'Download' folder⬇️ ")
    subprocess.run(["curl", "--output-dir", "/home/nahian/Downloads/", "-#OL", link])
    print("\n📂Extracting it to 'opt' folder")
    subprocess.run(
        [
            "sudo",
            "tar",
            "-C",
            "/opt",
            "-xvf",
            f"/home/nahian/Downloads/{file}",
        ]
    )
    print(
        f"\n🎉Congratulation You have now latest NVIM {checkRemoteNvim()}\nrun 'vi' command"
    )
else:
    print("󱞩You Have The Latest Version of Neovim👍️")
