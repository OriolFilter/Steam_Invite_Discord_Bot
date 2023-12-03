# Steam Lobby Discord Bot

## Description

Discord bot that shows the status of your minecraft server making usage of the Query requests.

## Requirements

```bash
docker
docker-compose
git
```

## How to run


### Build the docker image

First thing first, we will build the docker image.

```bash
docker-compose build
```

<pre>[+] Building 21.2s (14/14) FINISHED                                                                                                                                                                                        docker:default
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot internal] load build definition from Dockerfile                                                                                                                                                        0.0s</font>
<font color="#7FBAFF"> =&gt; =&gt; transferring dockerfile: 1.07kB                                                                                                                                                                                               0.0s</font>
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot internal] load .dockerignore                                                                                                                                                                           0.0s</font>
<font color="#7FBAFF"> =&gt; =&gt; transferring context: 2B                                                                                                                                                                                                      0.0s</font>
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot internal] load metadata for docker.io/library/python:3.11-alpine                                                                                                                                       0.4s</font>
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot internal] load build context                                                                                                                                                                           0.0s</font>
<font color="#7FBAFF"> =&gt; =&gt; transferring context: 707B                                                                                                                                                                                                    0.0s</font>
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 1/9] FROM docker.io/library/python:3.11-alpine@sha256:64bf6d40f8bbb4f7565642494bb267aa92f1ce1beade6c1a8a3581688abf7a52                                                                                 1.4s</font>
<font color="#7FBAFF"> =&gt; =&gt; resolve docker.io/library/python:3.11-alpine@sha256:64bf6d40f8bbb4f7565642494bb267aa92f1ce1beade6c1a8a3581688abf7a52                                                                                                          0.0s</font>
...
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 3/9] RUN apk add build-base postgresql-dev libpq                                                                                                                                                       4.1s</font> 
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 4/9] WORKDIR /tmp                                                                                                                                                                                      0.1s</font> 
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 5/9] ADD ./requirements.txt /tmp                                                                                                                                                                       0.1s</font> 
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 6/9] RUN pip3 install -r /tmp/requirements.txt --user                                                                                                                                                 11.9s</font> 
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 7/9] ADD ./code /main                                                                                                                                                                                  0.1s</font> 
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 8/9] WORKDIR /main                                                                                                                                                                                     0.1s</font> 
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot 9/9] RUN chmod +x ./main.py                                                                                                                                                                            0.3s</font> 
<font color="#7FBAFF"> =&gt; [steam_invite_discord_bot] exporting to image                                                                                                                                                                                    2.0s</font> 
<font color="#7FBAFF"> =&gt; =&gt; exporting layers                                                                                                                                                                                                              1.9s</font> 
<font color="#7FBAFF"> =&gt; =&gt; writing image sha256:ca13e7f02f6d5d911984e287dc014f4a30643d06c4996d7c7ed772b6b2c34514                                                                                                                                         0.0s</font> 
<font color="#7FBAFF"> =&gt; =&gt; naming to docker.io/library/steam_invite_discord_bot:latest                                                                                                                                                                   0.0s</font></pre>

### Modify the environments on the docker-compose file

Modify the environments on the docker compose file, using the [Environments table](#environments) as a guide/reference.

Keep in mind that the username / password should be kept securely stored as best practices.

Note that the `docker-compose.yaml` template shared is not intended to comply with the docker best practices when it comes to container security.

As well, it's a **requirement** to have a Steam API key, and a Discord Bot API key.

### Start the containers

Finally, we can start the containers.

```bash
docker-compose up -d
```

### Update container to a newer version

Set the `latest` tag to automatically pull the latest version, 
```yaml
service_name:
  image:  <dockerimage>:latest
```

Afterwards, proceed to download the last version of the image using `docker-compose` command

```shell
docker-compose pull
```

Finally, relaunch the containers with the last downloaded image and let `docker-compose` deal with the containers for you

```shell
docker-compose up -d
```




## Configuration

### Environments

| Environment         | Default Value                                                      | Description                                                                                                       |
|---------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| STEAM_TOKEN         | \<Null\>                                                           | Steam API token.                                                                                                  |
| DISCORD_TOKEN       | \<Null\>                                                           | Discord bot token.                                                                                                |
| DISCORD_PREFIX      | s.                                                                 | Prefix for the discord bot to read the commands.                                                                  |
| DISCORD_ACTIVITY    | Use {bot_prefix}help to get a list from all the available commands | Activity  message displayed on the bot. Highly recommended to specify which is the prefix command to use the bot. |
| DISCORD_DESCRIPTION | Discord bot mainly used to get Steam's lobby link                  | Description for the bot (visible during the help command).                                                        |
| DB_HOST             | 127.0.0.1                                                          | Hostname/IP to connect to the database server/container.                                                          |
| DB_PORT             | 5432                                                               | Port used to authenticate to the database server.                                                                 |
| DB_USERNAME         | \<Null\>                                                           | Username used to authenticate to the database server.                                                             |
| DB_PASSWORD         | \<Null\>                                                           | Password used to authenticate to the database server.                                                             |
| DB_DATABASE         | steam_invite                                                       | Database used to connect                                                                                          |
