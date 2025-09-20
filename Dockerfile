FROM jenkins/jenkins:lts
USER root

# Install Docker, AWS CLI, and Python
RUN apt-get update && apt-get install -y \
    docker.io \
    curl \
    unzip \
    python3 \
    python3-pip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws && \
    apt-get clean

RUN usermod -aG docker jenkins
USER jenkins