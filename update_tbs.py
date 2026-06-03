import pycaching
import json
from datetime import datetime
import re

JSON_FILE = 'racers.json'

print("🔑 Logging into Geocaching.com...")
gc = pycaching.login()

with open(JSON_FILE, 'r', encoding='utf-8') as f:
    racers = json.load(f)

print(f"Loaded {len(racers)} racers.\n")

for racer in racers:
    tb_code = racer.get('reference')
    if not tb_code:
        continue

    try:
        print(f"Fetching {tb_code} → {racer.get('car')}")
        tb = gc.get_trackable(tb_code)

        if tb:
            racer['name'] = getattr(tb, 'name', racer.get('car'))
            racer['location'] = str(getattr(tb, 'location', racer.get('location', 'Unknown')))

            # === Coordinates (working part) ===
            coords = None
            gc_code = racer.get('cache')
            if gc_code:
                try:
                    cache = gc.get_cache(gc_code)
                    cache.load()
                    if hasattr(cache, 'location') and cache.location:
                        point = cache.location
                        coords = [float(point.latitude), float(point.longitude)]
                except:
                    pass

            racer['coordinates'] = coords
            racer['last_updated'] = datetime.now().isoformat()

            print(f"   ✅ Updated | Location: {racer['location']} | KM: {racer.get('km', 0)} (manual)")

    except Exception as e:
        print(f"   ❌ Error with {tb_code}: {e}")

# Save
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(racers, f, indent=2, ensure_ascii=False)

print("\n🎉 Update completed! (Locations + Coordinates updated - KM stays manual)")
