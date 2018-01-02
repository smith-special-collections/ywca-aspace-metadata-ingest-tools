from aspaceimportsheet import importSheet, SortName
import jsonfieldmapper

corperateAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=0&single=true&output=csv"
personalAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=330234295&single=true&output=csv"

class SheetColumn(jsonfieldmapper.Column):
    pass

myCorperateAgent = {
    "jsonmodel_type":"agent_corporate_entity",
    'names': [{
        'jsonmodel_type': 'name_corporate_entity',
        'primary_name': SheetColumn('primary part of name'),
        'subordinate_name_1': SheetColumn('subordinate name 1'),
        'subordinate_name_2': SheetColumn('subordinate name 2'),
        'authority_id': SheetColumn('id'),
        'rules': SheetColumn('rules'),
        'source': SheetColumn('source'),
#        'sort_name': SortName(['primary part of name', 'subordinate name 1', 'subordinate name 2']),
    }],
}

# https://archivesspace.github.io/archivesspace/api/#post-agents-people
# https://github.com/archivesspace/archivesspace/blob/master/common/schemas/agent_person.rb
myPersonAgent = {
    "jsonmodel_type":"agent_person",
    # https://github.com/archivesspace/archivesspace/blob/master/common/schemas/name_person.rb
    'names': [{
        'jsonmodel_type': 'name_person',
        'prefix': SheetColumn('prefix'),
        'primary_name': SheetColumn('primary part of name'),
        'rest_of_name': SheetColumn('rest of name'),
        'suffix': SheetColumn('suffix'),
        'authority_id': SheetColumn('id'),
        'dates': SheetColumn('dates'),
        'rules': SheetColumn('rules'),
        'source': SheetColumn('source'),
#        'sort_name': SortName(['primary part of name', 'rest of name']),
        'name_order':'indirect' # Matching what's in the db already?
    }],
}

# Run the magic sauce to make the mappings pull from the input row from the csv
SheetColumn.setSourceRecord(row['data'])

#importSheet(corperateAgentsCsvUrl, '/agents/corporate_entities', myCorperateAgent)
importSheet(personalAgentsCsvUrl, '/agents/people', myPersonAgent)
