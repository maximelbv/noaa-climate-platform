#!/bin/bash

# Démarrer le service SSH
service ssh start

# Démarrer le DataNode
echo "Starting DataNode..."
$HADOOP_HOME/bin/hdfs datanode
