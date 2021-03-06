create unique index unique_daily_1990_1994_tscode_date on daily_1990_1994 (ts_code,trade_date);
create index ind_daily_1990_1994_tscode on daily_1990_1994(ts_code);
create index ind_daily_1990_1994_trade_date on daily_1990_1994(trade_date);

create unique index unique_daily_1995_1999_tscode_date on daily_1995_1999 (ts_code,trade_date);
create index ind_daily_1995_1999_tscode on daily_1995_1999(ts_code);
create index ind_daily_1995_1999_trade_date on daily_1995_1999(trade_date);

create unique index unique_daily_2000_2004_tscode_date on daily_2000_2004 (ts_code,trade_date);
create index ind_daily_2000_2004_tscode on daily_2000_2004(ts_code);
create index ind_daily_2000_2004_trade_date on daily_2000_2004(trade_date);

create unique index unique_daily_2005_2009_tscode_date on daily_2005_2009 (ts_code,trade_date);
create index ind_daily_2005_2009_tscode on daily_2005_2009(ts_code);
create index ind_daily_2005_2009_trade_date on daily_2005_2009(trade_date);

create unique index unique_daily_2010_2014_tscode_date on daily_2010_2014 (ts_code,trade_date);
create index ind_daily_2010_2014_tscode on daily_2010_2014(ts_code);
create index ind_daily_2010_2014_trade_date on daily_2010_2014(trade_date);

create unique index unique_daily_2015_2019_tscode_date on daily_2015_2019 (ts_code,trade_date);
create index ind_daily_2015_2019_tscode on daily_2015_2019(ts_code);
create index ind_daily_2015_2019_trade_date on daily_2015_2019(trade_date);

create unique index unique_daily_2020_2024_tscode_date on daily_2020_2024 (ts_code,trade_date);
create index ind_daily_2020_2024_tscode on daily_2020_2024(ts_code);
create index ind_daily_2020_2024_trade_date on daily_2020_2024(trade_date);

alter table daily_1990_1994 add column trade_date_int int;
update daily_1990_1994 set trade_date_int = cast(trade_date as unsigned);
create index ind_daily_1990_1994_trade_date_int on daily_1990_1994(trade_date_int);

alter table daily_1995_1999 add column trade_date_int int;
update daily_1995_1999 set trade_date_int = cast(trade_date as unsigned);
create index ind_daily_1995_1999_trade_date_int on daily_1995_1999(trade_date_int);

alter table daily_2000_2004 add column trade_date_int int;
update daily_2000_2004 set trade_date_int = cast(trade_date as unsigned);
create index ind_daily_2000_2004_trade_date_int on daily_2000_2004(trade_date_int);

alter table daily_2005_2009 add column trade_date_int int;
update daily_2005_2009 set trade_date_int = cast(trade_date as unsigned);
create index ind_daily_2005_2009_trade_date_int on daily_2005_2009(trade_date_int);

alter table daily_2010_2014 add column trade_date_int int;
update daily_2010_2014 set trade_date_int = cast(trade_date as unsigned);
create index ind_daily_2010_2014_trade_date_int on daily_2010_2014(trade_date_int);

alter table daily_2015_2019 add column trade_date_int int;
update daily_2015_2019 set trade_date_int = cast(trade_date as unsigned);
create index ind_daily_2015_2019_trade_date_int on daily_2015_2019(trade_date_int);

alter table daily_2020_2024 add column trade_date_int int;
update daily_2020_2024 set trade_date_int = cast(trade_date as unsigned);
create index ind_daily_2020_2024_trade_date_int on daily_2020_2024(trade_date_int);