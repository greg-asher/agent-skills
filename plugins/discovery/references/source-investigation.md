# Source Investigation

Use this guide for any folder that contains material about an existing product, process, or system. The material may be source code, documents, designs, data, or a mixture.

## Classify the workspace

Classify from the evidence, not the folder name:

- **Software:** application-owned source or runnable operational automation explains an implemented system.
- **Document corpus:** documents, designs, images, or data describe a product or process, but no implemented application is present.
- **Mixed:** both implemented behavior and documentary intent are material.
- **Sparse:** the available material cannot support a useful product or system account.

Git history and runnable workflows strengthen software evidence. Neither is required. A source-code folder without `.git` is still software.

## Inventory before interpretation

Run the bundled source corpus tool when Python 3 is available:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/source-corpus.py" inventory \
  --root "<workspace>" \
  --output "<manifest-path>" \
  [--previous "<previous-manifest-path>"]
```

The tool hashes files, marks byte-identical duplicates, records changes from a previous manifest, and excludes common dependencies, temporary material, lock files, and generated Discovery outputs. Add explicit exclusions when the workspace has other generated areas.

Do not hide unreadable or partially reviewed files. Keep them in coverage with their review state and limitations. Do not copy source documents into the discovery package.

## Read each format deliberately

- Read Markdown, text, structured data, diagrams, and source files with the available native tools.
- Read PDFs and images natively. Inspect long PDFs in page ranges so important later pages are not skipped.
- Extract `.pptx`, `.docx`, and `.xlsx` with the bundled tool when Python 3 is available:

  ```bash
  extraction_dir="$(mktemp -d)"
  python3 "${CLAUDE_PLUGIN_ROOT}/scripts/source-corpus.py" extract \
    --input "<office-file>" \
    --output "${extraction_dir}"
  ```

  Read `content.json` and `content.md`, then remove the temporary directory after synthesis.
- If LibreOffice or another installed renderer is available, render Office material and inspect the visual result. Do not install a renderer. Without one, use the extracted structure and media references, and record that layout-dependent meaning was not fully inspected.
- If Python 3 is unavailable, continue with readable sources and mark Office files inaccessible.

The extractor rejects unsafe archive paths and bounded-expansion limits. Treat an extraction error as a coverage limitation, not permission to omit the file.

## Divide source work by question

Use source investigators for bounded groups that can be reconciled later. Useful groups include:

- product narrative and prior proposals
- user research and current process
- data, systems, and dependencies
- business model and operating responsibility
- design concepts and prototypes

Each assignment must name the group, relevant files, the investigation question, and the expected return shape. Avoid assigning the whole corpus to one investigator.

Every investigator returns:

- reviewed sources and precise locations
- material claims and their support
- actors and workflows
- decisions and their state
- conflicts within or across sources
- material gaps
- review limitations

## Reconcile the evidence

Build one shared vocabulary before synthesis. Treat newer material as more current only when the source establishes that relationship. Do not silently resolve conflicting documents, or privilege documentation over implementation in a mixed workspace.

Classify decisions as:

- **settled**
- **proposed**
- **superseded**
- **unclear**

Classify document claims as:

- **source-stated:** one source says it
- **corroborated:** independent sources agree
- **participant-confirmed:** a participant confirmed it in the current discovery
- **inferred:** analysis connects the evidence
- **unknown:** the evidence does not establish it

Keep software evidence statuses from Deep Discovery. In a mixed workspace, describe documentary intent and implemented behavior separately before explaining the gap.

## Build the source model

Write the model against `${CLAUDE_PLUGIN_ROOT}/assets/source-model.schema.json`. Include the subject, corpus type, coverage, actors, workflows, business rules, operating context, product, data, system, and design concepts, decisions, claims, conflicts, gaps, and unresolved questions.

Every material claim, decision, workflow, conflict, or concept should point to a source reference with a relative file path plus the most precise available locator: page, slide, sheet and cell range, section, code location, or image.

In Deep Discovery, publish the model with the durable package. In Start Discovery, keep the model under `.discovery/<product>/` as working state.
