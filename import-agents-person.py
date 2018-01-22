from aspaceimportsheet import importSheet

personAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=330234295&single=true&output=csv"
importSheet(personAgentsCsvUrl, '/agents/people', 'as-json-templates/agent_person.yaml')
