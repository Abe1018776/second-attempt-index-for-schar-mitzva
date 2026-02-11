#!/usr/bin/env python3
"""Create HTML side-by-side viewer: PDF pages vs parsed sources."""

import json, base64, os

with open('/root/schar-mitzvah-project/sources.json') as f:
    sources = json.load(f)

PDF_DIR = "/root/schar-mitzvah-project/pdf-pages"
PAGE_OFFSET = 16

# Group sources by book page
by_page = {}
for s in sources:
    pg = s['book_page']
    if pg not in by_page:
        by_page[pg] = []
    by_page[pg].append(s)

# Build HTML
html_parts = ['''<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
<meta charset="utf-8">
<title>שכר מצוה — Side-by-Side Verification</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'David', 'Noto Sans Hebrew', Arial, sans-serif; background: #1a1a2e; color: #e0e0e0; }
.nav { position: fixed; top: 0; left: 0; right: 0; background: #16213e; padding: 8px 20px; z-index: 100; display: flex; align-items: center; gap: 10px; border-bottom: 2px solid #0f3460; }
.nav button { background: #0f3460; color: #e0e0e0; border: 1px solid #533483; padding: 6px 14px; cursor: pointer; border-radius: 4px; font-size: 14px; }
.nav button:hover { background: #533483; }
.nav select { background: #0f3460; color: #e0e0e0; border: 1px solid #533483; padding: 6px; border-radius: 4px; font-size: 14px; }
.nav .title { font-size: 18px; font-weight: bold; color: #e94560; margin-left: 20px; }
.nav .stats { font-size: 12px; color: #888; margin-left: auto; }
.container { margin-top: 50px; }
.page-section { display: none; padding: 10px; }
.page-section.active { display: flex; gap: 10px; min-height: calc(100vh - 50px); }
.left-panel { flex: 1; max-width: 50%; overflow: auto; }
.left-panel img { width: 100%; border: 1px solid #333; }
.right-panel { flex: 1; max-width: 50%; overflow: auto; padding: 10px; }
.chapter-header { background: #0f3460; padding: 8px 12px; margin: 5px 0; border-radius: 4px; font-size: 16px; font-weight: bold; color: #e94560; }
.mini-section { background: #1a1a4e; padding: 6px 12px; margin: 3px 0; border-radius: 4px; font-size: 14px; color: #a78bfa; border-right: 3px solid #a78bfa; }
.subchapter-header { background: #162447; padding: 6px 12px; margin: 5px 0 2px; border-radius: 4px; font-weight: bold; color: #00d2ff; font-size: 14px; }
.source-card { background: #1e1e3f; border: 1px solid #333; border-radius: 4px; margin: 3px 0; padding: 8px 12px; }
.source-card.supplementary { border-color: #f59e0b; border-style: dashed; }
.source-num { display: inline-block; background: #e94560; color: white; padding: 1px 6px; border-radius: 3px; font-size: 11px; margin-left: 5px; }
.source-text { font-size: 13px; color: #ccc; margin: 4px 0; line-height: 1.6; max-height: 80px; overflow: hidden; cursor: pointer; }
.source-text.expanded { max-height: none; }
.citation { display: inline-block; background: #065f46; color: #6ee7b7; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin-top: 4px; }
.no-cite { background: #7f1d1d; color: #fca5a5; }
.makor-badge { display: inline-block; background: #1e3a5f; color: #93c5fd; padding: 1px 6px; border-radius: 3px; font-size: 10px; }
.supp-badge { display: inline-block; background: #78350f; color: #fbbf24; padding: 1px 6px; border-radius: 3px; font-size: 10px; }
.page-info { text-align: center; padding: 5px; background: #0f3460; border-radius: 4px; margin-bottom: 5px; font-size: 13px; }
.count-bar { display: flex; gap: 10px; padding: 5px 10px; background: #162447; border-radius: 4px; margin-bottom: 5px; font-size: 12px; }
.count-bar span { color: #888; }
.count-bar .num { color: #00d2ff; font-weight: bold; }
</style>
</head>
<body>
<div class="nav">
  <span class="title">ספר שכר מצוה — Verification Viewer</span>
  <button onclick="prevPage()">← הקודם</button>
  <select id="pageSelect" onchange="goToPage(this.value)">
''']

# Add page options
content_pages = sorted(by_page.keys())
# Also add pages that might not have sources
all_book_pages = list(range(22, 105))

for pg in all_book_pages:
    src_count = len(by_page.get(pg, []))
    label = f"עמוד {pg} ({src_count} מקורות)"
    html_parts.append(f'    <option value="{pg}">{label}</option>\n')

html_parts.append('''  </select>
  <button onclick="nextPage()">הבא →</button>
  <span class="stats" id="globalStats"></span>
</div>
<div class="container">
''')

