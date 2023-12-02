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

### Modify the environments on the docker-compose file

Modify the environments on the docker compose file, using the chart bellow as a guide/reference (remember to use a somewhat decent password/username), and change the permission of the file(s) to avoid other users to access it and read your keys/credentials!

### ready-to-go deploy with docker-compose

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
