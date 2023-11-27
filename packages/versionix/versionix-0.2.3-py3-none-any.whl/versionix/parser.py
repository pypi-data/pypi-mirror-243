#
#  This file is part of Versionix software
#
#  Copyright (c) 2023 - Sequana Dev Team (https://sequana.readthedocs.io)
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  Website:       https://github.com/sequana/versionix
#  Contributors:  https://github.com/sequana/versionix/graphs/contributors
##############################################################################

import shutil
import subprocess
import sys

from .registry import metadata


def get_version(standalone, verbose=True):
    """Main entry point that returns the version of an existing executable"""
    # we use check_output in case the standalone opens a GUI (e.g. fastqc --WRONG pops up the GUI)

    try:
        meta = metadata[standalone]
    except KeyError:
        if verbose:
            print(
                "#ERROR Your input standalone is not registered. Please provide a PR or fill an issue on github/sequana/versionix"
            )
        sys.exit(1)

    # If there is no special caller defined, let us check that the standalone exists
    if "caller" not in meta.keys() and shutil.which(standalone) is None:
        if verbose:
            print(f"ERROR: {standalone} command not found in your environment")
        sys.exit(1)

    # The command used to get the version output
    caller = meta.get("caller", standalone)

    # The options necessary to get the version output
    options = meta.get("options", "")

    # The parser of the version output
    parser = meta.get("parser", lambda x: x.stdout.strip())

    try:
        cmd = f"{caller} {options}"

        p = subprocess.run(cmd, capture_output=True, universal_newlines=True, shell=True)
        version = parser(p)
        return version

    except Exception as err: #pragma: no cover
        print(err)
        sys.exit(1)
