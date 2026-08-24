# -*- coding: utf-8 -*-
import requests
import re
import time
import base64
from concurrent.futures import ThreadPoolExecutor, as_completed

requests.packages.urllib3.disable_warnings()

def _d(b64_str):
    return base64.b64decode(b64_str.encode("utf-8")).decode("utf-8")

class HamSter:
    def __init__(self):
        self.cache = {}
        self.v = _d("WTZNMTNZWU9LZWhmcmNDSVFNYjN1b1I3WTJ6cDBhbDdueWw1ckRoSjMyZXlFVTEvNFF6S2RXeXR1SkdoMGJLY1RQREwwZnZSZnZsQ2l5OEpFblRhNy91RWEyejBjNzE2SHI1VWQ0Z3RWVkFCVkUzN2JsTmFsNVU5Z1B0bXBjME42TURheWhsTmYzcmFxRWU5aDVudVNhWXV5MFZONmo0THdMY09oN1k1V1JpMGMzSjhIcTdML3Q2MS9UNkdYMGpiU2NSRTFlT0dSa1d3R2N6QWgrVGlCMFByVDFYWnJaVWRlMCtob0djR1BCOU0rai9qMlY0MUlFYTVvdVNYd3BZOUFOdE1lQmEvb0tXeHF5UjJNOUtpcGhKbExYclpJRS9RVWNKaDBkM3hFVGRlbmhuTHBHbFl3UVNFUmoyc2MraHBxTFZNYWdUMjZBbGhoWUhNVDF4R1kyR3NQQm9nL1FMZCtGY2s4cjNObWRZeHBYWjI1UXdMRHRJcThTR2hTdDNqNURFT2pVN3o0bWZCS0RuSDdCNm5jY2tBVkxNaWtWcWNiYk04TkZVZ0pJa1VhSTJJZmNCY3JjZ3I0bDNkQkgzZGpYYStPV0Vrc1FROHhQUnVNU3hEYVVxVEdzejJReWhweDFMZHBlMlpzd3E5VTR4SWltQnZZdytCU09URFUzektnOU9UYkFONEFjeVZMWmJlV1dVRWQwV2NOWVA0d0xlbmNVdnJEenQvUnNiNm80bjlWVmtPOVFqbVFRZ1RHbmxvOVFrT000SjRVSnppZHdYSEpSQVhBVHdoRWdrMHQyWSs3SFd1VjNtUG1yVkhnV2lnb0srYmVXem5KRUd1OWN5S2t6SDBxeUNZRm1PUHBXVVRJZy9xcjZOU3Jib1QzYnJPQ1FTYmIzRVMwNFY3RmpSR3ZlZU5ta3Jsa0hhaHd0bkVYNER5MlZwTDQ3U2REeGNLMWk2SWRxZ25YTUtKbi9vRFk4R29tb2RUUkFUcFl2TmZqQ2FBdXllTUZLRnlYMlh5aEV2NUt6bWkrWjJaOGR4aEIrU0F1RGhJZHN3dmE3aFU4NXVuTENCeklJMlBJZDErMm5RcmVUeU1POTJKNWxxZjZOZ3ZoQVYrMXhGa1lYL29seU4xOVhSY3hSR1BtbzZrOU5LeTY4Ryt2ZUltQkxLUXBIaFBQVU9tUUpXU3VacGZHQWdUU3I1MHdmZ1huT3BvdFlCNG13WmM3ejVUT0EyZWhxWW9kQ1B3RnE2c09PeHpnOGg1bllxbHFLc0Z2WEZ5S2JNWlpDdTFRRXlSUnQxMnFSaC9xdUxUckZhbUVrWElDNFRTblgvQnEwcG9PMFErQzJrMVFnK1RuZU9OS0V5Q2M5K0p4alFZWlQwWTh3YUxGaDM3WHA3ay9HazFLREJ5Q3h3QzUzOEgzR2U4amFQbDBsR25tRUpvdVVsWU5RamQyV2pEcGphZURINGZuR1l5UVIxeDRKMmFtcXAwbzVtdDVIbTY5RjBWTlBmLzdaUFNsKzRLR1Rrd3p4bWRIYm9aaXdGQ2lvMnNvQlZWdjQrclo5SWhxemFRakNWV3lsYUYzZTdlSEthWUU1cUFJcjlmd2pNVm1JYlhSNFdYOGE0bmkxRzdDTENqSmsxbEd1WTNFbjBjWjZVM094ZzkrK3crMTJPNG5YNGVOUTlwRUtIWUxEV0tlMGo3cmcraU04Q2FHMWlrcmZ2R3R2elpRMzN4OTRKZWp3RGRiY3hMb3JaYldJaGVtT09OQkgyQXRUZ1BhRlc3OGRybG1VNjAzUlp1eENVN2Y4dDhKVFhMZnZWSFhjYzRuUWlWRlpsV1JETFI2eEhUZmxoL1lmSDVTWi8zRy9IQ1h0R0p5dkdzU2Q2OTNROWlyaXhhTmpsQW1UQ0VvWG53aW1zaGdFb2xpYVV3ajVNakJYUjlwUFkwSkdNUFI4MGFzODZTMEZ4Ty9aVmF2U21Oc0M0Wm00MWZCTnFiY3Z1WFhRa2I3enQrWkhCbXg0eVcvTkNyWFlVSEljVlMzUlNQQ3ZaQ2FMTVQ5bVh3K1l4aWJDV3FXazhjUndUeDAvMXNMalg1b3owMitxaG1DM3M3RzIzT3ZzQUpPVGh5TC9jcDl0d0E1bkZRVDAxaGpxUEZoRFROUDNOcjViZjdGdy9mMy9Kc2JldzB4VHo2cDJYdGh6UlRCQ1pKS1pkMnVvVzIwWndOczJEbk1NTmgxeVpFUjQwS2pxUXJ1c3hVbjZxc1U5dktURytka3M5MjBKZ1Y0WnJaWS9Kc2xLSDY2ZlhtU0wzR0VrTlRESUlVZG9CcFladE5HNkpaS0hPbSs2N25seGU0b2dpc2JDcW5mYmhqTDRpR1RmTktKditjbXlUdWpINzlJQkc3bWltYWxvNDlNdVpyOWFLR2NscTdmWVRjR0dNVEVZeWlZdVdDa0VOa25YdGRLTkxsbzY3UnV3ZkY1dG9yajVqeTlCUVFhTVFXZituclB3ZHRyY2xyN0FkNnRtSnl3WkZBUS9oRDJvR3FsWFhROFZxcis4UzAxUDFLb05vZit1dEgwZ0xtOWVPRzQ3WFhUK05rZURUb2Y1UjVXQT09")
        self.user_agent = "MediaHubMX/2"
        self.catalog_url = _d("aHR0cHM6Ly92YXZvby5jYy92dG8tY2x1c3Rlci9tZWRpYWh1Ym14LWNhdGFsb2cuanNvbg==")
        self.resolve_url = _d("aHR0cHM6Ly92YXZvby50by92dG8tY2x1c3Rlci9tZWRpYWh1Ym14LXJlc29sdmUuanNvbg==")

    def get_auth_signature(self):
        now = int(time.time() * 1000)
        if self.cache.get("signfile") and now < (int(self.cache.get("signfile_valid_until", 0)) - 60000):
            return self.cache["signfile"]
        try:
            ping_url = _d("aHR0cHM6Ly93d3cudmF2b28udHYvYXBpL2JveC9waW5nMg==")
            r = requests.post(ping_url, data={_d("dmVj"): self.v}, timeout=10, verify=False)
            res = r.json().get("response", {})
            if res.get("signed"):
                self.cache["signfile"] = res["signed"]
                self.cache["signfile_valid_until"] = res.get("sigValidUntil")
                return res["signed"]
        except: return None

    def fetch_soja(self, language="de", region="AT", catalog_id=_d("dnRvLWlwdHY=")):
        soja = []
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
                    soja.append({"text": name, "url": item.get("url")})
                cursor = data.get("nextCursor")
                if not cursor: break
            except: break
        return soja

    def puste_kuchen(self, url):
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
    print("Starte Anfrage...")
    core = HamSter()
    raw_soja = core.fetch_soja()
    print(f"{len(raw_soja)} Möglichkeiten gefunden. Das dauert jetzt was...")

    salat_lines = [_d("I0VYVE0zVQ==")]
    
    def process_blatt(ch):
        name = ch.get('text', 'Unknown')
        orig_url = ch.get('url')
        if not orig_url:
            return None
        grob_ian = _d("dmF2b28udG8=")
        resolved = core.puste_kuchen(orig_url) if grob_ian in orig_url else orig_url
        if resolved:
            return f"#EXTINF:-1,{name}\n{resolved}"
        return None

    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(process_blatt, ch): ch for ch in raw_soja}
        for future in as_completed(futures):
            res = future.result()
            if res:
                salat_lines.append(res)

    with open("krautsalat", "w", encoding="utf-8") as f:
        f.write("\n".join(salat_lines))
    print("Krautsalat erfolgreich gespeichert.")