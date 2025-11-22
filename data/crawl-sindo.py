import json
import re
import time
import os
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# ===================== KONFIG DASAR =====================

# sitemap index/news Sindonews olahraga
SITEMAP_URL = "https://sports.sindonews.com/sitemap-news.xml"

MAX_ITEMS = 1000  # target artikel yang mau diambil

# File output
OUTPUT_FILE = "sindonews_bola_indonesia.json"

TITLE_SELECTORS = [
    ".detail__title",
    ".read_title",
    "h1",
]

CONTENT_BLOCK_SELECTORS = [
    ".detail-desc",
    "#detail-desc",
    ".detail_desc",
    ".clearfix",
]

IMAGE_SELECTORS = [
    ".detail_img img",
    ".photo__wrap img",
    ".detail-desc img",
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


def is_sindonews_sport_url(url: str) -> bool:
    """Pastikan URL dari kanal olahraga Sindonews (terutama sports.sindonews.com)."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path = parsed.path.lower()

    if "sindonews.com" not in host:
        return False

    # fokus sports.sindonews.com
    if host.startswith("sports.sindonews.com"):
        return True

    # jaga-jaga kalau ada pola lain
    if "/sports/" in path or "/sport/" in path:
        return True

    return False


def is_indonesia_football(title: str, content: str) -> bool:
    """Filter hanya artikel sepak bola Indonesia (berbasis keyword)."""
    text = f"{title or ''}\n{content or ''}".lower()
    return any(kw in text for kw in ID_FOOTBALL_KEYWORDS)


# ===================== URL DISCOVERY (SITEMAP, BISA REKURSIF) =====================

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

        # skip kalau ini sitemap gambar (kalau ada)
        if "images/sitemap" in u:
            continue

        # kalau masih sitemap (berakhir .xml) → rekursif
        if u.lower().endswith(".xml"):
            collect_article_urls_from_sitemap(u, limit, urls, visited)
            if len(urls) >= limit:
                break
            continue

        # kalau sudah URL artikel:
        if not is_sindonews_sport_url(u):
            continue

        parsed = urlparse(u)
        path = parsed.path.lower()

        # artikel Sindonews biasanya pakai /read/ di path
        if "/read/" not in path:
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
    Buang iklan/crossportal, 'Baca Juga', related, share,
    dan elemen pengganggu lain dalam satu blok konten Sindonews.
    """

    # 1. Buang elemen pengganggu via selector
    for sel in [
        ".crossportal", ".ads", ".advertisement",
        ".read-also", ".baca-juga", ".baca_juga", ".bacajuga",
        ".sosmed", ".share", ".tag", ".lihat-juga", ".related",
        ".pagination", ".recommendation",
        ".widget", ".widget-area",
        ".editor", ".author",
        ".breadcumb", ".breadcrumb",
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

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        low = stripped.lower()

        # Kalimat "Baca Juga" → buang baris ini + baris berikutnya (judul link)
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
    Cari halaman lanjutan.
    Di SINDOnews sering pakai /2, /3, dst, atau link angka.
    """
    extra_pages = []

    # cara 1: cari link angka yang mungkin halaman berikut
    for a in soup.select("a"):
        t = a.get_text(strip=True)
        if t.isdigit():
            href = a.get("href")
            if href:
                extra_pages.append(urljoin(url, href))

    # cara 2: brute force /2, /3, /4
    base = url.rstrip("/")
    for i in range(2, 5):
        guess = f"{base}/{i}"
        extra_pages.append(guess)

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
    untuk Sindonews olahraga, lalu filter hanya bola Indonesia.
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

    # halaman lanjutan (/2, /3, dst.)
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
        if added == 0 and u2.endswith("/2"):
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

    # published_at (beberapa kemungkinan meta)
    published_at = None
    ld = soup.find("meta", attrs={"itemprop": "datePublished"})
    if ld and ld.get("content"):
        published_at = ld["content"].strip()
    if not published_at:
        meta = soup.find("meta", property="article:published_time")
        if meta and meta.get("content"):
            published_at = meta["content"].strip()
    if not published_at:
        meta2 = soup.find("meta", attrs={"name": "pubdate"})
        if meta2 and meta2.get("content"):
            published_at = meta2["content"].strip()

    item = {
        "url": url,
        "title": title,
        "published_at": published_at,
        "images": images,
        "content": content_text,
        "content_length": len(content_text),
    }
    return item, None


# ===================== FUNGSI APPEND & BACKUP =====================

def load_existing_articles(filepath):
    """Load artikel yang sudah ada dari file JSON"""
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"\n📂 Data existing ditemukan: {len(data)} artikel")
                return data
        except Exception as e:
            print(f"\n⚠️ Error membaca file existing: {e}")
            return []
    else:
        print(f"\n📂 File {filepath} belum ada, akan dibuat baru")
        return []


def create_backup(filepath):
    """Buat backup file existing sebelum update"""
    if os.path.exists(filepath):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = filepath.replace('.json', f'_backup_{timestamp}.json')
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            with open(backup_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"💾 Backup dibuat: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"⚠️ Gagal membuat backup: {e}")
            return None
    return None


def save_with_append(new_articles, filepath, check_duplicate=True):
    """
    Simpan artikel baru dengan append ke data lama
    
    Args:
        new_articles: List artikel baru hasil crawling
        filepath: Path file JSON output
        check_duplicate: Check duplikasi berdasarkan URL (default True)
    
    Returns:
        Jumlah artikel baru yang ditambahkan
    """
    # Load data lama
    existing_articles = load_existing_articles(filepath)
    
    # Buat backup sebelum update
    if existing_articles:
        create_backup(filepath)
    
    if check_duplicate:
        # Buat set URL yang sudah ada
        existing_urls = {article['url'] for article in existing_articles}
        
        # Filter artikel baru yang belum ada
        unique_new = [
            article for article in new_articles 
            if article['url'] not in existing_urls
        ]
        
        print(f"\n{'='*60}")
        print(f"📊 RINGKASAN PENAMBAHAN DATA")
        print(f"{'='*60}")
        print(f"📋 Artikel lama: {len(existing_articles)}")
        print(f"🆕 Artikel hasil crawl: {len(new_articles)}")
        print(f"✅ Artikel baru (unik): {len(unique_new)}")
        print(f"❌ Duplikat (dilewati): {len(new_articles) - len(unique_new)}")
        print(f"{'='*60}")
        
        # Gabungkan
        all_articles = existing_articles + unique_new
        added_count = len(unique_new)
    else:
        all_articles = existing_articles + new_articles
        added_count = len(new_articles)
    
    # Simpan data gabungan
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Total artikel sekarang: {len(all_articles)}")
    print(f"📁 Disimpan di: {filepath}\n")
    
    return added_count


# ===================== MAIN =====================

def main():
    print("\n" + "="*60)
    print("🚀 MEMULAI CRAWLING SINDONEWS BOLA INDONESIA")
    print("="*60)
    print(f"🎯 Target: {MAX_ITEMS} artikel")
    print(f"📂 Output: {OUTPUT_FILE}")
    print("="*60 + "\n")
    
    # Ambil URL dari sitemap
    urls = get_urls_from_sitemap(SITEMAP_URL, MAX_ITEMS)
    print(f"\n✅ Total URL artikel dari sitemap: {len(urls)}")
    
    if not urls:
        print("❌ Tidak ada URL yang ditemukan. Proses dihentikan.")
        return

    # Crawl artikel
    print(f"\n{'='*60}")
    print("📰 MEMULAI SCRAPING ARTIKEL")
    print("="*60 + "\n")
    
    results = []
    success = 0
    failed = 0
    
    for i, u in enumerate(urls, 1):
        if not u.startswith("http"):
            u = urljoin(SITEMAP_URL, u)

        print(f"[{i}/{len(urls)}] {u[:80]}...")
        item, err = scrape_article(u)
        if err:
            print(f"  ❌ {err}")
            failed += 1
        else:
            results.append(item)
            print(f"  ✅ OK - {item['content_length']} chars")
            success += 1

        time.sleep(0.8)  # Jeda untuk menghindari rate limit

    # Simpan dengan append (tidak hapus data lama)
    print(f"\n{'='*60}")
    print("💾 MENYIMPAN HASIL")
    print("="*60)
    print(f"✅ Berhasil: {success} artikel")
    print(f"❌ Gagal: {failed} artikel")
    
    if results:
        added = save_with_append(results, OUTPUT_FILE, check_duplicate=True)
        
        print(f"\n{'='*60}")
        print("🎉 CRAWLING SELESAI!")
        print("="*60)
        print(f"✨ Artikel baru ditambahkan: {added}")
    else:
        print("\n⚠️ Tidak ada artikel baru yang berhasil di-crawl")


if __name__ == "__main__":
    main()