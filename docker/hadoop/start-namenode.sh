#!/bin/bash

# Démarrer le service SSH
service ssh start

# Formater le NameNode si nécessaire
if [ ! -d "/hadoop/dfs/name/current" ]; then
    echo "Formatting NameNode..."
    $HADOOP_HOME/bin/hdfs namenode -format
fi

# Démarrer le NameNode
echo "Starting NameNode..."
$HADOOP_HOME/bin/hdfs namenode
