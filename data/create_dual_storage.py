"""
Script untuk membuat CSV dengan DUAL STORAGE:
- Data ORIGINAL (title, content) untuk DISPLAY
- Data CLEAN (title_clean, content_clean) untuk INDEXING
"""

import pandas as pd

print('='*80)
print('MEMBUAT CSV DENGAN DUAL STORAGE')
print('='*80)

# Load data original
df_original = pd.read_csv('merge-all.csv')
print(f'✅ Loaded merge-all.csv: {len(df_original)} rows')

# Load data clean
df_clean = pd.read_csv('merge-all-clean.csv')
print(f'✅ Loaded merge-all-clean.csv: {len(df_clean)} rows')

# Buat dataframe baru dengan dual storage
df_dual = pd.DataFrame()

# Kolom ID dan metadata
df_dual['doc_id'] = df_original['id']
df_dual['source'] = df_original['source']
df_dual['url'] = df_original['url']
df_dual['main_image'] = df_original['main_image']

# ORIGINAL data (untuk DISPLAY)
df_dual['title'] = df_original['title']
df_dual['content'] = df_original['content']

# CLEAN data (untuk INDEXING)
df_dual['title_clean'] = df_clean['title']
df_dual['content_clean'] = df_clean['content']

# Metadata tambahan
if 'published_at' in df_original.columns:
    df_dual['published_at'] = df_original['published_at']

# Simpan ke file baru
output_file = 'merge-all-dual-storage.csv'
df_dual.to_csv(output_file, index=False)

print(f'\n✅ Saved to: {output_file}')
print(f'Total rows: {len(df_dual)}')

print('\n' + '='*80)
print('STRUKTUR FILE BARU:')
print('='*80)
print(f'Kolom: {list(df_dual.columns)}')

print('\n' + '='*80)
print('SAMPLE DATA (Row 0):')
print('='*80)
row = df_dual.iloc[0]
print(f'\ntitle (ORIGINAL):')
print(f'  {row["title"][:100]}...')
print(f'\ntitle_clean (INDEXING):')
print(f'  {row["title_clean"][:100]}...')
print(f'\ncontent (ORIGINAL):')
print(f'  {row["content"][:150]}...')
print(f'\ncontent_clean (INDEXING):')
print(f'  {row["content_clean"][:150]}...')

print('\n' + '='*80)
print('✅ DUAL STORAGE BERHASIL DIBUAT!')
print('='*80)
print('Gunakan kolom ini:')
print('  - title, content → untuk DISPLAY di frontend')
print('  - title_clean, content_clean → untuk INDEXING (TF-IDF & BM25)')
