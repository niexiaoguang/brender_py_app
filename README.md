build : 
docker build -t brender_py_dev_slim_3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f Dockerfile.py.dev .



dev run : 
docker run --rm -u $(id -u):$(id -g) -it --expose 5671 --expose 22121 -v $(pwd):/usr/app brender_py_dev_slim_3.7 bash


build with pyinstaller :
with local package path: 
pyinstaller test_avro.py --onefile -p avro-python3-1.9.2/