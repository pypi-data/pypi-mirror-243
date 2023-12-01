_host = "sapioqa-239.exemplareln.dev"
_port = 443
_guid = ""
headless = False
# username = "yqiao+test@sapiosciences.com"
# password = "Password1!"
username = "dwelch@sapiosciences.com"
password = "Kims2008!!"

HOMEPAGE_URL = "https://" + _host + ":" + str(_port) + "/veloxClient"
if _guid:
    HOMEPAGE_URL += "/VeloxClient.html?app=" + _guid
else:
    HOMEPAGE_URL += "/localauth"
