from aspaceimportsheet import importSheet, SortName
import jsonfieldmapper as jfm

corperateAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=0&single=true&output=csv"
personalAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=330234295&single=true&output=csv"

myCorperateAgent = {
    "jsonmodel_type":"agent_corporate_entity",
    'names': [{
        'jsonmodel_type': 'name_corporate_entity',
        'primary_name': jfm.Column('primary part of name'),
        'subordinate_name_1': jfm.Column('subordinate name 1'),
        'subordinate_name_2': jfm.Column('subordinate name 2'),
        'authority_id': jfm.Column('id'),
        'rules': jfm.Column('rules'),
        'source': jfm.Column('source'),
        'sort_name': SortName(['primary part of name', 'subordinate name 1', 'subordinate name 2']),
    }],
}

# https://archivesspace.github.io/archivesspace/api/#post-agents-people
# https://github.com/archivesspace/archivesspace/blob/master/common/schemas/agent_person.rb
myPersonAgent = {
    "jsonmodel_type":"agent_person",
    # https://github.com/archivesspace/archivesspace/blob/master/common/schemas/name_person.rb
    'names': [{
        'jsonmodel_type': 'name_person',
        'prefix': jfm.Column('prefix'),
        'primary_name': jfm.Column('primary part of name'),
        'rest_of_name': jfm.Column('rest of name'),
        'suffix': jfm.Column('suffix'),
        'authority_id': jfm.Column('id'),
        'dates': jfm.Column('dates'),
        'rules': jfm.Column('rules'),
        'source': jfm.Column('source'),
        'sort_name': SortName(['primary part of name', 'rest of name']),
        'name_order':'indirect' # Matching what's in the db already?
    }],
}

importSheet(corperateAgentsCsvUrl, '/agents/corporate_entities', myCorperateAgent)
#importSheet(personalAgentsCsvUrl, '/agents/people', myPersonAgent)
