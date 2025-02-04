import pytest

from collections import OrderedDict

from io import StringIO
import pandas as pd

from epic.merge.merge import main


@pytest.fixture
def regions(tmpdir):

    fs = []
    for i, c in enumerate(["""chr1	10000	10599	2.2761062711783457e-05	67.49046260339546	.
chr1	11400	17599	1.5475486939203985e-14	121.35954730992889	.""",
           """chr1	9800	15199	0.0048446172754557214	33.652547110032025	.""",
           """chr1	9800	10599	3.239383152206723e-79	204.30687218918862	."""]):

        name = str(i)
        f = tmpdir.mkdir(name).join(name)
        f.write(c)
        fs.append(str(f))

    return fs


@pytest.fixture
def files(tmpdir):

    od = OrderedDict()

    for n, c in [("fibroblast.matrix",u"""Chromosome Bin Enriched chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/ChIP_3_fibroblast.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_2_fibroblast.bed.gz chrX/Input_3_fibroblast.bed.gz
chr1 10000 1 4 14 13 2 4 14
chr1 10200 1 17 24 14 9 9 16
chr1 10400 1 3 1 1 1 0 2
chr1 11400 1 0 0 1 0 0 0
chr1 11600 1 0 0 0 0 0 0
chr1 11800 1 1 0 1 0 0 0
chr1 12000 1 0 0 0 0 0 0
chr1 12200 1 0 0 1 0 0 0
chr1 12400 1 0 0 0 0 0 0
chr1 12600 1 0 0 0 1 0 0
chr1 12800 1 0 0 0 0 0 0
chr1 13000 1 3 6 4 1 3 2
chr1 13200 1 0 1 0 1 1 0
chr1 13400 1 7 4 5 1 1 3
chr1 13600 1 0 0 0 0 0 0
chr1 13800 1 0 0 1 0 0 0
chr1 14000 1 0 0 0 0 0 0
chr1 14200 1 0 0 0 0 0 0
chr1 14400 1 0 0 0 0 0 0
chr1 14600 1 2 4 0 0 0 0
chr1 14800 1 0 4 6 2 2 4
chr1 15000 1 2 4 2 0 1 1
chr1 15200 1 0 0 1 0 0 1
chr1 15400 1 0 0 0 0 0 0
chr1 15600 1 0 0 2 0 0 1
chr1 15800 1 0 1 1 0 0 0
chr1 16000 1 1 8 3 1 0 0
chr1 16200 1 0 6 5 1 3 2
chr1 16400 1 3 5 3 4 7 0
chr1 16600 1 1 1 1 0 0 0
chr1 16800 1 0 0 0 0 0 0
chr1 17000 1 0 0 0 0 0 0
chr1 17200 1 0 0 0 0 0 0
chr1 17400 1 3 2 3 0 2 2"""),
("keratinocyte.matrix", u"""Chromosome Bin Enriched chrX/ChIP_1_keratinocyte.bed.gz chrX/ChIP_2_keratinocyte.bed.gz chrX/ChIP_3_keratinocyte.bed.gz chrX/Input_1_keratinocyte.bed.gz chrX/Input_2_keratinocyte.bed.gz chrX/Input_3_keratinocyte.bed.gz
chr1 9800 1 1 0 0 2 0 0
chr1 10000 1 13 15 17 11 2 17
chr1 10200 1 13 25 23 16 2 24
chr1 10400 1 2 0 2 10 0 3
chr1 10600 1 0 0 0 0 0 0
chr1 10800 1 0 0 1 0 0 0
chr1 11000 1 0 0 0 0 0 0
chr1 11200 1 0 0 0 0 0 0
chr1 11400 1 0 0 0 0 0 0
chr1 11600 1 0 0 1 0 0 0
chr1 11800 1 0 0 0 0 0 0
chr1 12000 1 0 0 2 0 0 0
chr1 12200 1 0 0 0 0 0 0
chr1 12400 1 0 0 0 0 0 0
chr1 12600 1 0 0 0 0 0 1
chr1 12800 1 0 1 1 0 0 0
chr1 13000 1 0 0 6 7 1 3
chr1 13200 1 0 2 0 2 1 1
chr1 13400 1 1 1 6 4 0 2
chr1 13600 1 0 0 0 0 0 0
chr1 13800 1 1 0 1 0 0 0
chr1 14000 1 0 0 0 0 0 0
chr1 14200 1 0 0 0 0 0 0
chr1 14400 1 0 0 0 0 0 0
chr1 14600 1 0 0 3 1 1 0
chr1 14800 1 1 2 4 6 0 0
chr1 15000 1 1 0 3 2 0 0"""),
        ("melanocyte.matrix", u"""Chromosome Bin Enriched chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/ChIP_3_melanocyte.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_melanocyte.bed.gz chrX/Input_3_melanocyte.bed.gz
chr1 9800 1 0 0 2 0 0 0
chr1 10000 1 13 3 128 2 2 21
chr1 10200 1 15 8 96 5 3 23
chr1 10400 1 3 0 4 3 0 7""")]:

        f = tmpdir.mkdir(n).join(n)
        f.write(c)
        od[str(f)] = str(f)

    return od

