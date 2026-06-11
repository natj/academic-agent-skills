---
name: ads-search
description: Search for scientific papers using NASA ADS. Use when the user asks to find, search for, or look up scientific papers, articles, or references in physics, astrophysics, astronomy, or mathematics.
autoContext: true
---

## When to use

Use this skill when the user asks to find, search for, or look up scientific papers. This is the primary tool for discovering papers — it searches NASA ADS which covers physics, astrophysics, astronomy, math, and related fields.

## Workflow

### Step 1: Search for papers

```bash
python3 /Users/jnattila/.claude/skills/ads-search/ads_search.py --search "query terms"
```

Use ADS query syntax for precise searches:
- Author: `--search "author:Nattila"` or `--search "author:\"Nattila, J.\""`
- Title words: `--search "title:magnetosphere"`
- First author: `--search "author:^Nattila"`
- Year range: `--search "author:Nattila year:2020-2024"`
- Combine: `--search "author:Nattila title:neutron star year:2020-2024"`

Present results as a numbered list showing: bibcode, title, first author, year, journal, and whether arXiv source is available.

### Step 2: Find citing papers

To find all papers that cite a given paper:

```bash
python3 /Users/jnattila/.claude/skills/ads-search/ads_search.py --citations "2024ApJ...971...37N"
```

Returns the same JSON format as `--search`. Use `--max-results` and `--sort` to control output (e.g., `--sort "citation_count desc"` for most-cited first).

### Step 3: Get BibTeX for selected paper(s)

```bash
python3 /Users/jnattila/.claude/skills/ads-search/ads_search.py --bibtex "2024ApJ...123..456N"
```

Multiple bibcodes can be comma-separated. Saves `.bib` file to `refs/` directory.

### Step 4: Get the paper source

Check the JSON output for the `arxiv_id` field:

- **If arXiv ID is available**: Use the arxiv-fetch skill to download LaTeX source:
  ```bash
  python3 /Users/jnattila/.claude/skills/arxiv-fetch/arxiv_fetch.py --id ARXIV_ID --outdir refs/
  ```

- **If no arXiv source**: Download the PDF via ADS:
  ```bash
  python3 /Users/jnattila/.claude/skills/ads-search/ads_search.py --pdf "2024ApJ...123..456N" --outdir refs/
  ```

### API Token

The script requires an ADS API token. It looks for the token in:
1. `ADS_DEV_KEY` environment variable
2. `~/.ads/dev_key` file

If no token is found, instruct the user to get one from https://ui.adsabs.harvard.edu/user/settings/token and set it:
```bash
export ADS_DEV_KEY="your-token-here"
```
