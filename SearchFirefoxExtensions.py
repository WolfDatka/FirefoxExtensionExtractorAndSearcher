import pickle
import webbrowser

def LoadSelectedExtensions(file="extensions.pkl"):
    try:
        with open(file, "rb") as f:
            extensionNames = pickle.load(f)
            f.close()

        return extensionNames

    except FileNotFoundError:
        print(f"File {file} not found.")
        exit(-1)

def SearchExtensions(extensions):
    base_url = "https://addons.mozilla.org/en-GB/firefox/search/?q="

    for ext in extensions:
        print(f"Searching: {ext}")
 
        searchURL = f"{base_url}{ext}"
        webbrowser.open(searchURL)

if __name__ == "__main__":
    extensions = LoadSelectedExtensions()
    if extensions:
        SearchExtensions(extensions)
    else:
        print("No extensions to search.")
