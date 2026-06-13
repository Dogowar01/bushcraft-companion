#!/usr/bin/env python
"""Download + optimise relevant Wikimedia Commons photos for Bushcraft Companion.
Resilient: per-image try/except, records attribution, writes a manifest."""
import json, os, sys, time, urllib.parse, urllib.request, io
from PIL import Image

UA = "BushcraftCompanion/1.0 (https://github.com/Dogowar01/bushcraft-companion; dogowar2010@gmail.com)"
OUT = "img"
os.makedirs(OUT, exist_ok=True)
API = "https://commons.wikimedia.org/w/api.php"

def api_search(query, want_w):
    params = {
        "action":"query","format":"json","generator":"search",
        "gsrsearch": query, "gsrnamespace":"6", "gsrlimit":"6",
        "prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":str(want_w),
    }
    url = API + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent":UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    pages = (data.get("query") or {}).get("pages") or {}
    # sort by search index order
    items = sorted(pages.values(), key=lambda p: p.get("index", 999))
    for p in items:
        title = p.get("title","")
        low = title.lower()
        if not (low.endswith(".jpg") or low.endswith(".jpeg") or low.endswith(".png")):
            continue
        if "icon" in low or "logo" in low or "map" in low or ".svg" in low:
            continue
        ii = (p.get("imageinfo") or [{}])[0]
        if ii.get("thumburl"):
            return title, ii
    return None, None

def crop_cover(im, tw, th):
    im = im.convert("RGB")
    w,h = im.size
    scale = max(tw/w, th/h)
    nw,nh = int(w*scale+0.5), int(h*scale+0.5)
    im = im.resize((nw,nh), Image.LANCZOS)
    left = (nw-tw)//2; top = (nh-th)//2
    return im.crop((left, top, left+tw, top+th))

def clean(s):
    import re
    s = re.sub("<[^>]+>"," ", s or "")
    s = s.replace("&amp;","&").replace("&#160;"," ")
    return " ".join(s.split())[:140]

# (key, query, target_w, target_h, quality)
ITEMS = [
 # ----- section banners (wide) -----
 ("ban-guides","Eucalyptus forest Australia",1000,360,80),
 ("ban-firstaid","First aid kit outdoor",1000,360,80),
 ("ban-projects","Bushcraft camp shelter",1000,360,80),
 ("ban-notes","Notebook pencil wood desk",1000,360,80),
 ("ban-plants","Bush tucker foraging Australia",1000,360,80),
 # ----- encyclopedia category banners (wide) -----
 ("cat-fire","Campfire night",1000,300,80),
 ("cat-shelter","Tarp shelter bushcraft",1000,300,80),
 ("cat-water","Mountain stream creek",1000,300,80),
 ("cat-food","Wild edible plants foraging",1000,300,80),
 ("cat-signalling","Signal fire smoke rescue",1000,300,80),
 ("cat-psychology","Hiker silhouette forest fog",1000,300,80),
 # ----- knots (square-ish cards) -----
 ("knot-bowline","Bowline knot",520,400,82),
 ("knot-clove-hitch","Clove hitch",520,400,82),
 ("knot-taut-line","Taut-line hitch",520,400,82),
 ("knot-figure-eight","Figure-eight knot",520,400,82),
 ("knot-sheet-bend","Sheet bend",520,400,82),
 ("knot-reef-knot","Reef knot",520,400,82),
 ("knot-timber-hitch","Timber hitch",520,400,82),
 ("knot-half-hitch","Half hitch knot",520,400,82),
 ("knot-rolling-hitch","Rolling hitch",520,400,82),
 ("knot-truckers-hitch","Trucker's hitch",520,400,82),
 ("knot-prusik","Prusik knot",520,400,82),
 ("knot-fishermans","Fisherman's knot",520,400,82),
 # ----- snakes / spiders (species, scientific names) -----
 ("fa-snake-brown","Pseudonaja textilis",520,400,82),
 ("fa-snake-tiger","Notechis scutatus",520,400,82),
 ("fa-snake-taipan","Oxyuranus scutellatus",520,400,82),
 ("fa-snake-rbb","Pseudechis porphyriacus",520,400,82),
 ("fa-snake-deathadder","Acanthophis antarcticus",520,400,82),
 ("fa-spider-funnelweb","Atrax robustus",520,400,82),
 ("fa-spider-redback","Latrodectus hasselti",520,400,82),
 ("fa-spider-whitetail","Lampona cylindrata",520,400,82),
 # ----- bush tucker plants (scientific names) -----
 ("plant-macadamia","Macadamia integrifolia nut",600,460,82),
 ("plant-finger-lime","Citrus australasica",600,460,82),
 ("plant-lilly-pilly","Syzygium smithii fruit",600,460,82),
 ("plant-warrigal-greens","Tetragonia tetragonioides",600,460,82),
 ("plant-quandong","Santalum acuminatum fruit",600,460,82),
 ("plant-bunya","Araucaria bidwillii cone",600,460,82),
 ("plant-kakadu-plum","Terminalia ferdinandiana",600,460,82),
 ("plant-wattleseed","Acacia victoriae seed",600,460,82),
 ("plant-native-raspberry","Rubus parvifolius fruit",600,460,82),
 ("plant-pigface","Carpobrotus glaucescens",600,460,82),
 ("plant-bush-tomato","Solanum centrale",600,460,82),
 ("plant-river-mint","Mentha australis",600,460,82),
]

manifest = {}
ok=0; fail=0
for key, query, tw, th, q in ITEMS:
    try:
        title, ii = api_search(query, max(tw, th)*2)
        if not ii:
            print("MISS", key, "|", query); fail+=1; continue
        thumb = ii["thumburl"]
        req = urllib.request.Request(thumb, headers={"User-Agent":UA})
        with urllib.request.urlopen(req, timeout=40) as r:
            raw = r.read()
        im = Image.open(io.BytesIO(raw))
        im = crop_cover(im, tw, th)
        path = os.path.join(OUT, key+".jpg")
        im.save(path, quality=q, optimize=True)
        em = ii.get("extmetadata") or {}
        manifest[key] = {
            "file": title,
            "artist": clean((em.get("Artist") or {}).get("value","")),
            "license": (em.get("LicenseShortName") or {}).get("value",""),
            "descurl": "https://commons.wikimedia.org/wiki/"+urllib.parse.quote(title.replace(" ","_")),
            "bytes": os.path.getsize(path),
            "query": query,
        }
        print("OK  ", key, "->", title, manifest[key]["bytes"], "b")
        ok+=1
        time.sleep(0.2)
    except Exception as e:
        print("ERR ", key, "|", query, "|", repr(e)[:120]); fail+=1

with open(os.path.join(OUT,"credits.json"),"w",encoding="utf-8") as f:
    json.dump(manifest, f, indent=1, ensure_ascii=False)
print(f"\nDONE ok={ok} fail={fail}  total bytes={sum(m['bytes'] for m in manifest.values())}")
