Mariadb

#### https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/

SteamApi

#### https://partner.steamgames.com/doc/webapi/ISteamUser

#### stats

https://partner.steamgames.com/doc/webapi/ISteamUserStats


#### sessions
mayb can extract current players, would be cool.

https://partner.steamgames.com/doc/webapi/IGameNotificationsService

https://partner.steamgames.com/doc/webapi/IPlayerService


#### Lobbies
Only for publisher api ...
https://partner.steamgames.com/doc/webapi/ILobbyMatchmakingService#GetLobbyData


#### docker
docker pull mariadb:10.8.3
docker run -d -p 3306:3306 --name steamdb --env MARIADB_USER=username --env MARIADB_PASSWORD=password --env MARIADB_ROOT_PASSWORD=password --env MARIADB_DATABASE=steam_invite  mariadb:10.8.3

docker run -d -p 5432:5432 --name steamdb -e POSTGRES_DB=steam_invite -e POSTGRES_USER=username -e POSTGRES_PASSWORD=password postgres:14.3

```
command register/set 
    sets up an account (no prior checking, who cares)
        uses an ID
        pop up embed/message, is this you account? *pops up name*

command invite
    embed with invite + invite info

command status
    prints the current status of your account

status @user
    prints the current status of the user

join @user
    prints the invite to the selected user (if did setup an account)
```

#### https://steamwebapi.azurewebsites.net/