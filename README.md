# AcclBrain

AcclBrain is a project focused on launching an efficient chatbot by integrating multiple powerful frameworks and tools. The architecture combines OpenWeb UI, Ollama, and Model Handler to ensure seamless operation and optimized performance.

## The architecture of AcclBrain is designed as follows:

![](./docs/architecture.svg)

1. **OpenWeb UI**

   -  Provides the user interaction interface.

2. **Ollama**

   -  Handles efficient model requests, managing load distribution and resource allocation.

3. **Model Handler**

   - Allows uploading and deploying models trained using Innodisk training tools.

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

### Usage

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/AccelBrain-dev__confidential.git
   cd AccelBrain-dev__confidential
   ```

2. Launch Docker containers:

   ```bash
   docker compose -f ./docker-compose.yml up -d
   ```
3. Stop Docker containers
    ```bash
   docker compose -f ./docker-compose.yml down
   ```

