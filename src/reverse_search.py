import os
import json
from pathlib import Path

import serpapi
from dotenv import load_dotenv


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "input"
OUTPUT_DIR = PROJECT_ROOT / "output"

IMAGE_PATH = INPUT_DIR / "test.jpeg"
RESULT_PATH = OUTPUT_DIR / "reverse_search_results.json"


def main():
    # Load API key from .env
    load_dotenv(PROJECT_ROOT / ".env")

    api_key = os.getenv("SERPAPI_KEY")

    if not api_key:
        print("ERROR: SERPAPI_KEY not found in .env")
        return

    if not IMAGE_PATH.exists():
        print(f"ERROR: Image not found: {IMAGE_PATH}")
        return

    print(f"Image: {IMAGE_PATH}")
    print("Uploading image to SerpApi...")

    # Create SerpApi client
    client = serpapi.Client(api_key=api_key)

    # Upload local image
    upload = client.upload_image(str(IMAGE_PATH))

    if "error" in upload:
        print("Upload error:", upload["error"])
        return

    image_id = upload["image_id"]
    print("Image uploaded successfully.")

    # Search the uploaded image with Google Lens
    print("Searching with Google Lens...")

    results = client.search({
        "engine": "google_lens",
        "image_id": image_id,
        "type": "all"
    })

    # Save complete structured results
    OUTPUT_DIR.mkdir(exist_ok=True)

    with open(RESULT_PATH, "w", encoding="utf-8") as file:
        json.dump(dict(results), file, indent=2, ensure_ascii=False)

    print()
    print("SUCCESS!")
    print(f"Results saved to: {RESULT_PATH}")

    # Show useful match information
    exact_matches = results.get("exact_matches", [])
    visual_matches = results.get("visual_matches", [])

    print(f"Exact matches found: {len(exact_matches)}")
    print(f"Visual matches found: {len(visual_matches)}")

    if exact_matches:
        print()
        print("EXACT MATCHES:")

        for match in exact_matches[:5]:
            print("-", match.get("title", "No title"))
            print(" ", match.get("link", "No link"))

    elif visual_matches:
        print()
        print("VISUAL MATCHES:")

        for match in visual_matches[:5]:
            print("-", match.get("title", "No title"))
            print(" ", match.get("link", "No link"))


if __name__ == "__main__":
    main()