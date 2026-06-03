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
            racer['location'] = str(getattr(tb, 'location', 'Unknown'))

            coords = None

            # === NEW: Try to extract GC code from location string ===
            gc_code = None
            if isinstance(racer['location'], str):
                # Look for GC followed by letters/numbers
                match = re.search(r'GC[A-Z0-9]+', racer['location'])
                if match:
                    gc_code = match.group(0)
                    print(f"   → Found GC code in location: {gc_code}")

            # Use extracted GC code or tb.cache
            if not gc_code and hasattr(tb, 'cache') and tb.cache and tb.cache.code:
                gc_code = tb.cache.code

            # === Fetch coordinates using GC code ===
            if gc_code:
                try:
                    print(f"   → Loading cache {gc_code} for coordinates...")
                    cache = gc.get_cache(gc_code)
                    if hasattr(cache, 'location') and cache.location:
                        coords = [float(cache.location.lat), float(cache.location.lon)]
                        print(f"   → ✅ SUCCESS! Coordinates found: {coords}")
                    racer['cache'] = gc_code
                except Exception as e:
                    print(f"   → Cache fetch failed: {e}")

            # Final fallback: manual coordinates (you can expand this)
            if not coords:
                manual = {
                    "Papaschlumpf": [51.12, 6.40],
                    "Todten Frau": [50.85, 4.35],
                    "Route 73": [48.85, 2.35]
                }
                for key, pos in manual.items():
                    if key.lower() in racer['location'].lower():
                        coords = pos
                        print(f"   → Used manual coordinates for {key}")
                        break

            racer['coordinates'] = coords
            racer['last_updated'] = datetime.now().isoformat()

            if hasattr(tb, 'distance_traveled') and tb.distance_traveled is not None:
                racer['km'] = int(tb.distance_traveled)

            status = "✅ WITH coordinates" if coords else "⚠️ without coordinates"
            print(f"   {status} - {racer['location']}\n")

    except Exception as e:
        print(f"   ❌ Error with {tb_code}: {e}\n")

# Save
with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(racers, f, indent=2, ensure_ascii=False)

print("🎉 Update completed!")
