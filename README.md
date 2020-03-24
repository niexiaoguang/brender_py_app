# brender_py_app

build :
docker build -t py_bl_dev_slim --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)  -f Dockerfile.py.dev  .

docker build -t py_bl_dev_slim --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .



dev run :
docker run --rm -u $(id -u):$(id -g) -it -p 5678:5678  -v $(pwd):/usr/app py_dev bash