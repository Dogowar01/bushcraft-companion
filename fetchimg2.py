#!/usr/bin/env python
"""Unique per-article photos + Weather + Tracks. Resilient; merges credits.json."""
import json, os, time, urllib.parse, urllib.request, io
from PIL import Image
UA="BushcraftCompanion/1.0 (https://github.com/Dogowar01/bushcraft-companion; dogowar2010@gmail.com)"
OUT="img"; API="https://commons.wikimedia.org/w/api.php"
os.makedirs(OUT,exist_ok=True)
def api_search(query,want_w):
    p={"action":"query","format":"json","generator":"search","gsrsearch":query,"gsrnamespace":"6",
       "gsrlimit":"8","prop":"imageinfo","iiprop":"url|extmetadata","iiurlwidth":str(want_w)}
    req=urllib.request.Request(API+"?"+urllib.parse.urlencode(p),headers={"User-Agent":UA})
    with urllib.request.urlopen(req,timeout=30) as r: data=json.load(r)
    pages=(data.get("query") or {}).get("pages") or {}
    for pg in sorted(pages.values(),key=lambda x:x.get("index",999)):
        t=pg.get("title",""); low=t.lower()
        if not(low.endswith(".jpg") or low.endswith(".jpeg") or low.endswith(".png")): continue
        if any(x in low for x in ("icon","logo",".svg"," map ","diagram","chart")): continue
        ii=(pg.get("imageinfo") or [{}])[0]
        if ii.get("thumburl"): return t,ii
    return None,None
def crop_cover(im,tw,th):
    im=im.convert("RGB"); w,h=im.size; s=max(tw/w,th/h)
    nw,nh=int(w*s+.5),int(h*s+.5); im=im.resize((nw,nh),Image.LANCZOS)
    l=(nw-tw)//2; t=(nh-th)//2; return im.crop((l,t,l+tw,t+th))
def clean(s):
    import re; s=re.sub("<[^>]+>"," ",s or ""); s=s.replace("&amp;","&").replace("&#160;"," ")
    return " ".join(s.split())[:140]

