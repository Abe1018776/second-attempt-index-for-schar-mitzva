# ספר שכר מצוה — Source-Level Index Project Guide
# Complete Implementation Plan for Claude Code

---

## 1. Project Overview

**Goal:** Create a granular, source-level index of the sefer "שכר מצוה" — a compilation of ~600 Torah sources addressing why there IS שכר מצוה בהאי עלמא (reward for mitzvos in this world), despite the Gemara's principle "שכר מצוה בהאי עלמא ליכא."

**Two deliverables:**

1. **Path 1 — Comprehensive Source-Level Index:** A 4-column Hebrew table (matching the דוגמא sample) with EVERY source: sequential number, one-line summary, reasoning (if given), and citation.

2. **Path 2 — Thematic "WHY" Classification:** A filtered/classified index of ONLY sources that explicitly explain WHY שכר מצוה בהאי עלמא ליכא doesn't apply, grouped by theological reasoning category.

---

## 2. Input Files

All files are in `/mnt/user-data/uploads/`:

| File | Description | Role |
|------|-------------|------|
| `ocr-f1a2fe79-9ec1-42ec-b6c3-783c07caaef0.docx` | **PRIMARY INPUT.** Tashma OCR. 354 paragraphs (each ≈ one printed page). Contains HTML markup (`<b>`, `<center>`, `<h1>`, `<footer>`) that encodes structure. Has `<footer>N</footer>` tags with original book page numbers. Better OCR accuracy than alternatives. | Parse this file for all data extraction. |
| `schar_mitzvah_actual_book_content__2_.docx` | **SECONDARY REFERENCE.** Sofer AI OCR with Heading 2 styles applied. 1,818 paragraphs. Has proper heading styles marking subchapters. Same OCR as Sofer AI but with manual styling. Suffers from line-breaking: single sources split across 5-10 tiny paragraphs. | Cross-reference for structure validation. Use to verify chapter/subchapter boundaries. |
| `ספר_שכר_מצוהpdf.docx` | Sofer AI OCR (raw). 2,655 paragraphs. Contains both the index section AND content section. Same line-breaking issue. First half = index (subchapter titles only), second half = full content with sources. | Tertiary reference only. |
| `__ספר_שכר_מצוה_.pdf` | Original PDF scan of the physical book. | Visual reference for resolving OCR ambiguities. |
| `original_schar_mitzvah_index.docx` | Original index from the PDF (subchapter level only). Text embedded in XML, not accessible via python-docx paragraphs — must extract via zipfile/lxml if needed. | Reference for validating chapter/subchapter counts. |
| `___ספר_שכר_מצוה_מפתח_דוגמא_.docx` | **OUTPUT TEMPLATE.** A 10-row example of the desired 4-column index format. | Template for output formatting. |

### Why Tashma OCR is Primary

| Feature | Tashma OCR | Sofer AI / Content File |
|---------|-----------|------------------------|
| OCR accuracy | Higher — reads "דשכר" correctly, "בחו״ל" correctly | Lower — misreads as "דקבל", "כחז״ל" |
| Source integrity | Sources stay together within page-sized paragraphs | Sources shattered across 5-10 tiny line-width paragraphs |
| Structural markup | `<b>` marks subchapter headers, `<center>` marks section headers | Has Heading 2 styles but inconsistent |
| Page mapping | `<footer>N</footer>` gives original book page numbers | `— Page N —` gives PDF page numbers (offset from book pages) |
| Parsing difficulty | Strip HTML tags, use markup as structural signals | Complex heuristics needed to rejoin broken lines |

---

## 3. Book Structure (5 Hierarchical Levels)

```
Level 1: פרק (Chapter)          — 6 chapters: פרק ראשון through פרק ששי
Level 2: Chapter Theme           — e.g., "שכר על כל מצוה", "סוגי מצוות"
Level 3: Mini-Section            — e.g., "תורה", "זכות אבות", "רצון והשתוקקות"
Level 4: Subchapter              — Numbered items: א., ב., ג. ... up to ~קמה.
Level 5: Source                  — Individual source paragraphs within a subchapter
```

### Chapter Map

