
FROM jmeter:1.0.1
ARG version=1.0.1
ENV label="Flask web service to call JMeter CLI"
LABEL \
    app="jmeter_webservice" \
    description=${label} \
    maintainer="Jaishankar Padmanabhan <jai@techjai.com>" \
    version=${version}

# Get Python, PIP
RUN apk add --update \
    python3 \
    py-pip && pip3 install --upgrade pip

COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]