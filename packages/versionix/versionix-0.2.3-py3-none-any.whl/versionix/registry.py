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

# default parser performs stdout.strip()

#v1.5.0
def parser_strip_v(x):
    return x.stdout.strip("v").strip()


# versionix 1.0.0
def parser_split_2(x):
    try:
        return x.stdout.split()[1]
    except IndexError:
        return x.stderr.split()[1]

# versionix v1.0.0
def parser_split_2_strip_v(x):
    try:
        return x.stdout.split()[1][1:]
    except IndexError:
        return x.stderr.split()[1][1:]

# versionix version 1.0.0
parser_split_3 = lambda x: x.stdout.split()[2]


metadata = {
    "apptainer": {
        "options": "version"
    },
    "bamtools": {
        "options": "--version",
        "parser": parser_split_2
    },
    "bcl2fastq": {
        "options": "--version",
        "parser": lambda data: [x.split()[1][1:] for x in data.stderr.split("\n") if x.startswith("bcl2fastq")][0]
    },
    "bedtools": {
        "options": "--version",
        "parser": parser_split_2_strip_v
    },
    "blastn": {
        "options": "-version",
        "parser": parser_split_2
    },
    "blastp": {
        "options": "-version",
        "parser": parser_split_2
    },
    "blastx": {
        "options": "-version",
        "parser": parser_split_2
    },
    "bowtie": {
        "options": "--version",
        "parser": parser_split_3
    },
    "bowtie2": {
        "options": "--version",
        "parser": parser_split_3
    },
    "bwa": {
        "parser": lambda x: x.stderr.strip().split("\n")[1].split()[1]
    },
    #"canu": {
    #    "options": ,
    #    "parser": 
    #},
    "checkm": {
        "options": "",
        "parser": lambda x: x.stdout.split()[2][1:]
    },
    "circlator": {
        "options": "version",
        "parser": lambda x: x.stdout.strip()
    },
    "ccs": {
        "options": "--version",
        "parser": parser_split_2
    },
    "cutadapt": {
        "options": "--version"
    },
    "deeptools": {
        "options": "--version",
        "parser": parser_split_2
    },
    "DESeq2": {
        "caller": "Rscript -e \"library(DESeq2)\\npackageVersion('DESeq2')\"",
        "parser": lambda x: x.stdout.split()[1].strip("’‘"),
    },
    "dot": {
        "options": "-V",
        "parser": lambda x: x.stderr.split()[4].strip(),
    },
    "falco": {
        "options": "--version",
        "parser": parser_split_2
    },
    "fastqc": {
        "options": "--version",
        "parser": parser_split_2_strip_v
    },
    "fastp": {
        "options": "--version", 
        "parser": parser_split_2
    },
    "featureCounts": {
        "options": "-v",
        "parser": lambda x: x.stderr.split("\n")[1].split()[1][1:], 
    },
    "flye": {
        "options": "--version",
    },
    "freebayes": {
        "options": "--version",
        "parser": parser_split_2_strip_v
    },
    "gffread": {
        "options": "--version"
    },
    #"hifiasm": {
    #    "options": ,
    #    "parser": 
    #},
    "idr": {
        "options": "--version",
        "parser": lambda x: x.stdout.split("\n")[0].split()[1]
    },
    "igvtools": {
        "options": "version",
        "parser": lambda data: [x.split()[2] for x in data.stdout.split("\n") if x.startswith("IGV Version")][0]
    },
    "jellyfish": {
        "options": "--version",
        "parser": parser_split_2
    },
    "kallisto": {
        "options": "version",
        "parser": parser_split_3
    },
    "kraken2": {
        "options": "--version",
        "parser": parser_split_3
    },
    "ktImportText": {
        "options": "",
        "parser": lambda x: x.stdout.split("\n")[1].split()[2]
    },
    "macs3": {
        "options": "--version",
        "parser": parser_split_2,
    },
    "mafft": {
        "options": "--version",
        "parser": lambda x: x.stderr.split()[0][1:]
    },
    "minimap2": {
        "options": "--version"
    },
    "multiqc": {
        "options": "--version",
        "parser": parser_split_3
    },
    "pbindex": {
        "options": "--version",
        "parser": parser_split_2
    },
    "picard": {
        "options": "SortVcf --version",
        "parser": lambda x: x.stderr.split("\n")[1].split(":")[1].split("-")[0]
    },
    "pigz": {
        "options": "--version",
        "parser": parser_split_2
    },
    "plotCorrelation": {
        "options": "--version",
        "parser": parser_split_2
    },
    "plotFingerprint": {
        "options": "--version",
        "parser": parser_split_2
    },
    "prokka": {
        "options": "--version",
        "parser": parser_split_2
    },
    "pycoQC": {
        "options": "--version",
        "parser": parser_split_2_strip_v
    },
    "quast": {
        "options": "",
        "parser": lambda x: x.stderr.split("\n")[1].split()[1]
    },
    "salmon": {
        "options": "--version",
        "parser": parser_split_2
    },
    "sambamba": {
        "options": "--version",
        "parser": lambda x: x.stderr.split()[1]
    },
    "samtools": {
        "options": "--version",
        "parser": parser_split_2
    },
    "seqtk": {
        "parser": lambda x: x.stderr.split("\n")[2].split()[1]
    },
    "seqkit": {
        "options": "version",
        "parser": parser_split_2_strip_v
    },
    "sequana": {
        "options": "--version",
        "parser": parser_split_3
    },
    "sequana_coverage": {
        "options": "--version",
        "parser": parser_split_3
    },
    "sequana_taxonomy": {
        "options": "--version",
        "parser": parser_split_3
    },
    "sequana_pipeotools": {
        "options": "--version",
        "parser": parser_split_3
    },
    "singularity": {
        "options": "version"
    },
    "STAR": {
        "options": "--version"
    },
    "snpEff": {
        "options": "-version",
        "parser": parser_split_2
    },
    "syri": {
        "options": "--version",
        #"parser": parser_split_2
    },
    "vt": {
        "options": "--version",
        "parser": parser_split_2_strip_v
    },
}
