build : 
docker build -t brender_render_node_py_dev_slim --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) -f Dockerfile.py.dev .

docker build -t brender_render_node_py_dev_slim --build-arg USER_ID=$(id -u) --build-arg GROUP_ID=$(id -g) .





dev run : 
for ftp and amqp
docker run --rm -u $(id -u):$(id -g) -it --expose 5671 --expose 22121 -v $(pwd):/usr/app brender_render_node_py_dev_slim bash
