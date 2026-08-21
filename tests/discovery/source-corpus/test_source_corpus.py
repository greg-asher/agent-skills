from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SCRIPT = ROOT / "plugins" / "discovery" / "scripts" / "source-corpus.py"
SPEC = importlib.util.spec_from_file_location("source_corpus", SCRIPT)
assert SPEC and SPEC.loader
SOURCE_CORPUS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SOURCE_CORPUS)


def write_zip(path: Path, members: dict[str, str | bytes]) -> None:
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as archive:
        for name, value in members.items():
            archive.writestr(name, value)


def relationships(items: list[tuple[str, str, str, str | None]]) -> str:
    rendered = []
    for rel_id, rel_type, target, mode in items:
        target_mode = f' TargetMode="{mode}"' if mode else ""
        rendered.append(f'<Relationship Id="{rel_id}" Type="{rel_type}" Target="{target}"{target_mode}/>')
    return '<?xml version="1.0"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rendered) + "</Relationships>"


class InventoryTests(unittest.TestCase):
    def test_inventory_hashes_deduplicates_excludes_and_detects_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "corpus"
            root.mkdir()
            (root / "notes.md").write_text("first")
            (root / "copy.md").write_text("first")
            (root / "package-lock.json").write_text("lock")
            (root / ".discovery").mkdir()
            (root / ".discovery" / "notebook.md").write_text("generated")
            (root / "discovery" / "concept-assets").mkdir(parents=True)
            (root / "discovery" / "concept-assets" / "diagram.md").write_text("generated")

            first = SOURCE_CORPUS.build_manifest(root, None, [])
            paths = [item["path"] for item in first["files"]]
            self.assertEqual(paths, ["copy.md", "notes.md"])
            self.assertEqual(first["summary"]["duplicateCount"], 1)
            duplicate = next(item for item in first["files"] if item["duplicateOf"])
            self.assertEqual(duplicate["reviewState"], "duplicate")

            previous = Path(directory) / "previous.json"
            previous.write_text(json.dumps(first))
            (root / "notes.md").write_text("changed")
            (root / "new.txt").write_text("new")
            (root / "copy.md").unlink()
            second = SOURCE_CORPUS.build_manifest(root, previous, [])
            state = {item["path"]: item["changeState"] for item in second["files"]}
            self.assertEqual(state, {"new.txt": "new", "notes.md": "changed"})
            self.assertEqual(second["removed"], ["copy.md"])


