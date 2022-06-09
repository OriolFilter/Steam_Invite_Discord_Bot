FROM python:alpine
ARG VERSION="0.9"
LABEL "author"="Oriol Filter Anson"
LABEL "version"="${VERSION}"
LABEL "description"="Discord bot mainly used to post Steam's lobby link"
LABEL "repository"="https://github.com/OriolFilter/Steam_Invite_Discord"

ENV VERSION=${VERSION}

ENV STEAM_TOKEN=

ENV DISCORD_TOKEN=
ENV DISCORD_PREFIX="s."
ENV DISCORD_DESCRIPTION="Welcome welcome, I'm a bot"

ENV DB_HOST="127.0.0.1"
ENV DB_PORT=5432
ENV DB_USERNAME=
ENV DB_PASSWORD=
ENV DB_DATABASE="steam_invite"

RUN apk add --no-cache libpq-dev postgresql-dev gcc


WORKDIR /tmp
ADD ./requirements.txt /tmp
RUN pip3 install -r ./requirements.txt --user

ADD ./code /main
WORKDIR /main
RUN chmod +x ./main.py
CMD ["python3","-u","/main/main.py"]
