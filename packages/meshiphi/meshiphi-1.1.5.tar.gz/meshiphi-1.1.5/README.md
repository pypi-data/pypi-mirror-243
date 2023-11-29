![](logo.jpg)

<!-- <a href="https://colab.research.google.com/drive/12D-CN10X7xAcXn_df0zNLHtdiiXxZVkz?usp=sharing"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab" alt="Colab">
<a href="https://antarctica.github.io/PolarRoute/"><img src="https://img.shields.io/badge/Manual%20-github.io%2FPolarRoute%2F-red" alt="Manual Page">
<a href="https://pypi.org/project/polar-route/"><img src="https://img.shields.io/pypi/v/polar-route" alt="PyPi">
<a href="https://github.com/antarctica/PolarRoute/tags"><img src="https://img.shields.io/github/v/tag/antarctica/PolarRoute" alt="Release Tag"></a>
<a href="https://github.com/antarctica/PolarRoute/issues"><img src="https://img.shields.io/github/issues/antarctica/PolarRoute" alt="Issues"></a>
<a href="https://github.com/antarctica/PolarRoute/blob/main/LICENSE"><img src="https://img.shields.io/github/license/antarctica/PolarRoute" alt="License"></a> -->

# Meshiφ (MeshiPhi)

Introducing Meshiφ, a versatile software package designed for comprehensive earth modeling and navigation planning. Meshiφ works by discretizing the Earth's surface into a non-uniform grid, allocating higher resolution in regions of geographic diversity, and conserving lower resolution in more uniform regions. The software also incorporates data-driven vehicle models, with the ability to calculate speed limits and fuel needs for specific vessels within each grid cell. These mesh objects can be output in standard formats, such as GeoJSON and GeoTIFF, enabling data-visualisation via GIS software such as ArcGIS. 

## Installation
The Meshiφ package has an optional dependance on GDAL, which is required to produce outputs in GeoJSON or GeoTIFF formats. More information on setting up GDAL can be found in the manual pages linked above. Once these requirements are met then the software can be installed by:

Github:
```
git clone https://github.com/Antarctica/MeshiPhi
python setup.py install
```

 Pip: 
```
pip install cartographi
```

> NOTE: The installation process may vary slightly dependent on OS. Please consult the documentation for further installation guidance.

## Required Data sources
Meshiφ has been built to work with a variety of open-source atmospheric and oceanographic data sources. 
A list of supported data sources and their associated data-loaders is given in the 
'Data Loaders' section of the manual

## Documentation
Sphinx is used to generate documentation for this project. The dependencies can be installed through pip:
```
pip install sphinx sphinx_markdown_builder sphinx_rtd_theme rinohtype
```
When updating the docs, run the following command within the MeshiPhi directory to recompile.
```
sphinx-build -b html ./docs/source ./docs/html
```
Sometimes the cache needs to be cleared for internal links to update. If facing this problem, run this from the MeshiPhi directory.
```
rm -r docs/build/.doctrees/
```
## Developers
Samuel Hall, Harrison Abbot, Ayat Fekry, George Coombs, Jonathan Smith, Maria Fox, and James Byrne 

## Collaboration
We are currently assessing the best practice for collaboration on the codebase, until then please contact [polarroute@bas.ac.uk](polarroute@bas.ac.uk) for further info.


## License
This software is licensed under a MIT license, but request users cite our publication.  

Jonathan D. Smith, Samuel Hall, George Coombs, James Byrne, Michael A. S. Thorne,  J. Alexander Brearley, Derek Long, Michael Meredith, Maria Fox,  (2022), Autonomous Passage Planning for a Polar Vessel, arXiv, https://arxiv.org/abs/2209.02389

For more information please see the attached ``LICENSE`` file. 

[version]: https://img.shields.io/PolarRoute/v/datadog-metrics.svg?style=flat-square
[downloads]: https://img.shields.io/PolarRoute/dm/datadog-metrics.svg?style=flat-square
