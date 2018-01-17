import pdb
import itertools
import logging

class SheetProcessor:
    """Routines for processing a sheet and doing something with
    the rows.
    
    On instantiation excepts a CSV object or any itteratable object. To use
    run the process() method, while passing a callback function and a set of
    keyword arguments.
    
    The callback function must accept a "row" which is the unit of data, and
    keyword arguments (aka **kwargs).

    Example callback function:
    
    >>> def myCallbackFunction(row, myPrefix=''):
    ...     print("%i %s %i: %s" % (row['number'], myPrefix, row['data']['id'], row['data']['name']))
    ...     # anything else you want to do...
    ... 
    >>>

    Run the processor:
    
    >>> from sheetprocessor import SheetProcessor
    >>> 
    >>> myFakeSheet = [
    ...     {'id': 8, 'name': 'Those that belong to the emperor.'},
    ...     {'id': 1, 'name': 'Embalmed ones.'},
    ...     {'id': 3, 'name': 'Those that are trained.'},
    ...     {'id': 4, 'name': 'Suckling pigs.'},
    ...     {'id': 11, 'name': 'Mermaids (or Sirens)'},
    ...     {'id': 6, 'name': 'Fabulous ones.'},
    ...     {'id': 7, 'name': 'Stray dogs.'},
    ...     {'id': 2, 'name': 'Those that are included in this classification.'},
    ...     {'id': 9, 'name': 'Those that tremble as if they were mad'},
    ...     {'id': 10, 'name': 'Innumerable ones'},
    ...     {'id': 5, 'name': 'Those drawn with a very fine camel hair brush'},
    ...     {'id': 1, 'name': 'Et cetera'},
    ...     {'id': 13 , 'name': 'Those that have just broken the flower vase'},
    ...     {'id': 14 , 'name': 'Those that, at a distance, resemble flies'},
    ... ]
    >>> 
    
    Instantiate the sheet processor, passing the sheet, which can be any
    itteratable object.
    
    >>> sheet = SheetProcessor(myFakeSheet)
    
    Run the processor, passing the callback function and keyword arguments:
    
    >>> sheet.process(myCallbackFunction, myPrefix='Classification')
    1 Classification 8: Those that belong to the emperor.
    2 Classification 1: Embalmed ones.
    3 Classification 3: Those that are trained.
    4 Classification 4: Suckling pigs.
    5 Classification 11: Mermaids (or Sirens)
    6 Classification 6: Fabulous ones.
    7 Classification 7: Stray dogs.
    8 Classification 2: Those that are included in this classification.
    9 Classification 9: Those that tremble as if they were mad
    10 Classification 10: Innumerable ones
    11 Classification 5: Those drawn with a very fine camel hair brush
    12 Classification 1: Et cetera
    13 Classification 13: Those that have just broken the flower vase
    14 Classification 14: Those that, at a distance, resemble flies
    >>> 

    """
    # Custom Error classes
    class NonUnique(Exception):
        pass

    def __init__(self, reader, uniquecolumns=[], idcolumn=''):
        self.reader = reader
        self.uniqueColumns = uniquecolumns
        self.idColumn = idcolumn
        
        self.debugMode = False
        self.linesToSkip = 0
        self.__rowNumber = 0
        self.__errorCount = 0
        self.__successCount = 0
        self.__failedRecords = []
        self.__currentRecord = {}

    def incrementRowNumber(self):
        self.__rowNumber = self.__rowNumber + 1

    def getRowNumber(self):
        return self.__rowNumber

    def incrementErrorCount(self):
        self.__errorCount = self.__errorCount + 1

    def getErrorCount(self):
        return self.__errorCount

    def incrementSuccessCount(self):
        self.__successCount = self.__successCount + 1

    def getSuccessCount(self):
        return self.__successCount

    def getFailedRecords(self):
        return self.__failedRecords
    
    def addFailedRecord(self):
        self.__failedRecords.append(self.getCurrentRecordId())

    def getCurrentRecordId(self):
        return self.__currentRecord[self.idColumn]

    def isColumnUnique(self, columnName):
        """Sanity check, are all the elements in this column in this sheet unique?"""
        columnValues = [] # start a running list of values

        # make a separate copy of the reader so that we don't exhaust it
        # before the main processor get's a change to process it.
        copy1, copy2 = itertools.tee(self.reader)
        self.reader = copy1

        for row in list(copy2):
            value = row[columnName]
            if len(value) > 0: # if there's stuff in here then add it to the list
                columnValues.append(value)
        uniqueValues = set(columnValues)
        if len(columnValues) > len(uniqueValues):
            for uniqueValue in uniqueValues:
                columnValues.remove(uniqueValue)
            logging.error("Column %s contains duplicate values: %s" % (columnName, str(columnValues)))
            raise self.NonUnique

    def process(self, callback, **kwargs):
        """Iterate through the rows and run a callback function against them"""
        # Sanity checks
        ## Does the unique column in this sheet have any dupes?
        for uniqueColumn in self.uniqueColumns:
            self.isColumnUnique(uniqueColumn)
        self.__rowNumber = 0
        for rowData in self.reader:
            self.__currentRecord = rowData
            self.incrementRowNumber()
            # Skip the first few lines if set
            if self.getRowNumber() < self.linesToSkip:
                continue
            # Build the row data structure to be passed to the callback function
            row = {"number": self.getRowNumber(), "id": self.getCurrentRecordId(), "data": rowData}
            # Run the callback function
            try:
                callback(row, **kwargs)
            except KeyboardInterrupt:
                raise
            except Exception as e:
                self.incrementErrorCount()
                self.addFailedRecord()
                logging.error('Failed record %s: %s' % (row['id'], str(e)))
                if self.debugMode is True:
                    raise
            else:
                # if all goes well increment the successCount
                self.incrementSuccessCount()

        logging.info('Processed %i records.' % self.getRowNumber())
        logging.info('%i successfully processed records.' % self.getSuccessCount())
        logging.info('%i failed records:' % self.getErrorCount())
        logging.info(str(self.getFailedRecords()))

# Code for running doctests
# To run tests, type python3 sheetprocessor.py
if __name__ == "__main__":
    import doctest
    print("Running tests...")
    
    doctest.testmod(optionflags=doctest.ELLIPSIS, verbose=True)
