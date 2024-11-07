# HAHSI

This repository provides real-world high-resolution hyperspectral video data recorded by a camera and registered afterwards.
The paper can be found on [Optica](https://opg.optica.org/josaa/fulltext.cfm?uri=josaa-41-12-2303&id=562685) and [arXiv](https://arxiv.org/abs/2407.09038).

Please cite the following publication if you use any of the data or code:
```
@article{Sippel:24,
	author = {Frank Sippel and J\"{u}rgen Seiler and Andr\'{e} Kaup},
	journal = {J. Opt. Soc. Am. A},
	number = {12},
	pages = {2303--2315},
	publisher = {Optica Publishing Group},
	title = {High-resolution hyperspectral video imaging using a hexagonal camera array},
	volume = {41},
	month = {Dec},
	year = {2024},
}
```

All 10 scenes of the hyperspectral video database are available [here](https://drive.google.com/drive/folders/1JeH8EE7LCk4SpaPdNQokO1lJO2ze6uud?usp=sharing).

# Hyperspectral Video Viewer

The folder [viewer](viewer) provides a GUI written in Python to look at the different scenes.
The anaconda environment has to be set up:
```
conda create -n gui python=3.11
conda activate gui
conda install pyqt
conda install numpy
conda install fastai::opencv-python-headless 
pip install pyqtdarktheme
```
Then, the GUI can be started by
```
cd src/
python main.py
```
