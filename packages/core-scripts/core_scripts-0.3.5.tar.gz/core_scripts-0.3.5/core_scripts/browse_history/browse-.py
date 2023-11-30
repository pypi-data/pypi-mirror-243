from browser_history.browsers import Chrome

c = Chrome()
home_path = "./browse/"

profiles_available = c.profiles(c.history_file)

print(profiles_available)

_1 = c.history_profiles([profiles_available[0]])
_2 = c.history_profiles([profiles_available[1]])
_3 = c.history_profiles([profiles_available[2]])
_4 = c.history_profiles([profiles_available[3]])

""" _1.save(f'{home_path}default.json')
_2.save(f'{home_path}Guest.json')
_3.save(f'{home_path}profile-1.json')
_4.save(f'{home_path}System.json') """
# c.fetch_history().save("chrome.json")

_1.save('default.json')