| Ch# | Chapter | Theme | Tashma Index Para | Tashma Content Start | Book Pages |
|-----|---------|-------|-------------------|---------------------|------------|
| 1 | פרק ראשון | שכר על כל מצוה | P29 | P71 (פתיחה), P74 (sources) | 22-26 |
| 2 | פרק שני | סוגי מצוות | P31-33 | P82 | 27-31 |
| 3 | פרק שלישי | מצוות והנהגות מיוחדות | P35-43 | P91 | 32-54 |
| 4 | פרק רביעי | אנשים, זמנים ומקומות מסויימים | P45-49 | P150 | 55-62 |
| 5 | פרק חמישי | ענינים מיוחדים | P49-61 | P180 | 63-88 |
| 6 | פרק ששי | אופנים בקיום המצוה | P63-69 | P245 | 88-100+ |

**Content ends around P274** (book page ~100). After that: הערות מחכימות (P276+), מצוה גוררת מצוה appendix (P300+), book listings (P350+).

### Mini-Sections Within Each Chapter

**פרק ראשון:** "סיבות שכל מצוה מביא אתו שכר", "על פרטים שבכל מצוה"

**פרק שני:** No mini-sections (all subchapters are direct types of mitzvos)

**פרק שלישי:**
- "מ״ע ול״ת מיוחדות" (specific positive/negative commandments)
- "תורה" (Torah study)
- "קר״ש תפלה וברכות" (Shema, prayer, blessings)
- "שבת, מועדים וזמנים" (Shabbos, holidays)
- "אהבה ויראה" (love and fear of God)
- "אמונה" (faith)
- "צדקה וגמילות חסדים" (charity and kindness)
- "חינוך" (education)

**פרק רביעי:**
- "אנשים מסויימים" (specific people)
- "זמנים מסויימים" (specific times)
- "מקום מסויים" (specific places — i.e., ארץ ישראל)

**פרק חמישי:**
- "זכות אבות", "ישראל", "יסורים", "כבוד שמים", "מזכה הרבים"
- "מחשבה ורצון", "משא ומתן" (or "מתנת שכר"), "נסיון", "עניו"
- "עבירה", "עבודה", "שלום", "תשובה", "שונות"

**פרק ששי:**
- "רצון והשתוקקות", "מקבל", "ממציא עצמו", "טירחא"
- "הכנה", "לומד", "שמחה", "זריזות", "הידור וכבוד"
- "מסי״נ", "כולל", "צער והעדר תענוג", "עזר מה'"
- "תוספות ברכה", "שונות"

---

## 4. Tashma OCR Structure and Parsing

### Document Layout

The Tashma OCR file has **354 paragraphs total** (197 non-empty). The structure is:

- **P0-P27:** Front matter (title pages, הסכמות/approbations, Gemara source)
- **P29-P69:** **INDEX section** — the book's table of contents listing subchapter titles by chapter (NO source text here)
- **P71-P274:** **CONTENT section** — the actual book with full source texts. Each non-empty paragraph ≈ one printed page
- **P276-P298:** הערות מחכימות (scholarly notes from rabbis) — **EXCLUDE**
- **P300-P348:** מצוה גוררת מצוה appendix and additional content — **EXCLUDE**
- **P350-P354:** Book listings — **EXCLUDE**

### HTML Markup Patterns

The Tashma OCR preserves the original typesetting via HTML tags. Here's what each tag signals:

| HTML Pattern | What It Means | Example |
|-------------|---------------|---------|
| `<center><b>פרק ...</b></center>` | Chapter header (Level 1) | `<center><b>פרק ראשון</b>` |
| `<center><b>Theme</b></center>` | Chapter theme (Level 2) | `<center><b>שכר על כל מצוה</b></center>` |
| `<center><b>Section</b></center>` or standalone `<b>Section</b>` | Mini-section header (Level 3) | `<b>תורה</b>`, `<center><b>אהבה ויראה</b></center>` |
| `<b>א. Title text</b>` | Subchapter header (Level 4) | `<b>א. על כל מצוה</b>` |
| `<b>מקור המצוה:</b>` | Source text marker (Level 5) | `<b>מקור המצוה:</b> דהנה אף...` |
| `(ספר name, location)` | Citation at end of source | `(מטה יששכר דרוש ט״ו)` |
| `<footer>N</footer>` | Original book page number | `<footer>32</footer>` |
| `<h1>`, `<h2>` | Major headings (chapters, sections) | `<h1>פרק שני</h1>` |

