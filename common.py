from django.conf import settings
def getHost(request):
    if settings.DEBUG:
        host = ""
    else:
        host = "http://jizhanggroup.appsp0t.com"
    return host
