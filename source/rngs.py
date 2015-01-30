__author__ = 'liux4@onid.oregonstate.edu'

MODULUS = 2147483647  # DON'T CHANGE THIS VALUE
MULTIPLIER = 48271  # DON'T CHANGE THIS VALUE
CHECK = 399268537  # DON'T CHANGE THIS VALUE
STREAMS = 256  # of streams, DON'T CHANGE THIS VALUE
A256 = 22925  # jump multiplier, DON'T CHANGE THIS VALUE
DEFAULT = 123456789  # initial seed, use 0 < DEFAULT < MODULUS

seed[STREAMS] = {DEFAULT}  # current state of each stream
stream = 0  # stream index, 0 is the default
initialized = 0  # test for stream initialization


def selectStream(index):
    """
    Use this function to set the current random number generator stream --
    that stream from which the next random number will come.
    """
    stream = index % STREAMS

    if initialized == 0 and stream != 0:  # protect against
        PlantSeeds(DEFAULT)  # un-initialized streams


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

    initialized = 1
    s = stream  # remember the current stream
    SelectStream(0)  # change to stream 0
    PutSeed(x)  # set seed[0]
    stream = s  # reset the current stream
    for j in range(STREAMS):
        x = A256 * (seed[j - 1] % Q) - R * (seed[j - 1] / Q)
        if x > 0:
            seed[j] = x
        else:
            seed[j] = x + MODULUS


def putSeed(x):

    if x > 0:
        x %= MODULUS  # correct if x is too large

    if x <= 0:
        while False:
            userinput = input('\nEnter a positive integer seed (9 digits or less) >> ')
            x = long(userinput)

            if x < 1 or x > MODULUS:
                print "\nInput out of range ... try again\n"
            else:
                break

    seed[stream] = x