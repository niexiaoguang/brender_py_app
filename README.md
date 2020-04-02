build : 
docker build -t brender_py_dev_slim_3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f Dockerfile.py.dev .



dev run : 
docker run -e TZ=Asia/Shanghai --rm -u $(id -u):$(id -g) -it --expose 5671 --expose 80 -v $(pwd):/usr/app brender_py_dev_slim_3.7 bash


build with pyinstaller :
with local package path: 
pyinstaller test_avro.py --onefile -p lib/avro-python3-1.9.2/