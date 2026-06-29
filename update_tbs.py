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
        print("=" * 60)
        print(f"Fetching {tb_code} → {racer.get('car')}")

        tb = gc.get_trackable(tb_code)
        if not tb:
            print("❌ Could not load trackable")
            continue

        racer['name'] = getattr(tb, 'name', racer.get('car'))

        location_str = str(getattr(tb, 'location', 'Unknown')).strip()
        racer['location'] = location_str

        # ----------------------------------------------------
        # TB zit in handen van een cacher
        # ----------------------------------------------------
        if location_str.lower().startswith("in the hands of"):
            racer['status'] = "in_hands"
            racer['last_updated'] = datetime.now().isoformat()

            print("🤝 TB is currently in the hands of a cacher.")
            print(f"Location : {location_str}")
            print("Keeping previous cache and coordinates.")

            continue

        # ----------------------------------------------------
        # TB zit in een cache
        # ----------------------------------------------------
        racer['status'] = "in_cache"

        current_cache_code = racer.get('cache', '').strip()

        if current_cache_code:
            print(f"Looking up cache: {current_cache_code}")

            try:
                cache = gc.get_cache(current_cache_code)
                print("✅ Cache object loaded")

                cache.load()
                print("✅ Cache details loaded")

                if hasattr(cache, "location") and cache.location:
                    point = cache.location

                    coords = [
                        float(point.latitude),
                        float(point.longitude)
                    ]

                    racer['coordinates'] = coords

                    print(f"✅ Coordinates : {coords}")
                else:
                    print("⚠️ Cache has no location!")

            except Exception as e:
                print("❌ Error while loading cache:")
                print(e)
        else:
            print("⚠️ No cache code supplied.")

        racer['last_updated'] = datetime.now().isoformat()

        print(f"Location : {racer['location']}")

    except Exception as e:
        print(f"❌ Error with {tb_code}:")
        print(e)

with open(JSON_FILE, 'w', encoding='utf-8') as f:
    json.dump(racers, f, indent=2, ensure_ascii=False)

print("\n🎉 Update completed.")
