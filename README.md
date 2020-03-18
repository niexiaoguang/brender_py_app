
build :
docker build -t py_dev_3.7 --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)  -f Dockerfile.py.dev  .

dev run for mqtt:
docker run --rm -u $(id -u):$(id -g) -it --expose 1883 --expose 5671  -v $(pwd):/usr/app py_dev_3.7 bash


for local python setup install libs:
pip3 install -r requirements.txt -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com