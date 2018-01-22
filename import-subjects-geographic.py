from aspaceimportsheet import importSheet

geographicSubectsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=1350156799&single=true&output=csv&"
importSheet(geographicSubectsCsvUrl, '/subjects', 'as-json-templates/subject.yaml')
