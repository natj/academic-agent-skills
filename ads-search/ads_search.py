#!/usr/bin/env python3
"""
ads_search.py - Search NASA ADS for scientific papers.

Usage:
    python3 ads_search.py --search "author:Nattila neutron star"
    python3 ads_search.py --bibtex "2024ApJ...123..456N" --outdir refs/
    python3 ads_search.py --pdf "2024ApJ...123..456N" --outdir refs/

Output: JSON to stdout, status/errors to stderr.
Dependencies: Python 3.7+ stdlib only.
Requires: ADS API token in ADS_DEV_KEY env var or ~/.ads/dev_key file.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

# --- Constants ---

ADS_API_URL = "https://api.adsabs.harvard.edu/v1"
ADS_SEARCH_FIELDS = (
    "bibcode,title,author,year,pub,volume,page,doi,"
    "identifier,esources,property,arxiv_class,abstract"
)
USER_AGENT = "ads-search/1.0 (Claude Code skill)"
REQUEST_TIMEOUT = 30
MAX_RESULTS_DEFAULT = 10


# --- Exceptions ---


class ADSError(Exception):
    """Error during ADS operations."""
    pass


# --- Helpers ---


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


def get_token():
    """Get ADS API token from env var or config file."""
    token = os.environ.get("ADS_DEV_KEY")
    if token:
        return token.strip()

    token_file = Path.home() / ".ads" / "dev_key"
    if token_file.is_file():
        token = token_file.read_text().strip()
        if token:
            return token

    raise ADSError(
        "No ADS API token found. Set ADS_DEV_KEY env var or create ~/.ads/dev_key.\n"
        "Get your token at: https://ui.adsabs.harvard.edu/user/settings/token"
    )


def make_request(url, method="GET", data=None, headers=None):
    """Make an authenticated ADS API request. Returns bytes."""
    token = get_token()
    req_headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {token}",
    }
    if headers:
        req_headers.update(headers)

    if data is not None:
        if isinstance(data, str):
            data = data.encode("utf-8")
        req_headers.setdefault("Content-Type", "application/json")

    req = Request(url, data=data, headers=req_headers, method=method)
    try:
        with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            return resp.read()
    except HTTPError as e:
        if e.code == 401:
            raise ADSError("Invalid ADS API token (401 Unauthorized)")
        elif e.code == 404:
            raise ADSError(f"Not found (404): {url}")
        elif e.code == 429:
            raise ADSError("Rate limited (429). Wait a moment and retry.")
        else:
            body = ""
            try:
                body = e.read().decode("utf-8", errors="replace")[:200]
            except Exception:
                pass
            raise ADSError(f"HTTP {e.code}: {url}\n{body}")
    except URLError as e:
        raise ADSError(f"Could not connect: {e.reason}")


# --- arXiv ID extraction ---


def extract_arxiv_id(identifiers):
    """Extract arXiv ID from ADS identifier list."""
    if not identifiers:
        return None
    for ident in identifiers:
        # New format: 2301.12345
        if re.match(r"^\d{4}\.\d{4,5}$", ident):
            return ident
        # Old format: astro-ph/0601234
        if re.match(r"^[a-z-]+/\d{7}$", ident):
            return ident
        # Prefixed: arXiv:2301.12345
        if ident.startswith("arXiv:"):
            return ident[6:]
    return None


# --- Search ---


def search_ads(query, max_results=MAX_RESULTS_DEFAULT, sort="date desc"):
    """Search ADS and return list of result dicts."""
    params = urlencode({
        "q": query,
        "fl": ADS_SEARCH_FIELDS,
        "rows": max_results,
        "sort": sort,
    })
    url = f"{ADS_API_URL}/search/query?{params}"
    eprint(f"Searching ADS for: {query}")

    data = make_request(url)
    result = json.loads(data)

    docs = result.get("response", {}).get("docs", [])
    if not docs:
        eprint("No results found.")
        return []

    papers = []
    for doc in docs:
        bibcode = doc.get("bibcode", "")
        title = doc.get("title", ["Unknown"])[0] if doc.get("title") else "Unknown"
        authors = doc.get("author", [])
        year = doc.get("year", "unknown")
        pub = doc.get("pub", "")
        volume = doc.get("volume", "")
        page = doc.get("page", [""])[0] if doc.get("page") else ""
        doi = doc.get("doi", [""])[0] if doc.get("doi") else ""
        esources = doc.get("esources", [])
        arxiv_id = extract_arxiv_id(doc.get("identifier", []))
        arxiv_class = doc.get("arxiv_class", [""])[0] if doc.get("arxiv_class") else ""

        papers.append({
            "bibcode": bibcode,
            "title": title,
            "authors": authors,
            "year": year,
            "pub": pub,
            "volume": volume,
            "page": page,
            "doi": doi,
            "arxiv_id": arxiv_id,
            "arxiv_class": arxiv_class,
            "esources": esources,
            "has_arxiv": arxiv_id is not None,
            "has_pdf": any(s.endswith("_PDF") for s in esources),
        })

    eprint(f"Found {len(papers)} result(s).")
    return papers


# --- BibTeX ---


def fetch_bibtex(bibcodes, outdir=None):
    """Fetch BibTeX entries for given bibcodes. Returns BibTeX string."""
    if isinstance(bibcodes, str):
        bibcodes = [b.strip() for b in bibcodes.split(",")]

    url = f"{ADS_API_URL}/export/bibtex"
    payload = json.dumps({"bibcode": bibcodes})
    eprint(f"Fetching BibTeX for {len(bibcodes)} paper(s)...")

    data = make_request(url, method="POST", data=payload)
    result = json.loads(data)
    bibtex = result.get("export", "")

    if not bibtex:
        raise ADSError("No BibTeX data returned")

    saved_files = []
    if outdir:
        os.makedirs(outdir, exist_ok=True)
        for bibcode in bibcodes:
            # Extract individual entry for this bibcode
            safe_name = bibcode.replace("/", "_").replace(".", "_")
            filepath = os.path.join(outdir, f"{safe_name}.bib")
            # Find this bibcode's entry in the combined bibtex
            entry = extract_bibtex_entry(bibtex, bibcode)
            if entry:
                with open(filepath, "w") as f:
                    f.write(entry + "\n")
                saved_files.append(f"{safe_name}.bib")
                eprint(f"  Saved: {filepath}")

        # If single bibcode or entries couldn't be split, save everything
        if not saved_files:
            filepath = os.path.join(outdir, "references.bib")
            with open(filepath, "w") as f:
                f.write(bibtex)
            saved_files.append("references.bib")
            eprint(f"  Saved: {filepath}")

    return {"bibtex": bibtex, "files": saved_files}


def extract_bibtex_entry(bibtex_text, bibcode):
    """Extract a single BibTeX entry matching a bibcode."""
    # BibTeX entries start with @type{key,
    # Try to find entry containing this bibcode
    lines = bibtex_text.split("\n")
    entry_lines = []
    depth = 0
    in_entry = False

    for line in lines:
        if not in_entry:
            # Look for @type{... line
            if line.strip().startswith("@") and "{" in line:
                entry_lines = [line]
                depth = line.count("{") - line.count("}")
                in_entry = True
        else:
            entry_lines.append(line)
            depth += line.count("{") - line.count("}")
            if depth <= 0:
                # Entry complete - check if it matches
                entry_text = "\n".join(entry_lines)
                # The bibcode appears in the key or as an ADS field
                # ADS uses bibcode as the cite key (with dots replaced)
                if bibcode in entry_text or bibcode.replace("&", "\\&") in entry_text:
                    return entry_text
                entry_lines = []
                in_entry = False

    # Fallback: return entire text if only one bibcode requested
    return bibtex_text if bibtex_text.strip() else None


# --- PDF Download ---


def download_pdf(bibcode, outdir="refs/"):
    """Download PDF for a paper via ADS link gateway."""
    os.makedirs(outdir, exist_ok=True)
    safe_name = bibcode.replace("/", "_").replace(".", "_")
    filepath = os.path.join(outdir, f"{safe_name}.pdf")

    # Try ADS PDF link gateway
    # ADS provides links at /link_gateway/{bibcode}/{link_type}
    link_types = ["EPRINT_PDF", "PUB_PDF", "ADS_PDF"]

    for link_type in link_types:
        url = f"https://ui.adsabs.harvard.edu/link_gateway/{bibcode}/{link_type}"
        eprint(f"  Trying {link_type}...")
        try:
            req = Request(url, headers={"User-Agent": USER_AGENT})
            with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                content = resp.read()
                # Check it's actually a PDF
                if content[:4] == b"%PDF":
                    with open(filepath, "wb") as f:
                        f.write(content)
                    eprint(f"  Downloaded: {filepath} ({len(content)} bytes)")
                    return {"file": f"{safe_name}.pdf", "source": link_type}
                else:
                    eprint(f"  {link_type}: not a direct PDF, skipping")
        except (HTTPError, URLError) as e:
            eprint(f"  {link_type}: failed ({e})")
            continue

    raise ADSError(f"Could not download PDF for {bibcode}")


# --- Main ---


def main():
    parser = argparse.ArgumentParser(description="Search NASA ADS for scientific papers")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--search", help="Search query (ADS syntax)")
    group.add_argument("--citations", help="Find papers that cite this bibcode")
    group.add_argument("--bibtex", help="Fetch BibTeX for bibcode(s), comma-separated")
    group.add_argument("--pdf", help="Download PDF for a bibcode")

    parser.add_argument("--outdir", default="refs/", help="Output directory (default: refs/)")
    parser.add_argument(
        "--max-results", type=int, default=MAX_RESULTS_DEFAULT,
        help=f"Max search results (default: {MAX_RESULTS_DEFAULT})"
    )
    parser.add_argument(
        "--sort", default="date desc",
        help='Sort order (default: "date desc"). Options: "date asc", "citation_count desc"'
    )

    args = parser.parse_args()

    try:
        if args.search:
            results = search_ads(args.search, max_results=args.max_results, sort=args.sort)
            print(json.dumps(results, indent=2))

        elif args.citations:
            eprint(f"Finding papers that cite: {args.citations}")
            query = f"citations(bibcode:{args.citations})"
            results = search_ads(query, max_results=args.max_results, sort=args.sort)
            print(json.dumps(results, indent=2))

        elif args.bibtex:
            result = fetch_bibtex(args.bibtex, outdir=args.outdir)
            print(json.dumps({"files": result["files"]}, indent=2))

        elif args.pdf:
            result = download_pdf(args.pdf, outdir=args.outdir)
            print(json.dumps(result, indent=2))

    except ADSError as e:
        eprint(f"Error: {e}")
        sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        eprint(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