E=520; H=400  # standard card/hero
ITEMS=[
 # encyclopedia (file = article id)
 ("fire-ferro-rod","Ferrocerium rod sparks fire",E,H),
 ("fire-bow-drill","Bow drill friction fire",E,H),
 ("fire-flint-steel","Flint and steel fire striker",E,H),
 ("fire-lay-types","Teepee campfire logs",E,H),
 ("fire-wet-conditions","Campfire rain wet wood",E,H),
 ("fire-tinder-quality","Tinder bundle birch bark fire",E,H),
 ("shelter-lean-to","Lean-to shelter bushcraft",E,H),
 ("shelter-debris-hut","Debris hut survival shelter",E,H),
 ("shelter-tarp-configs","Tarp shelter camping forest",E,H),
 ("shelter-bivouac","Bivouac emergency shelter",E,H),
 ("shelter-site-selection","Forest campsite clearing tent",E,H),
 ("water-finding","Bush spring waterhole rocks",E,H),
 ("water-solar-still","Solar still water survival",E,H),
 ("water-rain-dew","Rainwater collection tarp",E,H),
 ("water-filtration","Filtering water cloth outdoors",E,H),
 ("water-improvised-filter","Charcoal sand water filter bottle",E,H),
 ("water-purification","Boiling water billy campfire",E,H),
 ("water-arid-signs","Dry creek bed outback Australia",E,H),
 ("food-snare-trap","Wire snare primitive trap",E,H),
 ("food-tracks","Kangaroo footprints sand",E,H),
 ("food-fishing","Hand line fishing river",E,H),
 ("food-preservation","Drying meat jerky rack",E,H),
 ("food-caloric-priority","Wild foraged food gathering",E,H),
 ("signal-mirror","Signal mirror heliograph survival",E,H),
 ("signal-ground-air","Ground rescue signal beach",E,H),
 ("signal-whistle","Emergency survival whistle",E,H),
 ("signal-smoke","Signal smoke fire",E,H),
 ("signal-fire","Signal beacon fire night",E,H),
 ("psych-stop","Lost hiker forest map",E,H),
 ("psych-panic","Hiker resting rock alone",E,H),
 ("psych-decisions","Hiker compass map planning",E,H),
 ("psych-will","Lone hiker mountain sunrise",E,H),
 ("psych-group","Group hikers helping trail",E,H),
 # first aid procedures (file = fa id) — non-graphic / training imagery
 ("fa-bleeding","Pressure bandage arm first aid",E,H),
 ("fa-burns","Cooling burn running water first aid",E,H),
 ("fa-hypothermia","Emergency thermal blanket rescue",E,H),
 ("fa-heat","Hydration water hat sun heat",E,H),
 ("fa-snake-general","Snake bite first aid bandage",E,H),
 ("fa-pib","Compression bandage leg first aid",E,H),
 ("fa-fractures","Arm splint first aid",E,H),
 ("fa-shock","First aid recovery position",E,H),
 ("fa-cpr","CPR training manikin resuscitation",E,H),
 ("fa-drowning","Lifeguard water rescue",E,H),
 ("fa-eye","Eye wash irrigation first aid",E,H),
 ("fa-anaphylaxis","Adrenaline autoinjector epipen",E,H),
 # projects (file = proj-<id>)
 ("proj-camp-chair","Bushcraft wooden camp chair",E,H),
 ("proj-tripod-pot-hanger","Campfire tripod cooking pot",E,H),
 ("proj-fishing-kit","Improvised fishing hook line",E,H),
 ("proj-a-frame-tarp","A-frame tarp tent ridgeline",E,H),
 ("proj-stretcher","Improvised stretcher rescue carry",E,H),
 ("proj-debris-shelter-build","Bushcraft shelter building forest",E,H),
 ("proj-water-filter-build","DIY layered water filter bottle",E,H),
 # weather (file = id) — clouds/sky
 ("weather-red-sky","Red sky sunset clouds",600,400),
 ("weather-mares-tails","Cirrus clouds mares tails sky",600,400),
 ("weather-mackerel","Mackerel sky altocumulus",600,400),
 ("weather-halo","22 degree halo sun",600,400),
 ("weather-lenticular","Lenticular cloud",600,400),
 ("weather-cumulonimbus","Cumulonimbus thunderstorm cloud",600,400),
 ("weather-lowering","Dark storm clouds approaching",600,400),
 ("weather-fog","Valley fog morning mist",600,400),
 ("weather-wind","Wind storm bent trees",600,400),
 # tracks (file = id) — Australian animals
 ("track-kangaroo","Eastern grey kangaroo",E,H),
 ("track-wallaby","Red-necked wallaby",E,H),
 ("track-wombat","Common wombat",E,H),
 ("track-emu","Emu Dromaius",E,H),
 ("track-dingo","Dingo Canis",E,H),
 ("track-echidna","Short-beaked echidna",E,H),
 ("track-possum","Common brushtail possum",E,H),
 ("track-goanna","Lace monitor goanna Varanus varius",E,H),
 ("track-feral-pig","Feral pig Sus scrofa",E,H),
 ("track-deer","Fallow deer",E,H),
 ("track-platypus","Platypus",E,H),
 ("track-cassowary","Southern cassowary",E,H),
]
cr={}
try: cr=json.load(open(os.path.join(OUT,"credits.json"),encoding="utf-8"))
except Exception: pass
ok=fail=0
for it in ITEMS:
    key,query,tw,th=it
    try:
        t,ii=api_search(query,max(tw,th)*2)
        if not ii: print("MISS",key,"|",query); fail+=1; continue
        req=urllib.request.Request(ii["thumburl"],headers={"User-Agent":UA})
        with urllib.request.urlopen(req,timeout=40) as r: raw=r.read()
        crop_cover(Image.open(io.BytesIO(raw)),tw,th).save(os.path.join(OUT,key+".jpg"),quality=82,optimize=True)
        em=ii.get("extmetadata") or {}
        cr[key]={"file":t,"artist":clean((em.get("Artist") or {}).get("value","")),
            "license":(em.get("LicenseShortName") or {}).get("value",""),
            "descurl":"https://commons.wikimedia.org/wiki/"+urllib.parse.quote(t.replace(" ","_")),
            "bytes":os.path.getsize(os.path.join(OUT,key+".jpg")),"query":query}
        print("OK  ",key,"->",t[:60]); ok+=1; time.sleep(0.15)
    except Exception as e:
        print("ERR ",key,"|",repr(e)[:90]); fail+=1
json.dump(cr,open(os.path.join(OUT,"credits.json"),"w",encoding="utf-8"),indent=1,ensure_ascii=False)
print(f"\nDONE ok={ok} fail={fail}")
