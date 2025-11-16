import json
import re
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ===================== KONFIG DASAR =====================

SITEMAP_URL = "https://www.bola.net/sitemap/sitemap.xml"
MAX_ITEMS = 150  # target jumlah artikel

TITLE_SELECTORS = [
    "h1",
    "h1.title",
    ".title",
]

CONTENT_BLOCK_SELECTORS = [
    "article",
    ".article",
    ".content",
    "#content",
    ".main-content",
    ".news-content",
    "[itemprop='articleBody']",
]

IMAGE_SELECTORS = [
    "article img",
    ".article img",
    ".content img",
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
    "liga 1", "liga1", "bri liga 1", "bri super league",
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
    "tim nasional",
    "timnas u-23", "timnas u23",
    "timnas u-20", "timnas u20",
    "timnas u-19", "timnas u19",
    "garuda muda", "garuda nusantara",

    # tokoh / pengurus
    "erick thohir",
    "shin tae-yong", "shin taeyong",
    "indra sjafri",
    "nova arianto",

    # klub lokal
    "persib", "persija", "persebaya", "arema", "arema fc",
    "psm makassar", "psm", "bali united",
    "madura united", "borneo fc", "persik kediri",
    "psis semarang", "persita", "persikabo",
    "dewa united", "rans nusantara", "persis solo",
    "psbs biak", "bhayangkara fc", "psim yogyakarta",
]


def is_bolanet_indonesia_article_url(url: str) -> bool:
    """
    Pastikan ini URL artikel bola Indonesia:
    - domain bola.net
    - path pertama: indonesia / tim_nasional / bola_indonesia
    - bukan halaman tag/klasemen/jadwal/etc
    - biasanya .html di akhir
    """
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if "bola.net" not in host:
        return False

    # hindari halaman tag, jadwal, klasemen, galeri, video, dll
    if any(x in path for x in ["/tag/", "/klasemen/", "/jadwal", "/video", "/galeri"]):
        return False

    segments = [s for s in path.split("/") if s]
    if not segments:
        return False

    first = segments[0]
    if first not in ("indonesia", "tim_nasional", "bola_indonesia"):
        return False

    if not path.endswith(".html"):
        return False

    return True


def is_indonesia_football(title: str, content: str) -> bool:
    """Filter ekstra berbasis keyword konten + judul."""
    text = f"{title or ''}\n{content or ''}".lower()
    return any(kw in text for kw in ID_FOOTBALL_KEYWORDS)


# ===================== URL DISCOVERY (REKURSIF SITEMAP) =====================

