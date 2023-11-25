#  This file is part of Sequana software
#
#  Copyright (c) 2016-2020 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
import os

import click
import rich_click as click
import colorlog

from sequana import salmon

from .utils import CONTEXT_SETTINGS


logger = colorlog.getLogger(__name__)


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option("-i", "--input", required=True, help="The salmon input file.")
@click.option("-o", "--output", required=True, help="The feature counts output file")
@click.option("-f", "--gff", required=True, help="A GFF file compatible with your salmon file")
@click.option(
    "-a",
    "--attribute",
    default="ID",
    help="A valid attribute to be found in the GFF file and salmon input",
)
@click.option("-a", "--feature", default="gene", help="A valid feature")
def salmon_cli(**kwargs):
    """Convert output of Salmon into a feature counts file"""

    salmon_input = kwargs["input"]
    output = kwargs["output"]
    if os.path.exists(salmon_input) is False:
        logger.critical("Input file does not exists ({})".format(salmon_input))
    gff = kwargs["gff"]
    attribute = kwargs["attribute"]
    feature = kwargs["feature"]

    # reads file generated by salmon and generated count file as expected by
    # DGE.
    s = salmon.Salmon(salmon_input, gff)
    s.save_feature_counts(output, feature=feature, attribute=attribute)
