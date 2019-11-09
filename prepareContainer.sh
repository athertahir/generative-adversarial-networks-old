# pip install --upgrade pip
# pip install matplotlib_venn 


# pip install keras
# pip install Pillow

echo 'Installing Dependencies'

pip install opencv-python
pip install mtcnn
pip install numpy==1.16.0

pip install pydot
pip install graphviz

pip install git+https://github.com/rcmalli/keras-vggface.git

sudo yes | add-apt-repository ppa:gviz-adm/graphviz-dev
sudo apt-get update
sudo yes | apt-get install graphviz-dev

# conda install theano
# conda install -c conda-forge tensorflow
# conda install graphviz
# conda install pydotplus -y
conda install graphviz -y