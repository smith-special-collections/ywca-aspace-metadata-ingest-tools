from aspy import aspy
from googlecsv import googlecsv
from sheetprocessor import SheetProcessor
import jsonfieldmapper as jfm
import uuid
import logging
import pprint

corperateAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=0&single=true&output=csv"
personalAgentsCsvUrl = "https://docs.google.com/spreadsheets/d/e/2PACX-1vTKwOr2NFr0HNz1gnNhRWNUxttux0Awk6Qa-reGRLLhda7cAM2wl8qVEzUkrmfWIda16c5T80FLA7rQ/pub?gid=330234295&single=true&output=csv"


logging.basicConfig(format='%(levelname)s|%(asctime)s|%(message)s', level=logging.INFO, filename='import-agents-1.log')
logging.getLogger("requests").setLevel(logging.WARNING) # Suppress oververbosity of requests logging
logging.getLogger("urllib3").setLevel(logging.WARNING) # Same for urllib3 used by requests


# Connect to ArchivesSpace
aspace = aspy.ArchivesSpace('http', 'localhost', '8089', 'tchambers', 'sctchambers')
aspace.connect()

def asImportRecord(row, path='', mapping={}):
    jfm.setSourceRecord(row['data']) # make the mappings pull from the input row
    try:
        response = aspace.requestPost(path, requestData=mapping)
        logging.info('Imported record |%s| with data |%s| with response |%s| creating new location|%s' % (row['id'], mapping, response, response['uri']))
#        import pdb; pdb.set_trace()
    except Exception as e:
        logging.error('Failed record ' + str(row['id']) + ': ' + pprint.pformat(mapping))
        raise e

class SortName(jfm.JsonMappingObject):
    def renderValue(self):
        if jfm.JsonMappingObject.sourceRecord is not None:
            sortName = ''
            for myColumnName in self.value:
                sortName = sortName + jfm.JsonMappingObject.sourceRecord[myColumnName] + '. '
            return(sortName)
        else:
            return('')

def importSheet(sheetUrl, path, mapping):
    # Open the Google sheet csv
    reader = googlecsv.getCsv(sheetUrl)
    # Initialize the sheet processor
    sheet = SheetProcessor(reader, uniquecolumns=['id', 'batch id'], idcolumn='batch id')
    # Apply the json mapping
    aspace.setJsonSerializerDefault(jfm.customJsonSerial)
    # Process the records
    sheet.process(asImportRecord, path=path, mapping=mapping)

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

#importSheet(corperateAgentsCsvUrl, '/agents/corporate_entities', myCorperateAgent)
importSheet(personalAgentsCsvUrl, '/agents/people', myPersonAgent)
