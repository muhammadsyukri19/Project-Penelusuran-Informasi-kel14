import json
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ===================== KONFIG DASAR =====================

# sitemap index bola kompas
SITEMAP_URL = "https://bola.kompas.com/sitemap.xml"

MAX_ITEMS = 350  # target artikel yang mau diambil

TITLE_SELECTORS = [
    ".read__title",
    "h1.read__title",
    "h1",
]

# fokus hanya ke blok konten utama
CONTENT_BLOCK_SELECTORS = [
    ".read__content",
]

IMAGE_SELECTORS = [
    ".read__content img",
    ".article__body img",
    "figure img",
]

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

# ===================== FILTER BOLA INDONESIA =====================

ID_FOOTBALL_KEYWORDS = [
    # kompetisi lokal
    "liga 1", "liga1", "bri liga 1",
    "liga 2", "liga2",
    "liga 3", "liga3",
    "liga indonesia",
    "liga indonesia baru",
    "piala presiden",
    "piala menpora",
    "piala indonesia",
    "elite pro academy",

    # timnas
    "timnas indonesia",
    "timnas u-23", "timnas u23",
    "timnas u-20", "timnas u20",
    "timnas u-19", "timnas u19",
    "garuda muda", "garuda nusantara",

    # tokoh
    "erick thohir",
    "shin tae-yong", "shin taeyong",
    "indra sjafri",

    # klub lokal
    "persib", "persija", "persebaya", "arema", "arema fc",
    "psm makassar", "psm", "bali united",
    "madura united", "borneo fc", "persik kediri",
    "psis semarang", "persita", "persikabo",
    "dewa united", "rans nusantara", "persis solo",
]


