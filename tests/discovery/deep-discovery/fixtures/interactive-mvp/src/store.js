const documents = new Map();

export async function createDocument(sourceUrl) {
  const document = { id: crypto.randomUUID(), sourceUrl, status: "queued" };
  documents.set(document.id, document);
  return document;
}

export async function getDocument(id) {
  return documents.get(id);
}

export async function listDocuments() {
  return [...documents.values()];
}

export async function saveExtraction(id, facts) {
  documents.set(id, { ...documents.get(id), status: "complete", facts });
}
