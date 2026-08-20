import express from "express";
import { createDocument, getDocument, listDocuments } from "./store.js";

const app = express();
app.use(express.json());

app.post("/documents", async (request, response) => {
  const document = await createDocument(request.body.sourceUrl);
  await globalThis.processingQueue.publish({ documentId: document.id });
  response.status(202).json(document);
});

app.get("/documents/:id", async (request, response) => {
  response.json(await getDocument(request.params.id));
});

app.get("/documents", async (_request, response) => {
  response.json(await listDocuments());
});

app.get("/exports.csv", async (_request, response) => {
  response.status(501).json({ error: "Export formatting is not implemented" });
});

app.listen(process.env.PORT || 3000);
