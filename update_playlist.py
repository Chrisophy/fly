# -*- coding: utf-8 -*-
import requests
import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

requests.packages.urllib3.disable_warnings()

class HamSter:
    def __init__(self):
        self.cache = {}
        self.vec = "Y6M13YYOKehfrcCIQMb3uoR7Y2zp0al7nyl5rDhJ32eyEU1/4QzKdWytuJGh0bKcTPDL0fvRfvlCiy8JEnTa7/uEa2z0c716Hr5Ud4gtVVABVE37blNal5U9gPtmpc0N6MDayhlNf3raqEe9h5nuSaYuy0VN6j4LwLcOh7Y5WRi0c3J8Hq7L/t61/T6GX0jbScRE1eOGRkWwGczAh+TiB0PrT1XZrZUde0+hoGcGPB9M+j/j2V41IEa5ouSXwpY9ANtMeBa/oKWxqyR2M9KiphJlLXrZIE/QUcJh0d3xETdenhnLpGlYwQSERj2sc+hpqLVMagT26AlhhYHMT1xGY2GsPBog/QLd+Fck8r3NmdYxpXZ25QwLDtIq8SGhSt3j5DEOjU7z4mfBKDnH7B6ncckAVLMikVqcbbM8NFUgJIkUaI2IfcBcrcgr4l3dBH3djXa+OWEksQQ8xPRuMSxDaUqTGsz2Qyhpx1Ldpe2Zswq9U4xIimBvYw+BSOTDU3zKg9OTbAN4AcyVLZbeWWUEd0WcNYP4wLencUvrDzt/Rsb6o4n9VVkO9QjmQQgTGnlo9QkOM4J4UJzidwXHJRAXATwhEgk0t2Y+7HWuV3mPmrVHgWigoK+beWznJEGu9cyKkzH0qyCYFmOPpWUTIg/qr6NSrboT3brOCQSbb3ES04V7FjRGveeNmkrlkHahwtnEX4Dy2VpL47SdDxcK1i6IdqgnXMKJn/oDY8GomodTRATpYvNfjCaAuyeMFKFyX2XyhEv5Kzmi+Z2Z8dxhB+SAuDhIdswva7hU85unLCBzII2PId1+2nQreTyMO92J5lqf6NgvhAV+1xFkYX/olyN19XRcxRGPmo6k9NKy68G+veImBLKQpHhPPUOmQJWSuZpfGAgTSr50wfgXnOpotYB4mwZc7z5TOA2ehqYodCPwFq6sOOxzg8h5nYqlqKsFvXFyKbMZZCu1QEyRRt12qRh/quLTrFamEkXIC4TSnX/Bq0poO0Q+C2k1Qg+TneONKEyCc9+JxjQYZT0Y8waLFh37Xp7k/Gk1KDByCxwC538H3Ge8jaPl0lGnmEJouUlYNQjd2WjDpjaeDH4fnGYyQR1x4J2amqp0o5mt5Hm69F0VNPf/7ZPSl+4KGTkwzxmdHboZiwFCio2soBVVv4+rZ9IhqzaQjCVWylaF3e7eHKaYE5qAIr9fwjMVmIbXR4WX8a4ni1G7CLCjJk1lGuY3En0cZ6U3Oxg9++w+12O4nX4eNQ9pEKHYLDWKe0j7rg+iM8CaG1ikrfvGtvzZQ33x94JejwDdbcxLorZbWIhemOONBH2AtTgPaFW78drlmU603RZuxCU7f8t8JTXLfvVHXcc4nQiVFZlWRDLR6xHTflh/YfH5SZ/3G/HCXtGJyvGsSd693Q9irixaNjlAmTCEoXnwimshgEoliaUwj5MjBXR9pPY0JGMPR80as86S0FxO/ZVavSmNsC4Zm41fBNqbcvuXXQkb7zt+ZHBmx4yW/NCrXYUHIcVS3RSPCvZCaLMT9mXw+YxibCWqWk8cRwTx0/1sLjX5oz02+qhmC3s7G23OvsAJOThyL/cp9twA5nFQT01hjqPFhDTNP3Nr5bf7Fw/f3/Jsbew0xTz6p2XthzRTBCZJKZd2uoW20ZwNs2DnMMNh1yZER40KjqQrusxUn6qsU9vKTG+dks920JgV4ZrZY/JslKH66fXmSL3GEkNTDIIUdoBpYZtNG6JZKHOm+67nlxe4ogisbCqnfbhjL4iGTfNKJv+cmyTujH79IBG7mimalo49MuZr9aKGclq7fYTcGGMTEYyiYuWCkENknXtdKNLlo67RuwfF5torj5jy9BQQaMQWf+nrPwdtrclr7Ad6tmJywZFAQ/hD2oGqlXXQ8Vqr+8S01P1KoNof+utH0gLm9eOG47XXT+NkeDTof5R5WA=="
        self.user_agent = "MediaHubMX/2"
        self.catalog_url = "https://vavoo.cc/vto-cluster/mediahubmx-catalog.json"
        self.resolve_url = "https://vavoo.cc/vto-cluster/mediahubmx-resolve.json"

    def get_auth_signature(self):
        now = int(time.time() * 1000)
        if self.cache.get("signfile") and now < (int(self.cache.get("signfile_valid_until", 0)) - 60000):
            return self.cache["signfile"]
        try:
            r = requests.post("https://www.vavoo.tv/api/box/ping2", data={"vec": self.vec}, timeout=10, verify=False)
            res = r.json().get("response", {})
            if res.get("signed"):
                self.cache["signfile"] = res["signed"]
                self.cache["signfile_valid_until"] = res.get("sigValidUntil")
                return res["signed"]
        except: return None

    def fetch_channels(self, language="de", region="AT", catalog_id="vto-iptv"):
        channels = []
        sig = self.get_auth_signature()
        if not sig: return []
        headers = {"user-agent": self.user_agent, "mediahubmx-signature": sig}
        cursor = 0
        while True:
            payload = {
                "language": language, "region": region, "catalogId": catalog_id,
                "id": catalog_id, "adult": False, "search": "", "sort": "name",
                "filter": {}, "cursor": cursor, "clientVersion": "3.0.2",
            }
            try:
                r = requests.post(self.catalog_url, json=payload, headers=headers, timeout=10, verify=False)
                data = r.json()
                for item in data.get("items", []):
                    name = re.sub(r"( (SD|HD|FHD|UHD|H265))?( \(BACKUP\))? \(\d+\)$", "", item.get("name", "Unknown"))
                    channels.append({"text": name, "url": item.get("url")})
                cursor = data.get("nextCursor")
                if not cursor: break
            except: break
        return channels

    def resolve_stream(self, url):
        sig = self.get_auth_signature()
        if not sig: return None
        headers = {"user-agent": self.user_agent, "mediahubmx-signature": sig}
        payload = {"language": "de", "region": "AT", "url": url, "clientVersion": "3.0.2"}
        try:
            r = requests.post(self.resolve_url, json=payload, headers=headers, timeout=10, verify=False)
            data = r.json()
            return data[0].get("url") if isinstance(data, list) and data else None
        except: return None

if __name__ == "__main__":
    print("Starte Kanal-Abruf...")
    core = HamSter()
    raw_channels = core.fetch_channels()
    print(f"{len(raw_channels)} Kanäle gefunden. Löse Stream-URLs auf...")

    m3u_lines = ["#EXTM3U"]
    
    def process_channel(ch):
        name = ch.get('text', 'Unknown')
        orig_url = ch.get('url')
        if not orig_url:
            return None
        resolved = core.resolve_stream(orig_url) if "vavoo.cc" in orig_url else orig_url
        if resolved:
            return f"#EXTINF:-1,{name}\n{resolved}"
        return None

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(process_channel, ch): ch for ch in raw_channels}
        for future in as_completed(futures):
            res = future.result()
            if res:
                m3u_lines.append(res)

    with open("playlist.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(m3u_lines))
    print("Playlist erfolgreich in playlist.m3u gespeichert.")
