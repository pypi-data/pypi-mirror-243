# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sequana_pipelines', 'sequana_pipelines.mapper']

package_data = \
{'': ['*']}

install_requires = \
['click-completion>=0.5.2,<0.6.0',
 'sequana>=0.15.0',
 'sequana_pipetools>=0.16.1']

entry_points = \
{'console_scripts': ['sequana_mapper = sequana_pipelines.mapper.main:main']}

setup_kwargs = {
    'name': 'sequana-mapper',
    'version': '1.1.0',
    'description': 'A multi-sample mapper to map reads onto a reference',
    'long_description': "\n.. image:: https://badge.fury.io/py/sequana-mapper.svg\n     :target: https://pypi.python.org/pypi/sequana_mapper\n\n.. image:: https://github.com/sequana/mapper/actions/workflows/main.yml/badge.svg\n   :target: https://github.com/sequana/mapper/actions/    \n\n.. image:: https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C3.10-blue.svg\n    :target: https://pypi.python.org/pypi/sequana\n    :alt: Python 3.8 | 3.9 | 3.10\n\n.. image:: http://joss.theoj.org/papers/10.21105/joss.00352/status.svg\n   :target: http://joss.theoj.org/papers/10.21105/joss.00352\n   :alt: JOSS (journal of open source software) DOI\n\nThis is the **mapper** pipeline from the `Sequana <https://sequana.readthedocs.org>`_ projet\n\n:Overview: This is a simple pipeline to map several FastQ files onto a reference using different mappers/aligners\n:Input: A set of FastQ files (illumina, pacbio, etc).\n:Output: A set of BAM files (and/or bigwig) and HTML report\n:Status: Production\n:Documentation: This README file, and https://sequana.readthedocs.io\n:Citation: Cokelaer et al, (2017), 'Sequana': a Set of Snakemake NGS pipelines, Journal of Open Source Software, 2(16), 352, JOSS DOI https://doi:10.21105/joss.00352\n\nInstallation\n~~~~~~~~~~~~\n\nIf you already have all requirements, you can install the packages using pip::\n\n    pip install sequana_mapper --upgrade\n\nYou will need third-party software such as fastqc. Please see below for details.\n\nUsage\n~~~~~\n\nThis command will scan all files ending in .fastq.gz found in the local\ndirectory, create a directory called mapper/ where a snakemake pipeline can be executed.::\n\n    sequana_mapper --input-directory DATAPATH  --mapper bwa --create-bigwig\n    sequana_mapper --input-directory DATAPATH  --mapper bwa --do-coverage\n\nThis creates a directory with the pipeline and configuration file. You will then need\nto execute the pipeline::\n\n    cd mapper\n    sh mapper.sh  # for a local run\n\nThis launch a snakemake pipeline. If you are familiar with snakemake, you can \nretrieve the pipeline itself and its configuration files and then execute the pipeline yourself with specific parameters::\n\n    snakemake -s mapper.rules -c config.yaml --cores 4 \\\n        --wrapper-prefix https://raw.githubusercontent.com/sequana/sequana-wrappers/\n\nOr use `sequanix <https://sequana.readthedocs.io/en/main/sequanix.html>`_ interface.\n\n\nRequirements\n~~~~~~~~~~~~\n\nThis pipelines requires the following executable(s):\n\n- bamtools\n- bwa\n- multiqc\n- sequana_coverage\n- minimap2\n- bowtie2\n- deeptools\n\n.. image:: https://raw.githubusercontent.com/sequana/mapper/main/sequana_pipelines/mapper/dag.png\n\n\nDetails\n~~~~~~~~~\n\nThis pipeline runs **mapper** in parallel on the input fastq files (paired or not). \nA brief sequana summary report is also produced. When using **--pacbio** option, \n*-x map-pb* options is automatically added to the config.yaml file and the\nreadtag is set to None. \n\nThe BAM files are filtered to remove unmapped reads to keep BAM files to minimal size. However,\nthe multiqc and statistics to be found in  {sample}/bamtools_stats/ includes mapped and unmapped reads information. Each BAM file is stored in a directory named after the sample. \n\n\n\nRules and configuration details\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nHere is the `latest documented configuration file <https://raw.githubusercontent.com/sequana/mapper/main/sequana_pipelines/mapper/config.yaml>`_\nto be used with the pipeline. Each rule used in the pipeline may have a section in the configuration file. \n\n\nChangelog\n~~~~~~~~~\n\n========= ======================================================================\nVersion   Description\n========= ======================================================================\n1.1.0     * BAM files are now filtered to remove unmapped reads\n          * set wrappers branch in config file and update pipeline.\n          * refactorise to use click and new sequana-pipetools\n1.0.0     * Use latest sequana-wrappers and graphviz apptainer\n0.12.0    * Use latest pipetools and add singularity containers\n0.11.1    * Fix typo when setting coverage to True and allow untagged filenames\n0.11.0    * implement feature counts for capture-seq projects\n0.10.1    * remove getlogdir and getname\n0.10.0    * use new wrappers framework \n0.9.0     * fix issue with logger and increments requirements\n          * add new option --pacbio to automatically set the options for \n            pacbio data (-x map-pb and readtag set to None)\n0.8.13    * add the thread option in minimap2 case\n0.8.12    * factorise multiqc rule\n0.8.11    * Implemente the --from-project option and new framework\n          * custom HTMrLl report\n0.8.10    * change samtools_depth rule and switched to bam2cov to cope with null\n            coverage \n0.8.9     * fix requirements\n0.8.8     * fix pipeline rule for bigwig + renamed output_bigwig into\n            create_bigwig; fix the multiqc config file\n0.8.7     * fix config file creation (for bigwig)\n0.8.6     * added bowtie2 mapper + bigwig as output, make coverage optional\n0.8.5     * create a sym link to the HTML report. Better post cleaning.\n0.8.4     * Fixing multiqc (synchronized with sequana updates) \n0.8.3     * add sequana_coverage rule. \n0.8.2     * add minimap2 mapper \n0.8.1     * fix bamtools stats rule to have different output name for multiqc\n0.8.0     **First release.**\n========= ======================================================================\n\n\nContribute & Code of Conduct\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\nTo contribute to this project, please take a look at the \n`Contributing Guidelines <https://github.com/sequana/sequana/blob/main/CONTRIBUTING.rst>`_ first. Please note that this project is released with a \n`Code of Conduct <https://github.com/sequana/sequana/blob/main/CONDUCT.md>`_. By contributing to this project, you agree to abide by its terms.\n\n",
    'author': 'Sequana Team',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sequana/mapper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
