__author__ = 'liux4@onid.oregonstate.edu'

from array import *


MODULUS = 2147483647  # DON'T CHANGE THIS VALUE
MULTIPLIER = 48271  # DON'T CHANGE THIS VALUE
CHECK = 399268537  # DON'T CHANGE THIS VALUE
STREAMS = 256  # of streams, DON'T CHANGE THIS VALUE
A256 = 22925  # jump multiplier, DON'T CHANGE THIS VALUE
DEFAULT = 123456789  # initial seed, use 0 < DEFAULT < MODULUS

seed = array('l', [DEFAULT])  # current state of each stream
stream = 0  # stream index, 0 is the default
initialized = 0  # test for stream initialization


def selectStream(index):
    """
    Use this function to set the current random number generator stream --
    that stream from which the next random number will come.
    """

    global stream
    stream = index % STREAMS

    if initialized == 0 and stream != 0:  # protect against
        plantSeeds(DEFAULT)  # un-initialized streams


def plantSeeds(x):
    """
    Use this function to set the state of all the random number generator
    streams by "planting" a sequence of states (seeds), one per stream,
    with all states dictated by the state of the default stream.
    The sequence of planted states is separated one from the next by
    8,367,782 calls to Random().
    """
    Q = MODULUS / A256
    R = MODULUS % A256

    global initialized
    initialized = 1

    global stream
    s = stream  # remember the current stream
    selectStream(0)  # change to stream 0
    putSeed(x)  # set seed[0]
    stream = s  # reset the current stream

    for j in range(STREAMS):

        global seed
        x = A256 * (seed[j - 1] % Q) - R * (seed[j - 1] / Q)

        if x > 0:
            seed[j] = x
        else:
            seed[j] = x + MODULUS


def putSeed(randomSeed):
    """
    Use this function to set the state of the current random number
    generator stream according to the following conventions:
    if x > 0 then x is the state (unless too large)
    if x <= 0 then the state is to be supplied interactively

    :param randomSeed:
    :return:
    """

    if randomSeed > 0:
        randomSeed %= MODULUS  # correct if x is too large

    if randomSeed <= 0:
        while False:
            userinput = input('\nEnter a positive integer seed (9 digits or less) >> ')
            randomSeed = long(userinput)

            if randomSeed < 1 or randomSeed > MODULUS:
                print "\nInput out of range ... try again\n"
            else:
                break

    global seed
    seed[stream] = randomSeed