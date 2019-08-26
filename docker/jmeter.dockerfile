FROM openjdk:8-jre-alpine


ARG version=1.0.1
ENV label="Distributed JMeter for scalable load testing"
LABEL \
    app="jmeter_webservice" \
    description=${label} \
    maintainer="Jaishankar Padmanabhan <jai@techjai.com>" \
    version=${version}


ARG JMETER_VERSION
ENV JMETER_VERSION ${JMETER_VERSION:-4.0}
ENV JMETER_HOME /jmeter/apache-jmeter-$JMETER_VERSION
ENV PATH $JMETER_HOME/bin:$PATH

# INSTALL JMETER BASE 
RUN mkdir /jmeter
WORKDIR /jmeter

# INSTALL openjdk8, apache-jmeter, python3, pip3
RUN apk add --update \
    wget tar bash && \
    wget https://archive.apache.org/dist/jmeter/binaries/apache-jmeter-$JMETER_VERSION.tgz && \
    tar -xzf apache-jmeter-$JMETER_VERSION.tgz && \
    rm apache-jmeter-$JMETER_VERSION.tgz 


WORKDIR $JMETER_HOME 

# Copy lib jars, script and user.properties
    
COPY config/user.properties bin/user.properties
COPY lib lib
COPY test test
COPY scripts/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

EXPOSE 1099 50000 

ENTRYPOINT ["/docker-entrypoint.sh"]