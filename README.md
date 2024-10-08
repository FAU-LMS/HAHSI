# HAHSI

!!!The paper is submitted to the **Journal of the Optical Society of America A** and currently under review!!!
The submitted paper can be found on [arXiv](https://arxiv.org/abs/2407.09038).

This repository will contain the code and hyperspectral video data of the following publication:
```
@article{sippel2024,
   title={High-Resolution Hyperspectral Video Imaging Using A Hexagonal Camera Array},
   author={Sippel, Frank and Seiler, Jürgen and Kaup, André},
   journal={arXiv preprint arXiv:2407.09038},
   year={2024}
}
```

6 out of 10 scenes of the hyperspectral video database are already available [here](https://drive.google.com/drive/folders/1JeH8EE7LCk4SpaPdNQokO1lJO2ze6uud?usp=sharing).
All scenes will be available upon acceptance.

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
