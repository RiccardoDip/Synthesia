# CpacVideo
## OFFLINE
### Environment setup LINUX
Create a the conda environment to work locally with:
```
conda env create -f mag_tf.yml
```
If no problems occur, you can now activate the environment and work in it. 

If you experience this problem: 
```
/lib/x86_64-linux-gnu/libstdc++.so.6: version 'GLIBCXX_3.4.29' not found
```
It can be solved with <a href="https://github.com/pybind/pybind11/discussions/3453#discussioncomment-7068951">this</a>.

For other problems, please feel free to open an issue.

If you have the possibility to work with CUDA, you can do the following to exploit your GPU:
```
python3 -m pip install nvidia-cudnn-cu11==8.6.0.163
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$CUDNN_PATH/lib:$CONDA_PREFIX/lib/:$LD_LIBRARY_PATH' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
```
You can verify the installation with:
```
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```
This is an adaptation of the official tensorflow w/o GPU <a href="https://www.tensorflow.org/install/pip?hl=it">installation guide</a>.r