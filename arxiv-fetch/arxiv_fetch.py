#!/usr/bin/env python3
"""
arxiv_fetch.py - Fetch arXiv paper LaTeX sources.

Usage:
    python3 arxiv_fetch.py --search "neutron star magnetosphere"
    python3 arxiv_fetch.py --id 2301.12345 --outdir refs/

Output: JSON to stdout, status/errors to stderr.
Dependencies: Python 3.7+ stdlib only.
"""

import argparse
import gzip
import io
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import time
import xml.etree.ElementTree as ET
from urllib.error import HTTPError, URLError
from urllib.parse import quote, quote_plus
from urllib.request import Request, urlopen

# --- Constants ---

ARXIV_API_URL = "https://export.arxiv.org/api/query"
ARXIV_EPRINT_URL = "https://arxiv.org/e-print/{}"
ARXIV_BIBTEX_URL = "https://arxiv.org/bibtex/{}"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"
USER_AGENT = "arxiv-fetch/1.1 (Claude Code skill; mailto:nattila.joonas@gmail.com)"
REQUEST_DELAY = 3.0
REQUEST_TIMEOUT = 60
MAX_RETRIES = 5
BACKOFF_BASE = 5.0  # seconds; doubles each retry when no Retry-After header


# --- Exceptions ---


class ArxivFetchError(Exception):
    """Non-fatal error during arXiv operations."""
    pass


# --- Helpers ---


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, **kwargs)


_last_request_time = 0.0


def _throttle():
    """Enforce a minimum spacing between requests within this process."""
    global _last_request_time
    elapsed = time.monotonic() - _last_request_time
    if elapsed < REQUEST_DELAY:
        time.sleep(REQUEST_DELAY - elapsed)
    _last_request_time = time.monotonic()


def make_request(url):
    """Make an HTTP GET request, return bytes. Raises ArxivFetchError on failure.

    Retries on 429/5xx (honoring Retry-After) and on timeouts/connection errors,
    with exponential backoff. Fails immediately on 404.
    """
    last_error = None
    for attempt in range(MAX_RETRIES):
        _throttle()
        req = Request(url, headers={"User-Agent": USER_AGENT})
        try:
            with urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                return resp.read()
        except HTTPError as e:
            if e.code == 404:
                raise ArxivFetchError(f"Not found (404): {url}")
            retryable = e.code in (429, 500, 502, 503, 504)
            last_error = f"HTTP {e.code}: {url}"
            if not retryable:
                raise ArxivFetchError(last_error)
            retry_after = e.headers.get("Retry-After") if e.headers else None
            try:
                wait = float(retry_after)
            except (TypeError, ValueError):
                wait = BACKOFF_BASE * (2 ** attempt)
            wait = min(wait, 120.0)
        except (URLError, TimeoutError, OSError) as e:
            reason = getattr(e, "reason", e)
            last_error = f"Could not connect: {reason}"
            wait = BACKOFF_BASE * (2 ** attempt)
        if attempt < MAX_RETRIES - 1:
            eprint(f"  Retrying in {wait:.0f}s ({last_error}, attempt {attempt + 1}/{MAX_RETRIES})")
            time.sleep(wait)
    raise ArxivFetchError(f"Failed after {MAX_RETRIES} attempts: {last_error}")


def sanitize_id(raw_id):
    """Extract clean arXiv ID from URL or raw input. Strip version suffix."""
    raw_id = raw_id.strip()
    for prefix in (
        "http://arxiv.org/abs/",
        "https://arxiv.org/abs/",
        "http://arxiv.org/pdf/",
        "https://arxiv.org/pdf/",
    ):
        if raw_id.startswith(prefix):
            raw_id = raw_id[len(prefix):]
            break
    return re.sub(r"v\d+$", "", raw_id)


def sanitize_for_filename(arxiv_id):
    """Make arXiv ID safe for filenames (replace / with _)."""
    return arxiv_id.replace("/", "_")


# --- Search ---


def search_arxiv(query, max_results=5):
    """Search arXiv and return list of result dicts."""
    url = f"{ARXIV_API_URL}?search_query=all:{quote_plus(query)}&max_results={max_results}"
    eprint(f"Searching arXiv for: {query}")
    data = make_request(url)
    root = ET.fromstring(data)

    results = []
    for entry in root.findall(f"{ATOM_NS}entry"):
        id_el = entry.find(f"{ATOM_NS}id")
        if id_el is None or id_el.text is None:
            continue
        arxiv_id = sanitize_id(id_el.text)

        title_el = entry.find(f"{ATOM_NS}title")
        title = title_el.text.strip() if title_el is not None and title_el.text else "Unknown"
        title = re.sub(r"\s+", " ", title)

        authors = []
        for author_el in entry.findall(f"{ATOM_NS}author"):
            name_el = author_el.find(f"{ATOM_NS}name")
            if name_el is not None and name_el.text:
                authors.append(name_el.text.strip())

        published_el = entry.find(f"{ATOM_NS}published")
        year = published_el.text[:4] if published_el is not None and published_el.text else "unknown"

        cat_el = entry.find(f"{ARXIV_NS}primary_category")
        category = cat_el.get("term", "unknown") if cat_el is not None else "unknown"

        results.append({
            "id": arxiv_id,
            "title": title,
            "authors": authors,
            "year": year,
            "category": category,
        })

    if not results:
        eprint("No results found.")

    return results


