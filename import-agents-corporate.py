from aspaceimportsheet import importSheet

corporateAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=0&single=true&output=csv"
importSheet(corporateAgentsCsvUrl, '/agents/corporate_entities', 'as-json-templates/agent_corporate.yaml')
