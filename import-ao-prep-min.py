from aspaceimportsheet import importSheet

ao_prep_min = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRFvA4jWq-UvVlbFirELjLF3D3UHBhnPSJSFmb7emqW1pHxDS9lY21LXsulpYkuELmvsprfE39ShrtT/pub?gid=376449136&single=true&output=csv"

importSheet(ao_prep_min, '/repositories/2/archival_objects', 'as-json-templates/archival-object.yaml', linestoskip=6)