@pytest.fixture
def expected_result():

    c = u"""Chromosome Bin TotalEnriched chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_1_keratinocyte.bed.gz chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/ChIP_2_keratinocyte.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/ChIP_3_fibroblast.bed.gz chrX/ChIP_3_keratinocyte.bed.gz chrX/ChIP_3_melanocyte.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_1_keratinocyte.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_fibroblast.bed.gz chrX/Input_2_keratinocyte.bed.gz chrX/Input_2_melanocyte.bed.gz chrX/Input_3_fibroblast.bed.gz chrX/Input_3_keratinocyte.bed.gz chrX/Input_3_melanocyte.bed.gz
chr1 9800 2.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 10000 3.0 4.0 13.0 13.0 14.0 15.0 3.0 13.0 17.0 128.0 2.0 11.0 2.0 4.0 2.0 2.0 14.0 17.0 21.0
chr1 10200 3.0 17.0 13.0 15.0 24.0 25.0 8.0 14.0 23.0 96.0 9.0 16.0 5.0 9.0 2.0 3.0 16.0 24.0 23.0
chr1 10400 3.0 3.0 2.0 3.0 1.0 0.0 0.0 1.0 2.0 4.0 1.0 10.0 3.0 0.0 0.0 0.0 2.0 3.0 7.0
chr1 10600 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 10800 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11000 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11200 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11400 2.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11600 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 11800 2.0 1.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12000 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12200 2.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12400 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 12600 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0
chr1 12800 2.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 13000 2.0 3.0 0.0 0.0 6.0 0.0 0.0 4.0 6.0 0.0 1.0 7.0 0.0 3.0 1.0 0.0 2.0 3.0 0.0
chr1 13200 2.0 0.0 0.0 0.0 1.0 2.0 0.0 0.0 0.0 0.0 1.0 2.0 0.0 1.0 1.0 0.0 0.0 1.0 0.0
chr1 13400 2.0 7.0 1.0 0.0 4.0 1.0 0.0 5.0 6.0 0.0 1.0 4.0 0.0 1.0 0.0 0.0 3.0 2.0 0.0
chr1 13600 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 13800 2.0 0.0 1.0 0.0 0.0 0.0 0.0 1.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14000 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14200 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14400 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 14600 2.0 2.0 0.0 0.0 4.0 0.0 0.0 0.0 3.0 0.0 0.0 1.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0
chr1 14800 2.0 0.0 1.0 0.0 4.0 2.0 0.0 6.0 4.0 0.0 2.0 6.0 0.0 2.0 0.0 0.0 4.0 0.0 0.0
chr1 15000 2.0 2.0 1.0 0.0 4.0 0.0 0.0 2.0 3.0 0.0 0.0 2.0 0.0 1.0 0.0 0.0 1.0 0.0 0.0
chr1 15200 1.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0
chr1 15400 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 15600 1.0 0.0 0.0 0.0 0.0 0.0 0.0 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 1.0 0.0 0.0
chr1 15800 1.0 0.0 0.0 0.0 1.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 16000 1.0 1.0 0.0 0.0 8.0 0.0 0.0 3.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 16200 1.0 0.0 0.0 0.0 6.0 0.0 0.0 5.0 0.0 0.0 1.0 0.0 0.0 3.0 0.0 0.0 2.0 0.0 0.0
chr1 16400 1.0 3.0 0.0 0.0 5.0 0.0 0.0 3.0 0.0 0.0 4.0 0.0 0.0 7.0 0.0 0.0 0.0 0.0 0.0
chr1 16600 1.0 1.0 0.0 0.0 1.0 0.0 0.0 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 16800 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 17000 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 17200 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 17400 1.0 3.0 0.0 0.0 2.0 0.0 0.0 3.0 0.0 0.0 0.0 0.0 0.0 2.0 0.0 0.0 2.0 0.0 0.0"""

    return pd.read_table(StringIO(c), sep=" ", index_col=[0, 1, 2])