### Page Number Mapping

The `<footer>N</footer>` tags contain the **original printed book page numbers**. Coverage:

- **77% of content pages have explicit footer numbers** (61 out of ~79 pages)
- Pages 22-100 are the main content range
- Missing pages (24, 25, 29, 31, 36, etc.) can be interpolated since content flows sequentially
- Some footers appear as just the number (e.g., `<footer>33</footer>` at P101 is a standalone page number, not content)

**Mapping strategy:** Walk through paragraphs sequentially; when you see a `<footer>N</footer>`, assign that page number. For paragraphs between footers, interpolate. Each non-empty content paragraph typically corresponds to one printed page.

### Paragraph Structure Within Content

Each content paragraph in Tashma contains **one full page** of the original book. Within a single paragraph, you'll find:

```
[Optional: end of previous source from prior page]

<b>כד. כדי שיוכל לקיים עוד מצות</b>

<b>מקור המצוה:</b> ונראה דשכר מצוה
בהאי עלמא ליכא, והשכר הבא לו לאדם
ע"י איזה מצוה שעשה למשל כשהשי"ת
נותן לאדם ממון עבור איזה מצוה
שעשה אין זה עיקר השכר וכו' רק
שנתן השי"ת הממון הזה כדי שיעשה
עוד מצוה. (נועם אלימלך לך ).

<b>כה. כדי שיהיה במה לעורר לב
הקטנים לשמירת התורה</b>

<b>מקור המצוה:</b> וע"כ נותן השי"ת גם
שכר בעוה"ז להאיש ההולך בדרכי ה...
```

Key observations:
- Multiple subchapters and sources can appear within a single paragraph
- Sources that span page boundaries get split across paragraphs
- Line breaks within a paragraph are cosmetic (OCR line wrapping), not semantic
- The bold markup reliably identifies structural elements

---

## 5. Parsing Algorithm

### Phase 1A: Extract and Clean

```python
# Step 1: Read all Tashma paragraphs
# Step 2: Filter to content section only (P71 through ~P274)
# Step 3: For each paragraph, extract page number from <footer> if present
# Step 4: Concatenate ALL content paragraphs into one giant string
#         (preserving paragraph boundaries with a special delimiter like ¶)
# Step 5: Parse the concatenated text using HTML markup as structural signals
```

### Phase 1B: Structural Parsing

Process the concatenated content text to identify each element:

```
CHAPTER HEADER detection:
  - Pattern: text contains "פרק (ראשון|שני|שלישי|רביעי|חמישי|ששי)"
  - Usually wrapped in <center><b>...</b></center> or <h1>

CHAPTER THEME detection:
  - Appears right after chapter header
  - Wrapped in <center><b>...</b></center>
  - Examples: "שכר על כל מצוה", "סוגי מצוות", "מצוות והנהגות מיוחדות"

MINI-SECTION detection:
  - Short text (< 40 chars after stripping HTML)
  - Often wrapped in <center><b>...</b></center> or standalone <b>...</b>
  - NOT numbered (no א./ב. prefix)
  - NOT a citation (no parenthetical)
  - NOT "מקור המצוה"
  - Matches known mini-section names (see Section 3 above)

SUBCHAPTER detection:
  - Pattern: <b>[א-ת]{1,3}. Title text</b>
  - Regex: <b>([א-ת]{1,3})\.\s*(.+?)</b>
  - The bold wrapper is the key signal

SOURCE detection:
  - Text following <b>מקור המצוה:</b> marker, OR
  - Text between one subchapter header and the next
  - Ends with a parenthetical citation: (ספר name, location)
  - Citation regex: \(([^)]+)\)\s*\.?\s*$

PAGE FOOTER detection:
  - Pattern: <footer>(\d+)</footer>
  - Some footers contain just the number with no other content on that line
```

### Phase 1C: Source Splitting

Within a subchapter, there may be **multiple sources** (multiple citations from different seforim). Split on:

1. **Each `(citation)` followed by new text** = new source
2. **Each `<b>מקור המצוה:</b>`** = definitely a new source
3. Some sources DON'T have the "מקור המצוה:" prefix — they just start with the text directly. In that case, split on citation endings.

