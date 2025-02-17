FROM debian:trixie-slim
WORKDIR /

# install app dependencies
RUN apt-get update && apt-get install -y python3 python3-pip
RUN apt-get install -y chromium 

# install app
COPY templated_html_tools.py /

# final configuration
ENTRYPOINT ["python3", "templated_html_tools.py"]
