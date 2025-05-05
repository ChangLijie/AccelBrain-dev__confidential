# AccelBrain

AccelBrain is a project focused on launching an efficient chatbot by integrating multiple powerful frameworks and tools. The architecture combines ChatBot, Model Server, and Model Handler to ensure seamless operation and optimized performance.

## The architecture of AccelBrain is designed as follows:

![](./docs/accelbrain.svg)

1. **ChatBot**

   -  Provides the user interaction interface.

2. **Model Server**

   -  Handles efficient model requests, managing load distribution and resource allocation.

3. **Model Handler**

   - Allows uploading and deploying models trained using Innodisk training tools (AccelTune).

## Installation and Usage

### Requirements

* Basic
  * [Docker 20.10 + ](https://docs.docker.com/engine/install/ubuntu/)
    * `Docker Compose` > `v2.15.X`
      * **[ VERIFY ]** Use this command ( `docker compose version` ).
      * **[ INSTALL ]** Install the docker-compose by following this [document](https://docs.docker.com/compose/install/linux/#install-using-the-repository) if you don't have docker compose.
* For NVIDIA `dGPU`
  * [NVIDIA GPU Driver](https://docs.nvidia.com/datacenter/tesla/tesla-installation-notes/index.html)
  * [NVIDIA Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#step-1-install-nvidia-container-toolkit)
      * **Prerequisites**
         * You installed a supported container engine (Docker, Containerd, CRI-O, Podman).

         * You installed the NVIDIA Container Toolkit.

      * **Configuring Docker** 

         1. Configure the container runtime by using the nvidia-ctk command:
               ```
               sudo nvidia-ctk runtime configure --runtime=docker
               ```
               The nvidia-ctk command modifies the /etc/docker/daemon.json file on the host. The file is updated so that Docker can use the NVIDIA Container Runtime.
            
         2. Restart the Docker daemon:
               ```
               sudo systemctl restart docker
            ```
### Usage

1. Clone the repository:

   ```bash
   https://github.com/ChangLijie/AccelBrain-dev__confidential.git
   cd AccelBrain-dev__confidential
   ```

2. Launch Docker containers:
   * (Recommended) GUI executable: (Double-click AccelBrainLauncher.exe or run)
      ```bash
      ./AccelBrainLauncher.exe
      ```
   * Shell script 
      ```bash
      sudo ./run.sh
      ```
   - Access the provided URL in a browser to use AccelBrain.(Default)
        ```
        127.0.0.1:3000
        ```
3. Stop Docker containers
   * (Recommended) GUI executable: (Double-click ShutDown.exe or run)
      ```bash
      ./ShutDown.exe
      ```
   * Shell script 
      ```bash
      sudo ./stop.sh
      ```
4. Optional - Modify startup parameters via GUI
   * (Recommended) GUI executable: (Double-click Setting.exe or run)
      ```bash
      ./Setting.exe
      ```
 