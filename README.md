This folder contains scripts for ingesting into ArchivesSpace the archival
description of the YWCA materials digitized for the YWCA CLIR grant project.

ASpace Ingest project folder
https://drive.google.com/drive/folders/0B1RB5tYLN3WecjI3MHgxWHNPbEU

# Ingestion workflow
Agents and subjects must be ingested first, then Archival Object records. This
is because the Archival Object records link to the Agents and Subjects.

Steps:

1. Agents and Subjects
2. Archival Objects

# Source data
The adjoining scripts draw directly from the Google sheets containing the
metadata.

## Archival Object records
YWCA microfilm archival object mapping and metadata
https://docs.google.com/spreadsheets/d/1L-AB2rEeni0r2YC_PqdBr90bvScXXFA_DFBJJyX4L3M/edit#gid=376449136

## Subjects and Agent records
YWCA microfilm subjects and agents
https://docs.google.com/spreadsheets/d/1LKNioJOt279PpMGdRGWSErvwWSt9GadV4ejcK_rFK3o/edit#gid=0

# Usage
## Dependencies
This code relies on the ArchivesSpace Python module also authored by yours truly.

# Appendices
## Quick reference
ASpace API documentation
https://archivesspace.github.io/archivesspace/api/#archivesspace-rest-api

ASpace object model schema documentation
https://github.com/archivesspace/archivesspace/tree/master/common/schemas
