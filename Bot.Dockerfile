FROM python:alpine
ARG VERSION="0.9"
LABEL "author"="Oriol Filter Anson"
LABEL "version"="${VERSION}"
LABEL "description"="Discord bot mainly used to post Steam's lobby link"
LABEL "repository"="https://github.com/OriolFilter/Steam_Invite_Discord"

ENV DISCORD_TOKEN=
ENV DISCORD_PREFIX="s."
ENV DISCORD_DESCRIPTION="Welcome welcome, I'm a bot"

ENV DB_DATABASE="127.0.0.1"
ENV DB_USERNAME=
ENV DB_PASSWORD=
ENV DB_HOST=
ENV DB_PORT=5432
ENV VERSION=${VERSION}

ADD ./code /main
WORKDIR /main
RUN pip3 install -r ./requirements.txt --user
WORKDIR /main
RUN chmod +x ./main.py
CMD ["python3","-u","/main/main.py"]
