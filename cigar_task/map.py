#!/usr/bin/env python

from utils import Utils


class Map(Utils):
    def __init__(self, cigar_str, direction, start_site, inverted):
        super().__init__(cigar_str, direction, start_site)
        self.inverted = inverted

    def _prefix_sums(self, A):
        n = len(A)
        P = [0] * (n+1)
        for k in range(1,n+1):
            P[k]=P[k-1]+A[k-1]
        return P

    def paired_strands(self):
        read = self.index('read')
        ref = self.index('reference')
        P = (self._prefix_sums(read), self._prefix_sums(ref))
        if self.inverted:
            return P
        if not self.inverted:
            return P[::-1]

    def align(self, query):
        pairs = self.paired_strands()
        for i in range(1, len(pairs[0])):
            if not self.inverted and self.direction=='F':
                map_condition = pairs[1][i] > query

            if not self.inverted and self.direction=='R':
                map_condition = pairs[1][i] >= query
            if self.inverted:
                map_condition = pairs[1][i] >= query
            
            if map_condition:
                if pairs[0][i] > 0 and pairs[0][i] == pairs[0][i-1]:
                    return None
                else:
                    diff = pairs[0][i] - pairs[1][i]
                    result = diff + query
                    if result < 0:
                        return None
                    else:
                        return result

    def map_ranger(self, start=None, end=None):
        if start is None:
            start = 0
        if end is None:
            end = max(self.paired_strands()[1])
        align_range = range(start, end)
        return [(q, self.align(q)) for q in align_range]



