# GeoGebra COM analysis

Given a 2d shape consisting of mainly triangles (and circles/semicircles), calculates the center of mass by taking a mass weighted average of the center of mass of each subfigure. Area is used as a proxy for mass.

# Installation

1. Git Clone this repo and CD into it. 

2. Make sure a recent version of python (>3.7) is installed.

3. Install dependencies through pip (a virtual environment, such as through [venv](https://docs.python.org/3/library/venv.html), may be used):

```bash
pip install -r requirements.txt
```

# Running

*** By default, this project is pre-configured to calculate our GeoGebra project from class.
*** To use your own geogebra file, download your GeoGebra file (*.ggb) and unzip (yes, unzip! it is a zip file in secret) it. There, you should find a ``geogebra.xml`` file, which you should move into this project's directory and overwrite the default.

Run the script!

```bash
python analyze_xml.py
```

You should see a png titled ``canvas_TIMESTAMP.png`` in a (new) output directory of ``canvas_saves/``.