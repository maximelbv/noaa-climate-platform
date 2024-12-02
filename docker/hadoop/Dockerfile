FROM ubuntu:20.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    openssh-server openjdk-8-jdk wget curl rsync sudo && apt-get clean

# Set up SSH for Hadoop
RUN mkdir -p /var/run/sshd && echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config
RUN echo "root:root" | chpasswd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

# Generate SSH keys for root
RUN ssh-keygen -t rsa -f /root/.ssh/id_rsa -q -N ""
RUN cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys && chmod 600 /root/.ssh/authorized_keys

# Set Hadoop environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV HADOOP_VERSION=3.3.5
ENV HADOOP_HOME=/opt/hadoop
ENV PATH=$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

# Download Hadoop
RUN wget https://dlcdn.apache.org/hadoop/common/hadoop-$HADOOP_VERSION/hadoop-$HADOOP_VERSION.tar.gz && \
    tar -xzvf hadoop-$HADOOP_VERSION.tar.gz -C /opt && \
    mv /opt/hadoop-$HADOOP_VERSION /opt/hadoop && rm hadoop-$HADOOP_VERSION.tar.gz

# Copy configuration files
COPY core-site.xml $HADOOP_HOME/etc/hadoop/core-site.xml
COPY hdfs-site.xml $HADOOP_HOME/etc/hadoop/hdfs-site.xml
COPY hadoop-env.sh $HADOOP_HOME/etc/hadoop/hadoop-env.sh

# Conditionally copy start scripts
# Use different scripts for NameNode and DataNode
ARG NODE_TYPE=namenode
COPY start-$NODE_TYPE.sh /start-$NODE_TYPE.sh
RUN chmod +x /start-$NODE_TYPE.sh

# Expose necessary ports
# 9870: NameNode Web UI, 9000: HDFS RPC port, 9864: DataNode Web UI
EXPOSE 9000 9870 9864

# Start Hadoop
CMD ["/bin/bash", "/start-namenode.sh"]