**Multi-paragraph sources:** When a source spans a page boundary, the text gets split across Tashma paragraphs. Join them: if a paragraph ends mid-sentence (no citation) and the next paragraph continues the thought, concatenate.

### Output Schema

```json
[
  {
    "id": 1,
    "chapter": "פרק ראשון",
    "chapter_num": 1,
    "chapter_theme": "שכר על כל מצוה",
    "mini_section": null,
    "subchapter_num": "א",
    "subchapter_title": "על כל מצוה",
    "source_index_in_subchapter": 1,
    "source_text": "שבאמת יש לכל המצות שכר בעוה״ז ובעוה״ב...",
    "citation": "מטה יששכר דרוש ט״ו",
    "book_page": 22,
    "has_makor_prefix": true,
    "tashma_paragraph": 74
  }
]
```

Save as `/home/claude/sources.json`.

### Validation Checks

After parsing, verify:
- All 6 chapters are represented
- Total sources is approximately 500-650
- Every source has a citation (flag those without)
- Subchapter numbering is sequential within each chapter (numbering resets per chapter)
- No OCR artifacts leaked through (page headers like "כג שכר מצוה פרק ראשון")
- Print first 3 and last 3 sources per chapter for spot-checking

Also generate `/home/claude/parsing_report.txt` with:
- Sources per chapter
- Sources per mini-section
- Sources without citations
- Subchapter count per chapter
- Any anomalies found

---

## 6. AI Analysis (Phase 2)

### Setup
```bash
pip install anthropic --break-system-packages
```

Use Claude Sonnet (`claude-sonnet-4-20250514`) via the Anthropic API at `https://api.anthropic.com/v1/messages`. No API key needed — it's handled by the environment.

### System Prompt

```
You are analyzing sources from the Hebrew sefer "שכר מצוה" which collects Torah sources about reward for mitzvos in this world (שכר מצוה בהאי עלמא).

The Gemara states "שכר מצוה בהאי עלמא ליכא" — there is no reward for mitzvos in this world. This book collects hundreds of sources from Chassidic and other seforim that discuss cases where there IS such reward, and/or explain why the general rule doesn't apply.

For each source, provide:

1. **תמצית_הענין**: A concise one-line Hebrew summary (10-20 words) of what the source says — which case/situation gets reward in this world.

2. **הטעם**: If the source gives an explicit REASON or EXPLANATION for why שכר מצוה בהאי עלמא ליכא doesn't apply here, summarize that reasoning in Hebrew (15-30 words). If the source only STATES a case without explaining WHY the rule doesn't apply, write "לא מפורש טעם".

3. **has_why_explanation**: true if the source explicitly addresses WHY שכר מצוה בהאי עלמא ליכא doesn't apply in this case; false if it just states that there IS reward without explaining the mechanism.

4. **reasoning_category**: If has_why_explanation is true, classify into ONE of:
   - "זכות_אבות" — Merit of forefathers, not personal merit
   - "לא_שכר_עצמי" — Not reward for the mitzvah itself but for something else (effort, preparation, side-effects)
   - "חסד_לא_שכר" — Divine kindness/grace, not earned reward
   - "מזכה_רבים" — One who merits the public receives differently
   - "טבע_המצוה" — Natural consequence of the mitzvah, not "reward"
   - "קידוש_השם" — To prevent desecration / for public honor of Heaven
   - "מצוה_מיוחדת" — This particular mitzvah has special properties
   - "בן_לא_עבד" — Service from love (as child, not servant) earns differently
   - "אמונה" — Related to faith which has its own reward mechanism
   - "קיום_העולם" — Reward for sustaining the world, not for the mitzvah per se
   - "תנאי_מיוחד" — A special condition or circumstance changes the rule
   - "שכר_חלקי" — The reward is partial/physical, not the full spiritual reward
   - "פעולה_לא_מצוה" — Reward for the action/effort, not the mitzvah obligation
   - "other" — Doesn't fit above (specify briefly)
   If has_why_explanation is false, use "none".

Respond ONLY with a valid JSON array. Each element:
{
  "id": <number>,
  "תמצית_הענין": "...",
  "הטעם": "...",
  "has_why_explanation": true/false,
  "reasoning_category": "..."
}
```

### User Prompt Format (per batch of 10-15 sources)

