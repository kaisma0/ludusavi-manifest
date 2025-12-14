import yaml
import urllib.request
import os
import sys

# ================= CONFIGURATION =================
STATS_DIR = "C:/Program Files (x86)/Steam/appcache/stats"
OFFICIAL_MANIFEST_URL = "https://raw.githubusercontent.com/mtkennerly/ludusavi-manifest/master/data/manifest.yaml"
OUTPUT_FILENAME = "custom_manifest.yaml"
# =================================================

# Try to use C-Accelerated parser if available
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def generate_custom_manifest():
    print(f"Downloading official manifest...")
    try:
        with urllib.request.urlopen(OFFICIAL_MANIFEST_URL) as response:
            data = yaml.load(response.read(), Loader=Loader)
    except Exception as e:
        print(f"Error downloading: {e}")
        sys.exit(1)

    print("Injecting Steam Stats paths...")
    
    for game_name, game_data in data.items():
        if 'steam' in game_data and 'id' in game_data['steam']:
            steam_app_id = game_data['steam']['id']
            
            # Schema: UserGameStatsSchema_APPID.bin
            schema_file = f"{STATS_DIR}/UserGameStatsSchema_{steam_app_id}.bin"
            
            # Stats: UserGameStats_<storeUserId>_APPID.bin
            stats_file = f"{STATS_DIR}/UserGameStats_<storeUserId>_{steam_app_id}.bin"

            if 'files' not in game_data:
                game_data['files'] = {}

            # Inject Schema
            game_data['files'][schema_file] = {
                'tags': ['save'],
                'when': [{'store': 'steam'}]
            }

            # Inject Stats
            game_data['files'][stats_file] = {
                'tags': ['save'],
                'when': [{'store': 'steam'}]
            }

    print(f"Saving to {OUTPUT_FILENAME}...")
    with open(OUTPUT_FILENAME, 'w', encoding='utf-8') as f:
        # Sort keys makes the file deterministic (fewer git changes)
        yaml.dump(data, f, Dumper=Dumper, sort_keys=True)
    
    print("Success.")

if __name__ == "__main__":
    generate_custom_manifest()