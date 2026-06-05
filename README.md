# 🎛️ Bro. William Branham — Sermon Presentation Modules

Ready-made modules for importing **1,206 sermons** by Brother William Marrion Branham directly into church presentation software. Download, import, and display Brother Branham's messages on screen during service.

---

*"But in the days of the voice of the seventh angel, when he shall begin to sound, the mystery of God should be finished, as he hath declared to his servants the prophets." — Revelation 10:7 KJV*

---

## ⬇️ Download

Module files are distributed via **GitHub Releases**:

➜ **[Download from Releases](https://github.com/philipatosam/bro-branham-sermon-presentation-modules/releases)**

| File | Software | Format | Size |
|---|---|---|---|
| `bro-branham-sermons.fsb` | **FreeShow** | json-bible | ~95 MB |
| `bro-branham-sermons-opensong.xml` | **VideoPsalm**, OpenSong, OpenLP | OpenSong XML | ~95 MB — *coming soon* |
| `bro-branham-sermons-zefania.xml` | **SongBeamer**, VerseVIEW, EasySlides | Zefania XML | ~97 MB — *coming soon* |

---

## 📥 Import Instructions

### FreeShow

1. Download `bro-branham-sermons.fsb` from the [Releases](https://github.com/philipatosam/bro-branham-sermon-presentation-modules/releases) page
2. Open FreeShow
3. Click the **Scriptures** drawer in the left panel
4. Click **+** → **Import Bible**
5. Browse to `bro-branham-sermons.fsb` and select it
6. The module appears as **"Bro. William Branham — Messages"**

---

## 🔍 Searching in FreeShow

**Browse panel** — All 1,206 sermons are listed chronologically in the center of the Scriptures drawer. Click any sermon to open it, then click a paragraph to add it to your presentation.

**Bottom text search** — Click the magnifying glass icon at the bottom of the Scriptures drawer to search by words across all 208,274 paragraphs. Type any phrase — *"faith is the substance"*, *"seventh seal"*, *"pillar of fire"* — and it returns every matching paragraph across all sermons.

---

## 📖 How Sermons Are Structured

Each sermon is structured like a Bible book — so presentation software can handle it natively:

| Sermon data | Bible equivalent | Example |
|---|---|---|
| Sermon collection | Bible | *Bro. William Branham — Messages* |
| Each sermon | Book | *47-0412 · Faith Is the Substance* |
| Each sermon | 1 Chapter | Chapter 1 |
| Each paragraph | Verse | ¶44 |

A preacher can navigate to any sermon, jump to a specific paragraph by number, and display one paragraph per slide — the same way Scripture is displayed.

---

## 📦 Repo Structure

```
bro-branham-sermon-presentation-modules/
├── modules/
│   ├── freeshow/
│   │   ├── README.md          # FreeShow-specific import instructions
│   │   └── warnings.txt       # 90 paragraphs flagged as unusually long
│   └── README.md              # All modules overview
├── to_freeshow.py             # Converter script (generate the .fsb yourself)
├── .gitignore
├── LICENSE
└── README.md
```

> **Module files** (`.fsb`, `.xml`) are too large for GitHub. Download them from the [Releases](https://github.com/philipatosam/bro-branham-sermon-presentation-modules/releases) page.

---

## 🔨 Generate the Files Yourself

If you prefer to generate the module files from the source JSON data:

**Requirements:** Python 3.8+, no external dependencies.

**Step 1 — Clone the source JSON library:**
```bash
git clone https://github.com/philipatosam/bro-william-branham-sermon-library.git
```

**Step 2 — Run the converter:**
```bash
python3 to_freeshow.py \
  --input bro-william-branham-sermon-library/output \
  --output modules/freeshow/bro-branham-sermons.fsb
```

| Flag | Default | Description |
|---|---|---|
| `--input` | `../output` | Folder containing individual sermon JSON files |
| `--output` | `../modules/freeshow/bro-branham-sermons.fsb` | Output file path |
| `--limit N` | None | Process only first N sermons (for testing) |
| `--warn-threshold N` | 3000 | Flag paragraphs longer than N characters |

---

## 🙏 Credits

- **[Voice of God Recordings (VGR)](https://www.branham.org)** — original sermon content. VGR states their materials may be freely distributed for the purpose of spreading the Gospel, which is the sole intent of this project.
- **[bro-william-branham-sermon-library](https://github.com/philipatosam/bro-william-branham-sermon-library)** — the source JSON library this project is built on.
- **[branham-player/golden-dataset](https://github.com/branham-player/golden-dataset)** — sermon metadata (titles, dates, locations).

---

## 📜 License

**Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**

Free to use and share for any non-commercial purpose with attribution. Commercial use is not permitted. This project exists solely to promote the Gospel of Jesus Christ.

[![License: CC BY-NC 4.0](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc/4.0/)

---

## 🔗 Related

- [bro-william-branham-sermon-library](https://github.com/philipatosam/bro-william-branham-sermon-library) — source JSON data for developers
- [Voice of God Recordings](https://www.branham.org) — official VGR website
- [branham-player/golden-dataset](https://github.com/branham-player/golden-dataset) — sermon metadata source

---

*"Behold, I will send you Elijah the prophet before the coming of the great and dreadful day of the LORD: And he shall turn the heart of the fathers to the children, and the heart of the children to their fathers, lest I come and smite the earth with a curse." — Malachi 4:5-6 KJV*
