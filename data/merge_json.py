import json

def load_articles(path, source_name):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    articles = []
    for i, item in enumerate(data):
        images = item.get("images") or []
        # ambil 1 gambar utama (kalau ada)
        main_image = images[0] if images else ""

        articles.append({
            "id": f"{source_name}_{i}",
            "source": source_name,
            "url": item.get("url", ""),
            "title": item.get("title", ""),
            "content": item.get("content", ""),
            "images": images,          # simpan semua (opsional)
            "main_image": main_image   # satu gambar utama
        })
    return articles

bolanet = load_articles("bolanet_bola_indonesia.json", "bolanet")
kompas = load_articles("kompas_bola_indonesia.json", "kompas")
sindonews = load_articles("sindonews_bola_indonesia.json", "sindonews")

all_articles = bolanet + kompas + sindonews
print(f"Total dokumen: {len(all_articles)}")

with open("merge-all.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)

print("[DONE] merge-all.json updated with images/main_image")
