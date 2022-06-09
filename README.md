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

| Environment                 | Default Value                                   | Description                                                                                                                                                                                         |
|-----------------------------|-------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| MINECRAFT_HOSTNAME          | \<Null\>                                        | Hostname/IP to connect to the minecraft server/container.                                                                                                                                           |
| MINECRAFT_QUERY_PORT        | 25565                                           | Port to connect to the minecraft server through the RCON protocol (must be enabled on the server).                                                                                                  |
| MINECRAFT_RCON_PORT         | 25575                                           | *Not being used* Port to connect to the minecraft server through the RCON protocol (must be enabled on the server).                                                                                 |
| MEMCACHED_HOSTNAME          | \<Null\>                                        | Hostname/IP to connect to the memcached server/container.                                                                                                                                           |
| MEMCACHED_PORT              | 11211                                           | Port to connect to the memcached server.                                                                                                                                                            |
| MEMCACHED_USERNAME          | \<Null\>                                        | Username to authenticate to the minecraft server.                                                                                                                                                   |
| MEMCACHED_PASSWORD          | \<Null\>                                        | Password to authenticate to the minecraft server.                                                                                                                                                   |
| DISCORD_TOKEN               | \<Null\>                                        | Hostname/IP to connect to the minecraft server/container.                                                                                                                                           |
| DISCORD_PREFIX              | mc.                                             | Prefix for the discord bot to read the commands.                                                                                                                                                    |
| DISCORD_DESCRIPTION         | Hi, I'm a Bot! <br> My function is to help you! | Description for the bot.                                                                                                                                                                            |
| DISCORD_MC_URL              | \<Null\>                                        | Url to display for the users to join the server.                                                                                                                                                    |
| DISCORD_MC_REFRESH_COOLDOWN | 20                                              | (not implemented yet)(seconds) Cooldown before doing another request to the minecraft server and insert it to the memcached server (while on cooldown will grab the data from the memcached server) |
