# Missing runtime boundary

The proposed change extracts an in-process worker into a separate package. The saved workspace model covers source imports and local tests but lists the production scheduler, deployed process topology, and environment ownership as unknown. No current deployment configuration is available in the workspace.
