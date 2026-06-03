import pycaching
import asyncio
import json
from datetime import datetime
import os

# ====================== CONFIG ======================
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"❌ Error: {CONFIG_FILE} not found!")
        print("Please create the config.json file first.")
        exit(1)
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

config = load_config()

# ====================== YOUR TBS ======================
TB_CODES = [
    "TB83TQH",   # ← Replace with your real TB codes
    "TB83TPR",
    # Add maximum 10 here
]

# =====================================================

async def fetch_tb(tb_code: str):
    try:
        c = pycaching.Geocaching()
        await c.login(config["gc_username"], config["gc_password"])

        tb = await c.get_trackable(tb_code.upper())
        
        if not tb:
            print(f"   ❌ {tb_code} not found")
            return None

        data = {
            "car": tb.name,                    # Using TB name as car for now
            "reference": tb.code,
            "cache": None,
            "lat": None,
            "lng": None,
            "last_updated": datetime.utcnow().isoformat()
        }

        if tb.current_cache:
            cache = tb.current_cache
            data["cache"] = cache.code
            
            if hasattr(cache, 'location') and cache.location:
                data["lat"] = cache.location.latitude
                data["lng"] = cache.location.longitude

        print(f"   ✅ {tb.code}  →  {data['cache'] or 'Not in cache'}")
        return data

    except Exception as e:
        print(f"   ❌ Error with {tb_code}: {e}")
        return None


async def update_all():
    print(f"🚀 Starting update at {datetime.utcnow()}")
    
    results = []
    for i, tb_code in enumerate(TB_CODES):
        print(f"[{i+1}/{len(TB_CODES)}] Fetching {tb_code}...")
        result = await fetch_tb(tb_code)
        if result:
            results.append(result)
        
        await asyncio.sleep(4)   # Polite delay

    # Save in the exact format your website expects
    output = {
        "updated": datetime.utcnow().isoformat(),
        "tb": results
    }

    with open("locations.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Done! Updated {len(results)} Travelbugs.")
    print("   locations.json has been updated.")


if __name__ == "__main__":
    asyncio.run(update_all())