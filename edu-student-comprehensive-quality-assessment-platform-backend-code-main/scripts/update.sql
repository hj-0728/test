--- 2023-12-16 方卫 创建视图sv_menu
create view sv_menu as (
 WITH RECURSIVE menu_tree AS (
         SELECT m.id,
            m.version,
            m.parent_id,
            NULL::character varying AS parent_name,
            m.name,
            m.code,
            m.path,
            m.icon,
            m.outline,
            m.open_method,
            m.category,
            1 AS level,
            m.seq,
            ARRAY[m.id::text] AS tree_id_list,
            ARRAY[m.seq] AS sort_info
           FROM st_menu m
          WHERE m.parent_id IS NULL
        UNION ALL
         SELECT child.id,
            child.version,
            child.parent_id,
            parent.name AS parent_name,
            child.name,
            child.code,
            child.path,
            child.icon,
            child.outline,
            child.open_method,
            child.category,
            parent.level + 1,
            child.seq,
            array_append(parent.tree_id_list, child.id::text) AS tree_id_list,
            array_append(parent.sort_info, child.seq) AS sort_info
           FROM st_menu child
             JOIN menu_tree parent ON parent.id::text = child.parent_id::text
        )
 SELECT id,
    version,
    parent_id,
    parent_name,
    name,
    code,
    path,
    icon,
    outline,
    open_method,
    category,
    level,
    seq,
    tree_id_list,
    sort_info
   FROM menu_tree
  ORDER BY sort_info
);

--- 2023-12-16 方卫 创建视图sv_k12_dept_tree
drop view if exists sv_k12_dept_tree;
create view sv_k12_dept_tree as (
with recursive tree as (
select sd.id, sd.name, sd.name::text as display_name, null::text as parent_name, st.parent_dept_id, st.id as dimension_dept_tree_id, array[sd.id]::varchar[] as dept_path,
array[st.id]::varchar[] as tree_path, array[st.seq]::integer[] as seq_list
from st_dimension sdi
inner join st_dimension_dept_tree st on st.dimension_id = sdi.id
inner join st_dept sd on sd.id =  st.dept_id
where sdi.code = 'K12' and st.parent_dept_id is null
union all
select sd.id, sd.name, concat(tree.name, '/', sd.name) as display_name, tree.name, st.parent_dept_id, st.id,
array_append(tree.dept_path, sd.id), array_append(tree.tree_path, st.id), array_append(tree.seq_list, st.seq)
from tree
inner join st_dimension_dept_tree st on st.parent_dept_id = tree.id
inner join st_dept sd on sd.id = st.dept_id
)
select * from tree order by seq_list
);


---- 方卫 2024-01-03 创建视图
drop view if exists sv_file_info;
create view sv_file_info as (
select sr.id, sr.file_id, sr.res_category, sr.res_id, sr.relationship, sr.summary,
si.original_name, si.storage_info_id, ssr.bucket_name, ssr.object_name, ssr.checksum, ssr.size
from st_file_relationship sr
inner join st_file_info si on sr.file_id = si.id
inner join st_object_storage_raw ssr on ssr.id = si.storage_info_id
);

drop view if exists sv_file_relationship_public_link;
create view sv_file_relationship_public_link as (
select sr.id, sr.file_id, sr.res_id, sr.res_category, sr.relationship, sl.public_link
from st_file_relationship sr
inner join st_file_public_link sl on sl.file_id = sr.file_id
);


--- 2024-1-4 wu 修改视图sv_menu
drop view if exists sv_menu;
create view sv_menu as (
WITH RECURSIVE menu_tree AS (
         SELECT m.id,
            m.version,
            m.parent_id,
            NULL::character varying AS parent_name,
            m.name,
            m.code,
            m.path,
            m.icon,
            m.outline,
            m.open_method,
            m.category,
            1 AS level,
            m.seq,
            ARRAY[m.id::text] AS tree_id_list,
            ARRAY[m.seq] AS sort_info
           FROM st_menu m
          WHERE m.parent_id IS NULL
        UNION ALL
         SELECT child.id,
            child.version,
            child.parent_id,
            parent.name AS parent_name,
            child.name,
            child.code,
            child.path,
            child.icon,
            child.outline,
            child.open_method,
            child.category,
            parent.level + 1,
            child.seq,
            array_append(parent.tree_id_list, child.id::text) AS tree_id_list,
            array_append(parent.sort_info, child.seq) AS sort_info
           FROM st_menu child
             JOIN menu_tree parent ON parent.id::text = child.parent_id::text
        )
 SELECT menu_tree.id,
    menu_tree.version,
    menu_tree.parent_id,
    menu_tree.parent_name,
    menu_tree.name,
    menu_tree.code,
    menu_tree.path,
    menu_tree.icon,
    menu_tree.outline,
    menu_tree.open_method,
    menu_tree.category,
    menu_tree.level,
    menu_tree.seq,
    menu_tree.tree_id_list,
    menu_tree.sort_info,
        CASE
            WHEN mp.permission_id_list IS NULL THEN ARRAY[]::character varying[]
            ELSE mp.permission_id_list
        END AS permission_id_list,
    mp.permission_name
   FROM menu_tree
     LEFT JOIN ( SELECT apa.assign_resource_id AS menu_id,
            array_agg(apa.ability_permission_id) AS permission_id_list,
            string_agg(DISTINCT ap.name::text, '；'::text) AS permission_name
           FROM st_ability_permission_assign apa
             JOIN st_ability_permission ap ON apa.ability_permission_id::text = ap.id::text AND apa.assign_resource_category::text = 'MENU'::text
          GROUP BY apa.assign_resource_id) mp ON menu_tree.id::text = mp.menu_id::text
  ORDER BY menu_tree.sort_info
);



--- 方卫 2024-01-09 sv_dept_sort
drop view if exists sv_dept_sort;
create view sv_dept_sort as (
select * from (values
  ('一年级', 1),
  ('二年级', 2),
  ('三年级', 3),
  ('四年级', 4),
  ('五年级', 5),
  ('六年级', 6),
  ('七年级', 7),
  ('八年级', 8),
  ('九年级', 9)
) as dept_seq(name, seq)
);

