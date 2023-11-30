from Browser import Browser


class Chrome(Browser):
    def __init__(
            self,
            history_folder = f"C:/Users/{super().username}/AppData/Local/Google/Chrome/User Data/Default",
            history_query = "select url, title, visit_count, datetime(last_visit_time / 1000000 + (strftime('%s', '1601-01-01')), 'unixepoch', 'localtime') from urls",
            history_file = "History",
            browser_process_name = "chrome.exe"
    ):
        super().__init__(history_folder, history_query, history_file, browser_process_name)

    def close_chrome(self):
        # cierra a google chrome
        super().close_browser(self.browser_process_name)
        return True


a = Chrome()

print()
