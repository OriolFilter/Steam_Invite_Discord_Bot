# Mosscraft

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

## Configuration

### Environments

| Environment         | Default Value              | Description                                              |
|---------------------|----------------------------|----------------------------------------------------------|
| STEAM_TOKEN         | \<Null\>                   | Steam API token.                                         |
| DISCORD_TOKEN       | \<Null\>                   | Discord bot token.                                       |
| DISCORD_PREFIX      | s.                         | Prefix for the discord bot to read the commands.         |
| DISCORD_DESCRIPTION | Welcome welcome, I'm a bot | Description for the bot.                                 |
| DB_HOST             | 127.0.0.1                  | Hostname/IP to connect to the database server/container. |
| DB_PORT             | 5432                       | Port used to authenticate to the database server.        |
| DB_USERNAME         | \<Null\>                   | Username used to authenticate to the database server.    |
| DB_PASSWORD         | \<Null\>                   | Password used to authenticate to the database server.    |
| DB_DATABASE         | steam_invite               | Database used to connect                                 |
