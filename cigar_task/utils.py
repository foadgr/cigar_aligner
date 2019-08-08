#!/usr/bin/env python

import re

class Utils(object):
    """
    Class object for CIGAR string parsing utilities

    Parameters
    ----------
    cigar_str : str, string-like object. Any valid string is acceptable,
        however should adhere to CIGAR representation of SAM-formatted 
        alignment.
    direction : str, string-like object. Specifies strand directionality.
        Valid arguments: 'F', 'R'     
    start_site : int, integer. None-type or valid integer is acceptable.
        Specifies the transcript start site to the reference strand.
        If no argument is not passed, the `start_site` class variable 
        will be assigned to default value = 0.
    """

    def __init__(self, cigar_str, direction, start_site=None):
        self.cigar_str = cigar_str
        try:
            if direction not in ('F', 'R'):
                raise ValueError(
                    "Valid args for direction: 'F' or 'R'"
                    )
            self.direction = direction
            
            if start_site is None:
                self.start_site = [(0, 'S')] # S-padding for cigar
            
            else:
                self.start_site = [(start_site, 'S')]

        except ValueError as err:
            print(err.args[0])

    def _groups(self):
        """
        Convert CIGAR-formatted regex elements from 
        string to list of tuples. Establish strand orientation
        """
        pattern = r'(\d+)([MID]{1})'
        pmatch = re.findall(pattern, self.cigar_str)
        cigar = [(int(i[0]), str(i[1])) for i in pmatch]


        if self.direction in ('forward', 'F'):
            return cigar 
        if self.direction in ('reverse', 'R'):
            return cigar[::-1]

    def index(self, itype):
        """
        Convert to list of ranges from parsed index

        Parameters
        ----------
        itype : str, string-like object. Specifies strand type.
            Valid arguments: 'read', 'reference' 
        """
        try:
            if itype not in ('read', 'reference'):
                raise ValueError(
                    "Valid args for itype: 'read' or 'reference'"
                    )
        except ValueError as err:
            print(err.args[0])

        cigar =  self.start_site + self._groups()
        if itype=='reference':
            ops = ('M', 'D', 'S') # Reference consuming operations
        if itype=='read':
            ops = ('M', 'I') # Read consuming operations

        return [i[0] if i[1] in ops else 0 for i in cigar]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
