#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# CREATED:2015-02-04 14:22:10 by Brian McFee <brian.mcfee@nyu.edu>
'''Utility transformers'''

from ..base import BaseTransformer

__all__ = ['Bypass']


class Bypass(BaseTransformer):
    r'''Bypass transformer.  Wraps an existing transformer object.

    This allows pipeline stages to become optional.

    The first example generated by a Bypass's transform method is the input,
    followed by all examples generated by the contained transformer object.

    Attributes
    ----------
    transformer : muda.BaseTransformer
        The transformer object to bypass

    Examples
    --------
    >>> # Generate examples with and without a pitch-shift
    >>> D = muda.deformers.Pitchshift(n_semitones=2.0)
    >>> B = muda.deformers.Bypass(transformer=D)
    >>> out_jams = list(B.transform(input_jam))
    '''

    def __init__(self, transformer=None):
        if not isinstance(transformer, BaseTransformer):
            raise TypeError('transformer must be a BaseTransformer object')

        BaseTransformer.__init__(self)

        self.transformer = transformer

    def transform(self, jam):
        '''Bypass transformations.

        Parameters
        ----------
        jam : pyjams.JAMS
            A muda-enabled JAMS object

        Generates
        ---------
        jam_out : pyjams.JAMS iterator
            The first result is `jam` (unmodified), by reference
            All subsequent results are generated by `transformer`
        '''
        # Step 1: yield the unmodified jam
        yield jam

        # Step 2: yield from the transformer
        for jam_out in self.transformer.transform(jam):
            yield jam_out
