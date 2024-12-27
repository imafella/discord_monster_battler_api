use monster_battler;

create table if not exists monster_battler.monsters (monster_id varchar(255) not null primary key, monster_species_id varchar(255) not null, 
monster_species_form int not null default 1, monster_name varchar(50) default null, level int not null default 1, exp_total double not null default 0 ,archived bool not null default False);

create table if not exists monster_battler.monster_stats (monster_id varchar(255) not null primary key, archived bool not null default False, 
hp int default 0, pAttk int default 0, pDef int default 0, sAttk int default 0, sDef int default 0, spd int default 0);
create table if not exists monster_battler.monster_IVs (monster_id varchar(255) not null primary key, archived bool not null default False, 
hp int default 0, pAttk int default 0, pDef int default 0, sAttk int default 0, sDef int default 0, spd int default 0);
create table if not exists monster_battler.monster_EVs (monster_id varchar(255) not null primary key, archived bool not null default False, 
hp int default 0, pAttk int default 0, pDef int default 0, sAttk int default 0, sDef int default 0, spd int default 0);

create table if not exists monster_battler.monster_species (monster_species_id varchar(255) not null, monster_species_form int not null default 1, monster_species_name varchar(255) not null, 
archived  bool not null default false, primary key (monster_species_id, monster_species_form));
create table if not exists monster_battler.monster_species_base_stats (monster_species_id varchar(255) not null, monster_species_form int not null , archived bool not null default False, 
hp int default 0, pAttk int default 0, pDef int default 0, sAttk int default 0, sDef int default 0, spd int default 0, primary key(monster_species_id, monster_species_form));

insert into monster_species (monster_species_id, monster_species_name) values('','');
select * from monster_species where monster_species_id = 1 and archived = 0;
insert into monsters (monster_id, monster_species_id, monster_species_form, monster_name) values('', '', '');