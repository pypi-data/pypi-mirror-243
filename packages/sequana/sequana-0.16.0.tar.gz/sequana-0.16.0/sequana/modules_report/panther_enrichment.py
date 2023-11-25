#
#  This file is part of Sequana software
#
#  Copyright (c) 2020 - Sequana Development Team
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/sequana/sequana
#  documentation: http://sequana.readthedocs.io
#
##############################################################################
"""Module to write enrichment report"""
import os
import sys
from pathlib import Path

from sequana.lazy import pandas as pd
from sequana.lazy import pylab

from sequana.modules_report.base_module import SequanaBaseModule
from sequana.utils.datatables_js import DataTable
from sequana.enrichment.panther import PantherEnrichment
from sequana.utils import config
from plotly import offline

from easydev import Progress

import colorlog

logger = colorlog.getLogger(__name__)


class ModulePantherEnrichment(SequanaBaseModule):
    """Write HTML report of variant calling. This class takes a csv file
    generated by sequana_variant_filter.
    """

    def __init__(
        self,
        gene_lists,
        taxon,
        enrichment_params={
            "padj": 0.05,
            "log2_fc": 3,
            "max_entries": 3000,  # not used in enrichment
            "nmax": 50,
            "mapper": None,
            "plot_compute_levels": False,
            "plot_logx": True,
        },
        command="",
        ontologies=["MF", "BP", "CC"],
    ):
        """.. rubric:: constructor"""
        super().__init__()
        self.title = "Panther Enrichment"

        self.command = command
        self.gene_lists = gene_lists
        self.enrichment_params = enrichment_params
        self.nmax = enrichment_params.get("nmax", 50)
        self.csv_directory = Path(config.output_dir) / "tables"
        self.plot_directory = Path(config.output_dir) / "plots"
        self.csv_directory.mkdir()
        self.plot_directory.mkdir()

        # compute the enrichment here once for all, This may take time
        from sequana import logger

        logger.setLevel("INFO")

        logger.info(" === Module PanthEnrichment. === ")
        self.pe = PantherEnrichment(
            self.gene_lists,
            taxon,
            # max_entries=self.enrichment_params["max_entries"],
            log2_fc_threshold=self.enrichment_params["log2_fc"],
        )

        self.ontologies = ontologies

        # Compute the enrichment
        self.pe.compute_enrichment(ontologies=self.ontologies)
        self.df_stats = self.pe.get_mapping_stats()

        self.create_report_content()
        self.create_html("enrichment.html")

    def create_report_content(self):
        self.sections = list()
        self.summary()
        self.add_go()
        self.sections.append({"name": "5 - Info", "anchor": "command", "content": self.command})

    def summary(self):
        """Add information."""

        total_up = len(self.gene_lists["up"])
        total_down = len(self.gene_lists["down"])
        total = total_up + total_down
        log2fc = self.enrichment_params["log2_fc"]

        # create html table for taxon information
        _taxon_id = self.pe.taxon_info["taxon_id"]
        _taxon_name = self.pe.taxon_info["long_name"]

        # table of undertermined IDs
        df_stats = self.df_stats.drop_duplicates()
        datatable = DataTable(df_stats, "unmapped")
        datatable.datatable.datatable_options = {
            "scrollX": "true",
            "pageLength": 10,
            "scrollCollapse": "true",
            "dom": "Bfrtip",
            "buttons": ["copy", "csv"],
        }
        js = datatable.create_javascript_function()
        html_table = datatable.create_datatable(float_format="%E")

        self.sections.append(
            {
                "name": "1 - Summary",
                "anchor": "filters_option",
                "content": f"""

<p>In the following sections, you will find the GO
terms enrichment. The input data for those analyis is the output of the RNADiff
analysis where adjusted p-values above 0.05 are excluded. Moreover, we removed 
candidates with log2 fold change below {log2fc}. Using these filters, the list of
differentially expressed genes is made of {total_up} up and {total_down} down genes (total {total})</p>
<p> In the following plots you can find the first GO terms that are enriched, keeping a 
maximum of {self.nmax} identifiers. </p>

<p>The taxon used is {_taxon_name} (ID {_taxon_id}).<br>

<p> Check the following table for the percentage of mapped genes on Panther
DB</p>

{js}{html_table}
""",
            }
        )

    def add_go(self):
        # somehow, logger used here and in add_kegg must be global. If you call
        # add_go and then add_kegg, logger becomes an unbound local variable.
        # https://stackoverflow.com/questions/10851906/python-3-unboundlocalerror-local-variable-referenced-before-assignment
        # global logger
        level = logger.level
        logger.setLevel(level)

        html_intro = """
<p>Here below is a set of plots showing the enriched GO terms using the down
regulated genes only, and then the up-regulated genes only. When possible a
graph of the found GO terms is provided. MF stands for molecular
function, CC for cellular components and BP for biological process.</p>
        </div>
        """.format(
            self.pe.summary["padj_threshold"],
            self.pe.summary["fold_change_range"][0],
            self.pe.summary["fold_change_range"][1],
            self.pe.summary["DGE_after_filtering"]["down"],
            self.pe.summary["DGE_after_filtering"]["up"],
            self.pe.summary["DGE_after_filtering"]["all"],
        )

        html = self._get_enrichment("down")
        self.sections.append(
            {
                "name": "2 - Enriched GO terms (Down cases)",
                "anchor": "go_down",
                "content": html,
            }
        )

        html = self._get_enrichment("up")
        self.sections.append(
            {
                "name": "3 - Enriched GO terms (Up cases)",
                "anchor": "go_up",
                "content": html,
            }
        )

        html = self._get_enrichment("all")
        self.sections.append(
            {
                "name": "4 - Enriched GO terms (All cases)",
                "anchor": "go_all",
                "content": html,
            }
        )

    # a utility function to create the proper html table
    def get_html_table(self, this_df, identifier):
        df = this_df.copy()

        # depending on the Panther category, we add the link to the identifier
        links = []
        for x in df["id"]:
            if x.startswith("PC"):
                links.append(f"http://www.pantherdb.org/panther/category.do?categoryAcc={x}")
            elif x.startswith("R-"):
                links.append(f"https://reactome.org/PathwayBrowser/#/{x}")
            else:
                links.append(f"https://www.ebi.ac.uk/QuickGO/term/{x}")
        df["links"] = links

        # remove non-informative or redundant fields
        df = df.drop(
            ["term", "fdr2", "abs_log2_fold_enrichment", "pct_diff_expr"],
            errors="ignore",
            axis=1,
        )

        first_col = df.pop("id")
        df.insert(0, "id", first_col)
        df = df.sort_values(by="fold_enrichment", ascending=False)

        datatable = DataTable(pd.DataFrame(df), identifier)
        datatable.datatable.set_links_to_column("links", "id")
        datatable.datatable.datatable_options = {
            "scrollX": "true",
            "pageLength": 10,
            "scrollCollapse": "true",
            "dom": "Bfrtip",
            "buttons": ["copy", "csv"],
        }
        js = datatable.create_javascript_function()
        html_table = datatable.create_datatable(float_format="%E")
        return js + html_table

    def _get_enrichment(self, category):
        # category is in down/up/all

        style = "width:95%"
        _temp_df = {}
        _minus = {}
        _plus = {}

        if not self.pe.enrichment[category]:
            return ""

        html = ""

        for ontology in self.ontologies:
            # get dat without plotting to store the entire set of GO terms
            df, subdf = self.pe._get_plot_go_terms_data(category, ontologies=ontology, compute_levels=False)
            if df is not None and len(df):
                _temp_df[ontology] = df.copy()
                _plus[ontology] = sum(df.plus_minus == "+")
                _minus[ontology] = sum(df.plus_minus == "-")

                # now plotting but showing only some restricted GO terms
                fig = self.pe.plot_go_terms(
                    category,
                    ontologies=ontology,
                    compute_levels=self.enrichment_params["plot_compute_levels"],
                    log=self.enrichment_params["plot_logx"],
                    max_features=self.nmax,
                )
                html_scatter_plotly = offline.plot(fig, output_type="div", include_plotlyjs=False)

                _temp_df[ontology].to_csv(self.csv_directory / f"DEGs_enrichment_{category}_{ontology}.csv")
                fig.write_image(self.plot_directory / f"DEGs_enrichment_{category}_{ontology}.pdf")
                html += f"""
<h3>{category.title()} - {ontology}</h3>
<p>For {ontology}, we found {_plus[ontology]+_minus[ontology]} go terms.
Showing {self.nmax} here below (at most). The full list is downloadable from the CSV
 file hereafter.</p> {html_scatter_plotly} <br>"""
                html += self.get_html_table(_temp_df[ontology], f"GO_table_{category}_{ontology}")
            else:
                html += f"""
<h4>{category.title()} - {ontology}</h4><p>For {ontology} case, we found 0
enriched go terms. </p><br>"""

            filenames = []
            for ontology in self.ontologies:
                if "PROTEIN" in ontology or "PATHWAY" in ontology:
                    continue
                filename = self.plot_directory / f"Chart_{category}_{ontology}.png"
                if ontology in _temp_df and len(_temp_df[ontology]):
                    logger.info(f"Saving chart for case {ontology} ({category}) in {filename}")

                    self.pe.save_chart(_temp_df[ontology].iloc[0 : self.nmax], filename)
                    # Files path should be relative to the location of the enrichment.html file
                    # ie relative to self.output_dir (.parents[1] here)
                    filenames.append(filename.relative_to(filename.parents[1]))
        foto = self.add_fotorama(filenames, width=1000)
        html += f"<h4>Charts {category} -- </h4> {foto}"

        return html
