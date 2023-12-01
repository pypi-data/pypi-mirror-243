# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sequana_pipelines', 'sequana_pipelines.denovo']

package_data = \
{'': ['*']}

install_requires = \
['click-completion>=0.5.2,<0.6.0',
 'sequana>=0.15.0',
 'sequana_pipetools>=0.16.1']

entry_points = \
{'console_scripts': ['sequana_denovo = sequana_pipelines.denovo.main:main']}

setup_kwargs = {
    'name': 'sequana-denovo',
    'version': '0.10.0',
    'description': 'Multi-sample denovo assembly of FastQ sequences (short read)',
    'long_description': '\n.. image:: https://badge.fury.io/py/sequana-denovo.svg\n     :target: https://pypi.python.org/pypi/sequana_denovo\n\n.. image:: https://github.com/sequana/denovo/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/sequana/denovo/actions/workflows/main.yml\n\n.. image:: https://coveralls.io/repos/github/sequana/denovo/badge.svg?branch=main\n    :target: https://coveralls.io/github/sequana/denovo?branch=main\n\n.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C3.10-blue.svg\n    :target: https://pypi.python.org/pypi/sequana\n    :alt: Python 3.8 | 3.9 | 3.10\n\n.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg\n   :target: http://joss.theoj.org/papers/10.21105/joss.00352\n   :alt: JOSS (journal of open source software) DOI\n\nThis is is the **denovo** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet\n\n\n:Overview: a de-novo assembly pipeline for short-read sequencing data\n:Input: A set of FastQ files\n:Output: Fasta, VCF, HTML report\n:Status: production\n:Citation: Cokelaer et al, (2017), ‘Sequana’: a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI doi:10.21105/joss.00352\n\n\nInstallation\n~~~~~~~~~~~~\n\n**sequana_denovo** is based on Python3, just install the package as follows::\n\n    pip install sequana --upgrade\n\nYou will need third-party software such as fastqc. Please see below for details.\n\nUsage\n~~~~~\n\nThe following command will scan all files ending in .fastq.gz found in the local\ndirectory, create a directory called denovo/ where a snakemake pipeline is\nstored. Depending on the number of files and their sizes, the\nprocess may be long::\n\n::\n\n    sequana_denovo --help\n    sequana_denovo --input-directory DATAPATH \n\nThis creates a directory with the pipeline and configuration file. You will then need \nto execute the pipeline::\n\n    cd denovo\n    sh denovo.sh  # for a local run\n\nThis launch a snakemake pipeline. If you are familiar with snakemake, you can \nretrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::\n\n    snakemake -s denovo.smk -c config.yaml --cores 4 --stats stats.txt\n\nOr use `sequanix <https://sequana.readthedocs.io/en/main/sequanix.html>`_ interface.\n\nRequirements\n~~~~~~~~~~~~\n\nThis pipelines requires the following executable(s):\n\n- spades\n- busco\n- bwa\n- khmer : there is not executable called kmher but a set of executables (.e.g .normalize-by-median.py)\n- freebayes\n- picard\n- prokka\n- quast\n- spades\n- sambamba\n- samtools\n\n\n\n.. image:: https://raw.githubusercontent.com/sequana/sequana_denovo/main/sequana_pipelines/denovo/dag.png\n\n\nDetails\n~~~~~~~~~\n\n\nSnakemake *de-novo* assembly pipeline dedicates to small genome like bacteria.\nIt is based on `SPAdes <http://cab.spbu.ru/software/spades/>`_.\nThe assembler corrects reads and then assemble them using different size of kmer.\nIf the correct option is set, SPAdes corrects mismatches and short INDELs in\nthe contigs using BWA.\n\nThe sequencing depth can be normalised with `khmer <https://github.com/dib-lab/khmer>`_.\nDigital normalisation converts the existing high coverage regions into a Gaussian\ndistributions centered around a lower sequencing depth. To put it another way,\ngenome regions covered at 200x will be covered at 20x after normalisation. Thus,\nsome reads from high coverage regions are discarded to reduce the quantity of data.\nAlthough the coverage is drastically reduce, the assembly will be as good or better\nthan assembling the unnormalised data. Furthermore, SPAdes with normalised data\nis notably speeder and cost less memory than without digital normalisation.\nAbove all, khmer does this in fixed, low memory and without any reference\nsequence needed.\n\nThe pipeline assess the assembly with several tools and approach. The first one\nis `Quast <http://quast.sourceforge.net/>`_, a tools for genome assemblies\nevaluation and comparison. It provides a HTML report with useful metrics like\nN50, number of mismatch and so on. Furthermore, it creates a viewer of contigs\ncalled `Icarus <http://quast.sourceforge.net/icarus.html>`_.\n\nThe second approach is to characterise coverage with sequana coverage and\nto detect mismatchs and short INDELs with\n`Freebayes <https://github.com/ekg/freebayes>`_.\n\nThe last approach but not the least is `BUSCO <http://busco.ezlab.org/>`_, that\nprovides quantitative measures for the assessment of genome assembly based on\nexpectations of gene content from near-universal single-copy orthologs selected\nfrom `OrthoDB <http://www.orthodb.org/>`_.\n\n\n========= ====================================================================\nVersion   Description\n========= ====================================================================\n0.10.0    * use click / include multiqc apptainer\n0.9.0     * Major refactoring to include apptainers, use wrappers\n0.8.5     * add multiqc and use newest version of sequana\n0.8.4     * update pipeline to use new pipetools features\n0.8.3     * fix requirements (spades -> spades.py)\n0.8.2     * fix readtag, update config to account for new coverage setup\n0.8.1 \n0.8.0     **First release.**\n========= ====================================================================\n',
    'author': 'Sequana Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sequana/demultiplex',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
