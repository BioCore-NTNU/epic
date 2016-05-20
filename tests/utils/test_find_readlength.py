import pytest

import pandas as pd
import numpy as np

from io import StringIO


@pytest.fixture
def input_data():
    pass


@pytest.fixture
def expected_result():
    pass


def find_readlength(args):

    import logging
    from sys import platform
    from re import search, IGNORECASE
    from io import BytesIO
    from subprocess import check_output
    from epic.config import logging_settings
    """Estimate length of reads based on 1000 first."""

    bed_file = args.treatment[0]

    filereader = "cat "
    if bed_file.endswith(".gz") and search("linux", platform, IGNORECASE):
        filereader = "zcat "
    elif bed_file.endswith(".gz") and search("darwin", platform, IGNORECASE):
        filereader = "gzcat "
    elif bed_file.endswith(".bz2"):
        filereader = "bzgrep "
    elif bed_file.endswith(".bam"):
        filereader = "bamToBed -i "

    command = filereader + "{} | head -1000".format(bed_file)
    output = check_output(command, shell=True)

    df = pd.read_table(
        BytesIO(output),
        header=None,
        usecols=[1, 2],
        sep="\s+",
        names=["Start", "End"])

    avg_readlength = (df.End - df.Start).mean()

    logging.info("Used {} to estimate an average read length of {}".format(
        bed_file, avg_readlength))

    raise "Must now implement function that finds closest length in pkg_utils"

    return avg_readlength


def test_find_readlength(args_200):

    result = find_readlength(args_200)
    assert 0
    # assert result == expected_result
