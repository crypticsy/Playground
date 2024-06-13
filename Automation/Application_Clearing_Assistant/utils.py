import webbrowser

base_url = "https://intranet.londonmet.ac.uk/"

def open_webpage(url):
  if "https://" in url:
    webbrowser.open_new_tab(url)
  else:
    webbrowser.open_new_tab(base_url + url)