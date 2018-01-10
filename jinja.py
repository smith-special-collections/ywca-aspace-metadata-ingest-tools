from aspaceimportsheet import importSheet

topicalSubectsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=1295352806&single=true&output=csv"

importSheet(topicalSubectsCsvUrl, '/subjects', 'as-json-templates/subject-topical.yaml')