def is_kompas_bola_url(url: str) -> bool:
    """Pastikan URL dari kanal bola Kompas."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if "kompas.com" not in host:
        return False

    if host.startswith("bola.kompas.com"):
        return True

    if "/bola/" in path:
        return True

    return False


def is_indonesia_football(title: str, content: str) -> bool:
    """Filter hanya artikel sepak bola Indonesia (berbasis keyword)."""
    text = f"{title or ''}\n{content or ''}".lower()
    return any(kw in text for kw in ID_FOOTBALL_KEYWORDS)


# ===================== URL DISCOVERY (REKURSIF SITEMAP) =====================

def collect_article_urls_from_sitemap(sitemap_url: str, limit: int, urls: list, visited: set):
    """
    Rekursif:
      - kalau loc berakhir .xml → dianggap sitemap lagi → fetch lagi
      - kalau loc bukan .xml → dianggap kandidat artikel
    """
    if sitemap_url in visited:
        return
    if len(urls) >= limit:
        return

    visited.add(sitemap_url)

    try:
        resp = requests.get(sitemap_url, headers=HEADERS, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"Gagal fetch sitemap {sitemap_url}: {e}")
        return

    soup = BeautifulSoup(resp.content, "xml")

    loc_tags = soup.find_all("loc")
    if not loc_tags:
        return

    for loc in loc_tags:
        u = loc.get_text(strip=True)
        u = re.sub(r"\s+", " ", u).strip()
        if not u:
            continue

        # skip sitemap gambar
        if "images/sitemap" in u:
            continue

        # kalau masih sitemap (berakhir .xml) → rekursif
        if u.lower().endswith(".xml"):
            collect_article_urls_from_sitemap(u, limit, urls, visited)
            if len(urls) >= limit:
                break
            continue

        # kalau sudah URL artikel:
        if not is_kompas_bola_url(u):
            continue

        parsed = urlparse(u)
        path = parsed.path.lower()

        # kompas artikel bola biasanya pakai /read/ di path
        if "/read/" not in path:
            # biasanya ini halaman kategori / homepage, bukan artikel
            continue

        if u not in urls:
            urls.append(u)
            if len(urls) >= limit:
                break


def get_urls_from_sitemap(root_sitemap_url: str, limit: int):
    urls = []
    visited = set()
    collect_article_urls_from_sitemap(root_sitemap_url, limit, urls, visited)

    print("Contoh URL artikel dari hasil crawling sitemap (max 10):")
    for u in urls[:10]:
        print("  ", u)

    return urls


# ===================== CLEANING KONTEN =====================

def clean_block(block):
    """
    Buang iklan/crossportal, 'Baca Juga', menu, footer, dan elemen pengganggu
    lain dalam satu blok konten Kompas.
    """

    # 1. Buang elemen pengganggu via selector
    for sel in [
        ".crossportal", ".ads", ".advertisement",
        ".read-also", ".baca-juga", ".baca_juga", ".bacajuga",
        ".sosmed", ".share", ".tag", ".lihat-juga", ".related",
        ".pagination", ".recommendation",
        ".widget", ".widget-area",
        ".breadcumb", ".breadcrumb", ".read__footer",
        "script", "style", "noscript", "iframe",
        "aside",
        "[class*='ads']", "[id*='ads']",
        "[class*='ad-']", "[id*='ad-']",
        "[class*='banner']", "[id*='banner']",
        "[class*='promo']", "[id*='promo']",
        "[class*='iklan']", "[id*='iklan']",
    ]:
        for bad in block.select(sel):
            bad.decompose()

    # 2. Ambil teks per baris
    raw_text = block.get_text("\n", strip=True)
    lines = raw_text.splitlines()

    cleaned_lines = []
    skip_next_after_baca_juga = False

    # keyword yang kalau muncul → barisnya dibuang (menu, footer, dll)
    chrome_keywords = [
        "otomatis",
        "mode gelap",
        "mode terang",
        "login",
        "gabung kompas.com+",
        "konten yang disimpan",
        "konten yang disukai",
        "atur minat",
        "berikan masukanmu",
        "langganan kompas one",
        "membership kompas.com+",
        "now trending",
        "terpopuler",
        "mungkin anda melewatkan ini",
        "komentar di artikel lainnya",
        "kanal",
        "network",
        "artikel terpopuler",
        "artikel terkini",
        "topik pilihan",
        "artikel headline",
        "about us",
        "advertise",
        "ketentuan penggunaan",
        "kebijakan data pribadi",
        "pedoman media siber",
        "career",
        "contact us",
        "copyright 2008",
        "kg media",
        "kgnow!",
        "daftarkan email",
        "dapatkan informasi dan insight pilihan redaksi kompas.com",
        "baca berita tanpa iklan.",
        "unduh kompas.com app",
        "download kompas.com app",
        "download sekarang",
    ]

    # kalau ketemu salah satu ini → anggap footer, stop di sini
    hard_stop_phrases = [
        "dalam segala situasi, kompas.com berkomitmen",
        "baca berita tanpa iklan.",
    ]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        low = stripped.lower()

        # 2.a. hard stop → semua setelah ini tidak diambil
        if any(stop in low for stop in hard_stop_phrases):
            break

        # 2.b. buang baris yang jelas bagian chrome / menu
        if any(kw in low for kw in chrome_keywords):
            continue

        # 2.c. logika khusus "Baca Juga": buang baris ini + baris berikutnya
        if "baca juga" in low:
            skip_next_after_baca_juga = True
            continue

        if skip_next_after_baca_juga:
            skip_next_after_baca_juga = False
            continue

        cleaned_lines.append(stripped)

    text = "\n".join(cleaned_lines)

    # 3. Rapikan whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()

    return text


def extract_title(soup):
    for sel in TITLE_SELECTORS:
        el = soup.select_one(sel)
        if el and el.get_text(strip=True):
            return el.get_text(strip=True)
    og = soup.find("meta", property="og:title")
    if og and og.get("content"):
        return og["content"].strip()
    return None


def extract_images(soup, base_url):
    imgs = []
    for sel in IMAGE_SELECTORS:
        for im in soup.select(sel):
            if im.name == "img":
                src = (
                    im.get("src")
                    or im.get("data-src")
                    or im.get("data-original")
                )
                if src:
                    imgs.append(urljoin(base_url, src))

    if not imgs:
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            imgs.append(urljoin(base_url, og["content"]))

    out = []
    for u in imgs:
        if u and u not in out:
            out.append(u)
    return out


def find_content_blocks(soup):
    blocks = []
    for sel in CONTENT_BLOCK_SELECTORS:
        blocks.extend(soup.select(sel))
    uniq = []
    seen = set()
    for b in blocks:
        if id(b) not in seen:
            uniq.append(b)
            seen.add(id(b))
    return uniq


def try_follow_pagination(url, soup):
    """
    Cari halaman lanjutan (?page=2,3,all).
    """
    extra_pages = []

    for a in soup.select("a[href]"):
        href = a["href"]
        if "page=" in href:
            extra_pages.append(urljoin(url, href))

    base = url.split("?")[0].rstrip("/")
    for i in range(2, 5):
        guess = f"{base}?page={i}"
        extra_pages.append(guess)
    extra_pages.append(f"{base}?page=all")

    seen = set()
    ordered = []
    for u in extra_pages:
        if u not in seen:
            ordered.append(u)
            seen.add(u)

    return ordered


def fetch(url):
    # ini sekarang HANYA dipakai untuk URL artikel, bukan sitemap .xml
    r = requests.get(url, headers=HEADERS, timeout=25)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


def scrape_article(url):
    """
    Ambil title, content (multi-page), images, published_at
    untuk Kompas Bola, lalu filter hanya bola Indonesia.
    """
    try:
        soup = fetch(url)
    except Exception as e:
        return None, f"request failed: {e}"

    title = extract_title(soup)

    # halaman utama
    blocks = find_content_blocks(soup)
    texts = []
    for b in blocks:
        txt = clean_block(b)
        if txt:
            texts.append(txt)

    # halaman lanjutan
    for u2 in try_follow_pagination(url, soup):
        parsed_main = urlparse(url)
        parsed_child = urlparse(u2)
        if parsed_child.netloc and parsed_child.netloc != parsed_main.netloc:
            continue
        try:
            s2 = fetch(u2)
        except Exception:
            continue
        b2 = find_content_blocks(s2)
        added = 0
        for b in b2:
            txt = clean_block(b)
            if txt and txt not in texts:
                texts.append(txt)
                added += 1
        if added == 0 and "page=2" in u2:
            break

    content_text = "\n\n".join(texts).strip()

    # --- batasi panjang maksimum konten (misal 5000 karakter) ---
    MAX_CONTENT_CHARS = 5000

    if len(content_text) > MAX_CONTENT_CHARS:
        paragraphs = content_text.split("\n")
        truncated = []
        total = 0
        for p in paragraphs:
            p = p.strip()
            if not p:
                continue
            if total + len(p) + 1 > MAX_CONTENT_CHARS:
                break
            truncated.append(p)
            total += len(p) + 1
        content_text = "\n".join(truncated).strip()
    # -------------------------------------------------------------

    # threshold minimum
    if len(content_text) < 400:
        return None, "content too short"

    # filter bola Indonesia
    if not is_indonesia_football(title, content_text):
        return None, "not indonesia football"

    images = extract_images(soup, url)

    published_at = None
    ld = soup.find("meta", attrs={"itemprop": "datePublished"})
    if ld and ld.get("content"):
        published_at = ld["content"].strip()
    if not published_at:
        meta = soup.find("meta", property="article:published_time")
        if meta and meta.get("content"):
            published_at = meta["content"].strip()

    item = {
        "url": url,
        "title": title,
        "published_at": published_at,
        "images": images,
        "content": content_text,
        "content_length": len(content_text),
    }
    return item, None


# ===================== MAIN =====================

def main():
    urls = get_urls_from_sitemap(SITEMAP_URL, MAX_ITEMS)
    print(f"Total URL artikel hasil pengambilan dari sitemap: {len(urls)}")

    results = []
    for i, u in enumerate(urls, 1):
        if not u.startswith("http"):
            u = urljoin(SITEMAP_URL, u)

        print(f"[{i}/{len(urls)}] {u}")
        item, err = scrape_article(u)
        if err:
            print(f"  -> {err}, skipped")
        else:
            results.append(item)
            print(f"  -> ok, {item['content_length']} chars")

        time.sleep(0.8)

    with open("kompas_bola_indonesia.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} items to kompas_bola_indonesia.json")


if __name__ == "__main__":
    main()
