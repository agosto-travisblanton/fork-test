#
# MySQL Dockerfile
#
# https://github.com/dockerfile/mysql
#

# Pull base image.
FROM ubuntu


ENV DEBIAN_FRONTEND noninteractive

# Install MySQL.
RUN \
  apt-get update && \
  apt-get install -y mysql-client-5.6 mysql-server-5.6 pwgen && \
  rm -rf /var/lib/apt/lists/* && \
  sed -i 's/^\(bind-address\s.*\)/# \1/' /etc/mysql/my.cnf && \
  sed -i 's/^\(log_error\s.*\)/# \1/' /etc/mysql/my.cnf && \
  echo "mysqld_safe &" > /tmp/config && \
  echo "mysqladmin --silent --wait=30 ping || exit 1" >> /tmp/config && \
  echo "mysqladmin --silent --wait=30 create provisioning || exit 1" >> /tmp/config && \
  echo "mysql -e 'GRANT ALL PRIVILEGES ON *.* TO \"root\"@\"%\" WITH GRANT OPTION;'" >> /tmp/config && \
  echo "mysql -e 'FLUSH PRIVILEGES;'" >> /tmp/config  && \
  bash /tmp/config && \
  rm -f /tmp/config \
  service mysql start

# Define mountable directories.
VOLUME ["/etc/mysql", "/var/lib/mysql"]

# Define working directory.
WORKDIR /data

# Expose ports.
EXPOSE 3306

# Define default command.
CMD ["mysqld_safe"]