def collect_article_urls_from_sitemap(sitemap_url: str, limit: int, urls: list, visited: set):
    """
    Rekursif:
      - kalau loc berakhir .xml → dianggap sitemap → fetch lagi
      - kalau loc bukan .xml → kandidat artikel (diseleksi lagi)
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
        if "sitemap_images" in u:
            continue

        # kalau masih sitemap (.xml) → rekursif
        if u.lower().endswith(".xml"):
            collect_article_urls_from_sitemap(u, limit, urls, visited)
            if len(urls) >= limit:
                break
            continue

        # sudah URL artikel → filter bola Indonesia
        if not is_bolanet_indonesia_article_url(u):
            continue

        if u not in urls:
            urls.append(u)
            if len(urls) >= limit:
                break


def get_urls_from_sitemap(root_sitemap_url: str, limit: int):
    urls = []
    visited = set()
    collect_article_urls_from_sitemap(root_sitemap_url, limit, urls, visited)

    print("Contoh URL artikel bola Indonesia (max 10):")
    for u in urls[:10]:
        print("  ", u)

    return urls


# ===================== CLEANING KONTEN =====================

def clean_block(block):
    """
    Bersihkan:
    - navbar / breadcrumb (Bola.net, '>')
    - 'Baca Juga' / 'Baca Ini Juga'
    - Advertisement & widget
    - baris metadata tanggal (Diperbarui:, Diterbitkan:, dll)
    (footer seperti Klasemen / Baca Artikel Menarik dipotong di level global)
    """

    # 1. Buang elemen HTML pengganggu
    for sel in [
        ".ads", ".advertisement", ".ad-banner",
        ".related", ".related-article", ".related-articles",
        ".baca-juga", ".bacajuga",
        ".widget", ".widget-area",
        ".share", ".social-share",
        "script", "style", "noscript", "iframe", "aside",
        "[class*='ads']", "[id*='ads']",
        "[class*='ad-']", "[id*='ad-']",
        "[class*='banner']", "[id*='banner']",
        "[class*='promo']", "[id*='promo']",
        "[class*='iklan']", "[id*='iklan']",
        "header", "nav",
    ]:
        for bad in block.select(sel):
            bad.decompose()

    raw_text = block.get_text("\n", strip=True)
    lines = raw_text.splitlines()

    cleaned_lines = []
    skip_next_after_baca_juga = False

    # keyword menu/navbar kalau masih nyangkut sebagai teks
    menu_keywords = [
        "eropa", "liga inggris", "liga italia", "liga spanyol",
        "bundesliga", "liga champions", "liga eropa",
        "dunia", "asia", "amerika latin",
        "indonesia", "tim nasional", "jadwal & skor",
        "basket", "bulu tangkis", "tenis", "otomotif", "voli",
        "video", "galeri", "ragam", "editorial", "sport",
        "lainnya",
    ]

    chrome_keywords = [
        "jadwal pertandingan",
        "klasemen sementara",
        "topskor",
        "jadwal tv",
    ]

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        low = stripped.lower()

        # buang breadcrumb awal
        if stripped == "Bola.net" or stripped == ">":
            continue

        # buang baris metadata tanggal/waktu:
        # "Diperbarui: ...", "Diterbitkan: ...", dll
        meta_prefixes = (
            "diperbarui:",
            "diperbaharui:",
            "diterbitkan:",
            "updated:",
            "published:",
        )
        if any(low.startswith(p) for p in meta_prefixes):
            continue

        # buang page marker "1 dari 3 halaman"
        if re.match(r"^\d+\s+dari\s+\d+\s+halaman$", low):
            continue

        # buang navbar/menu ALL CAPS
        if stripped.isupper() and low in menu_keywords:
            continue
        if low in menu_keywords:
            continue

        # buang baris yang jelas chrome (bukan isi berita)
        if any(kw in low for kw in chrome_keywords):
            continue

        # buang "Baca Juga"/"Baca Ini Juga" + 1 baris setelahnya
        if "baca juga" in low or "baca ini juga" in low:
            skip_next_after_baca_juga = True
            continue

        if skip_next_after_baca_juga:
            skip_next_after_baca_juga = False
            continue

        cleaned_lines.append(stripped)

    text = "\n".join(cleaned_lines)
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

    # fallback: kalau selector ga dapet apa-apa, pakai <body>
    if not blocks and soup.body:
        blocks = [soup.body]

    uniq = []
    seen = set()
    for b in blocks:
        if id(b) not in seen:
            uniq.append(b)
            seen.add(id(b))
    return uniq


def try_follow_pagination(url, soup):
    """
    Cari halaman lanjutan (?page=2,3,all) kalau ada.
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
    r = requests.get(url, headers=HEADERS, timeout=25)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")


def scrape_article(url):
    """
    Ambil title, content (multi-page), images, published_at
    untuk bola.net, lalu filter hanya sepak bola Indonesia.
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

    # halaman lanjutan (jika ada)
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

    # hapus prefix "Bola.net -" jika ada
    prefix = "bola.net -"
    if content_text.lower().startswith(prefix):
        content_text = content_text[len(prefix):].lstrip()

    # hapus judul jika muncul lebih dari sekali di dalam konten
    if title:
        lines = content_text.split("\n")
        seen_title = False
        new_lines = []
        for ln in lines:
            if ln.strip() == title.strip():
                if seen_title:
                    continue
                seen_title = True
            new_lines.append(ln)
        content_text = "\n".join(new_lines).strip()

    # potong footer global (Klasemen, Baca Artikel Menarik, dsb)
    FOOTER_MARKERS = [
        "klasemen bri super league",
        "klasemen",
        "baca artikel-artikel menarik lainnya",
        "latest update",
        "berita terkait",
        "berita lainnya",
        "jangan lewatkan!",
    ]
    lower_content = content_text.lower()
    cut_idx = len(content_text)
    for marker in FOOTER_MARKERS:
        pattern = "\n" + marker  # cari marker di awal baris
        idx = lower_content.find(pattern)
        if idx != -1 and idx < cut_idx:
            cut_idx = idx
    if cut_idx != len(content_text):
        content_text = content_text[:cut_idx].rstrip()

    # batasi panjang maksimum, misalnya 5000 karakter
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

    # threshold minimum
    if len(content_text) < 400:
        return None, "content too short"

    # filter bola Indonesia (berbasis konten)
    if not is_indonesia_football(title, content_text):
        return None, "not indonesia football"

    images = extract_images(soup, url)

    # published_at
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
    print(f"Total URL artikel bola Indonesia (kandidat) dari sitemap: {len(urls)}")

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

    with open("bolanet_bola_indonesia.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(results)} items to bolanet_bola_indonesia.json")


if __name__ == "__main__":
    main()