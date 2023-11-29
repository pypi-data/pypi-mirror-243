# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ra2ce',
 'ra2ce.analyses',
 'ra2ce.analyses.analysis_config_data',
 'ra2ce.analyses.analysis_config_data.enums',
 'ra2ce.analyses.direct',
 'ra2ce.analyses.direct.damage',
 'ra2ce.analyses.direct.damage_calculation',
 'ra2ce.analyses.indirect',
 'ra2ce.analyses.indirect.traffic_analysis',
 'ra2ce.common',
 'ra2ce.common.configuration',
 'ra2ce.common.io',
 'ra2ce.common.io.readers',
 'ra2ce.common.io.writers',
 'ra2ce.common.validation',
 'ra2ce.configuration',
 'ra2ce.graph',
 'ra2ce.graph.exporters',
 'ra2ce.graph.graph_files',
 'ra2ce.graph.hazard',
 'ra2ce.graph.hazard.hazard_intersect',
 'ra2ce.graph.network_config_data',
 'ra2ce.graph.network_config_data.enums',
 'ra2ce.graph.network_wrappers',
 'ra2ce.graph.network_wrappers.osm_network_wrapper',
 'ra2ce.runners']

package_data = \
{'': ['*']}

install_requires = \
['GDAL==3.5.1',
 'Rtree>=1.0.0,<2.0.0',
 'affine>=2.3.1,<3.0.0',
 'click>=8.1.3,<9.0.0',
 'geopandas>=0.14.0,<0.15.0',
 'geopy>=2.4.0,<3.0.0',
 'joblib>=1.3.2,<2.0.0',
 'momepy==0.5.0',
 'networkx>=2.8.6,<3.0.0',
 'numpy>=1.23.3,<2.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'osmnx>=1.6.0,<2.0.0',
 'pandas>=1.4.4,<2.0.0',
 'pyarrow>=9.0.0,<10.0.0',
 'pygeos>=0.14,<0.15',
 'pyinstaller>=6.2.0,<7.0.0',
 'pyogrio>=0.6.0,<0.7.0',
 'rasterio>=1.3.2,<2.0.0',
 'rasterstats>=0.17.0,<0.18.0',
 'scipy>=1.9.1,<2.0.0',
 'seaborn>=0.12.0,<0.13.0',
 'shapely>=2.0.1,<3.0.0',
 'tqdm>=4.66.1,<5.0.0',
 'xarray>=2022.6.0,<2023.0.0',
 'xlrd>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['build-cli = scripts.make_exe:build_cli',
                     'run_ra2ce = ra2ce.run:main']}

setup_kwargs = {
    'name': 'ra2ce',
    'version': '0.6.0',
    'description': 'Risk Assessment and Adaptation for Critical infrastructurE (RA2CE).',
    'long_description': '[![Python 3.10](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/downloads/release/python-3109/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n![TeamCity build status](https://dpcbuild.deltares.nl/app/rest/builds/buildType:id:Ra2ce_Ra2ceContinuousDelivery_RunAllTests/statusIcon.svg)\n[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Deltares_ra2ce&metric=alert_status&token=35cd897258b4c3017a42077f18304e6a73042dd6)](https://sonarcloud.io/summary/new_code?id=Deltares_ra2ce)\n[![GitHub Pages documentation](https://github.com/Deltares/ra2ce/actions/workflows/deploy_docs.yml/badge.svg)](https://github.com/Deltares/ra2ce/actions/workflows/deploy_docs.yml)\n[![Binder branch](https://github.com/Deltares/ra2ce/actions/workflows/binder_branch.yml/badge.svg)](https://github.com/Deltares/ra2ce/actions/workflows/binder_branch.yml)\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/Deltares/ra2ce/jupyter-binder)\n\n\n![RA2CE](./docs/_resources/ra2ce_banner.png "Ra2ce banner")\n\nThis is the repository of RA2CE (*just say race!*) - the Resilience Assessment and Adaptation for Critical infrastructurE Toolkit Python Package developed by Deltares. RA2CE helps to quantify resilience of critical infrastructure networks, prioritize interventions and adaptation measures and select the most appropriate action perspective to increase resilience considering future conditions.\n\n**Contact** Margreet van Marle (Margreet.vanMarle@Deltares.nl)\n\nFind more about the following topics in our [official documentation page](https://deltares.github.io/ra2ce/):\n\n- [Contributing](https://deltares.github.io/ra2ce/collaboration/collaboration.html)\n- [Installation](https://deltares.github.io/ra2ce/installation/installation.html)\n- [Network user guide](https://deltares.github.io/ra2ce/network_module/network_module.html)\n- [Analysis user guide](https://deltares.github.io/ra2ce/analysis_module/analysis_module.html)\n\n## Distribution\nRa2ce is shared with [GPL3 license](https://www.gnu.org/licenses/gpl-3.0.en.html), you may use and/or extend it by using the same license. For specific agreements we urge you to contact us.\n\n## Usage\nIf you wish to run ra2ce locally we recommend to have a look at the [installation section](#installation). \nOn the other hand, if you wish to run a preinstalled environment, you may use our [examples in binder](examples/README.md).\n\n## Third-party Notices\nThis project incorporates components from the projects listed below.\n\n**NetworkX**: NetworkX is distributed with the [3-clause BSD license](https://opensource.org/license/bsd-3-clause/).\n\n   > Copyright (C) 2004-2022, NetworkX Developers\n   Aric Hagberg <hagberg@lanl.gov>\n   Dan Schult <dschult@colgate.edu>\n   Pieter Swart <swart@lanl.gov>\n   All rights reserved.\n\n**OSMnx**: OSMnx is distributed under the [MIT License](https://opensource.org/license/mit/).\n\n  > Boeing, G. 2017. \n  [OSMnx: New Methods for Acquiring, Constructing, Analyzing, and Visualizing Complex Street Networks](https://geoffboeing.com/publications/osmnx-complex-street-networks/)\n  Computers, Environment and Urban Systems 65, 126-139. doi:10.1016/j.compenvurbsys.2017.05.004\n',
    'author': 'Margreet van Marle',
    'author_email': 'Margreet.vanMarle@deltares.nl',
    'maintainer': 'Frederique de Groen',
    'maintainer_email': 'frederique.degroen@deltares.nl',
    'url': 'https://github.com/Deltares/ra2ce',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<3.11',
}


setup(**setup_kwargs)
