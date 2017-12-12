import json

def saveSettings(Settings : dict):
    settings_file = open('Settings/settings.json', "w")
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