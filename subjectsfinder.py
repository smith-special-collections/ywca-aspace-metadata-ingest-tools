import pickle
import pprint

USECACHE = True
CACHE_FILENAME = 'subjects.cache'

class AsSubjectsFinder(object):
    """
    Get all subjects from ArchivesSpace and search them in memory, instead of via
    API search interface, which I could not get to search on authority_id.

    >>> from archivesspace import archivesspace
    >>> from subjectsfinder import AsSubjectsFinder
    >>> aspace = archivesspace.ArchivesSpace('http', 'localhost', '8089', 'tchambers', 'sctchambers')
    >>> aspace.connect()
    >>> finder = AsSubjectsFinder(aspace)
    Using cache file: subjects.cache
    >>> subject = finder.findSubjectByAuthority_id('sh85025042')
    >>> print(subject['title'])
    Christian education
    >>> print(subject['uri'])
    /subjects/...
    >>> 
    """
    def __init__(self, archivesspace):
        self.archivesspace = archivesspace
        self.allsubjects = self._getAllSubjectsCached()

    def _getAllSubjects(self):
        allsubjectS = self.archivesspace.pagedRequestGet('/subjects')
        with open(CACHE_FILENAME, 'wb') as f:
            # Pickle the 'data' dictionary using the highest protocol available.
            pickle.dump(allsubjectS, f, pickle.HIGHEST_PROTOCOL)
        return allsubjectS
    
    def _getAllSubjectsCached(self):
        if USECACHE is True:
            print("Using cache file: %s" % CACHE_FILENAME)
            try:
                with open(CACHE_FILENAME, 'rb') as f:
                    allsubjects = pickle.load(f)
            except FileNotFoundError:
                allsubjects = self._queryAllSubjects()
        else:
            allsubjects = self._queryAllSubjects()
        return allsubjects
    
    def findSubjectByAuthority_id(self, authority_id):
        for subject in self.allsubjects:
            try:
                if subject['authority_id'] == authority_id:
                    return subject
            except KeyError:
                pass
 
if __name__ == "__main__":
    import doctest
    print("Running tests...")
    
    doctest.testmod(optionflags=doctest.ELLIPSIS, verbose=True)