```
Analyze these sources from ספר שכר מצוה:

---
[Source ID: 1]
Chapter: פרק ראשון — שכר על כל מצוה
Section: (none)
Subchapter: א. על כל מצוה
Citation: מטה יששכר דרוש ט״ו
Text: שבאמת יש לכל המצות שכר בעוה״ז ובעוה״ב באשר שהקב״ה הוא חי וקים ונצחי ולכך גם השכר הוא נצחי לעד בעוה״ז ובעוה״ב.
---
[Source ID: 2]
...

Respond with JSON array only.
```

### Batch Processing

- Batch 10-15 sources per API call
- Total: ~40-60 API calls
- Max tokens per call: 4000
- Save progress incrementally — write each batch result to a temp file
- If API returns malformed JSON, retry that batch with smaller size
- If a source text is too garbled to understand, mark as `"תמצית_הענין": "טקסט לא ברור"`

Save merged results to `/home/claude/analyzed_sources.json`.

---

## 7. Output Generation (Phase 3)

### Setup
```bash
npm install -g docx
```

Read the docx skill at `/mnt/skills/public/docx/SKILL.md` for detailed instructions on creating Word documents with tables.

### Output 1: Full Source-Level Index (Path 1)

Create `schar_mitzvah_full_index.docx` — an RTL Word document with a 4-column table.

**Table columns:**

| Column | Hebrew Header | Width (DXA) | Content |
|--------|--------------|-------------|---------|
| 1 (rightmost) | אופן | 700 | Sequential number: א., ב., ג. etc. |
| 2 | תמצית הענין | 3400 | AI-generated one-line summary |
| 3 | הטעם | 3400 | AI-generated reasoning (or "לא מפורש טעם") |
| 4 (leftmost) | מקור | 1860 | Citation extracted from source |

