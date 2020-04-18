#!/bin/bash

# References:
# https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/
# https://www.digitalocean.com/community/tutorials/how-to-install-hadoop-in-stand-alone-mode-on-ubuntu-16-04

# Install HDFS on complete new Ubuntu
# Usage:

# For master node
# ./install-hdfs.sh master <master ip>,<data node1 ip>,<data node2 ip>...
# OR
# wget https://gist.github.com/shootsoft/3b6b87dd978a67af9141bcd89a58874b/raw/install-hdfs.sh ; chmod +x install-hdfs.sh ; ./install-hdfs.sh master <master ip>,<data node1 ip>,<data node2 ip>...
# Master node will output trust master host authentication command for data node

# For data node
# ./install-hdfs.sh data <master ip>,<data node1 ip>,<data node2 ip>...
# OR
# wget https://gist.github.com/shootsoft/3b6b87dd978a67af9141bcd89a58874b/raw/install-hdfs.sh ; chmod +x install-hdfs.sh ; ./install-hdfs.sh data <master ip>,<data node1 ip>,<data node2 ip>...

# It is actually going to install entire hadoop package, but I only tested on HDFS part


is_master=$1
ips=$2

if [ -z "$is_master" ] || [ -z "$ips" ]; then
    echo "You mast provide full parameters"
    echo "./install-hdfs.sh master <master ip>,<data node1 ip>,<data node2 ip>..."
    exit
fi

if [ "$is_master" != "master" ] && ["$is_master" != "data" ]; then
    echo "First parameter must be master or data"
    exit
fi

IFS=',' read -ra ip_array <<< "$ips"
master_ip=${ip_array[0]}

echo "Install ${is_master} node"
echo "Master IP: ${master_ip}"
echo "Data node IP:"
for i in "${ip_array[@]}"
do
    echo $i
done

read -p "Are these input correct(y/n)? " -n 1 -r
echo    # (optional) move to a new line
if [[ $REPLY =~ ^[Nn]$ ]];
then
    echo "Exit, please retry with correct parameter."
    exit
fi

if [ "$is_master" == "master" ] && [ ! -f  ~/.ssh/id_rsa.pub ]; then
    echo "Install master, generating keys"
    ssh-keygen -b 4096
    cat ~/.ssh/id_rsa.pub >>  ~/.ssh/authorized_keys
fi

sudo apt update
sudo apt install default-jdk wget -y

wget https://downloads.apache.org/hadoop/common/hadoop-3.1.3/hadoop-3.1.3.tar.gz
tar -xzvf hadoop-3.1.3.tar.gz
sudo mv hadoop-3.1.3 /usr/local/hadoop
java_home=$(readlink -f /usr/bin/java | sed "s:bin/java::")
echo "export JAVA_HOME=${java_home}" | sudo tee -a /usr/local/hadoop/etc/hadoop/hadoop-env.sh

sudo rm -f /usr/local/hadoop/etc/hadoop/core-site.xml.backup
sudo mv /usr/local/hadoop/etc/hadoop/core-site.xml /usr/local/hadoop/etc/hadoop/core-site.xml.backup
cross_site=$(cat <<-END
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>fs.default.name</name>
        <value>hdfs://${master_ip}:9000</value>
    </property>
</configuration>
END
)
echo "$cross_site" > /usr/local/hadoop/etc/hadoop/core-site.xml

sudo mkdir /hadoop
sudo mkdir /hadoop/data
sudo chown $(id -u):$(id -g) -R /hadoop
sudo chmod 777  /hadoop
sudo mkdir /usr/local/hadoop/logs
sudo chown $(id -u):$(id -g) -R /usr/local/hadoop/logs

sudo rm -f /usr/local/hadoop/etc/hadoop/hdfs-site.xml.backup
sudo mv /usr/local/hadoop/etc/hadoop/hdfs-site.xml /usr/local/hadoop/etc/hadoop/hdfs-site.xml.backup
hdfs_site=$(cat <<-END
<configuration>
    <property>
            <name>dfs.namenode.name.dir</name>
            <value>/hadoop/data/nameNode</value>
    </property>

    <property>
            <name>dfs.datanode.data.dir</name>
            <value>/hadoop/data/dataNode</value>
    </property>

    <property>
            <name>dfs.replication</name>
            <value>1</value>
    </property>
    <property>
            <name>dfs.namenode.datanode.registration.ip-hostname-check</name>
            <value>false</value>
    </property>
    <property>
        <name>dfs.permissions.enabled</name>
        <value>false</value>
    </property>
</configuration>
END
)
echo "$hdfs_site" > /usr/local/hadoop/etc/hadoop/hdfs-site.xml



sudo rm -f /usr/local/hadoop/etc/hadoop/mapred-site.xml.backup
sudo mv /usr/local/hadoop/etc/hadoop/mapred-site.xml /usr/local/hadoop/etc/hadoop/mapred-site.xml.backup
mapred_site=$(cat <<-END
<configuration>
    <property>
            <name>mapreduce.framework.name</name>
            <value>yarn</value>
    </property>
    <property>
            <name>yarn.app.mapreduce.am.env</name>
            <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
    <property>
            <name>mapreduce.map.env</name>
            <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
    <property>
            <name>mapreduce.reduce.env</name>
            <value>HADOOP_MAPRED_HOME=/usr/local/hadoop</value>
    </property>
</configuration>
END
)
echo "$mapred_site" > /usr/local/hadoop/etc/hadoop/mapred-site.xml


sudo rm -f /usr/local/hadoop/etc/hadoop/yarn-site.xml.backup
sudo mv /usr/local/hadoop/etc/hadoop/yarn-site.xml /usr/local/hadoop/etc/hadoop/yarn-site.xml.backup
mapred_site=$(cat <<-END
<configuration>
    <property>
            <name>yarn.acl.enable</name>
            <value>0</value>
    </property>

    <property>
            <name>yarn.resourcemanager.hostname</name>
            <value>${master_ip}</value>
    </property>

    <property>
            <name>yarn.nodemanager.aux-services</name>
            <value>mapreduce_shuffle</value>
    </property>
</configuration>
END
)
echo "$mapred_site" > /usr/local/hadoop/etc/hadoop/yarn-site.xml


sudo rm -f /usr/local/hadoop/etc/hadoop/workers.backup
sudo mv /usr/local/hadoop/etc/hadoop/workers /usr/local/hadoop/etc/hadoop/workers.backup
for i in "${ip_array[@]}"
do
    echo $i >> /usr/local/hadoop/etc/hadoop/workers
done


if [ "$is_master" == "master" ]; then
    echo "Please run this command on each data node:"
    echo "echo \"$(cat ~/.ssh/id_rsa.pub)\" >>  ~/.ssh/authorized_keys"
    echo
    echo "After all nodes are installed, use the following command to format HDFS first":
    echo "/usr/local/hadoop/bin/hdfs namenode -format"
    echo
    echo "After all nodes are installed, use the following command to start HDFS":
    echo "/usr/local/hadoop/sbin/start-dfs.sh"
    echo
    echo "Use the following command on each node to verify process"
    echo "jps"
    echo "See https://www.linode.com/docs/databases/hadoop/how-to-install-and-set-up-hadoop-cluster/#run-and-monitor-hdfs"
    echo
    echo "Use the following command on each node to see summary"
    echo "/usr/local/hadoop/bin/hdfs dfsadmin -report"
fi
