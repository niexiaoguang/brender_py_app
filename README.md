# brender_py_app

build :
docker build -t py_dev --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g)  -f Dockerfile.py.dev  .

dev run :
docker run --rm -u $(id -u):$(id -g) -it --expose=5671 -p 9000:9000  -v $(pwd):/usr/app py_dev bash