@pytest.mark.integration
def test_epic_merge_with(regions, files, expected_result):

    result_regions = main(files, regions, False, False, 1, )

    print("with")
    print(result_regions.to_csv(sep=" "))

    assert expected_result.equals(result_regions)
    # assert result_regions.equals(result_without)


@pytest.fixture
def simple_regions(tmpdir):

    fs = []
    for n, c in zip(["melanocyte.matrix", "fibroblast.matrix"], [
            u"""chr1	600	1200	2.2761062711783457e-05	67.49046260339546	.""",
            u"""chr1	400	1600	0.0048446172754557214	33.652547110032025	."""]):

        n = "regions_" + n
        f = tmpdir.mkdir(n).join(n)
        f.write(c)
        fs.append(str(f))

    return fs


@pytest.fixture
def simple_files(tmpdir):

    od = OrderedDict()

    for n, c in [("melanocyte.matrix", """Chromosome Bin Enriched chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_melanocyte.bed.gz
chr1 200 1 0 2 0 0
chr1 1200 1 13 128 2 2"""),
                 ("fibroblast.matrix", """Chromosome Bin Enriched chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_2_fibroblast.bed.gz
chr1 200 1 0 2 0 0
chr1 1200 1 13 128 2 2""")]:

        n = n
        f = tmpdir.mkdir(n).join(n)
        f.write(c)
        od[str(f)] = str(f)

    return od

@pytest.fixture
def expected_result_simple():

    c = u"""Chromosome Bin TotalEnriched chrX/ChIP_1_fibroblast.bed.gz chrX/ChIP_1_melanocyte.bed.gz chrX/ChIP_2_fibroblast.bed.gz chrX/ChIP_2_melanocyte.bed.gz chrX/Input_1_fibroblast.bed.gz chrX/Input_1_melanocyte.bed.gz chrX/Input_2_fibroblast.bed.gz chrX/Input_2_melanocyte.bed.gz
chr1 400 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 600 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 800 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 1000 2.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 1200 2.0 13.0 13.0 128.0 128.0 2.0 2.0 2.0 2.0
chr1 1400 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0
chr1 1600 1.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0"""

    return pd.read_table(StringIO(c), sep=" ", index_col=[0, 1, 2])


def test_simple_epic_merge_with_regions(simple_regions, simple_files, expected_result_simple):

    result_simple_regions = main(simple_files, simple_regions, False, False, 1)

    print("result")
    print(result_simple_regions.to_csv(sep=" "))

    print("expected_result")
    print(expected_result_simple.to_csv(sep=" "))

    assert result_simple_regions.equals(expected_result_simple)
