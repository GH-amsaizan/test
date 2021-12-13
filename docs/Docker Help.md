Docker Help
---
### Definitions

**Dockerfile** - master file that defines a docker container, using Docker commands that implement shell scripting and language specific instructions.

**Image** - A set of files that will define an image but have no state. Usually a linux operating system like ubuntu or debian with other settings and files loaded in.

**Container** - A lightweight virtual machine that runs on a built image and contains state.

**CLI** - Command line interface. For Windows, either **Command Prompt** or **Powershell**. For Docker containers using linux, it is called **BASH**.

### General Info
Running a docker container happens in three general steps

1. Pull
2. Build
3. Run

Further explanation of these steps happens below.

For help when using docker on the command line, type `docker --help`

### Build an image from local Dockerfile
Now that you have either downloaded a Github Repo with a Dockerfile, use these steps to build your image. If you used docker pull to get an image from Docker Hub, that image is already built so you can skip to the Run a Container section.

1. Open a CLI
2. `cd` to the local folder where the Dockerfile is stored or the repo resides.
3. Run `docker build --no-cache --rm -t <name> .` from within the repo to build the image. <name> can be any image name you want. Docker will detect the Dockerfile and other files to build the image from.

	-t tag the name specified to the image
	--rm remove intermediate images
	--no-cache does not save a cache of components for subsequent builds. This ensure that all changes get propogated to an image when it is re-built.

Docker Website: [docker build](https://docs.docker.com/engine/reference/commandline/build/)

### Run a Container
The following CLI commands will run built images in different ways
	
`docker run -d -p PORT:PORT <image name or path>`
Runs a new container instance of image <image name>. If the image has exposed output to a port, then substitute the port number for PORT in PORT:PORT

	-d run container detached, in the background. Useful if you are accessing a service through a port, such as the Airflow webserver.
	-p port number specification, for example -p HOST:CONTAINER. Note that this port needs to be exposed by the image for you to access it from a browser in Windows.
	

`docker run -it ubuntu bash`
Runs a container interactively using the latest version of ubuntu and opens the bash shell

	-it enables interactivity with the image from a CLI

If docker doesn't detect a local copy of the image when you use docker run, it will try to pull and build it from an online version.

Docker Website: [docker run](https://docs.docker.com/engine/reference/commandline/run/)

### Bind mount directory to the container
If you want changes in the container to persist on the host machine (your laptop in this case), then bind mounting will help achieve that goal. Bind mounting will mount your local directory to the container, and any changes to the volume on the host of container will propagate to the other. The changes will persist after the container stops running.

`docker run -v LOCAL_DIR:CONTAINER_DIR`