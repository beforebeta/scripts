alter table main_entity add index idx_permalink (`permalink`);
alter table main_image add index idx_url (`url`);
alter table main_tag add index idx_name (`name`);



alter table main_entity add index idx_founded_company (`founded_year`, `is_company`);