drop table if exists relationships;
create table if not exists relationships(
    id serial primary key , -- entry_id
    discord_id varchar(18) not null unique,
    steam_id varchar(17) not null, -- no reason to be unique, people can have multiple discord accounts, or loose access to the previous one
    last_update timestamp null -- last time it was updated
);

-- create or replace function trigger_check_values_relationships()
-- returns Trigger
-- language plpgsql
-- as $$
--     begin
--     case when length(NEW.discord_id)!=18 then
--         RAISE 'discord_id not correct length: % instead of 18', length(new.discord_id) USING ERRCODE = '22026';
--         when length(NEW.steam_id)!=17 then
--         RAISE 'steam_id not correct length: % instead of 18', length(new.steam_id) USING ERRCODE = '22026';
--         else
--             new.last_update=NOW();
--             return new;
--     end case;
--     end;
-- $$;

-- create or replace function trigger_set_last_update_now()
-- returns Trigger
-- language plpgsql
-- as $$
--     begin
--         update relationships as rel set last_update=now() where new.id=rel.id;
--     end;
-- $$;

-- create trigger check_values_insert before insert on relationships for each row execute procedure trigger_check_values_relationships();
-- create trigger check_values_update before update on relationships for each row execute procedure trigger_check_values_relationships();
-- create trigger check_values_update after insert on relationships for each row execute procedure trigger_set_last_update_now();
-- create trigger check_values_update after update on relationships for each row execute procedure trigger_set_last_update_now();

create or replace function func_discord_id_exists(arg_discord_id varchar(18))
returns bool
language plpgsql
as $$
    begin
        case when exists(select rel.id from relationships as rel where rel.discord_id = arg_discord_id)
            then return TRUE;
            else return FALSE;
            end case;
    end;
$$;

create or replace function func_return_steam_id_form_discord_id(arg_discord_id varchar(18))
returns varchar(17)
language plpgsql
as $$
    declare result varchar(17);
    begin
        case when func_discord_id_exists(arg_discord_id) then
            select rel.steam_id into result from relationships as rel where rel.discord_id=arg_discord_id;
            return result;
        else
            RAISE 'steam_id not found from the given discord_id: %', arg_discord_id USING ERRCODE = 'P0002';
    end case;
    end;
$$;


create or replace procedure proc_set_relationship(arg_discord_id varchar(18), arg_steam_id varchar(17))
language plpgsql
as $$
    begin
        case when func_discord_id_exists(arg_discord_id) then
            update relationships as rel set steam_id=arg_steam_id where rel.discord_id=arg_discord_id;
        else
            insert into relationships (discord_id,steam_id) VALUES (arg_discord_id,arg_steam_id);
        end case;
    end;
$$;

create or replace procedure proc_unset_relationship(arg_discord_id varchar(18))
language plpgsql
as $$
    begin
        delete from relationships as rel where rel.discord_id=arg_discord_id;
    end;
$$;

