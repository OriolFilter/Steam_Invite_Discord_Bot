ARG IMAGE="python"
ARG TAG="3-alpine"
ARG BASEIMAGE="${IMAGE}:${TAG:-latest}"

FROM ${BASEIMAGE} as build

ARG VERSION="1.0"
ARG BUILDDATE="02/Dec/2023"
LABEL "author"="Oriol Filter Anson"
LABEL "version"="${VERSION}"
LABEL "description"="Discord bot mainly used to post Steam's lobby link"
LABEL "repository"="https://github.com/OriolFilter/Steam_Invite_Discord"
LABEL "BUILDDATE"="${BUILDDATE}"

ENV VERSION=${VERSION}
ENV BUILDDATE=${BUILDDATE}

ENV STEAM_TOKEN=""

ENV DISCORD_TOKEN=""
ENV DISCORD_PREFIX="s."
ENV DISCORD_DESCRIPTION=""

ENV DB_HOST="127.0.0.1"
ENV DB_PORT=5432
ENV DB_USERNAME=""
ENV DB_PASSWORD=""
ENV DB_DATABASE="steam_invite"

RUN apk update --no-cache
RUN apk add build-base postgresql-dev libpq


WORKDIR /tmp
ADD ./requirements.txt /tmp
RUN pip3 install -r /tmp/requirements.txt --user

ADD ./code /main
WORKDIR /main
RUN chmod +x ./main.py
CMD ["python3","-u","/main/main.py"]