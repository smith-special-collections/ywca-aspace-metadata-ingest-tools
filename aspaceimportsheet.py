from archivesspace import archivesspace
from googlecsv import googlecsv
from sheetprocessor import SheetProcessor
import uuid
import logging
import pprint

import jinja2
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import pprint
import json

DRY_RUN = False
DEBUG_MODE = False

# Set up logging
import datetime
logfileName = 'logs/aspace-import-%s.log' % datetime.datetime.now().isoformat()
#, filename=logfileName
logging.basicConfig(format='%(levelname)s|%(asctime)s|%(message)s', level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING) # Suppress oververbosity of requests logging
logging.getLogger("urllib3").setLevel(logging.WARNING) # Same for urllib3 used by requests

# Set up jinja loader and template objects
templateLoader = jinja2.FileSystemLoader( searchpath="." )
templateEnv = jinja2.Environment( loader=templateLoader )

# Connect to ArchivesSpace
if DRY_RUN is not True:
    aspace = archivesspace.ArchivesSpace('http', 'localhost', '8089', 'tchambers', 'sctchambers')
    aspace.connect()
else:
    logging.error('DRY RUN')

def asImportRecord(row, apiPath='', mapping=''):
    """This is the callback function to be run by the sheet processor on each row."""
    # load the jinja template
    template = templateEnv.get_template( mapping )
    # run the templater, merging the data into the template
    merged_data_yaml = template.render( row['data'] )
    # convert the yaml format data into real python data
    asRecordDataStruct = load(merged_data_yaml, Loader=Loader)
    try:
        # The actual request to ASpace
        if DRY_RUN is not True:
            response = aspace.requestPost(apiPath, requestData=asRecordDataStruct)
            logging.info('Imported record |%s| with data |%s| with response |%s| creating new location|%s' % (row['id'], asRecordDataStruct, response, response['uri']))
        else:
            logging.error('DRY RUN not querying %s with data: %s' % (apiPath, asRecordDataStruct))
            pass
    except Exception as e:
        # If something goes wrong log it
        #logging.error('Failed record ' + str(row['id']) + ': ' + pprint.pformat(asRecordDataStruct))
        raise e

def importSheet(sheetUrl, path, mapping, linestoskip=0, uniquecolumns=[]):
    # Open the Google sheet csv
    reader = googlecsv.getCsv(sheetUrl)
    # Initialize the sheet processor
    sheet = SheetProcessor(reader, uniquecolumns=uniquecolumns, idcolumn='batch_id')
    # Set debug mode on processor
    sheet.debugMode = DEBUG_MODE
    # Skip however may lines at the beginning of the sheet
    sheet.linesToSkip = linestoskip
    # Process the records
    sheet.process(asImportRecord, apiPath=path, mapping=mapping)
