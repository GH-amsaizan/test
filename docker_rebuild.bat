docker container prune -f
docker rmi pyrepo_dev
docker build -t pyrepo_dev .
docker run -it pyrepo_dev
