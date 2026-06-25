import pycaching
import json
from datetime import datetime

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
        if not tb:
            print("   ❌ Could not load trackable")
            continue

        racer['name'] = getattr(tb, 'name', racer.get('car'))

        # Use the manual cache code from JSON
        current_cache_code = racer.get('cache', '').strip()

        location_str = str(getattr(tb, 'location', 'Unknown')).strip()
        racer['location'] = location_str

        # Get coordinates if cache code is provided
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
            print(f"   📍 Cache: {current_cache_code} | Coordinates: {'Yes' if coords else 'No'}")
        else:
            print("   📍 In hands of a geocacher (no cache code set)")

    except Exception as e:
        print(f"   ❌ Error with {tb_code}: {e}")

# Save updated data
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(racers, f, indent=2, ensure_ascii=False)

print("\n🎉 Update completed! (Manual cache mode)")
