use seotester;
create index idx_url on main_backlink (crawl_id, url_255);
create index idx_backlinkurl on main_backlink (crawl_id, backlink_url_255);