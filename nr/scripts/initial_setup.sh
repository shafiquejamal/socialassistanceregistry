/usr/bin/wget https://raw.github.com/pypa/virtualenv/master/virtualenv.py
python virtualenv.py private-python
echo 'export PATH=$HOME/private-python/bin:$PATH' >> ~/.bash_profile
source ~/.bash_profile
which python
mkdrir ~/projects/
pip install flup
pip install virtualenvwrapper
python virtualenv.py --no-site-packages av4live
source ~/av4live/bin/activate
pip install flup
pip install virtualenvwrapper
/usr/bin/wget -O Django-1.5.1.tar.gz https://www.djangoproject.com/download/1.5.1/tarball/
tar xzvf Django-1.5.1.tar.gz
cd Django-1.5.1
python setup.py install
python -c "import django; print django.get_version()"
# copy bash profile file
source ~/.bash_profile
mkdir ~/scripts/
touch ~/scripts/update_files.sh
chmod 0755 ~/scripts/update_files.sh

cd ~/html/
# copy .htaccess and dispatch.fcgi files
# upload av4repo
# password protect files

chmod 0755 dispatch.fcgi
cd ~/projects
ln -s ~/projects/testsite/ ~/private-python/lib/python2.6/site-packages/

av4live
add2virtualenv /home/am/amvoliman.com/projects/av4repo/av4

ln -s /home/am/amvoliman.com/projects/av4repo/ /home/am/amvoliman.com/private-python/lib/python2.6/site-packages/av4repo
ln -s /home/am/amvoliman.com/projects/av4repo/av4 /home/am/amvoliman.com/private-python/lib/python2.6/site-packages/av4

# export the masking key
# export MASKING_KEY= # whateer
# export SECTRET_KEY='dfasfasdfasfdasdfhetweywyrwerdsf'
# on the local development server, add these to the activate script for your virtual environment
# on the testing and production server, add these to .bash_profile
