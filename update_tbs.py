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

            # === Auto-detect current cache code ===
            current_cache_code = None
            location_str = str(getattr(tb, 'location', 'Unknown'))

            # Try to extract GC code from location string
            match = re.search(r'(GC[0-9A-Z]+)', location_str)
            if match:
                current_cache_code = match.group(1)
                racer['cache'] = current_cache_code
            else:
                # If no GC code found, it's probably in someone's hands
                racer['cache'] = ""

            racer['location'] = location_str

            # === Get coordinates if we have a cache code ===
            coords = None
            if current_cache_code:
                try:
                    cache = gc.get_cache(current_cache_code)
                    cache.load()
                    if hasattr(cache, 'location') and cache.location:
                        point = cache.location
                        coords = [float(point.latitude), float(point.longitude)]
                except:
                    pass

            racer['coordinates'] = coords
            racer['last_updated'] = datetime.now().isoformat()

            print(f"   ✅ Updated | Location: {racer['location']}")
            if current_cache_code:
                print(f"   📍 Cache: {current_cache_code} | Coordinates: {coords}")
            else:
                print("   📍 In hands of a geocacher (no cache)")

    except Exception as e:
        print(f"   ❌ Error with {tb_code}: {e}")

# Save updated data
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(racers, f, indent=2, ensure_ascii=False)

print("\n🎉 Update completed! (Auto cache detection + coordinates)")