# --- Fetch ---


def fetch_metadata(arxiv_id):
    """Fetch paper metadata (title, authors) from arXiv API."""
    url = f"{ARXIV_API_URL}?id_list={quote(arxiv_id, safe='')}"
    data = make_request(url)
    root = ET.fromstring(data)

    entry = root.find(f"{ATOM_NS}entry")
    if entry is None:
        return {"title": "Unknown", "authors": []}

    title_el = entry.find(f"{ATOM_NS}title")
    title = title_el.text.strip() if title_el is not None and title_el.text else "Unknown"
    title = re.sub(r"\s+", " ", title)

    authors = []
    for author_el in entry.findall(f"{ATOM_NS}author"):
        name_el = author_el.find(f"{ATOM_NS}name")
        if name_el is not None and name_el.text:
            authors.append(name_el.text.strip())

    return {"title": title, "authors": authors}


def detect_file_type(data):
    """Detect if data is PDF, tar.gz, single gzip, or plain text."""
    if data[:4] == b"%PDF":
        return "pdf"
    if data[:2] == b"\x1f\x8b":
        try:
            bio = io.BytesIO(data)
            with tarfile.open(fileobj=bio, mode="r:gz"):
                return "tar.gz"
        except (tarfile.ReadError, tarfile.CompressionError, EOFError):
            return "gzip"
    return "text"


def extract_tar(data, dest):
    """Extract tar.gz data to dest directory with path safety."""
    bio = io.BytesIO(data)
    with tarfile.open(fileobj=bio, mode="r:gz") as tar:
        for member in tar.getmembers():
            if member.name.startswith("/") or ".." in member.name:
                eprint(f"  Skipping unsafe path: {member.name}")
                continue
            tar.extract(member, dest)


def extract_gzip(data, dest):
    """Decompress single gzip file to dest/main.tex."""
    decompressed = gzip.decompress(data)
    outpath = os.path.join(dest, "main.tex")
    with open(outpath, "wb") as f:
        f.write(decompressed)


def extract_text(data, dest):
    """Write plain text data to dest/main.tex."""
    outpath = os.path.join(dest, "main.tex")
    with open(outpath, "wb") as f:
        f.write(data)


def find_main_tex(directory):
    """Find the main .tex file (the one with \\documentclass)."""
    tex_files = []
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if f.endswith(".tex"):
                tex_files.append(os.path.join(root, f))

    if not tex_files:
        return None

    # Priority: common main file names at the top level
    priority_names = ["main.tex", "paper.tex", "ms.tex", "manuscript.tex", "article.tex"]
    for pname in priority_names:
        candidate = os.path.join(directory, pname)
        if candidate in tex_files:
            try:
                with open(candidate, "r", errors="replace") as f:
                    content = f.read()
                if re.search(r"\\documentclass", content):
                    return candidate
            except OSError:
                pass

    # Any file with \documentclass
    for tex_file in sorted(tex_files):
        try:
            with open(tex_file, "r", errors="replace") as f:
                content = f.read()
            if re.search(r"\\documentclass|\\documentstyle", content):
                return tex_file
        except OSError:
            continue

    # Fallback: first .tex file
    return tex_files[0] if tex_files else None


def find_input_files(tex_content, base_dir):
    """Find files referenced by \\input, \\include, \\bibliography."""
    files = []

    # \input{file} and \include{file}
    for match in re.finditer(r"\\(?:input|include)\s*\{([^}]+)\}", tex_content):
        ref = match.group(1).strip()
        candidates = [ref]
        if not ref.endswith((".tex", ".bbl", ".sty", ".cls")):
            candidates.append(ref + ".tex")
        for cand in candidates:
            full = os.path.join(base_dir, cand)
            if os.path.isfile(full):
                files.append(full)
                break

    # \bibliography{name} -> look for name.bbl
    for match in re.finditer(r"\\bibliography\s*\{([^}]+)\}", tex_content):
        ref = match.group(1).strip()
        for part in ref.split(","):
            part = part.strip()
            bbl = os.path.join(base_dir, part + ".bbl")
            if os.path.isfile(bbl):
                files.append(bbl)

    return files


