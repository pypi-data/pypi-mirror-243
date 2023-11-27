from getpass import getuser

username = getuser()
chrome_history_folder = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data"
get_history_query = "select url, title, visit_count, datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime') from urls"
