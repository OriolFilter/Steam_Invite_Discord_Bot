# Steam Player Lobby Discord Bot

## Description

Discord bot that posts your Steam lobbies for others to join.

## Invite the bot

Use the following link to invite the "official" bot.

- https://discord.com/oauth2/authorize?client_id=981672056145993759&permissions=84032&scope=bot

If you want to test/try/invite the development/testing bot, use this other link:

- https://discord.com/oauth2/authorize?client_id=793623507384139843&permissions=84032&scope=bot


## FAQ

- Do I need to set an email or password/token from my Steam account or Log In on any way?

No.

The bot will only use and store "vanity URL".

If you receive a message requesting further data than the vanity URL, please contact the bot administrator as there could have been a security breach.

- If I change my steam name will I need to relink my account?

No.

When you link the account, it obtains and stores your Steam ID instead of your Steam **Name**, therefore unless you desire to link a different steam account, there is no need to relink it.

- Which information does this bot store from the users?

It only stores:

Steam vanity url and the ID from the user who submitted such account.

- Is `Shlink` related variables obligatory/required if I don't want to set up the link shortener functionality?

No, you can ignore them.

If any from the both variables (`SHLINK_SERVER_URL` and `SHLINK_TOKEN`) is unset, the functionality won't be enabled.

- Why `God` instead of `Owner` or `BotAdmin` something like that?

I think it's more funny that way. 

## Docker image

Docker image is located here:

- https://hub.docker.com/repository/docker/oriolfilter/steam_invite_discord_bot/general

> **Note:**\
> Image tags/versions don't match the bot versions.
> Recommended to always use the `latest` tag to get the latest version.

## How to run

> **Note:**\
> After generating the bot that will be used, the `Message Content Intent` field on the Discord developer page needs to be enabled.

> **Note:**\
> Hosting a Shlink server will not be covered.

### docker-compose

#### Clone the repo
```shell
git clone https://gitea.filterhome.xyz/ofilter/Steam_Invite_Discord
```
```text
Cloning into 'Steam_Invite_Discord'...
remote: Enumerating objects: 771, done.
remote: Counting objects: 100% (771/771), done.
remote: Compressing objects: 100% (767/767), done.
remote: Total 771 (delta 519), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (771/771), 1.51 MiB | 7.52 MiB/s, done.
Resolving deltas: 100% (519/519), done.
```

#### Set ENV vars

Modify the file `docker-compose.yaml` and set (at least) the environment variables **STEAM_TOKEN** and **DISCORD_TOKEN** for a basic usage.

Username and password are **heavily recommended** to be changed.

> **Note:**\
> The provided `docker-compose.yaml` file is not expected to comply with any security standard, but to provide a usable configuration reference. 

#### Run

```shell
docker compose up
```
<pre><font color="#FF7F7F"><b>➜  </b></font><font color="#7F7FFF"><b>Steam_Invite_Discord</b></font> <font color="#7F7FFF"><b>git:(</b></font><font color="#FF7F7F"><b>master</b></font><font color="#7F7FFF"><b>) </b></font><font color="#FF7F7F"><b>✗</b></font> docker-compose up 
<font color="#7FBAFF">[+] Running 11/11</font>
 <font color="#7F3FBF">✔</font> steam_invite_discord_bot <font color="#CC3980">10 layers</font> [<font color="#7F3FBF">⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿</font>]      0B/0B      Pulled                                                                                                                                                           <font color="#7FBAFF">14.2s </font>
   <font color="#7F3FBF">✔</font> 661ff4d9561e Already exists                                                                                                                                                                                                     <font color="#7FBAFF">0.0s </font>
   <font color="#7F3FBF">✔</font> 44cda88cd45d Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">0.7s </font>
   <font color="#7F3FBF">✔</font> 2cbca0db7eef Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">0.7s </font>
   <font color="#7F3FBF">✔</font> 5c03c2d36281 Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">0.4s </font>
   <font color="#7F3FBF">✔</font> b7fa17f943fb Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">0.9s </font>
   <font color="#7F3FBF">✔</font> 901e8b243d94 Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">5.9s </font>
   <font color="#7F3FBF">✔</font> 13f45f3b068a Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">1.1s </font>
   <font color="#7F3FBF">✔</font> 717e63635303 Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">2.0s </font>
   <font color="#7F3FBF">✔</font> e7ebdb3fa36f Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">1.7s </font>
   <font color="#7F3FBF">✔</font> bdf104ac998a Pull complete                                                                                                                                                                                                      <font color="#7FBAFF">2.4s </font>
<font color="#7FBAFF">[+] Running 2/2</font>
 <font color="#7F3FBF">✔</font> Container steam_invite_db           <font color="#7F3FBF">Recreated</font>                                                                                                                                                                                     <font color="#7FBAFF">0.3s </font>
 <font color="#7F3FBF">✔</font> Container steam_invite_discord_bot  <font color="#7F3FBF">Recreated</font>                                                                                                                                                                                     <font color="#7FBAFF">0.1s </font>
