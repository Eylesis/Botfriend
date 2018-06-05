import json

def saveFile(Settings : dict, filename : str):
    settings_file = open(filename, "w")
    settings_file.write(json.dumps(Settings, ensure_ascii=False))
    settings_file.close()

def discord_trim(str):
    result = []
    trimLen = 0
    lastLen = 0
    while trimLen <= len(str):
        trimLen += 1999
        result.append(str[lastLen:trimLen])
        lastLen += 1999
    return result    