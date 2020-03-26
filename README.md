build : 
docker build -t brender_render_node_py_dev_slim --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f Dockerfile.py.dev .

docker build -t brender_render_node_py_dev_slim --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .





dev run : 

docker run --rm -u $(id -u):$(id -g) -it -p 5678:5678 -v $(pwd):/usr/app brender_render_node_py_dev_slim bash