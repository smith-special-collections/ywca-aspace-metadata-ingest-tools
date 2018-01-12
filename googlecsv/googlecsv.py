import requests
import csv
from io import StringIO

def getCsv(csvUrl):
    """Take a url of a CSV file published on Google Sheets and return a DictReader object:
    reader = googlecsv.getCsv("https://docs.google.com/spreadsheets/d/e/IDCODEHERE/pub?gid=99999999&single=true&output=csv")
    reader.fieldnames
    ['term 1', 'term type', 'subdivision 1', 'subdivision 2 term type', 'subdivision 2', 'subdivision 2 term type', 'subdivision 3', 'subdivision 3 term type', 'source', 'authority id']
    
    for row in reader:
        print(row)
    
    More about Python csv DictReader object: https://docs.python.org/3/library/csv.html#csv.DictReader
    """
    request = requests.get(csvUrl, stream=True, headers={'Cache-Control': 'no-cache'})
    # make requests read the response as utf-8 (which it is of course!)
    request.encoding = 'utf-8'
    # convert the text into a file stream thing that DictReader likes
    fakefile = StringIO(request.text)

    data = csv.DictReader(fakefile)
    return data
