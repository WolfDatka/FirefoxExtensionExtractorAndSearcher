import os
import json
import pickle
from tabulate import tabulate

def GetFirefoxProfileDir() -> str:
    if os.name == "nt":
        firefox_path = os.path.join(os.getenv("APPDATA"), "Mozilla", "Firefox", "Profiles")
    elif os.name == "posix":
        firefox_path = os.path.expanduser("~/.mozilla/firefox/")
    else:
        raise OSError("Unsupported operating system")

    if not os.path.exists(firefox_path):
        raise FileNotFoundError("Firefox profile directory not found.")

    # Find the profile directory, usually the one with a `.default-release` suffix
    for profile in os.listdir(firefox_path):
        if profile.endswith(".default-release"):
            return os.path.join(firefox_path, profile)

    raise FileNotFoundError("Firefox profile directory not found.")

def ExtractExtensions():
    profile_dir = GetFirefoxProfileDir()
    extensions_file = os.path.join(profile_dir, "extensions.json")

    if not os.path.exists(extensions_file):
        raise FileNotFoundError("extensions.json not found in Firefox profile.")

    with open(extensions_file, 'r', encoding="utf-8") as file:
        data = json.load(file)

    extensions = []
    for addon in data.get("addons", []):
        if addon.get("type") == "extension":
            if ("mozilla.org" in addon.get("id", "Unknown") or
                "mozilla.com" in addon.get("id", "Unknown")):
                continue

            extensions.append([
                addon.get("defaultLocale", {}).get("name", "Unknown"),
                addon.get("version", "Unknown"),
                addon.get("id", "Unknown")
            ])

    return extensions

def SaveSelectedExtensions(SelectedExtensionNames):
    with open("extensions.pkl", "wb") as f:
        pickle.dump(SelectedExtensionNames, f)
        f.close()

    print(f"Saved {len(SelectedExtensionNames)} extensions to \"extensions.pkl\"")

def CheckSelectionIDsToBeInRange(extensions, selected_extenions):
    for selectionID in selected_extenions:
        if selectionID > len(extensions):
            print("SelectionID is larger than the amount of extensions!", flush=True)
            exit(-1)

def ConvertInputSelectionIDsToIntsAndProcessRanges(selected_extenions):
    for i in range(len(selected_extenions)):
        if '-' in selected_extenions[i]:
            rangeStart, rangeEnd = selected_extenions[i].split('-')
            rangeStart = int(rangeStart)
            rangeEnd = int(rangeEnd)

            for j in range(rangeStart, rangeEnd):
                selected_extenions.append(j)

            selected_extenions[i] = rangeEnd
        else:
            selected_extenions[i] = int(selected_extenions[i])

def ExtensionSelection():
    print("\nEnter the extensions' selection ID separated by spaces.")
    print("You may also enter ranges (both sides inclusive) by the following pattern *range start*-*range end*.")
    selected_extenions = input("Selection IDs: ")
    selected_extenions = selected_extenions.split(' ')
    return selected_extenions

def CreateSelectionIDs(extensions):
    for i in range(len(extensions)):
        extensions[i].insert(0, i)

def ClearConsole():
    if os.name == "nt":
        os.system("cls")
    elif os.name == "posix":
        firefox_path = os.path.expanduser("~/.mozilla/firefox/")
    else:
        raise OSError("Unsupported operating system")

def CopySelectedExtensions(extensions, selected_extenions):
    for i in range(len(selected_extenions)):
        selected_extenions[i] = extensions[selected_extenions[i]]
        selected_extenions[i].pop(0)

if __name__ == "__main__":
    try:
        extensions = ExtractExtensions()
        if extensions:
            headers = ["Selection ID", "Extension Name", "Version", "ID"]

            CreateSelectionIDs(extensions)

            print(tabulate(extensions, headers=headers, tablefmt="grid"))

            selected_extenions = ExtensionSelection()

            ConvertInputSelectionIDsToIntsAndProcessRanges(selected_extenions)
            CheckSelectionIDsToBeInRange(extensions, selected_extenions)

            CopySelectedExtensions(extensions, selected_extenions)

            headers.pop(0)
            ClearConsole()

            print(tabulate(selected_extenions, headers=headers, tablefmt="grid"))

            SelectedExtensionNames = []
            for extension in selected_extenions:
                SelectedExtensionNames.append(extension[0])

            SaveSelectedExtensions(SelectedExtensionNames)

        else:
            print("No extensions found.")
    except Exception as e:
        print(f"Error: {e}")
