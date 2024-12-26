create database monster_battler;
create table if not exists monster_battler.tamers (tamer_id varchar(255) not null primary key, active_battle_id varchar(255) default null, 
tamer_party text, tamer_monster_storage text, archived bool not null default False);

select * from monster_battler.tamers;
use monster_battler;
insert into tamers (tamer_id, tamer_party, tamer_monster_storage) values('bob', '[]', '[]');
update tamers set active_battle_id = 'B-101' where tamer_id = 'bob' and archived = false;
update tamers set active_battle_id = null where tamer_id = 'bob' and archived = false;

