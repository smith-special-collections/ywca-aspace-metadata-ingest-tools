"""A system for mapping data in json datastructures.

Use jsonfieldmapper to map data from a source row to a json datastructure.

Example:

>>> import json
>>> import jsonfieldmapper as jfm
>>> 
>>> myTemplate = {
...     # The name of the column in the input data is passed to the Column
...     # instance
...     'primary_name': jfm.Column('myName'), 
...     'myconstant': 'foobar'
... }
>>> 

The Column instance resolves to a blank string because there's no input data

>>> myTemplate['myconstant']
'foobar'
>>> myTemplate['primary_name']
<BLANKLINE>
>>> 

Input data comes onto the scene

>>> fakeRow = {
...     'myName': 'Tristan Chambers'
... }
>>> 
>>> jfm.setSourceRecord(fakeRow)

Now all instances of the Column class resolves to the value addressed from
the input data

>>> myTemplate['myconstant']
'foobar'
>>> myTemplate['primary_name']
Tristan Chambers
>>> 

And they render correctly when we serialize with json.dumps
_if_ we pass the custom serializer for Column() included with this module.

>>> json.dumps(myTemplate, default=jfm.customJsonSerial, sort_keys=True)
'{"myconstant": "foobar", "primary_name": "Tristan Chambers"}'

"""
import logging

class JsonMappingObject():
    sourceRecord = None
    
    def __init__(self, value):
        self.value = value
    
    def renderValue(self):
        return self.value

    def getJsonOutput(self):
        return self.renderValue()

    def __repr__(self):
        return self.renderValue()

class Column(JsonMappingObject):
    """A mapping for columns from the input spreadsheet. Subclasses the native
    str object from Python so that json.dumps() (which is invoked by requests)
    is happy. Use monkey patching to pull in the current record.
    """
        
    def __init__(self, columnName):
        self.columnName = columnName

    def renderValue(self):
        if JsonMappingObject.sourceRecord is not None:
            return(str(JsonMappingObject.sourceRecord[self.columnName]))
        else:
            return('')

def setSourceRecord(sourceRecord):
    """Make all instances of Column magically aware of the current source
    record.
    """
    JsonMappingObject.sourceRecord = sourceRecord

def customJsonSerial(unknownObject):
    """This runs in JSON serializer if the object isn't known to json.dumps()"""
    # Is the object a JsonMappingObject?
    if isinstance(unknownObject, JsonMappingObject):
        # If so, then it's one of our json mapping objects
        myJsonMappingObject = unknownObject
        # And thus it will have a getJsonOutput method, so let's use it
        return(myJsonMappingObject.getJsonOutput())
    else:
        # Otherwise faithfully do what json.dumps() would do and raise an error
        raise TypeError ("Type %s not serializable" % type(unknownObject))

# Code for running doctests
# To run tests, type python3 jsonfieldmapper.py
if __name__ == "__main__":
    import doctest
    print("Running tests...")
    
    doctest.testmod(optionflags=doctest.ELLIPSIS, verbose=True)
