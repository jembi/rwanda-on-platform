import environ
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

def getUrl(endpoint, host):
    header = env('HEADER')
    port = env('JEMPI_PORT')
    url = header+"://" + host + ":" + port + "/" + endpoint
    print("url -"+url)
    return url
