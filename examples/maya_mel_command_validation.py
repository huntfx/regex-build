import os
import sys

sys.path.append(os.path.normpath(__file__).rsplit(os.path.sep, 2)[0])
from regex_build import RegexBuild


def validate_mel_command(command, flags, relaxed=True):
    """Build regex for a MEL command.

    Parameters:
        command (str): Name of the command.
        flags (dict): Command flags and their types.
            An example would be {'startFrame': int}
        relaxed (bool): If the checks should allow valid alternatives.
            For example, MEL allows ints to be used in float flags.

    >>> mel_regex('playbackOptions', dict(min=int, max=int, ps=float, q=None), relaxed=True)
    'playbackOptions([ ]*-(q[ ]*|(min|max|ps)[ ]*( |-|\.)(|[0-9]+|([0-9]+\.[0-9]+|\.[0-9]+|[0-9]+\.))))*[ ]*(|;?[ ]*)$'
    >>> mel_regex('playbackOptions', dict(min=int, max=int, ps=float, q=None), relaxed=False)
    'playbackOptions([ ]*-(q[ ]*|(min|max)[ ]*( |-|\.)(|[0-9]+)|ps[ ]*( |-|\.)(|[0-9]+\.[0-9]+)))*[ ]*(|;?[ ]*)$'
    """
    # Separate each flag into types
    empty_flags = []
    int_flags = []
    float_flags = []
    for flag, flag_type in flags.items():
        if flag_type is None:
            empty_flags.append(flag)
        elif flag_type == int:
            int_flags.append(flag)
        elif flag_type == float:
            float_flags.append(flag)
        else:
            raise NotImplementedError('unknown type {}'.format(flag_type.__name__))

    # Regex to match empty spaces
    spaces = RegexBuild('[ ]*')

    # What can be used to separate a flag from its value
    # This comes after any number of spaces
    separators = RegexBuild(' ', '-', r'\.')

    empty_match = ''
    int_match = '[0-9]+'
    with RegexBuild() as float_match:
        float_match(r'[0-9]+\.[0-9]+')
        if relaxed:
            float_match(r'\.[0-9]+')
            float_match(r'[0-9]+\.')

    # Match a valid end of line
    eol = RegexBuild(spaces)('', RegexBuild(';?')(spaces))('$')

    with RegexBuild(command, exit=eol) as regex:
        # Loop through each flag
        with regex('(', exit=')*') as repeat:
            with repeat(spaces)('-') as flags:
                if relaxed:
                    flags(*empty_flags)(spaces)(empty_match)
                    flags(*(int_flags + float_flags))(spaces)(separators)(empty_match, int_match, float_match)
                else:
                    flags(*empty_flags)(spaces)(empty_match)
                    flags(*int_flags)(spaces)(separators)(empty_match, int_match)
                    flags(*float_flags)(spaces)(separators)(empty_match, float_match)

    return str(regex)
