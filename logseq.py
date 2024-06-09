#!/bin/python3
import subprocess
import re
import requests
from packaging import version
import os

home = os.environ["HOME"]
appname = "Logseq"
owner = "logseq"
repo = "logseq"


def isExist(version=False):
    pattern = re.compile(r"Logseq-linux-x64-\d+\.\d+\.\d+\.AppImage$")
    for app in os.listdir(f"{home}/.local/bin"):
        if pattern.match(app):
            if version == False:
                return True
            else:
                return app[17:-9]
    else:
        return False


def checkRemote():
    api = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(api)
    return response.json()["tag_name"]


def shortcut(fileName):
    desktopFile = f"{home}/.local/share/applications/Logseq.desktop"
    if os.path.isfile(desktopFile) is True:
        with open(desktopFile, "r") as f:
            data = f.readlines()
        if data[2] == f"Exec={home}/.local/bin/{fileName} %U\n":
            pass
        else:
            data[2] = f"Exec={home}/.local/bin/{fileName} %U\n"
            with open(desktopFile, "w") as f:
                f.writelines(data)
    else:
        with open(desktopFile, "w") as f:
            data = f"""[Desktop Entry]
Name={appname}
Exec={home}/.local/bin/{fileName} %U
Comment=A privacy first, open source knowledge base
Terminal=false
PrefersNonDefaultGPU=false
Icon=logseq
Type=Application
Categories=Office;
MimeType=x-scheme-handler/logseq;text/html;"""
            f.write(data)


file = f"Logseq-linux-x64-{checkRemote()}.AppImage"
link = f"https://github.com/{owner}/{repo}/releases/download/{checkRemote()}/{file}"  # noqa:E501
print(f"➡️ Let's see current state of {appname}👀")
if isExist() is False or version.parse(isExist(version=True)) < version.parse(  # type: ignore
    checkRemote()
):
    os.system(
        f"notify-send 'Update {appname}' 'Looks like Your {appname} either old or does not exist'"
    )
    print(f" 󱞩❕Looks like Your {appname} either old or does not exist")
    if os.path.isfile(f"{home}/.local/bin/{file}") is True:
        print(f"  󱞩Removing {file} from '{home}/.local/bin' folder")
        os.remove(f"{home}/.local/bin/{file}")
    print(f"\n⬇️ Downloading latest {appname} in 'Download' folder⬇️ ")
    subprocess.run(["curl", "--output-dir", f"{home}/Downloads/", "-#OL", link])
    subprocess.run(["chmod", "+x", f"{home}/Downloads/{file}"])
    print(f"\n📂Moving newer version it to '{home}/.local/bin' folder")
    subprocess.run(["mv", f"{home}/Downloads/{file}", f"{home}/.local/bin/"])
    print(f"\n🏷️ Updating Shortcut")
    shortcut(file)
    print(f"\n🎉Congratulation You have now latest {appname} {checkRemote()}")
else:
    print(f"󱞩You Have The Latest Version of {appname}👍️")
