import json

def load_articles(path, source_name):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    articles = []
    for i, item in enumerate(data):
        articles.append({
            "id": f"{source_name}_{i}",
            "source": source_name,
            "url": item.get("url", ""),
            "title": item.get("title", ""),
            "published_at": item.get("published_at", ""),
            "content": item.get("content", "")
        })
    return articles

bolanet = load_articles("data/bolanet_bola_indonesia.json", "bolanet")
kompas = load_articles("data/kompas_bola_indonesia.json", "kompas")
sindonews = load_articles("data/sindonews_bola_indonesia.json", "sindonews")

all_articles = bolanet + kompas + sindonews
print(f"Total dokumen: {len(all_articles)}")

with open("merge-all.json", "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=2)