def fetch_bibtex(arxiv_id, outdir):
    """Download BibTeX entry and save to outdir. Returns filename or None."""
    url = ARXIV_BIBTEX_URL.format(arxiv_id)
    try:
        data = make_request(url)
    except ArxivFetchError:
        eprint("  Warning: Could not fetch BibTeX (non-fatal)")
        return None

    text = data.decode("utf-8", errors="replace").strip()
    if not text or "<html" in text.lower():
        eprint("  Warning: BibTeX not available for this paper")
        return None

    filename = sanitize_for_filename(arxiv_id) + ".bib"
    filepath = os.path.join(outdir, filename)
    with open(filepath, "w") as f:
        f.write(text + "\n")
    return filename


def fetch_paper(arxiv_id, outdir):
    """Fetch paper source and extract relevant files."""
    arxiv_id = sanitize_id(arxiv_id)
    safe_id = sanitize_for_filename(arxiv_id)
    eprint(f"Fetching paper: {arxiv_id}")

    # Get metadata (non-fatal: the e-print download below is the real job)
    try:
        meta = fetch_metadata(arxiv_id)
    except ArxivFetchError as e:
        eprint(f"  Warning: Could not fetch metadata ({e})")
        meta = {"title": "Unknown", "authors": []}
    eprint(f"  Title: {meta['title']}")
    authors_str = ", ".join(meta["authors"][:3])
    if len(meta["authors"]) > 3:
        authors_str += "..."
    eprint(f"  Authors: {authors_str}")

    # Download e-print source
    eprint("  Downloading source...")
    url = ARXIV_EPRINT_URL.format(arxiv_id)
    data = make_request(url)

    # Detect type
    ftype = detect_file_type(data)
    eprint(f"  Source type: {ftype}")

    if ftype == "pdf":
        eprint("Error: This paper has no LaTeX source (PDF-only submission).")
        sys.exit(1)

    # Extract to temp dir
    tmpdir = tempfile.mkdtemp(prefix="arxiv_")
    try:
        if ftype == "tar.gz":
            extract_tar(data, tmpdir)
        elif ftype == "gzip":
            extract_gzip(data, tmpdir)
        else:
            extract_text(data, tmpdir)

        # Find main .tex
        main_tex = find_main_tex(tmpdir)
        if main_tex is None:
            eprint("Error: No .tex file found in the source archive.")
            sys.exit(1)

        eprint(f"  Main TeX: {os.path.relpath(main_tex, tmpdir)}")

        # Read main tex, find input files
        with open(main_tex, "r", errors="replace") as f:
            content = f.read()

        input_files = find_input_files(content, os.path.dirname(main_tex))
        eprint(f"  Found {len(input_files)} input file(s)")

        # Copy files to outdir
        os.makedirs(outdir, exist_ok=True)
        copied_files = []

        # Copy main tex
        main_dest = os.path.join(outdir, safe_id + ".tex")
        shutil.copy2(main_tex, main_dest)
        copied_files.append(safe_id + ".tex")

        # Copy input files
        for inp in input_files:
            basename = os.path.basename(inp)
            dest = os.path.join(outdir, basename)
            if os.path.abspath(dest) != os.path.abspath(main_dest):
                shutil.copy2(inp, dest)
                copied_files.append(basename)

        # Fetch BibTeX
        bib_file = fetch_bibtex(arxiv_id, outdir)
        if bib_file:
            copied_files.append(bib_file)
            eprint(f"  BibTeX saved: {bib_file}")

    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    result = {
        "id": arxiv_id,
        "title": meta["title"],
        "authors": meta["authors"],
        "files": copied_files,
    }
    eprint(f"  Done. {len(copied_files)} file(s) saved to {outdir}")
    return result


# --- Main ---


def main():
    parser = argparse.ArgumentParser(description="Fetch arXiv paper LaTeX sources")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--id", dest="arxiv_id", help="arXiv paper ID to fetch")
    group.add_argument("--search", help="Search query for arXiv")
    parser.add_argument("--outdir", default="refs/", help="Output directory (default: refs/)")
    parser.add_argument(
        "--max-results", type=int, default=5, help="Max search results (default: 5)"
    )

    args = parser.parse_args()

    try:
        if args.search:
            results = search_arxiv(args.search, max_results=args.max_results)
            print(json.dumps(results, indent=2))
        else:
            result = fetch_paper(args.arxiv_id, args.outdir)
            print(json.dumps(result, indent=2))
    except ArxivFetchError as e:
        eprint(f"Error: {e}")
        sys.exit(1)
    except SystemExit:
        raise
    except Exception as e:
        eprint(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