**Formatting:**
- RTL document direction (bidi: true on all paragraphs and table cells)
- Hebrew font: David Libre (or David), 11pt body, 12pt headers
- Table headers: bold, light blue shading (#D5E8F0)
- Chapter header rows: merged across all 4 columns, bold, larger font, medium blue shading
- Mini-section sub-header rows: merged across all 4 columns, bold, light gray shading
- Numbering: Use the ORIGINAL subchapter numbers from the book (א., ב., ג.)
- Page size: A4 landscape for readability (or 170x240mm portrait to match book format)

**Organization:** Follow the book's order exactly — Chapter → Mini-Section → Subchapter → Sources within subchapter.

### Output 2: Thematic WHY Analysis (Path 2)

Create `schar_mitzvah_why_analysis.docx` — containing ONLY sources where `has_why_explanation == true`.

**Summary table at top:**

| קטגוריה | כמות | תיאור |
|---------|------|-------|
| בזכות האבות | N | שכר בזכות האבות, לא שכר עצמי |
| אינו שכר על המצוה עצמה | N | השכר הוא על דבר אחר |
| ... | ... | ... |

**Main table — grouped by reasoning category:**

| Column | Header | Content |
|--------|--------|---------|
| 1 | # | Sequential number within category |
| 2 | תמצית הענין | Summary |
| 3 | הטעם | The explanation |
| 4 | מקור | Citation |
| 5 | מיקום בספר | Chapter + subchapter reference |

**Category Hebrew display names:**

| Code | Display Name |
|------|-------------|
| זכות_אבות | בזכות האבות |
| לא_שכר_עצמי | אינו שכר על המצוה עצמה |
| חסד_לא_שכר | מצד החסד ולא שכר |
| מזכה_רבים | מזכה את הרבים |
| טבע_המצוה | טבע המצוה להביא טוב |
| קידוש_השם | משום כבוד שמים |
| מצוה_מיוחדת | מצוה מיוחדת בסגולתה |
| בן_לא_עבד | עובד מאהבה כבן |
| אמונה | מצד האמונה |
| קיום_העולם | מצד קיום העולם |
| תנאי_מיוחד | תנאי או נסיבה מיוחדת |
| שכר_חלקי | שכר גשמי/חלקי בלבד |
| פעולה_לא_מצוה | שכר על הפעולה ולא על המצוה |

---

## 8. Content Boundaries — What to Include and Exclude

### INCLUDE in the index:
- **P71 (פתיחה):** The introduction paragraph — treat as context, not as an indexed source
- **P74 through ~P274:** All content from פרק ראשון through the end of פרק ששי שונות
- **תוספות ברכה section** (within פרק ששי, around book pages 96-100): This IS main content

### EXCLUDE from the index:
- **P0-P27:** Front matter, title pages, הסכמות
- **P29-P69:** Index/table of contents section (lists subchapter titles only, no source text)
- **P276+:** הערות מחכימות (scholarly notes from rabbis)
- **P300+:** מצוה גוררת מצוה appendix
- **P350+:** Book listings and back matter
- **Standalone footer paragraphs:** Paragraphs containing ONLY `<footer>N</footer>` and nothing else (e.g., P101, P113, P159, P173, P200, etc.) — these are page-number-only paragraphs

### How to detect content end:
The last content source should be around book page 100 (P268 has `<footer>100</footer>`). After P274, the next non-empty paragraph (P276) starts with "בס״ד הערות מחכימות" — that's the boundary.

---

## 9. Known Issues and Edge Cases

### A. Source Text Spanning Page Boundaries
When a source is longer than one page, it gets split across Tashma paragraphs. For example, a source starting on page 22 might end on page 23. The first paragraph won't end with a citation, and the next paragraph will start mid-sentence.

**Solution:** After splitting content by paragraph, check if each paragraph's content section ends without a citation. If so, prepend it to the next paragraph's content before parsing sources.

### B. Pages with Many Short Sources
Some pages (especially in פרק שלישי for מזוזה-related sources) have 5-8 very short sources on a single page. Each gets its own mini-paragraph within the Tashma paragraph (P93-P100 region). These parse cleanly since each has its own `<b>` header and citation.

### C. Sources Without "מקור המצוה:" Prefix
Not all sources begin with "מקור המצוה:". Many (especially in later chapters) just start directly with the text. The subchapter `<b>` header is the reliable delimiter — everything between one `<b>X. Title</b>` and the next is that subchapter's content, which may contain one or more sources.

### D. Multiple Sources Per Subchapter
A subchapter like "א. על כל מצוה" may have 5+ sources from different seforim. Each source ends with a `(citation)`. Split on these citation boundaries.

### E. The Index Section (P29-P69) vs Content Section (P71+)
The Tashma file contains BOTH the book's table of contents (P29-P69) AND the full content (P71+). The index section lists subchapter titles but has NO source text. **Only parse from P71 onward.**

The index section is recognizable because it has numbered items WITHOUT "מקור המצוה:" text.

### F. OCR Errors
Despite being better than Sofer AI, Tashma still has some OCR errors:
- "קייגים" should be "סייגים" (in P86)
- Some words may have incorrect vowel marks or letter substitutions
- HTML tags occasionally break mid-word

These don't affect parsing but may affect AI analysis quality. The AI prompt should handle gracefully.

### G. Paragraph P71 (פתיחה)
This is an introductory paragraph discussing the Gemara in שבת קכז and the general principle. It's context for the book, not an indexed source. Skip it or treat it as a preface.

### H. Footer-Only Paragraphs
Some paragraphs contain ONLY a `<footer>N</footer>` tag with no content (e.g., P101, P113, P159, P173, P200, etc.). These are page-number anchors — use them for page mapping but skip them as content.

---

## 10. Implementation Steps

### Step 0: Setup
```bash
pip install python-docx lxml anthropic --break-system-packages
npm install -g docx
```

Read `/mnt/skills/public/docx/SKILL.md` before generating Word documents.

### Step 1: Parse Tashma OCR → Structured JSON
Create `/home/claude/parse_tashma.py`:

1. Read `ocr-f1a2fe79-9ec1-42ec-b6c3-783c07caaef0.docx` with python-docx
2. Extract all non-empty paragraphs from P71 through P274
3. For each paragraph, extract `<footer>N</footer>` page number
4. Strip HTML tags while using them as structural signals:
   - `<b>X. Title</b>` → subchapter header
   - `<b>מקור המצוה:</b>` → source marker
   - `<center><b>Section</b></center>` → chapter/section header
5. Handle page-boundary sources (join paragraphs where text continues)
6. Split sources within subchapters on citation boundaries
7. Output `/home/claude/sources.json` + `/home/claude/parsing_report.txt`

### Step 2: Validate Parsing
- Print summary statistics
- Spot-check 5 sources from each chapter
- Verify against secondary reference file (content file with Heading 2 styles)
- Check total source count is in the 500-650 range

### Step 3: AI Analysis
Create `/home/claude/analyze_sources.py`:

1. Read `sources.json`
2. Batch into groups of 10-15 sources
3. Call Claude Sonnet API for each batch
4. Parse JSON responses
5. Merge results into `/home/claude/analyzed_sources.json`
6. Handle errors with retries
7. Save progress after each batch (append to temp file)

### Step 4: Generate Output Documents
Create `/home/claude/generate_outputs.js`:

1. Read `analyzed_sources.json`
2. Generate Path 1 document (full index table)
3. Generate Path 2 document (thematic WHY analysis)
4. Copy to `/mnt/user-data/outputs/`

### Step 5: Final Quality Check
- Spot-check 10-15 entries in the generated documents
- Verify RTL rendering
- Verify Hebrew display
- Check category distribution makes sense
- Ensure all chapters are represented proportionally

---

## 11. Cross-Reference Validation Using Secondary File

To validate the Tashma parsing, cross-check against `schar_mitzvah_actual_book_content__2_.docx`:

```python
from docx import Document
import re

# Count Heading 2 paragraphs that match subchapter pattern
doc = Document('schar_mitzvah_actual_book_content__2_.docx')
subchapters = [p.text.strip() for p in doc.paragraphs 
               if p.style and p.style.name == 'Heading 2'
               and re.match(r'^[א-ת]{1,3}\.', p.text.strip())]
print(f"Secondary file subchapter count: {len(subchapters)}")
# Compare with Tashma-parsed subchapter count
```

This gives an independent count of subchapters to validate against.

---

## 12. Sample Expected Output

### Path 1 (Full Index) — First few rows:

| אופן | תמצית הענין | הטעם | מקור |
|------|------------|------|------|
| א. | על כל מצוה יש שכר בעוה"ז ובעוה"ב כי הקב"ה נצחי וכן שכרו | השכר נצחי כנצחיות הקב"ה ולכך משתרע גם בעוה"ז | מטה יששכר דרוש ט"ו |
| א. | הקב"ה נותן קצת שכר בעוה"ז כמו שמוסיפין מחול אל הקודש | כשם שמוסיפין מחול אל הקודש כך עוה"ז שהוא חול מקבל מן הקודש | בנין דוד וישלח |
| א. | השי"ת משלם גמול על כל עבודה פרטית בעוה"ז | שכר הפעולות הפרטיות בעוה"ז אבל שכר כלל העבודה רק בעוה"ב | קול אליהו רות |

### Path 2 (WHY Analysis) — Example category:

**קטגוריה: שכר חלקי — שכר גשמי/חלקי בלבד**

| # | תמצית הענין | הטעם | מקור | מיקום |
|---|------------|------|------|------|
| 1 | שכר מצוה בשני בחינות גשמי ורוחני | השכר הגשמי ניתן בעוה"ז והרוחני בעוה"ב | רחובות הנהר עקב | פ"א, א. |
| 2 | אוכל פירותיהן בעוה"ז והקרן קיימת לעוה"ב | הפירות (שכר חלקי) בעוה"ז אבל הקרן (עיקר השכר) לעוה"ב | לתרופה / רביד הזהב | פ"א, א. |

---

## 13. File Outputs

All final outputs go to `/mnt/user-data/outputs/`:

1. `sources.json` — Parsed structured data (for reference/debugging)
2. `parsing_report.txt` — Statistics and validation report
3. `analyzed_sources.json` — AI analysis results
4. `schar_mitzvah_full_index.docx` — Complete source-level 4-column index (Path 1)
5. `schar_mitzvah_why_analysis.docx` — Thematic WHY analysis grouped by category (Path 2)

---

## 14. Estimated Timeline

| Phase | Task | Time |
|-------|------|------|
| 1 | Parse Tashma OCR → JSON | ~15-30 min |
| 1.5 | Validate + fix edge cases | ~15 min |
| 2 | AI Analysis (~50 API calls) | ~15-20 min |
| 3 | Generate Word documents | ~15-30 min |
| 4 | Quality check + fixes | ~15 min |
| **Total** | | **~1-2 hours** |
