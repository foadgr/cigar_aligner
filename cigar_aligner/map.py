#!/usr/bin/env python

from utils import Utils


class Map(Utils):
  """
  Class object for CIGAR element alignment. Includes the efficient array
  implementation of prefix sums fast calculation. Also provides other element
  manipulation methods, such as strand inversion and mapping of coordinate
  ranges.

  Parameters
  ----------
  All arguments from the Utils class object are inherited.

  cigar_str : str, string-like object. Any valid string is acceptable,
    however should adhere to CIGAR representation of SAM-formatted
    alignment.
  direction : str, string-like object. Specifies strand directionality.
    Valid arguments: 'F', 'R'
  start_site : int, integer. None-type or valid integer is acceptable.
    Specifies the transcript start site to the reference strand.
    If no argument is not passed, the `start_site` class variable
    will be assigned to default value = 0.
  inverted : bool, boolean type object. To invert the read-reference pair,
    any 'True' type is acceptable. 'False' to maintain the non-inverted
    strand pair.
  """
  def __init__(self, cigar_str, direction, start_site, inverted):
    super().__init__(cigar_str, direction, start_site)
    self.inverted = inverted

  @classmethod
  def prefix_sums(self, A):
    """
    Allows for the fast calculation O(n) of sums of contiguous elements
    in the passed array A.

    Parameters
    ----------
    A : 1-D array object. Any valid array of integers is acceptable. For
      the purpose of this exercise, the integer values represent the
      digit element from each CIGAR grouping (i.e. 11 from '11M').
    """
    n = len(A)
    P = [0] * (n+1)
    for k in range(1,n+1):
      P[k]=P[k-1]+A[k-1]
    return P

  def _paired_strands(self):
    """
    Instantiates the Utils().index() method to decode the read and
      reference indices from a provided CIGAR string. Converts to a tuple
      of the two strand lists. If 'inverted', swap tuple positions.
    """
    read = self.index('read')
    ref = self.index('reference')
    P = (self.prefix_sums(read), self.prefix_sums(ref))
    if self.inverted:
      return P
    if not self.inverted:
      return P[::-1]

  def align(self, query):
    """
    This is a strand alignment solution. Generality is built-in to infer
    if strands are inverted or reversed.

    Parameters
    ----------
    query : int, integer. Any valid integer less than or equal to the
      maximum length of the template strand is acceptable. The query and
      result represent coordinates for both coordinates in strand pair.
    """
    pairs = self._paired_strands(x)

    for i in range(1, len(pairs[0])):
      """
      A weakness of this alignment method is how the below conditional
      statement handles inclusion of the 0th-index between summed array
      pairs if the read and reference strands are parsed as a reversed
      cigar. Note, `map_condition` > `query` in a forward cigar and this
      changes to `map_condition` >= `query` in a reversed cigar. Moreover,
      the condition does not change for an inverted alignment. Additional
      testing is required here.
      """
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
    """
    This is a range mapping solution. A range slice is passed in order to
    output an ordered list of coordinate tuples.

    Parameters
    ----------
    start : int, integer. Any valid integer less than or equal to the
      maximum length of the template strand is acceptable.
    end : int, integer. Any valid integer greater than the slice start and
      less than or equal to the maximum length of the template strand
      is acceptable.
    """
    max_length = max(self._paired_strands()[1])

    if start is None:
      start = 0
    if end is None:
      end = max_length
    else:
      end = end+1
    align_range = range(start, end+1)
    return [(q, self.align(q)) for q in align_range if q <= max_length]

if __name__ == "__main__":
  import doctest
  doctest.testmod()
