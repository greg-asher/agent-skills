import { getDocument, saveExtraction } from "./store.js";

globalThis.processingQueue.consume(async ({ documentId }) => {
  const document = await getDocument(documentId);
  const extracted = await globalThis.documentExtractor.extract(document.sourceUrl);
  await saveExtraction(documentId, {
    carrier: extracted.carrier,
    shipmentNumber: extracted.shipmentNumber,
    deliveryDate: extracted.deliveryDate
  });
});

export async function createBillingEvent() {
  throw new Error("Unused experiment: billing integration was never connected");
}
