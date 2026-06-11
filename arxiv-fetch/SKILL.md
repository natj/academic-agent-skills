---
name: arxiv-fetch
description: Fetch scientific article LaTeX source from arXiv and store in refs/. Use when asked to download, fetch, or get a paper from arXiv.
autoContext: false
---

## Usage

Use the Python script to search and fetch arXiv papers. Always use the absolute path to the script.

### When the user provides an arXiv ID or URL

Run the fetch script directly:

```bash
python3 /Users/jnattila/.claude/skills/arxiv-fetch/arxiv_fetch.py --id PAPER_ID --outdir refs/
```

The script outputs JSON to stdout with the paper metadata and list of saved files. Report the results to the user.

### When the user provides a title, author, or description

First search:

```bash
python3 /Users/jnattila/.claude/skills/arxiv-fetch/arxiv_fetch.py --search "search terms"
```

Present the JSON results as a numbered list (ID, title, first author, year, category). Ask the user which paper to fetch, then run the fetch command with the selected ID.

### After fetching

Report which files were saved to `refs/` and offer to read the `.tex` file if the user wants to examine the paper content.
