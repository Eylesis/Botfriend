import json

def saveSettings(Settings : dict):
    settings_file = open('Settings/settings.json', "w")
    settings_file.write(json.dumps(Settings, ensure_ascii=False))
    settings_file.close()