# Generate page sections
for pg in all_book_pages:
    pdf_pg = pg + PAGE_OFFSET
    img_path = f"{PDF_DIR}/page-{pdf_pg:03d}.png"

    page_sources = by_page.get(pg, [])

    html_parts.append(f'<div class="page-section" id="page-{pg}">\n')

    # Left panel: PDF image
    html_parts.append('<div class="left-panel">\n')
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            img_b64 = base64.b64encode(f.read()).decode()
        html_parts.append(f'  <img src="data:image/png;base64,{img_b64}" alt="Page {pg}">\n')
    else:
        html_parts.append(f'  <p style="color:red;">Image not found: page-{pdf_pg:03d}.png</p>\n')
    html_parts.append('</div>\n')

    # Right panel: parsed sources
    html_parts.append('<div class="right-panel">\n')
    html_parts.append(f'  <div class="page-info">עמוד {pg} בספר (PDF עמוד {pdf_pg}) — {len(page_sources)} מקורות</div>\n')

    if page_sources:
        chapters = set(s['chapter_num'] for s in page_sources)
        subs = set(s['subchapter_num'] for s in page_sources)
        supp = sum(1 for s in page_sources if s.get('tashma_paragraph') == 'supplementary')
        html_parts.append(f'  <div class="count-bar">')
        html_parts.append(f'    <span>פרקים: <span class="num">{",".join(str(c) for c in sorted(chapters))}</span></span>')
        html_parts.append(f'    <span>תת-פרקים: <span class="num">{len(subs)}</span></span>')
        html_parts.append(f'    <span>מקורות: <span class="num">{len(page_sources)}</span></span>')
        if supp:
            html_parts.append(f'    <span style="color:#fbbf24;">משלים: {supp}</span>')
        html_parts.append(f'  </div>\n')

    current_ch = None
    current_mini = None
    current_sub = None

    for s in page_sources:
        # Chapter header
        if s['chapter_num'] != current_ch:
            current_ch = s['chapter_num']
            current_mini = None
            html_parts.append(f'  <div class="chapter-header">{s["chapter"]} — {s["chapter_theme"]}</div>\n')

        # Mini-section
        mini = s.get('mini_section') or ''
        if mini and mini != current_mini:
            current_mini = mini
            html_parts.append(f'  <div class="mini-section">{mini}</div>\n')

        # Subchapter header
        sub_key = f"{s['chapter_num']}-{s['subchapter_num']}"
        if sub_key != current_sub:
            current_sub = sub_key
            title = s.get('subchapter_title', '') or ''
            html_parts.append(f'  <div class="subchapter-header">{s["subchapter_num"]}. {title}</div>\n')

        # Source card
        is_supp = s.get('tashma_paragraph') == 'supplementary'
        supp_class = ' supplementary' if is_supp else ''
        html_parts.append(f'  <div class="source-card{supp_class}">\n')
        html_parts.append(f'    <span class="source-num">#{s["id"]}</span>\n')
        if s.get('has_makor_prefix'):
            html_parts.append(f'    <span class="makor-badge">מקור המצוה</span>\n')
        if is_supp:
            html_parts.append(f'    <span class="supp-badge">משלים מקובץ משני</span>\n')

        text = s.get('source_text', '')
        escaped_text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        html_parts.append(f'    <div class="source-text" onclick="this.classList.toggle(\'expanded\')">{escaped_text}</div>\n')

        cite = s.get('citation') or ''
        if cite:
            escaped_cite = cite.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            html_parts.append(f'    <span class="citation">({escaped_cite})</span>\n')
        else:
            html_parts.append(f'    <span class="citation no-cite">אין ציטוט</span>\n')

        html_parts.append(f'  </div>\n')

    if not page_sources:
        html_parts.append('  <p style="text-align:center; color:#888; padding:20px;">אין מקורות מיוחסים לעמוד זה</p>\n')

    html_parts.append('</div>\n')
    html_parts.append('</div>\n')

# JavaScript
html_parts.append(f'''
<script>
const allPages = {json.dumps(all_book_pages)};
let currentIdx = 0;

function showPage(idx) {{
  document.querySelectorAll('.page-section').forEach(el => el.classList.remove('active'));
  const pg = allPages[idx];
  const el = document.getElementById('page-' + pg);
  if (el) el.classList.add('active');
  document.getElementById('pageSelect').value = pg;
  currentIdx = idx;
  document.getElementById('globalStats').textContent = `Page ${{idx+1}} of ${{allPages.length}}`;
}}

function prevPage() {{ if (currentIdx > 0) showPage(currentIdx - 1); }}
function nextPage() {{ if (currentIdx < allPages.length - 1) showPage(currentIdx + 1); }}
function goToPage(pg) {{
  const idx = allPages.indexOf(parseInt(pg));
  if (idx >= 0) showPage(idx);
}}

// Keyboard navigation
document.addEventListener('keydown', e => {{
  if (e.key === 'ArrowLeft') nextPage();
  if (e.key === 'ArrowRight') prevPage();
}});

showPage(0);
</script>
</body>
</html>
''')

output_path = '/root/schar-mitzvah-project/verification_viewer.html'
with open(output_path, 'w') as f:
    f.write(''.join(html_parts))

print(f"Created: {output_path}")
print(f"Size: {os.path.getsize(output_path) / 1024 / 1024:.1f} MB")
print(f"Pages: {len(all_book_pages)}")
print(f"Total sources shown: {len(sources)}")
