import pandas as pd

def add_color_trunks_flanks_valleys_bed(df):

    cols_to_keep = "Chromosome Start End Index RegionKind".split()

    df = df[cols_to_keep]

    df.insert(4, "Score", 0)
    df.insert(5, "Strand", ".")
    df.insert(6, "ThickStart", df.Start)
    df.insert(7, "ThickEnd", df.End)

    df.loc[:, "RegionKind"] = df.RegionKind.str.replace("trunk", "255,215,0").str.replace("valley", "128,0,128").str.replace("flank", "255,140,0")

    return df


if __name__ == "__main__":

    df = pd.read_table(snakemake.input[0], sep="\t", index_col=None, header=0)

    result = add_color_trunks_flanks_valleys_bed(df)

    result.to_csv(snakemake.output[0], sep="\t", index=False, header=None)
