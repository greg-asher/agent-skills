#!/usr/bin/env python3
"""Inventory local source material and safely extract OOXML structure."""

from __future__ import annotations

import argparse
import hashlib
import json
import posixpath
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable
from xml.etree import ElementTree as ET


DEPENDENCY_DIRS = {
    ".git",
    ".discovery",
    ".idea",
    ".next",
    ".pytest_cache",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "target",
    "tmp",
    "vendor",
}
TEMP_SUFFIXES = {".bak", ".swp", ".temp", ".tmp", "~"}
LOCK_NAMES = {
    "bun.lock",
    "bun.lockb",
    "composer.lock",
    "gemfile.lock",
    "package-lock.json",
    "pnpm-lock.yaml",
    "poetry.lock",
    "uv.lock",
    "yarn.lock",
}
OFFICE_SUFFIXES = {".pptx", ".docx", ".xlsx"}
TEXT_SUFFIXES = {
    ".csv",
    ".html",
    ".json",
    ".md",
    ".mmd",
    ".rst",
    ".sql",
    ".svg",
    ".toml",
    ".tsv",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
IMAGE_SUFFIXES = {".bmp", ".gif", ".jpeg", ".jpg", ".png", ".tif", ".tiff", ".webp"}
SOFTWARE_SUFFIXES = {
    ".c", ".cc", ".clj", ".cpp", ".cs", ".css", ".ex", ".exs", ".go",
    ".h", ".hpp", ".java", ".js", ".jsx", ".kt", ".kts", ".lua", ".php",
    ".pl", ".py", ".rb", ".rs", ".scala", ".sh", ".swift", ".ts", ".tsx",
    ".vue",
}
GENERATED_DISCOVERY_PATTERNS = (
    re.compile(r"^(docs/discovery|discovery)/[^/]+-assets(/|$)"),
    re.compile(r"^(docs/discovery|discovery)/[^/]+-(deep|greenfield)-discovery\.md$"),
    re.compile(r"(^|/)source-(manifest|model)\.json$"),
)
MAX_ARCHIVE_ENTRIES = 10_000
MAX_UNCOMPRESSED_BYTES = 250 * 1024 * 1024
MAX_ENTRY_BYTES = 50 * 1024 * 1024
MAX_COMPRESSION_RATIO = 1_000
OFFICE_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def attr_by_local(element: ET.Element, name: str) -> str | None:
    for key, value in element.attrib.items():
        if local_name(key) == name:
            return value
    return None


def relationship_id(element: ET.Element) -> str | None:
    namespaced = element.attrib.get(f"{{{OFFICE_REL_NS}}}id")
    if namespaced:
        return namespaced
    return next(
        (
            value
            for key, value in element.attrib.items()
            if local_name(key) == "id" and (key.startswith("{") or value.startswith("rId"))
        ),
        None,
    )


def xml_text(element: ET.Element, include_deleted: bool = True) -> str:
    parts: list[str] = []
    for item in element.iter():
        name = local_name(item.tag)
        if name in {"t", "instrText"} or (include_deleted and name == "delText"):
            if item.text:
                parts.append(item.text)
        elif name in {"tab"}:
            parts.append("\t")
        elif name in {"br", "cr"}:
            parts.append("\n")
    return "".join(parts).strip()


def parse_xml(data: bytes, source: str) -> ET.Element:
    try:
        return ET.fromstring(data)
    except ET.ParseError as error:
        raise ValueError(f"Malformed XML in {source}: {error}") from error


def relationship_map(archive: zipfile.ZipFile, rel_path: str) -> dict[str, dict[str, str]]:
    if rel_path not in archive.namelist():
        return {}
    root = parse_xml(archive.read(rel_path), rel_path)
    relationships: dict[str, dict[str, str]] = {}
    for element in root:
        if local_name(element.tag) != "Relationship":
            continue
        rel_id = element.attrib.get("Id")
        if rel_id:
            relationships[rel_id] = {
                "target": element.attrib.get("Target", ""),
                "type": element.attrib.get("Type", ""),
                "targetMode": element.attrib.get("TargetMode", "Internal"),
            }
    return relationships


def resolve_part(base_part: str, target: str) -> str:
    if target.startswith("/"):
        return target.lstrip("/")
    return posixpath.normpath(posixpath.join(posixpath.dirname(base_part), target))


def rels_path(part: str) -> str:
    return posixpath.join(posixpath.dirname(part), "_rels", posixpath.basename(part) + ".rels")


def safe_archive(path: Path) -> zipfile.ZipFile:
    try:
        archive = zipfile.ZipFile(path)
    except (OSError, zipfile.BadZipFile) as error:
        raise ValueError(f"Unreadable OOXML archive: {error}") from error

    infos = archive.infolist()
    if len(infos) > MAX_ARCHIVE_ENTRIES:
        archive.close()
        raise ValueError(f"Archive has {len(infos)} entries; limit is {MAX_ARCHIVE_ENTRIES}")

    total = 0
    for info in infos:
        member = PurePosixPath(info.filename)
        if member.is_absolute() or ".." in member.parts or "\\" in info.filename:
            archive.close()
            raise ValueError(f"Unsafe archive path: {info.filename}")
        if info.file_size > MAX_ENTRY_BYTES:
            archive.close()
            raise ValueError(f"Archive entry exceeds size limit: {info.filename}")
        total += info.file_size
        if total > MAX_UNCOMPRESSED_BYTES:
            archive.close()
            raise ValueError("Archive exceeds total expansion limit")
        if info.file_size and info.compress_size == 0:
            archive.close()
            raise ValueError(f"Unsafe compressed entry: {info.filename}")
        if info.compress_size and info.file_size / info.compress_size > MAX_COMPRESSION_RATIO:
            archive.close()
            raise ValueError(f"Archive entry exceeds compression ratio limit: {info.filename}")
    return archive


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_type(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix in OFFICE_SUFFIXES:
        return "office-document", "ooxml-extractor"
    if suffix == ".pdf":
        return "pdf", "native-pdf"
    if suffix in IMAGE_SUFFIXES:
        return "image", "native-image"
    if suffix in SOFTWARE_SUFFIXES:
        return "software-source", "native-text"
    if suffix in TEXT_SUFFIXES or path.name.lower() in {"dockerfile", "makefile"}:
        return "text-or-structured-data", "native-text"
    return "other", "unknown"


def excluded_reason(relative: str, path: Path, explicit: set[str]) -> str | None:
    parts = PurePosixPath(relative).parts
    if any(part in DEPENDENCY_DIRS for part in parts[:-1]):
        return "dependency-or-generated-directory"
    if any(relative == item or relative.startswith(item.rstrip("/") + "/") for item in explicit):
        return "explicit-exclusion"
    lower_name = path.name.lower()
    if lower_name in {".ds_store", "thumbs.db"}:
        return "system-file"
    if lower_name in LOCK_NAMES or lower_name.endswith(".lock"):
        return "lock-file"
    if any(path.name.endswith(suffix) for suffix in TEMP_SUFFIXES):
        return "temporary-file"
    if any(pattern.search(relative) for pattern in GENERATED_DISCOVERY_PATTERNS):
        return "generated-discovery-output"
    return None


def load_previous(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    try:
        data = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise ValueError(f"Cannot read previous manifest: {error}") from error
    return {item["path"]: item for item in data.get("files", []) if "path" in item}


def build_manifest(root: Path, previous_path: Path | None, exclusions: Iterable[str]) -> dict[str, Any]:
    root = root.resolve()
    if not root.is_dir():
        raise ValueError(f"Workspace is not a directory: {root}")
    previous = load_previous(previous_path)
    explicit = {PurePosixPath(item).as_posix().lstrip("./") for item in exclusions}
    files: list[dict[str, Any]] = []
    excluded: list[dict[str, str]] = []

    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
        if not path.is_file() or path.is_symlink():
            continue
        relative = path.relative_to(root).as_posix()
        reason = excluded_reason(relative, path, explicit)
        if reason:
            excluded.append({"path": relative, "reason": reason})
            continue
        stat = path.stat()
        digest = sha256(path)
        kind, method = source_type(path)
        prior = previous.get(relative)
        if prior is None:
            change = "new"
        elif prior.get("sha256") == digest:
            change = "unchanged"
        else:
            change = "changed"
        limitations = [] if method != "unknown" else ["No bundled extraction method is known for this file type."]
        files.append(
            {
                "path": relative,
                "type": kind,
                "size": stat.st_size,
                "modifiedTime": datetime.fromtimestamp(stat.st_mtime, timezone.utc).isoformat(),
                "sha256": digest,
                "duplicateOf": None,
                "reviewState": "unreviewed",
                "extractionMethod": method,
                "limitations": limitations,
                "changeState": change,
            }
        )

    first_by_hash: dict[str, str] = {}
    for item in files:
        digest = item["sha256"]
        if digest in first_by_hash:
            item["duplicateOf"] = first_by_hash[digest]
            item["reviewState"] = "duplicate"
            item["limitations"] = ["Byte-identical duplicate; review the canonical source instead."]
        else:
            first_by_hash[digest] = item["path"]

    current_paths = {item["path"] for item in files}
    removed = sorted(path for path in previous if path not in current_paths)
    counts: dict[str, int] = {}
    for item in files:
        counts[item["changeState"]] = counts.get(item["changeState"], 0) + 1

    return {
        "schemaVersion": "1.0",
        "generatedAt": datetime.now(timezone.utc).isoformat(),
        "root": ".",
        "files": files,
        "excluded": excluded,
        "removed": removed,
        "summary": {
            "fileCount": len(files),
            "duplicateCount": sum(1 for item in files if item["duplicateOf"]),
            "changeCounts": counts,
        },
    }


def pptx_slide_parts(archive: zipfile.ZipFile) -> list[str]:
    presentation = "ppt/presentation.xml"
    if presentation not in archive.namelist():
        return sorted(
            (name for name in archive.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", name)),
            key=lambda name: int(re.search(r"(\d+)", Path(name).stem).group(1)),
        )
    root = parse_xml(archive.read(presentation), presentation)
    rels = relationship_map(archive, rels_path(presentation))
    ordered: list[str] = []
    for element in root.iter():
        if local_name(element.tag) != "sldId":
            continue
        rel_id = relationship_id(element)
        relationship = rels.get(rel_id or "")
        if relationship:
            ordered.append(resolve_part(presentation, relationship["target"]))
    return ordered


def extract_pptx(archive: zipfile.ZipFile) -> dict[str, Any]:
    slides: list[dict[str, Any]] = []
    names = set(archive.namelist())
    for order, part in enumerate(pptx_slide_parts(archive), start=1):
        if part not in names:
            continue
        root = parse_xml(archive.read(part), part)
        rels = relationship_map(archive, rels_path(part))
        text = [item.text for item in root.iter() if local_name(item.tag) == "t" and item.text]
        alt_text: list[dict[str, str]] = []
        for item in root.iter():
            if local_name(item.tag) != "cNvPr":
                continue
            values = {key: item.attrib[key] for key in ("name", "title", "descr") if item.attrib.get(key)}
            if values.get("title") or values.get("descr"):
                alt_text.append(values)
        links: list[dict[str, str]] = []
        for item in root.iter():
            if local_name(item.tag) not in {"hlinkClick", "hlinkHover"}:
                continue
            rel_id = relationship_id(item)
            rel = rels.get(rel_id or "")
            if rel:
                links.append({"target": rel["target"], "mode": rel["targetMode"]})
        media: list[str] = []
        note_text: list[str] = []
        for rel in rels.values():
            target = resolve_part(part, rel["target"])
            if "/media" in rel["target"] or "/media/" in target:
                media.append(target)
            if rel["type"].endswith("notesSlide") and target in names:
                notes_root = parse_xml(archive.read(target), target)
                note_text.extend(item.text for item in notes_root.iter() if local_name(item.tag) == "t" and item.text)
        slides.append(
            {
                "slide": order,
                "part": part,
                "text": text,
                "speakerNotes": note_text,
                "links": links,
                "altText": alt_text,
                "embeddedMedia": sorted(set(media)),
            }
        )
    return {"format": "pptx", "slides": slides}


def paragraph_record(element: ET.Element, styles: dict[str, str] | None = None) -> dict[str, Any]:
    style_id = None
    inserted = False
    deleted = False
    for item in element.iter():
        name = local_name(item.tag)
        if name == "pStyle":
            style_id = attr_by_local(item, "val")
        elif name == "ins":
            inserted = True
        elif name == "del":
            deleted = True
    style_name = (styles or {}).get(style_id or "", style_id)
    return {
        "text": xml_text(element),
        "style": style_name,
        "heading": bool(style_name and style_name.lower().startswith("heading")),
        "trackedChange": {"inserted": inserted, "deleted": deleted},
    }


def docx_styles(archive: zipfile.ZipFile) -> dict[str, str]:
    path = "word/styles.xml"
    if path not in archive.namelist():
        return {}
    root = parse_xml(archive.read(path), path)
    styles: dict[str, str] = {}
    for style in root.iter():
        if local_name(style.tag) != "style":
            continue
        style_id = attr_by_local(style, "styleId")
        name = next((attr_by_local(item, "val") for item in style if local_name(item.tag) == "name"), None)
        if style_id:
            styles[style_id] = name or style_id
    return styles


def extract_docx(archive: zipfile.ZipFile) -> dict[str, Any]:
    document_path = "word/document.xml"
    if document_path not in archive.namelist():
        raise ValueError("DOCX is missing word/document.xml")
    styles = docx_styles(archive)
    root = parse_xml(archive.read(document_path), document_path)
    paragraphs: list[dict[str, Any]] = []
    tables: list[list[list[str]]] = []
    table_paragraphs = {
        id(item)
        for table in root.iter()
        if local_name(table.tag) == "tbl"
        for item in table.iter()
        if local_name(item.tag) == "p"
    }
    for element in root.iter():
        name = local_name(element.tag)
        if name == "p" and id(element) not in table_paragraphs:
            record = paragraph_record(element, styles)
            if record["text"]:
                paragraphs.append(record)
        elif name == "tbl":
            table: list[list[str]] = []
            for row in element:
                if local_name(row.tag) != "tr":
                    continue
                table.append([xml_text(cell) for cell in row if local_name(cell.tag) == "tc"])
            tables.append(table)

    comments: list[dict[str, Any]] = []
    if "word/comments.xml" in archive.namelist():
        comments_root = parse_xml(archive.read("word/comments.xml"), "word/comments.xml")
        for item in comments_root:
            if local_name(item.tag) == "comment":
                comments.append(
                    {
                        "id": attr_by_local(item, "id"),
                        "author": attr_by_local(item, "author"),
                        "date": attr_by_local(item, "date"),
                        "text": xml_text(item),
                    }
                )

    headers: list[dict[str, str]] = []
    footnotes: list[dict[str, str]] = []
    for name in archive.namelist():
        if re.fullmatch(r"word/header\d+\.xml", name):
            headers.append({"part": name, "text": xml_text(parse_xml(archive.read(name), name))})
        elif name == "word/footnotes.xml":
            note_root = parse_xml(archive.read(name), name)
            for item in note_root:
                note_id = attr_by_local(item, "id")
                if note_id not in {"-1", "0"}:
                    footnotes.append({"id": note_id or "", "text": xml_text(item)})

    tracked = any(
        record["trackedChange"]["inserted"] or record["trackedChange"]["deleted"]
        for record in paragraphs
    )
    if "word/settings.xml" in archive.namelist():
        settings = parse_xml(archive.read("word/settings.xml"), "word/settings.xml")
        tracked = tracked or any(local_name(item.tag) == "trackRevisions" for item in settings.iter())
    return {
        "format": "docx",
        "paragraphs": paragraphs,
        "tables": tables,
        "comments": comments,
        "headers": headers,
        "footnotes": footnotes,
        "trackedChangesPresent": tracked,
    }


def excel_column_index(reference: str) -> int:
    match = re.match(r"([A-Z]+)", reference.upper())
    if not match:
        return 0
    value = 0
    for char in match.group(1):
        value = value * 26 + ord(char) - 64
    return value


def shared_strings(archive: zipfile.ZipFile) -> list[str]:
    path = "xl/sharedStrings.xml"
    if path not in archive.namelist():
        return []
    root = parse_xml(archive.read(path), path)
    return [xml_text(item) for item in root if local_name(item.tag) == "si"]


def workbook_sheets(archive: zipfile.ZipFile) -> list[tuple[str, str]]:
    path = "xl/workbook.xml"
    if path not in archive.namelist():
        raise ValueError("XLSX is missing xl/workbook.xml")
    root = parse_xml(archive.read(path), path)
    rels = relationship_map(archive, rels_path(path))
    sheets: list[tuple[str, str]] = []
    for item in root.iter():
        if local_name(item.tag) != "sheet":
            continue
        rel_id = relationship_id(item)
        rel = rels.get(rel_id or "")
        if rel:
            sheets.append((item.attrib.get("name", "Unnamed"), resolve_part(path, rel["target"])))
    return sheets


def cell_value(cell: ET.Element, strings: list[str]) -> tuple[str | None, str | None]:
    formula = next((item.text for item in cell if local_name(item.tag) == "f"), None)
    value = next((item.text for item in cell if local_name(item.tag) == "v"), None)
    inline = next((xml_text(item) for item in cell if local_name(item.tag) == "is"), None)
    cell_type = cell.attrib.get("t")
    if inline is not None:
        value = inline
    elif cell_type == "s" and value is not None:
        try:
            value = strings[int(value)]
        except (ValueError, IndexError):
            value = f"[invalid shared string {value}]"
    elif cell_type == "b" and value is not None:
        value = "TRUE" if value == "1" else "FALSE"
    return value, formula


def xlsx_comments(archive: zipfile.ZipFile, sheet_part: str) -> list[dict[str, str]]:
    rels = relationship_map(archive, rels_path(sheet_part))
    comments: list[dict[str, str]] = []
    for rel in rels.values():
        if not rel["type"].endswith("comments"):
            continue
        part = resolve_part(sheet_part, rel["target"])
        if part not in archive.namelist():
            continue
        root = parse_xml(archive.read(part), part)
        for item in root.iter():
            if local_name(item.tag) == "comment":
                comments.append({"cell": item.attrib.get("ref", ""), "text": xml_text(item)})
    return comments


def xlsx_tables(archive: zipfile.ZipFile, sheet_part: str) -> list[dict[str, Any]]:
    rels = relationship_map(archive, rels_path(sheet_part))
    tables: list[dict[str, Any]] = []
    for rel in rels.values():
        if not rel["type"].endswith("table"):
            continue
        part = resolve_part(sheet_part, rel["target"])
        if part not in archive.namelist():
            continue
        root = parse_xml(archive.read(part), part)
        columns = [item.attrib.get("name", "") for item in root.iter() if local_name(item.tag) == "tableColumn"]
        tables.append({"name": root.attrib.get("displayName", root.attrib.get("name", "")), "range": root.attrib.get("ref", ""), "columns": columns})
    return tables


def extract_xlsx(archive: zipfile.ZipFile, max_cells: int) -> dict[str, Any]:
    strings = shared_strings(archive)
    sheets: list[dict[str, Any]] = []
    for sheet_name, part in workbook_sheets(archive):
        if part not in archive.namelist():
            sheets.append({"name": sheet_name, "part": part, "cells": [], "limitations": ["Worksheet part is missing."]})
            continue
        root = parse_xml(archive.read(part), part)
        cells: list[dict[str, Any]] = []
        omitted = 0
        first_omitted = None
        last_omitted = None
        max_row = 0
        max_col = 0
        for cell in (item for item in root.iter() if local_name(item.tag) == "c"):
            ref = cell.attrib.get("r", "")
            row_match = re.search(r"(\d+)$", ref)
            max_row = max(max_row, int(row_match.group(1)) if row_match else 0)
            max_col = max(max_col, excel_column_index(ref))
            value, formula = cell_value(cell, strings)
            if value is None and formula is None:
                continue
            if len(cells) < max_cells:
                cells.append({"cell": ref, "value": value, "formula": formula})
            else:
                omitted += 1
                first_omitted = first_omitted or ref
                last_omitted = ref
        limitations = []
        if omitted:
            limitations.append(f"Omitted {omitted} non-empty cells after the {max_cells}-cell preview limit.")
        sheets.append(
            {
                "name": sheet_name,
                "part": part,
                "usedRange": {"maxRow": max_row, "maxColumn": max_col},
                "cells": cells,
                "omittedCellCount": omitted,
                "omittedRanges": (
                    [{"firstCell": first_omitted, "lastCell": last_omitted, "count": omitted}]
                    if omitted
                    else []
                ),
                "tables": xlsx_tables(archive, part),
                "comments": xlsx_comments(archive, part),
                "limitations": limitations,
            }
        )
    return {"format": "xlsx", "sheets": sheets, "maxCellsPerSheet": max_cells}


def markdown_for(content: dict[str, Any], source_name: str) -> str:
    lines = [f"# Extracted structure: {source_name}", ""]
    if content["format"] == "pptx":
        for slide in content["slides"]:
            lines.extend([f"## Slide {slide['slide']}", "", " ".join(slide["text"]) or "[No text]", ""])
            if slide["speakerNotes"]:
                lines.extend(["**Speaker notes:** " + " ".join(slide["speakerNotes"]), ""])
            if slide["links"]:
                lines.extend(["**Links:** " + ", ".join(item["target"] for item in slide["links"]), ""])
            if slide["altText"]:
                lines.extend(["**Alt text:** " + "; ".join(item.get("descr") or item.get("title", "") for item in slide["altText"]), ""])
            if slide["embeddedMedia"]:
                lines.extend(["**Embedded media:** " + ", ".join(slide["embeddedMedia"]), ""])
    elif content["format"] == "docx":
        for item in content["paragraphs"]:
            prefix = "## " if item["heading"] else ""
            lines.extend([prefix + item["text"], ""])
        for index, table in enumerate(content["tables"], start=1):
            lines.extend([f"## Table {index}", ""])
            lines.extend(" | ".join(row) for row in table)
            lines.append("")
        if content["comments"]:
            lines.extend(["## Comments", ""])
            lines.extend(f"- {item['text']}" for item in content["comments"])
            lines.append("")
    else:
        for sheet in content["sheets"]:
            lines.extend([f"## Sheet: {sheet['name']}", ""])
            for cell in sheet["cells"]:
                formula = f" (formula: {cell['formula']})" if cell["formula"] else ""
                lines.append(f"- {cell['cell']}: {cell['value']}{formula}")
            for limitation in sheet["limitations"]:
                lines.append(f"- Limitation: {limitation}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def extract_office(path: Path, output: Path, max_cells: int) -> dict[str, Any]:
    suffix = path.suffix.lower()
    if suffix not in OFFICE_SUFFIXES:
        raise ValueError(f"Unsupported Office format: {suffix or '[none]'}")
    output = output.resolve()
    source_parent = path.resolve().parent
    if output == source_parent or source_parent in output.parents:
        raise ValueError("Extraction output must be outside the source folder")
    if output.exists() and any(output.iterdir()):
        raise ValueError(f"Extraction output is not empty: {output}")
    output.mkdir(parents=True, exist_ok=True)
    archive = safe_archive(path)
    try:
        if suffix == ".pptx":
            content = extract_pptx(archive)
        elif suffix == ".docx":
            content = extract_docx(archive)
        else:
            content = extract_xlsx(archive, max_cells)
    finally:
        archive.close()
    document = {
        "schemaVersion": "1.0",
        "source": path.name,
        "extractedAt": datetime.now(timezone.utc).isoformat(),
        "content": content,
    }
    (output / "content.json").write_text(json.dumps(document, indent=2) + "\n")
    (output / "content.md").write_text(markdown_for(content, path.name))
    return document


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(document, indent=2) + "\n")


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    subcommands = command.add_subparsers(dest="command", required=True)
    inventory = subcommands.add_parser("inventory", help="Inventory and hash a source folder")
    inventory.add_argument("--root", required=True, type=Path)
    inventory.add_argument("--output", required=True, type=Path)
    inventory.add_argument("--previous", type=Path)
    inventory.add_argument("--exclude", action="append", default=[])
    extract = subcommands.add_parser("extract", help="Extract OOXML structure")
    extract.add_argument("--input", required=True, type=Path)
    extract.add_argument("--output", required=True, type=Path)
    extract.add_argument("--max-cells", type=int, default=2_000)
    return command


def main() -> int:
    arguments = parser().parse_args()
    try:
        if arguments.command == "inventory":
            document = build_manifest(arguments.root, arguments.previous, arguments.exclude)
            write_json(arguments.output, document)
            print(json.dumps(document["summary"], sort_keys=True))
        else:
            if arguments.max_cells < 1:
                raise ValueError("--max-cells must be at least 1")
            document = extract_office(arguments.input, arguments.output, arguments.max_cells)
            print(json.dumps({"format": document["content"]["format"], "output": str(arguments.output)}, sort_keys=True))
        return 0
    except (OSError, ValueError, zipfile.BadZipFile) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
