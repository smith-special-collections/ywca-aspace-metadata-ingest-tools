from aspy import aspy
from googlecsv import googlecsv
from sheetprocessor import SheetProcessor
import jsonfieldmapper as jfm
import uuid
import logging
import pprint

# Set up logging
import datetime
logfileName = 'logs/aspace-import-%s.log' % datetime.datetime.now().isoformat()
logging.basicConfig(format='%(levelname)s|%(asctime)s|%(message)s', level=logging.INFO, filename=logfileName)
logging.getLogger("requests").setLevel(logging.WARNING) # Suppress oververbosity of requests logging
logging.getLogger("urllib3").setLevel(logging.WARNING) # Same for urllib3 used by requests

# Connect to ArchivesSpace
aspace = aspy.ArchivesSpace('http', 'localhost', '8089', 'tchambers', 'sctchambers')
aspace.connect()

def asImportRecord(row, path='', mapping={}):
    """This is the callback function to be run by the sheet processor on each row."""
    # Run the magic sauce to make the mappings pull from the input row from the csv
    jfm.setSourceRecord(row['data'])
    try:
        # The actual request to ASpace
        response = aspace.requestPost(path, requestData=mapping)
        logging.info('Imported record |%s| with data |%s| with response |%s| creating new location|%s' % (row['id'], mapping, response, response['uri']))
    except Exception as e:
        # If something goes wrong log it
        logging.error('Failed record ' + str(row['id']) + ': ' + pprint.pformat(mapping))
        raise e

class SortName(jfm.JsonMappingObject):
    """Create custom mapping for a sortname field. Takes an array of csv sheet field names."""
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
