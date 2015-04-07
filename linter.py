#
# linter.py
# Linter for SublimeLinter3, a code checking framework for Sublime Text 3
#
# Written by Bruno JJE
# Copyright (c) 2015 Bruno JJE
#
# License: MIT
#

"""This module exports the Nvc plugin class."""

from SublimeLinter.lint import Linter


class Nvc(Linter):

    """Provides an interface to nvc."""

    syntax = 'vhdl'
    cmd = 'nvc -a @'
    version_re = r'nvc (?P<version>\d+\.\d+)'
    version_requirement = '>= 0.1'
    multiline = True
    tempfile_suffix = 'vhd'

    # Here is a sample nvc error output:
    # ----8<------------
    # ** Error: unexpected identifier while parsing block declarative item, expecting
    #           one of signal, type, subtype, file, constant, function, impure,
    #           pure, procedure, alias, attribute, for, component, use or shared
    #     File filtre8.vhd, Line 36
    #       ignal en_division : std_logic;
    #       ^^^^^
    # ----8<------------

    regex = (
        r"^\*\* (?P<error>Error: )(?P<message>[^\^]*)"
        r"^\tFile (?P<path>.*), Line (?P<line>[0-9]+)\n"
        r"(?P<code>[^\n]+)\n"
        r"(?P<align>    )(?P<col>[^\^]+)(?P<near>[\^]+)"
    )

    def split_match(self, match):
        """
        Extract and return values from match.

        We override this method so that we can return an highlight that cover
        exactly what nvc has underlined, and deal with possible multiline
        error messages.

        NB: To highlight for a given length, we put a string with the required
            highlight length in the 'near' parameter.

        """

        match, line, col, error, warning, message, near = super().split_match(match)

        if match:
            # The error messages given by nvc can be very long,
            # thus we also print it in the console so the user
            # can see it in full extend if needed.
            print('\n' + message[:-1])
            print(match.group('code'))
            print(match.group('align') + " " * col + near)

            # The error message may contain line break and
            # alignment spaces, so we delete them for readability.
            message = '[nvc] ' + ' '.join(message.replace('\n', ' ').split())

        return match, line, col, error, warning, message, near
