import requests
import os
from tqdm import tqdm

# === CONFIG ===
query = "candid"
access_key = "8sAUUyVIo6TO3PeVZDHVBzqB-O5BjZuMkmR-L--Jtug"  # Replace this
download_dir = "unsplash_portraits"
num_images = 400
per_page = 30  # Max allowed per API call

os.makedirs(download_dir, exist_ok=True)

# === Fetch images ===
downloaded = 0
page = 1

print(f"🔍 Searching Unsplash for: {query}")

while downloaded < num_images:
    url = "https://api.unsplash.com/search/photos"
    params = {
        "query": query,
        "page": page,
        "per_page": per_page,
        "client_id": access_key
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    results = data.get("results", [])
    if not results:
        print("⚠️ No more results.")
        break

    for img in tqdm(results, desc=f"Page {page}"):
        if downloaded >= num_images:
            break

        img_url = img["urls"]["full"]
        img_id = img["id"]
        img_path = os.path.join(download_dir, f"{img_id}.jpg")

        try:
            img_data = requests.get(img_url).content
            with open(img_path, "wb") as f:
                f.write(img_data)
            downloaded += 1
        except Exception as e:
            print(f"Failed to download image {img_id}: {e}")

    page += 1

print(f"✅ Downloaded {downloaded} images to '{download_dir}'")