class ExtractionTests(unittest.TestCase):
    def test_extracts_powerpoint_structure(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "corpus"
            source.mkdir()
            path = source / "brief.pptx"
            write_zip(
                path,
                {
                    "ppt/presentation.xml": '<p:presentation xmlns:p="p" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:sldIdLst><p:sldId id="256" r:id="rId1"/></p:sldIdLst></p:presentation>',
                    "ppt/_rels/presentation.xml.rels": relationships([("rId1", "slide", "slides/slide1.xml", None)]),
                    "ppt/slides/slide1.xml": '<p:sld xmlns:p="p" xmlns:a="a" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><p:cSld><p:spTree><p:pic><p:nvPicPr><p:cNvPr name="Chart" descr="Revenue by segment"/></p:nvPicPr></p:pic><a:t>Whitespace review</a:t><a:hlinkClick r:id="rId2"/></p:spTree></p:cSld></p:sld>',
                    "ppt/slides/_rels/slide1.xml.rels": relationships(
                        [
                            ("rId2", "hyperlink", "https://example.com", "External"),
                            ("rId3", "notesSlide", "../notesSlides/notesSlide1.xml", None),
                            ("rId4", "image", "../media/image1.png", None),
                        ]
                    ),
                    "ppt/notesSlides/notesSlide1.xml": '<p:notes xmlns:p="p" xmlns:a="a"><a:t>Ask finance</a:t></p:notes>',
                    "ppt/media/image1.png": b"image",
                },
            )
            output = base / "extract"
            document = SOURCE_CORPUS.extract_office(path, output, 100)
            slide = document["content"]["slides"][0]
            self.assertEqual(slide["text"], ["Whitespace review"])
            self.assertEqual(slide["speakerNotes"], ["Ask finance"])
            self.assertEqual(slide["links"][0]["target"], "https://example.com")
            self.assertEqual(slide["altText"][0]["descr"], "Revenue by segment")
            self.assertEqual(slide["embeddedMedia"], ["ppt/media/image1.png"])
            self.assertTrue((output / "content.md").is_file())

    def test_extracts_word_structure_and_revision_state(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "corpus"
            source.mkdir()
            path = source / "proposal.docx"
            write_zip(
                path,
                {
                    "word/document.xml": '<w:document xmlns:w="w"><w:body><w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t>Proposal</w:t></w:r></w:p><w:p><w:ins><w:r><w:t>New rule</w:t></w:r></w:ins><w:del><w:r><w:delText>Old rule</w:delText></w:r></w:del></w:p><w:tbl><w:tr><w:tc><w:p><w:r><w:t>Owner</w:t></w:r></w:p></w:tc></w:tr></w:tbl></w:body></w:document>',
                    "word/styles.xml": '<w:styles xmlns:w="w"><w:style w:styleId="Heading1"><w:name w:val="Heading 1"/></w:style></w:styles>',
                    "word/comments.xml": '<w:comments xmlns:w="w"><w:comment w:id="1" w:author="Sean"><w:p><w:r><w:t>Confirm this</w:t></w:r></w:p></w:comment></w:comments>',
                    "word/header1.xml": '<w:hdr xmlns:w="w"><w:p><w:r><w:t>Confidential</w:t></w:r></w:p></w:hdr>',
                    "word/footnotes.xml": '<w:footnotes xmlns:w="w"><w:footnote w:id="1"><w:p><w:r><w:t>Source note</w:t></w:r></w:p></w:footnote></w:footnotes>',
                    "word/settings.xml": '<w:settings xmlns:w="w"><w:trackRevisions/></w:settings>',
                },
            )
            document = SOURCE_CORPUS.extract_office(path, base / "extract", 100)
            content = document["content"]
            self.assertTrue(content["paragraphs"][0]["heading"])
            self.assertTrue(content["trackedChangesPresent"])
            self.assertEqual(content["tables"][0], [["Owner"]])
            self.assertEqual(content["comments"][0]["text"], "Confirm this")
            self.assertEqual(content["headers"][0]["text"], "Confidential")
            self.assertEqual(content["footnotes"][0]["text"], "Source note")

    def test_extracts_bounded_excel_preview_formulas_tables_and_comments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "corpus"
            source.mkdir()
            path = source / "model.xlsx"
            write_zip(
                path,
                {
                    "xl/workbook.xml": '<workbook xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"><sheets><sheet name="Pipeline" r:id="rId1"/></sheets></workbook>',
                    "xl/_rels/workbook.xml.rels": relationships([("rId1", "worksheet", "worksheets/sheet1.xml", None)]),
                    "xl/sharedStrings.xml": '<sst><si><t>Account</t></si><si><t>Acme</t></si></sst>',
                    "xl/worksheets/sheet1.xml": '<worksheet><sheetData><row r="1"><c r="A1" t="s"><v>0</v></c><c r="B1"><f>1+1</f><v>2</v></c></row><row r="2"><c r="A2" t="s"><v>1</v></c></row></sheetData></worksheet>',
                    "xl/worksheets/_rels/sheet1.xml.rels": relationships(
                        [
                            ("rId2", "comments", "../comments1.xml", None),
                            ("rId3", "table", "../tables/table1.xml", None),
                        ]
                    ),
                    "xl/comments1.xml": '<comments><commentList><comment ref="A2"><text><t>Top target</t></text></comment></commentList></comments>',
                    "xl/tables/table1.xml": '<table name="Targets" displayName="Targets" ref="A1:B2"><tableColumns><tableColumn name="Account"/><tableColumn name="Score"/></tableColumns></table>',
                },
            )
            document = SOURCE_CORPUS.extract_office(path, base / "extract", 2)
            sheet = document["content"]["sheets"][0]
            self.assertEqual(len(sheet["cells"]), 2)
            self.assertEqual(sheet["omittedCellCount"], 1)
            self.assertEqual(sheet["omittedRanges"], [{"firstCell": "A2", "lastCell": "A2", "count": 1}])
            self.assertEqual(sheet["cells"][1]["formula"], "1+1")
            self.assertEqual(sheet["comments"][0], {"cell": "A2", "text": "Top target"})
            self.assertEqual(sheet["tables"][0]["name"], "Targets")
            self.assertIn("Omitted 1", sheet["limitations"][0])

    def test_rejects_archive_traversal_and_malformed_archives(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "corpus"
            source.mkdir()
            unsafe = source / "unsafe.docx"
            write_zip(unsafe, {"../escape.xml": "bad", "word/document.xml": "<document/>"})
            with self.assertRaisesRegex(ValueError, "Unsafe archive path"):
                SOURCE_CORPUS.extract_office(unsafe, base / "unsafe-output", 100)

            malformed = source / "malformed.docx"
            malformed.write_bytes(b"not a zip")
            with self.assertRaisesRegex(ValueError, "Unreadable OOXML archive"):
                SOURCE_CORPUS.extract_office(malformed, base / "malformed-output", 100)

    def test_rejects_archive_entries_over_the_expansion_limit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "large.docx"
            write_zip(path, {"word/document.xml": "x" * 100})
            original_limit = SOURCE_CORPUS.MAX_ENTRY_BYTES
            SOURCE_CORPUS.MAX_ENTRY_BYTES = 50
            try:
                with self.assertRaisesRegex(ValueError, "exceeds size limit"):
                    SOURCE_CORPUS.safe_archive(path)
            finally:
                SOURCE_CORPUS.MAX_ENTRY_BYTES = original_limit

    def test_requires_temporary_output_outside_source_folder(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            source = base / "corpus"
            source.mkdir()
            path = source / "brief.docx"
            write_zip(path, {"word/document.xml": "<document/>"})
            with self.assertRaisesRegex(ValueError, "outside the source folder"):
                SOURCE_CORPUS.extract_office(path, source / "output", 100)


if __name__ == "__main__":
    unittest.main()