Attaching to steam_invite_db, steam_invite_discord_bot
<font color="#7F7FFF">steam_invite_db           | </font>
<font color="#7F7FFF">steam_invite_db           | </font>PostgreSQL Database directory appears to contain a database; Skipping initialization
<font color="#7F7FFF">steam_invite_db           | </font>
<font color="#7F7FFF">steam_invite_db           | </font>2023-12-27 00:09:23.257 UTC [1] LOG:  starting PostgreSQL 16.1 (Debian 16.1-1.pgdg120+1) on x86_64-pc-linux-gnu, compiled by gcc (Debian 12.2.0-14) 12.2.0, 64-bit
<font color="#7F7FFF">steam_invite_db           | </font>2023-12-27 00:09:23.257 UTC [1] LOG:  listening on IPv4 address &quot;0.0.0.0&quot;, port 5432
<font color="#7F7FFF">steam_invite_db           | </font>2023-12-27 00:09:23.257 UTC [1] LOG:  listening on IPv6 address &quot;::&quot;, port 5432
<font color="#7F7FFF">steam_invite_db           | </font>2023-12-27 00:09:23.268 UTC [1] LOG:  listening on Unix socket &quot;/var/run/postgresql/.s.PGSQL.5432&quot;
<font color="#7F7FFF">steam_invite_db           | </font>2023-12-27 00:09:23.279 UTC [28] LOG:  database system was shut down at 2023-12-27 00:09:22 UTC
<font color="#7F7FFF">steam_invite_db           | </font>2023-12-27 00:09:23.286 UTC [1] LOG:  database system is ready to accept connections
<font color="#CC3980">steam_invite_discord_bot  | </font>Connected!
<font color="#CC3980">steam_invite_discord_bot  | </font>------
<font color="#CC3980">steam_invite_discord_bot  | </font>Logged as
<font color="#CC3980">steam_invite_discord_bot  | </font>MyTestingBot
<font color="#CC3980">steam_invite_discord_bot  | </font>XXXXXXXXXXXXXXXXXX
<font color="#CC3980">steam_invite_discord_bot  | </font>invite me with: https://discord.com/oauth2/authorize?client_id=XXXXXXXXXXXXXXXX&amp;permissions=84032&amp;scope=bot
<font color="#CC3980">steam_invite_discord_bot  | </font>------
</pre>


## Configuration

### Environments

| Environment       | Default Value                                                      | Description                                                                                                                                           |
|-------------------|--------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| STEAM_TOKEN       | \<Null\>                                                           | Steam API token.                                                                                                                                      |
| DISCORD_TOKEN     | \<Null\>                                                           | Discord bot token.                                                                                                                                    |
| DISCORD_PREFIX    | s.                                                                 | Prefix for the discord bot to read the commands.                                                                                                      |
| DISCORD_ACTIVITY  | Use {bot_prefix}help to get a list from all the available commands | Activity  message displayed on the bot. Highly recommended to specify which is the prefix command to use the bot.                                     |
| GOD_DISCORD_ID    | \<Null\>                                                           | Used for certain special commands and stuff. Aka Discord Account ID for the admin of this bot.                                                        |
| DB_HOST           | 127.0.0.1                                                          | Hostname/IP to connect to the database server/container.                                                                                              |
| DB_PORT           | 5432                                                               | Port used to authenticate to the database server.                                                                                                     |
| DB_USERNAME       | \<Null\>                                                           | Username used to authenticate to the database server.                                                                                                 |
| DB_PASSWORD       | \<Null\>                                                           | Password used to authenticate to the database server.                                                                                                 |
| DB_DATABASE       | steam_invite                                                       | Database used to connect                                                                                                                              |
| SHLINK_SERVER_URL | \<Null\>                                                           | Api key from a Shlink server. Not required. If both `SHLINK_SERVER_URL` and `SHLINK_TOKEN` are configured, it will be automatically enabled.          |
| SHLINK_TOKEN      | \<Null\>                                                           | URL for the Shlink API server/service. Not required. If both `SHLINK_SERVER_URL` and `SHLINK_TOKEN` are configured, it will be automatically enabled. |
| HEALTHCHECK_PORT  | 8080                                                               | On which port you wanna run the healthcheck.                                                                                                          |
| REPOSITORY        | https://github.com/OriolFilter/Steam_Lobby_Discord_Bot             | Link to the repository. Requieres to start with "http" or "https"                                                                                     |
| ISSUES            | \<Null\>                                                           | Link to the external wiki, if empty will use `${REPOSITORY}/wiki`. Requieres to start with "http" or "https"                                          |
| WIKI              | \<Null\>                                                           | Link to the external wiki, if empty will use `${REPOSITORY}/issues`. Requieres to start with "http" or "https"                                        |

### Shlink

Shlink is a self-hosted link shortener service.

https://shlink.io/documentation/api-docs/

Needless to say that this project is not associated nor correlated nor whatever, I chose that service out of my own convenience. 

Using a Shlink server might be more advanced than a "minimal setup".

As per the moment **only API v3 is supported.**

### Healthcheck

Healthcheck path is `/healthz`

Port is `8080` by **DEFAULT**, you can select yours by setting an environment variable named `HEALTHCHECK_PORT`.

#### What returns

> Note:\
The status code from the request will match the numeric value specified on the server reply.

The healthcheck web server will return a Json as the following:

```json
{"status_code": 200}
```

The status code can be `200` or `503`.



## Proxy

Regarding running this bot behind a proxied/restricted network.

### Discord

This seems relevant, I didn't test.

- https://discord.com/developers/docs/topics/gateway#connections

- https://discord.com/developers/docs/reference#api-reference-base-url

### Steam

- https://partner.steamgames.com/doc/webapi_overview#addresses
