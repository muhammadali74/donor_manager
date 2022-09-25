FROM python:3

# set work directory
WORKDIR /app

ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn

RUN set -e; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        software-properties-common \
    ; \
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 0xB1998361219BD9C9; \
    apt-add-repository 'deb http://repos.azulsystems.com/debian stable main'; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
        zulu-11 \
    ; \
    apt-get clean; \
    rm -rf /var/tmp/* /tmp/* /var/lib/apt/lists/*

RUN set -e; \
    pip install JPype1

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

# ENV PATH="/scripts:${PATH}"

# RUN apk add -update

# RUN pip install -r requirements.txt
# COPY . /app
# RUN apk del.tmp

# Install OpenJDK-8
# RUN apt-get update && \
#     apt-get install -y openjdk-8-jdk && \
#     apt-get install -y ant && \
#     apt-get clean;

# # Fix certificate issues
# RUN apt-get update && \
#     apt-get install ca-certificates-java && \
#     apt-get clean && \
#     update-ca-certificates -f;

# # Setup JAVA_HOME -- useful for docker commandline
# ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/
# RUN export JAVA_HOME

# RUN mkdir /set_manager
# COPY ./set_manager /set_manager

# WORKDIR /set_manager
# COPY ./scripts /scripts

# RUN chmod +x /scripts/*

# RUN mkdir -p /vol/web/media
# RUN mkdir -p /vol/web/static

# RUN adduser -D user
# RUN chown -R user:user /vol
# RUN chmod -R 755 /vol/web
# USER user
# USER root

# CMD ["entryoint.sh"]




