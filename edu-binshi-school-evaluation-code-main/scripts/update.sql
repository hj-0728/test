-- 初始化视图
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

create view sv_ability_permission_group as (
  WITH RECURSIVE ability_permission_group AS (
         SELECT apg.id,
            apg.version,
            apg.code,
            ARRAY[apg.id::text] AS tree_id_list,
            NULL::character varying AS parent_id,
            NULL::character varying AS parent_name,
            apg.name,
            1 AS level,
            apt.id AS tree_id,
            apt.version AS tree_version,
            apt.seq,
            ARRAY[apt.seq] AS sort_info
           FROM st_ability_permission_group apg
             JOIN st_ability_permission_tree apt ON apg.id::text = apt.child_resource_id::text AND apt.child_resource_category::text = 'ABILITY_PERMISSION_GROUP'::text AND apt.ability_permission_group_id IS NULL
        UNION ALL
         SELECT child.id,
            child.version,
            child.code,
            array_append(parent.tree_id_list, child.id::text) AS tree_id_list,
            parent.id AS parent_id,
            parent.name AS parent_name,
            child.name,
            parent.level + 1,
            apt.id AS tree_id,
            apt.version AS tree_version,
            apt.seq,
            array_append(parent.sort_info, apt.seq) AS sort_info
           FROM st_ability_permission_group child
             JOIN st_ability_permission_tree apt ON child.id::text = apt.child_resource_id::text AND apt.child_resource_category::text = 'ABILITY_PERMISSION_GROUP'::text
             JOIN ability_permission_group parent ON apt.ability_permission_group_id::text = parent.id::text
        )
 SELECT ability_permission_group.id,
    ability_permission_group.version,
    ability_permission_group.code,
    ability_permission_group.tree_id_list,
    ability_permission_group.parent_id,
    ability_permission_group.parent_name,
    ability_permission_group.name,
    ability_permission_group.level,
    ability_permission_group.tree_id,
    ability_permission_group.tree_version,
    ability_permission_group.seq,
    ability_permission_group.sort_info
   FROM ability_permission_group
  ORDER BY ability_permission_group.sort_info, ability_permission_group.name
);

create view sv_ability_permission as (
 WITH RECURSIVE permission_tree AS (
         SELECT spf.id,
            spf.version,
            spf.tree_id_list,
            spf.parent_id,
            spf.parent_name,
            spf.name,
            spf.code,
            spf.level,
            spf.tree_id,
            spf.tree_version,
            spf.seq,
            spf.sort_info,
            'ABILITY_PERMISSION_GROUP'::text AS node_type
           FROM sv_ability_permission_group spf
        UNION ALL
         SELECT child.id,
            child.version,
            array_append(parent.tree_id_list, child.id::text) AS tree_id_list,
            parent.id AS parent_id,
            parent.name AS parent_name,
            child.name,
            child.code,
            parent.level + 1 AS level,
            child.tree_id,
            child.tree_version,
            child.seq,
            array_append(parent.sort_info, child.seq) AS sort_info,
            'ABILITY_PERMISSION'::text AS node_type
           FROM ( SELECT sp.id,
                    sp.version,
                    sp.name,
                    sp.code,
                    us.seq,
                    us.id AS tree_id,
                    us.version AS tree_version,
                    us.ability_permission_group_id
                   FROM st_ability_permission_tree us
                     JOIN st_ability_permission sp ON sp.id::text = us.child_resource_id::text AND us.child_resource_category::text = 'ABILITY_PERMISSION'::text) child
             JOIN permission_tree parent ON parent.id::text = child.ability_permission_group_id::text
        )
 SELECT pt.id,
    pt.version,
    pt.tree_id_list,
    pt.parent_id,
    pt.parent_name,
    pt.name,
    pt.code,
    pt.level,
    pt.tree_id,
    pt.tree_version,
    pt.seq,
    pt.sort_info,
    pt.node_type
   FROM permission_tree pt
UNION
 SELECT sp.id,
    sp.version,
    ARRAY[sp.id::text] AS tree_id_list,
    NULL::character varying AS parent_id,
    NULL::character varying AS parent_name,
    sp.name,
    sp.code,
    1 AS level,
    us.id AS tree_id,
    us.version AS tree_version,
    us.seq,
    ARRAY[us.seq] AS sort_info,
    'ABILITY_PERMISSION'::text AS node_type
   FROM st_ability_permission sp
     JOIN st_ability_permission_tree us ON us.child_resource_id::text = sp.id::text AND us.child_resource_category::text = 'ABILITY_PERMISSION'::text AND us.ability_permission_group_id IS NULL
  ORDER BY 8
);


----- 张旭盈 创建sv_evaluation_criteria_plan 20230726
CREATE view sv_evaluation_criteria_plan as
SELECT cp.*, ec.name as evaluation_criteria_name, ec.status as evaluation_criteria_status,
ec.evaluation_object_category FROM st_evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria ec on cp.evaluation_criteria_id = ec.id
WHERE ec.status <> 'DRAFT'


-- wyp 2023-08-02 sv_dimension_dept_tree

CREATE view sv_dimension_dept_tree as
(
 WITH RECURSIVE dept_tree(id, name, organization_id, route_name, display_name, dept_tree_id, dimension_id, seq, parent_dept_id, parent_dept_id_list, level, sort_info) AS (
         SELECT d.id,
            d.name,
            d.organization_id,
            d.name::text AS route_name,
            d.name::text AS display_name,
            t.id AS dept_tree_id,
            t.dimension_id,
            t.seq,
            t.parent_dept_id,
            ARRAY[d.id::text] AS parent_dept_id_list,
            1 AS level,
            ARRAY[t.seq] AS sort_info
           FROM st_dimension_dept_tree t
             JOIN st_dept d ON t.dept_id::text = d.id::text
          WHERE t.parent_dept_id IS NULL AND t.finish_at > now() AND d.finish_at > now()
        UNION
         SELECT d.id,
            d.name,
            d.organization_id,
            (dt_1.route_name || '/'::text) || d.name::text AS route_name,
            (dt_1.name::text || '/'::text) || d.name::text AS display_name,
            t.id AS dept_tree_id,
            t.dimension_id,
            t.seq,
            t.parent_dept_id,
            array_append(dt_1.parent_dept_id_list, d.id::text) AS parent_dept_id_list,
            dt_1.level + 1 AS level,
            array_append(dt_1.sort_info, t.seq) AS sort_info
           FROM st_dimension_dept_tree t
             JOIN st_dept d ON t.dept_id::text = d.id::text
             JOIN dept_tree dt_1 ON dt_1.id::text = t.parent_dept_id::text AND dt_1.dimension_id::text = t.dimension_id::text
          WHERE t.finish_at > now() AND d.finish_at > now()
        )
 SELECT dt.id,
    dt.name,
    dt.organization_id,
    dt.route_name,
    dt.display_name,
    dt.dept_tree_id AS dimension_dept_tree_id,
    dt.dimension_id,
    dt.seq,
    dt.parent_dept_id,
    dt.parent_dept_id_list AS path_list,
    dt.level,
    dt.sort_info
   FROM dept_tree dt
     LEFT JOIN dept_tree dt2 ON dt2.parent_dept_id::text = dt.id::text AND dt2.dimension_id::text = dt.dimension_id::text
  GROUP BY dt.id, dt.name, dt.organization_id, dt.route_name, dt.display_name, dt.dept_tree_id, dt.dimension_id, dt.seq, dt.parent_dept_id, dt.parent_dept_id_list, dt.level, dt.sort_info
  );

----- 张旭盈 创建sv_current_benchmark_input_node 20230802
CREATE VIEW sv_current_benchmark_input_node as
SELECT bin.*, ec.id as evaluation_criteria_id, ec.name as evaluation_criteria_name,
si.id as indicator_id, si.name as indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name
FROM st_evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct on ec.id = ct.evaluation_criteria_id
INNER JOIN st_indicator si on ct.indicator_id = si.id
INNER JOIN st_benchmark sb on si.id = sb.indicator_id
INNER JOIN st_benchmark_execute_node ben on sb.id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
WHERE now() BETWEEN ct.start_at AND ct.finish_at
and now() BETWEEN sb.start_at AND sb.finish_at
and si.is_activated is true

----- 张旭盈 创建sv_current_evaluation_assignment 20230802
CREATE VIEW sv_current_evaluation_assignment AS
SELECT ea.*, cp.name as plan_name, cp.focus_period_id,
cp.status as plan_status, cp.executed_start_at, cp.executed_finish_at,
cp.evaluation_criteria_id, ec.name as evaluation_criteria_name,
ec.status as evaluation_criteria_status, ec.evaluation_object_category
FROM st_evaluation_criteria ec
INNER JOIN st_evaluation_criteria_plan cp on ec.id = cp.evaluation_criteria_id
INNER JOIN st_evaluation_assignment ea on cp.id = ea.evaluation_criteria_plan_id
AND now() BETWEEN ea.start_at AND ea.finish_at
WHERE ec.status <> 'DRAFT' and (cp.status = 'PUBLISHED' OR cp.status = 'ARCHIVED')
and cp.executed_start_at < now()


--- 方卫 2023-08-02 创建当前小组视图
create view sv_current_team as (
select st.id as team_id,  st.name as team_name, sg.goal_category, sg.goal_id, sg.activity,
       sc.id as team_category_id, sc.name as team_category_name
from st_team st
inner join st_team_goal sg on sg.team_id = st.id
inner join st_team_category sc on sc.id = st.team_category_id
where st.start_at < now() and now() < st.finish_at
and sg.start_at < now() and now() < sg.finish_at
);


-- 方卫 2023-08-04 加索引
create unique index on st_k12_teacher_subject(dimension_dept_tree_id, subject_id, start_at, finish_at);

----- 张旭盈 更新sv_current_benchmark_input_node 20230804
CREATE OR REPLACE VIEW  sv_current_benchmark_input_node as
SELECT bin.*, ec.id as evaluation_criteria_id, ec.name as evaluation_criteria_name,
si.id as indicator_id, si.name as indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ss.name as score_symbol_name,
ss.value_type as score_symbol_value_type,
ss.numeric_precision as score_symbol_numeric_precision,
ss.string_options as score_symbol_string_options
FROM st_evaluation_criteria ec
INNER JOIN (
SELECT evaluation_criteria_id, indicator_id
FROM st_evaluation_criteria_tree WHERE now() BETWEEN start_at AND finish_at
) ct on ec.id = ct.evaluation_criteria_id
INNER JOIN st_indicator si on ct.indicator_id = si.id
INNER JOIN (
SELECT id, name, indicator_id
FROM st_benchmark where now() BETWEEN start_at AND finish_at
) sb on si.id = sb.indicator_id
INNER JOIN st_benchmark_execute_node ben on sb.id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE si.is_activated is true AND ss.is_activated is TRUE

---- 张旭盈 创建sv_current_evaluation_criteria_tree 20230804
CREATE OR REPLACE VIEW sv_current_evaluation_criteria_tree as
WITH RECURSIVE evaluation_criteria_tree as (
SELECT
si.id,
si.name,
si.comments,
ct.id AS evaluation_criteria_tree_id,
ct.evaluation_criteria_id,
ct.seq,
ct.parent_indicator_id,
ARRAY[si.id::text] AS parent_id_list,
1 AS level,
ARRAY[ct.seq] AS sort_info
FROM st_indicator si
INNER JOIN st_evaluation_criteria_tree ct on si.id = ct.indicator_id
WHERE si.is_activated is TRUE and now() BETWEEN ct.start_at AND ct.finish_at
and ct.parent_indicator_id is null
UNION
SELECT
si.id,
si.name,
si.comments,
ct.id AS evaluation_criteria_tree_id,
ct.evaluation_criteria_id,
ct.seq,
ct.parent_indicator_id,
array_append(ect.parent_id_list, ct.id) AS parent_dept_id_list,
ect.level + 1 AS level,
array_append(ect.sort_info, ct.seq) AS sort_info
FROM st_indicator si
INNER JOIN st_evaluation_criteria_tree ct on si.id = ct.indicator_id
JOIN evaluation_criteria_tree ect ON ect.id = ct.parent_indicator_id
WHERE si.is_activated is TRUE and now() BETWEEN ct.start_at AND ct.finish_at
) SELECT ect.*, ec.name as evaluation_criteria_name,
ec.status as evaluation_criteria_status, ec.evaluation_object_category
FROM evaluation_criteria_tree ect
INNER JOIN st_evaluation_criteria ec
on ect.evaluation_criteria_id = ec.id
WHERE ec.status <> 'DRAFT';


--- 方卫 2023-08-04 创建基准策略当前数据视图
create view cv_benchmark_strategy as (
select * from st_benchmark_strategy where start_at < now() and now() < finish_at
);


-- wyp 2023-08-08 创建视图
create view sv_current_input_score_log as
(
 SELECT sl.id,
    sl.handler_category,
    sl.handler_id,
    sl.handled_at,
    sl.remark,
    sl.version,
    sl.evaluation_assignment_id,
    sl.benchmark_input_node_id,
    sl.generated_at,
    sl.expected_filler_category,
    sl.expected_filler_id,
    sl.filler_category,
    sl.filler_id,
    sl.fill_start_at,
    sl.fill_finish_at,
    sl.filled_at,
    sl.numeric_score,
    sl.string_score,
    sl.status,
    sl.comments
   FROM st_evaluation_assignment ea
     JOIN st_input_score_log sl ON ea.id::text = sl.evaluation_assignment_id::text
  WHERE ea.finish_at >= now() AND ea.start_at < now()
);

create view sv_current_calc_score_log as
(
 SELECT sl.id,
    sl.handler_category,
    sl.handler_id,
    sl.handled_at,
    sl.remark,
    sl.version,
    sl.evaluation_assignment_id,
    sl.benchmark_calc_node_id
   FROM st_evaluation_assignment ea
     JOIN st_calc_score_log sl ON ea.id::text = sl.evaluation_assignment_id::text
  WHERE ea.finish_at >= now() AND ea.start_at < now()
);

---- 张旭盈 创建sv_current_establishment_assign 20230808
CREATE OR REPLACE VIEW sv_current_establishment_assign as
SELECT sea.*, se.seq as establishment_seq, sc.name as capacity_name,
sc.code as st_dept_capacity_constraint
FROM st_establishment se
INNER JOIN st_establishment_assign sea on se.id = sea.establishment_id
INNER JOIN st_capacity sc on se.capacity_id = sc.id
WHERE sc.is_available is TRUE and now() BETWEEN sea.start_at AND sea.finish_at
and now() BETWEEN se.start_at AND se.finish_at

---- 张旭盈 更新sv_current_benchmark_input_node 20230808
CREATE OR REPLACE VIEW  sv_current_benchmark_input_node as
SELECT bin.*, ec.id as evaluation_criteria_id, ec.name as evaluation_criteria_name,
si.id as indicator_id, si.name as indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ss.name as score_symbol_name,
ss.value_type as score_symbol_value_type,
ss.numeric_precision as score_symbol_numeric_precision,
ss.string_options as score_symbol_string_options
FROM st_evaluation_criteria ec
INNER JOIN (
SELECT evaluation_criteria_id, indicator_id
FROM st_evaluation_criteria_tree WHERE now() BETWEEN start_at AND finish_at
) ct on ec.id = ct.evaluation_criteria_id
INNER JOIN st_indicator si on ct.indicator_id = si.id
INNER JOIN (
SELECT id, name, indicator_id
FROM st_benchmark where now() BETWEEN start_at AND finish_at
) sb on si.id = sb.indicator_id
INNER JOIN st_benchmark_execute_node ben on sb.id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE si.is_activated is true AND ss.is_activated is TRUE
and now() BETWEEN bin.start_at and bin.finish_at

---- 张旭盈 创建sv_tag_info 20230809
CREATE OR REPLACE VIEW sv_tag_info as
SELECT ti.name, sto.code, sto.owner_category, sto.owner_id,
sto.is_editable, sto.is_activated, tor.resource_category, tor.resource_id,
tor.relationship
FROM st_tag_info ti
INNER JOIN st_tag_ownership sto on ti.id = sto.tag_id
INNER JOIN st_tag_ownership_relationship tor on sto.id = tor.tag_ownership_id


---- 张旭盈 创建sv_team_member 202308011
CREATE VIEW sv_current_team_member as
SELECT tm.*, st.team_category_id, st.name as team_name FROM st_team st
INNER JOIN st_team_member tm on st.id = tm.team_id
WHERE now() BETWEEN st.start_at AND st.finish_at
and now() BETWEEN tm.start_at AND tm.finish_at


---- 张旭盈 更新sv_current_benchmark_input_node 202308014
CREATE OR REPLACE VIEW  sv_current_benchmark_input_node as
SELECT bin.*, ec.id as evaluation_criteria_id, ec.name as evaluation_criteria_name,
si.id as indicator_id, si.name as indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ss.name as score_symbol_name,
ss.value_type as score_symbol_value_type,
ss.numeric_precision as score_symbol_numeric_precision,
ss.string_options as score_symbol_string_options
FROM st_evaluation_criteria ec
INNER JOIN (
SELECT evaluation_criteria_id, indicator_id
FROM st_evaluation_criteria_tree WHERE now() BETWEEN start_at AND finish_at
) ct on ec.id = ct.evaluation_criteria_id
INNER JOIN st_indicator si on ct.indicator_id = si.id
INNER JOIN (
SELECT id, name, indicator_id
FROM st_benchmark where now() BETWEEN start_at AND finish_at
) sb on si.id = sb.indicator_id
INNER JOIN st_benchmark_execute_node ben on sb.id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE si.is_activated is true
and now() BETWEEN bin.start_at and bin.finish_at


--- 方卫 创建视图 cv_k12_teacher_subject 20230814
create view cv_k12_teacher_subject as (
select * from st_k12_teacher_subject
where finish_at = 'infinity'
);

--- 方卫 加gin索引 20230814
create index on st_benchmark using gin(benchmark_strategy_params);
create index on st_benchmark_history using gin(benchmark_strategy_params);

--- 方卫 创建视图 cv_evaluation_criteria_tree 20230815
create view cv_evaluation_criteria_tree as (
    select * from st_evaluation_criteria_tree where finish_at = 'infinity'
);

---- 陆柯婷 修改sv_tag_info 20230815
DROP VIEW IF EXISTS sv_tag_info;

CREATE VIEW sv_tag_info AS
SELECT ti.id, ti.name, sto.code, sto.owner_category, sto.owner_id,
sto.is_editable, sto.is_activated, tor.resource_category, tor.resource_id,
tor.relationship
FROM st_tag_info ti
INNER JOIN st_tag_ownership sto on ti.id = sto.tag_id
INNER JOIN st_tag_ownership_relationship tor on sto.id = tor.tag_ownership_id;


---- 方卫 创建视图 sv_k12_dimension_dept_tree_path 20230816
drop view if exists sv_k12_dimension_dept_tree_path;
create view sv_k12_dimension_dept_tree_path as (
with recursive tree as(
select st.id, st.dimension_id, st.dept_id, st.parent_dept_id, st.seq, st.start_at, st.finish_at, array[st.id]::text[] as tree_path,
array[st.seq] as seq_list
from st_dimension sd
inner join st_dimension_dept_tree st on st.dimension_id = sd.id
where sd.code = 'DINGTALK_EDU' and st.parent_dept_id is null
union
select st.id, st.dimension_id, st.dept_id, st.parent_dept_id, st.seq, st.start_at, st.finish_at,
array_append(t.tree_path, st.id) as tree_path,
array_append(t.seq_list, st.seq) as seq_list
from st_dimension_dept_tree st
inner join tree t on st.parent_dept_id = t.dept_id
)
select * from tree order by seq_list
);


---- 方卫 创建视图 20230818
create view cv_dept as (
select * from st_dept where finish_at = 'infinity'
);

create view cv_dimension_dept_tree as (
select * from st_dimension_dept_tree where finish_at = 'infinity'
);


----- 张旭盈 修改sv_current_evaluation_assignment 20230817
CREATE VIEW OR REPLACE sv_current_evaluation_assignment AS
SELECT ea.*, cp.name as plan_name, cp.handled_at AS plan_handled_at, cp.focus_period_id,
cp.status as plan_status, cp.executed_start_at, cp.executed_finish_at,
cp.evaluation_criteria_id, ec.name as evaluation_criteria_name,
ec.status as evaluation_criteria_status, ec.evaluation_object_category
FROM st_evaluation_criteria ec
INNER JOIN st_evaluation_criteria_plan cp on ec.id = cp.evaluation_criteria_id
INNER JOIN st_evaluation_assignment ea on cp.id = ea.evaluation_criteria_plan_id
AND now() BETWEEN ea.start_at AND ea.finish_at
WHERE ec.status <> 'DRAFT' and (cp.status = 'PUBLISHED' OR cp.status = 'ARCHIVED')
and cp.executed_start_at < now()


----- 张旭盈 创建sv_benchmark_input_node 20230818
CREATE OR REPLACE view sv_benchmark_input_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, executed_finish_at as compare_at,
status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria_tree as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
ec.name as evaluation_criteria_name, ct.indicator_id,
ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ct.id, cp.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria ec on cp.evaluation_criteria_id = ec.id
INNER JOIN st_evaluation_criteria_tree ct on ec.id = ct.evaluation_criteria_id
and (ct.start_at < cp.compare_at and ct.finish_at > cp.compare_at)
), indicator_info as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.evaluation_criteria_name, si.name as indicator_name, ect.evaluation_criteria_id,
rank() OVER (PARTITION BY si.id, ect.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
INNER JOIN st_indicator_history si on ect.indicator_id = si.id
and (si.begin_at < ect.compare_at and si.end_at > ect.compare_at)
WHERE ect.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
)SELECT DISTINCT bin.*, bi.evaluation_criteria_name, bi.evaluation_criteria_id,
bi.indicator_id, bi.indicator_name, bi.benchmark_id, bi.plan_status, bi.plan_name,
bi.plan_id, bi.benchmark_name, ss.name AS score_symbol_name,
ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_info bi
INNER JOIN st_benchmark_execute_node ben on bi.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE bi.seq = 1

----- 张旭盈 更新sv_benchmark_input_node 增加标签 20230822
DROP VIEW IF EXISTS sv_benchmark_input_node;
CREATE OR REPLACE view sv_benchmark_input_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, executed_finish_at as compare_at,
status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ct.indicator_id, ec.evaluation_criteria_id,
ct.id as evaluation_criteria_tree_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ti.name as tag_name,
sto.code as tag_code, ti.id as tag_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
INNER JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
INNER JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
INNER JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, si.name as indicator_name, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
ii.tag_name, ii.tag_code, ii.tag_id,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
)SELECT DISTINCT bin.*, bi.evaluation_criteria_name, bi.evaluation_criteria_id,
bi.indicator_id, bi.indicator_name, bi.benchmark_id, bi.plan_status, bi.plan_name,
bi.plan_id, bi.benchmark_name, ss.name AS score_symbol_name, ss.code AS score_symbol_name,
bi.tag_name, bi.tag_code, bi.tag_id,
ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_info bi
INNER JOIN st_benchmark_execute_node ben on bi.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE bi.seq = 1

----- 张旭盈 更新sv_current_establishment_assign 20230823
CREATE OR REPLACE VIEW sv_current_establishment_assign as
SELECT sea.*, se.seq as establishment_seq, sc.name as capacity_name,
sc.code as capacity_code, se.dimension_dept_tree_id
FROM st_establishment se
INNER JOIN st_establishment_assign sea on se.id = sea.establishment_id
INNER JOIN st_capacity sc on se.capacity_id = sc.id
WHERE sc.is_available is TRUE and now() BETWEEN sea.start_at AND sea.finish_at
and now() BETWEEN se.start_at AND se.finish_at

----- 张旭盈 更新sv_benchmark_input_node 增加字段 20230825
DROP VIEW IF EXISTS sv_benchmark_input_node;
CREATE OR REPLACE view sv_benchmark_input_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ti.name as tag_name, sto.code as tag_code, ti.id as tag_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
INNER JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
INNER JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
INNER JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, si.name as indicator_name,
ectt.executed_start_at, ectt.executed_finish_at, ectt.evaluation_object_category,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
ii.tag_name, ii.tag_code, ii.tag_id, ii.focus_period_id,
ii.executed_start_at, ii.executed_finish_at, ii.evaluation_object_category,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
)SELECT DISTINCT bin.*, bi.evaluation_criteria_name, bi.evaluation_criteria_id,
bi.indicator_id, bi.indicator_name, bi.benchmark_id, bi.plan_status, bi.plan_name,
bi.plan_id, bi.benchmark_name, bi.executed_start_at, bi.executed_finish_at,
bi.evaluation_object_category,bi.tag_name, bi.tag_code, bi.tag_id, bi.focus_period_id,
bi.compare_at, ss.name AS score_symbol_name, ss.code AS score_symbol_code,
ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_info bi
INNER JOIN st_benchmark_execute_node ben on bi.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE bi.seq = 1;

----- 张旭盈 创建sv_evaluation_criteria_plan_indicator 20230826
CREATE view sv_evaluation_criteria_plan_indicator as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ti.name as tag_name, sto.code as tag_code, ti.id as tag_id, ect.evaluation_criteria_tree_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
LEFT JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
LEFT JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
LEFT JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, ectt.executed_start_at,
ectt.executed_finish_at, ectt.evaluation_object_category, ectt.evaluation_criteria_tree_id,
si.begin_at, si.end_at, si.id, si.name as indicator_name,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
)SELECT * FROM indicator_info WHERE seq = 1

--- 方卫 20230829 创建视图
drop view if exists cv_establishment_assign;
create view cv_establishment_assign as (
select * from st_establishment_assign
where finish_at = 'infinity'
);

drop view if exists cv_establishment;
create view cv_establishment as (
select * from st_establishment
where finish_at = 'infinity'
);


----- 张旭盈 创建sv_benchmark_clac_node 20230831
CREATE OR REPLACE view sv_benchmark_clac_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ti.name as tag_name, sto.code as tag_code, ti.id as tag_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
LEFT JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
LEFT JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
LEFT JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, si.name as indicator_name,
ectt.executed_start_at, ectt.executed_finish_at, ectt.evaluation_object_category,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
ii.tag_name, ii.tag_code, ii.tag_id, ii.focus_period_id,
ii.executed_start_at, ii.executed_finish_at, ii.evaluation_object_category,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
)SELECT DISTINCT bcn.*, bi.evaluation_criteria_name,
bi.evaluation_criteria_id,
bi.indicator_id, bi.indicator_name, bi.benchmark_id, bi.plan_status, bi.plan_name,
bi.plan_id, bi.benchmark_name, bi.executed_start_at, bi.executed_finish_at,
bi.evaluation_object_category,bi.tag_name, bi.tag_code, bi.tag_id, bi.focus_period_id,
bi.compare_at, ss.name AS score_symbol_name, ss.code AS score_symbol_code,
ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_info bi
INNER JOIN st_benchmark_execute_node ben on bi.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_calc_node bcn on ben.id = bcn.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bcn.output_score_symbol_id
WHERE bi.seq = 1;

----- 张旭盈 修改sv_benchmark_input_node 20230907
DROP VIEW IF EXISTS sv_benchmark_input_node;
CREATE OR REPLACE view sv_benchmark_input_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ti.name as tag_name, sto.code as tag_code, ti.id as tag_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
LEFT JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
LEFT JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
LEFT JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, si.name as indicator_name,
ectt.executed_start_at, ectt.executed_finish_at, ectt.evaluation_object_category,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
ii.tag_name, ii.tag_code, ii.tag_id, ii.focus_period_id,
ii.executed_start_at, ii.executed_finish_at, ii.evaluation_object_category,
sb.benchmark_strategy_id,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
), benchmark_with_strategy as (
SELECT bi.plan_id, bi.compare_at, bi.plan_name, bi.indicator_id,
bi.evaluation_criteria_name, bi.indicator_name, bi.benchmark_id,
bi.benchmark_name, bi.evaluation_criteria_id, bi.plan_status,
bi.tag_name, bi.tag_code, bi.tag_id, bi.focus_period_id,
bi.executed_start_at, bi.executed_finish_at, bi.evaluation_object_category,
sbs.source_category as benchmark_source_category,
rank() OVER (PARTITION BY sbs.id, bi.plan_id ORDER BY sbs.start_at DESC) AS seq
FROM benchmark_info bi
INNER JOIN st_benchmark_strategy sbs on bi.benchmark_strategy_id = sbs.id
and (sbs.start_at < bi.compare_at and sbs.finish_at > bi.compare_at)
WHERE bi.seq = 1
) SELECT DISTINCT bin.*, bws.evaluation_criteria_name, bws.evaluation_criteria_id,
bws.indicator_id, bws.indicator_name, bws.benchmark_id, bws.plan_status, bws.plan_name,
bws.plan_id, bws.benchmark_name, bws.executed_start_at, bws.executed_finish_at,
bws.evaluation_object_category,bws.tag_name, bws.tag_code, bws.tag_id, bws.focus_period_id,
bws.compare_at, bws.benchmark_source_category,
ss.name AS score_symbol_name, ss.code AS score_symbol_code,
ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_with_strategy bws
INNER JOIN st_benchmark_execute_node ben on bws.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE bws.seq = 1

  ----- 张旭盈 修改sv_benchmark_clac_node 20230907
DROP view sv_benchmark_clac_node;
CREATE OR REPLACE view sv_benchmark_clac_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ti.name as tag_name, sto.code as tag_code, ti.id as tag_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
LEFT JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
LEFT JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
LEFT JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, si.name as indicator_name,
ectt.executed_start_at, ectt.executed_finish_at, ectt.evaluation_object_category,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
ii.tag_name, ii.tag_code, ii.tag_id, ii.focus_period_id,
ii.executed_start_at, ii.executed_finish_at, ii.evaluation_object_category,
sb.benchmark_strategy_id,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
), benchmark_with_strategy as (
SELECT bi.plan_id, bi.compare_at, bi.plan_name, bi.indicator_id,
bi.evaluation_criteria_name, bi.indicator_name, bi.benchmark_id,
bi.benchmark_name, bi.evaluation_criteria_id, bi.plan_status,
bi.tag_name, bi.tag_code, bi.tag_id, bi.focus_period_id,
bi.executed_start_at, bi.executed_finish_at, bi.evaluation_object_category,
sbs.source_category as benchmark_source_category,
rank() OVER (PARTITION BY sbs.id, bi.plan_id ORDER BY sbs.start_at DESC) AS seq
FROM benchmark_info bi
INNER JOIN st_benchmark_strategy sbs on bi.benchmark_strategy_id = sbs.id
and (sbs.start_at < bi.compare_at and sbs.finish_at > bi.compare_at)
WHERE bi.seq = 1
) SELECT DISTINCT bcn.*, bws.evaluation_criteria_name,
bws.evaluation_criteria_id,
bws.indicator_id, bws.indicator_name, bws.benchmark_id, bws.plan_status, bws.plan_name,
bws.plan_id, bws.benchmark_name, bws.executed_start_at, bws.executed_finish_at,
bws.evaluation_object_category,bws.tag_name, bws.tag_code, bws.tag_id, bws.focus_period_id,
bws.compare_at, bws.benchmark_source_category,
ss.name AS score_symbol_name, ss.code AS score_symbol_code,
ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_with_strategy bws
INNER JOIN st_benchmark_execute_node ben on bws.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_calc_node bcn on ben.id = bcn.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bcn.output_score_symbol_id
WHERE bws.seq = 1;


--- 方卫 20230905 创建视图
create view sv_tag_ownership_relationship_history as (
select sh.*, si.name from st_tag_ownership_relationship_history sh
inner join st_tag_ownership so on so.id = sh.tag_ownership_id
inner join st_tag_info si on si.id = so.tag_id
);

--- 张旭盈 20230909 创建视图
create view cv_evaluation_assignment as
SELECT * FROM st_evaluation_assignment
WHERE finish_at = 'infinity'::timestamp with time zone

--- 张旭盈 202309013 修改视图sv_benchmark_clac_node
DROP view sv_benchmark_clac_node;
CREATE OR REPLACE view sv_benchmark_clac_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, 'IN_PROGRESS' as plan_status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ti.name as tag_name, sto.code as tag_code, ti.id as tag_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
LEFT JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
LEFT JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
LEFT JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, si.name as indicator_name,
ectt.executed_start_at, ectt.executed_finish_at, ectt.evaluation_object_category,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
ii.tag_name, ii.tag_code, ii.tag_id, ii.focus_period_id,
ii.executed_start_at, ii.executed_finish_at, ii.evaluation_object_category,
sb.benchmark_strategy_id,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
), benchmark_with_strategy as (
SELECT bi.plan_id, bi.compare_at, bi.plan_name, bi.indicator_id,
bi.evaluation_criteria_name, bi.indicator_name, bi.benchmark_id,
bi.benchmark_name, bi.evaluation_criteria_id, bi.plan_status,
bi.tag_name, bi.tag_code, bi.tag_id, bi.focus_period_id,
bi.executed_start_at, bi.executed_finish_at, bi.evaluation_object_category,
sbs.source_category as benchmark_source_category,
rank() OVER (PARTITION BY sbs.id, bi.plan_id ORDER BY sbs.start_at DESC) AS seq
FROM benchmark_info bi
INNER JOIN st_benchmark_strategy sbs on bi.benchmark_strategy_id = sbs.id
and (sbs.start_at < bi.compare_at and sbs.finish_at > bi.compare_at)
WHERE bi.seq = 1
) SELECT DISTINCT bcn.*, bws.evaluation_criteria_name,
bws.evaluation_criteria_id,
bws.indicator_id, bws.indicator_name, bws.benchmark_id, bws.plan_status, bws.plan_name,
bws.plan_id, bws.benchmark_name, bws.executed_start_at, bws.executed_finish_at,
bws.evaluation_object_category,bws.tag_name, bws.tag_code, bws.tag_id, bws.focus_period_id,
bws.compare_at, ss.name AS score_symbol_name, bws.benchmark_source_category,
ss.code AS score_symbol_code, ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_with_strategy bws
INNER JOIN st_benchmark_execute_node ben on bws.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_calc_node bcn on ben.id = bcn.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bcn.output_score_symbol_id
WHERE bws.seq = 1;

--- 张旭盈 202309013 修改视图sv_benchmark_input_node
DROP VIEW IF EXISTS sv_benchmark_input_node;
CREATE OR REPLACE view sv_benchmark_input_node as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, 'IN_PROGRESS' as plan_status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id,
rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
WHERE ec.seq = 1
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.indicator_id, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ti.name as tag_name, sto.code as tag_code, ti.id as tag_id,
rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
FROM evaluation_criteria_tree ect
LEFT JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
LEFT JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
LEFT JOIN st_tag_info ti on ti.id = sto.tag_id
WHERE ect.seq = 1
), indicator_info as (
SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.indicator_id, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, si.name as indicator_name,
ectt.executed_start_at, ectt.executed_finish_at, ectt.evaluation_object_category,
rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at)
WHERE ectt.seq = 1
), benchmark_info as (
SELECT ii.plan_id, ii.compare_at, ii.plan_name, ii.indicator_id,
ii.evaluation_criteria_name, ii.indicator_name, sb.id as benchmark_id,
sb.name as benchmark_name, ii.evaluation_criteria_id, ii.plan_status,
ii.tag_name, ii.tag_code, ii.tag_id, ii.focus_period_id,
ii.executed_start_at, ii.executed_finish_at, ii.evaluation_object_category,
sb.benchmark_strategy_id,
rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
FROM indicator_info ii
INNER JOIN st_benchmark sb on ii.indicator_id = sb.indicator_id
and (sb.start_at < ii.compare_at and sb.finish_at > ii.compare_at)
WHERE ii.seq = 1
), benchmark_with_strategy as (
SELECT bi.plan_id, bi.compare_at, bi.plan_name, bi.indicator_id,
bi.evaluation_criteria_name, bi.indicator_name, bi.benchmark_id,
bi.benchmark_name, bi.evaluation_criteria_id, bi.plan_status,
bi.tag_name, bi.tag_code, bi.tag_id, bi.focus_period_id,
bi.executed_start_at, bi.executed_finish_at, bi.evaluation_object_category,
sbs.source_category as benchmark_source_category,
rank() OVER (PARTITION BY sbs.id, bi.plan_id ORDER BY sbs.start_at DESC) AS seq
FROM benchmark_info bi
INNER JOIN st_benchmark_strategy sbs on bi.benchmark_strategy_id = sbs.id
and (sbs.start_at < bi.compare_at and sbs.finish_at > bi.compare_at)
WHERE bi.seq = 1
)
SELECT DISTINCT bin.*, bws.evaluation_criteria_name, bws.evaluation_criteria_id,
bws.indicator_id, bws.indicator_name, bws.benchmark_id, bws.plan_status, bws.plan_name,
bws.plan_id, bws.benchmark_name, bws.executed_start_at, bws.executed_finish_at,
bws.evaluation_object_category,bws.tag_name, bws.tag_code, bws.tag_id, bws.focus_period_id,
bws.compare_at, bws.benchmark_source_category,
ss.name AS score_symbol_name, ss.code AS score_symbol_code,
ss.value_type AS score_symbol_value_type,
ss.numeric_precision AS score_symbol_numeric_precision,
ss.string_options AS score_symbol_string_options
FROM benchmark_with_strategy bws
INNER JOIN st_benchmark_execute_node ben on bws.benchmark_id = ben.benchmark_id
INNER JOIN st_benchmark_input_node bin on ben.id = bin.benchmark_execute_node_id
INNER JOIN st_score_symbol ss on ss.id = bin.score_symbol_id
WHERE bws.seq = 1;

--- 张旭盈 202309016 修改视图sv_evaluation_criteria_plan_indicator
drop view sv_evaluation_criteria_plan_indicator;
CREATE view sv_evaluation_criteria_plan_indicator as
with evaluation_criteria_plan as (
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
CASE WHEN (status = 'ABOLISHED') THEN handled_at
ELSE executed_finish_at END AS compare_at,
CASE WHEN (status = 'ABOLISHED') THEN 'ABOLISHED'
ELSE 'ARCHIVED' END AS plan_status, status
FROM st_evaluation_criteria_plan
WHERE (status = 'ABOLISHED' and handled_at > executed_start_at
and handled_at < executed_finish_at)
or (status = 'PUBLISHED' and executed_finish_at < now())
or status = 'ARCHIVED'
UNION ALL
SELECT id as plan_id, name as plan_name, evaluation_criteria_id,
executed_start_at, executed_finish_at, focus_period_id,
executed_finish_at as compare_at, status as plan_status, status
FROM st_evaluation_criteria_plan
WHERE status = 'PUBLISHED' AND now() > executed_start_at
and now() <= executed_finish_at
), evaluation_criteria as (
SELECT cp.plan_id, cp.compare_at, cp.plan_name, cp.plan_status,
cp.executed_start_at, cp.executed_finish_at, cp.focus_period_id,
ec.evaluation_object_category,
ec.name as evaluation_criteria_name, ec.id as evaluation_criteria_id
FROM evaluation_criteria_plan cp
INNER JOIN st_evaluation_criteria_history ec on cp.evaluation_criteria_id = ec.id
and (ec.begin_at < cp.compare_at and ec.end_at > cp.compare_at)
), evaluation_criteria_tree as (
SELECT ec.plan_id, ec.compare_at, ec.plan_name, ec.plan_status,
ec.evaluation_criteria_name, ec.focus_period_id, ec.evaluation_criteria_id,
ec.executed_start_at, ec.executed_finish_at, ec.evaluation_object_category,
ct.id as evaluation_criteria_tree_id, ct.indicator_id,
ct.parent_indicator_id, ct.seq
FROM evaluation_criteria ec
INNER JOIN st_evaluation_criteria_tree ct
on ec.evaluation_criteria_id = ct.evaluation_criteria_id
and (ct.start_at < ec.compare_at and ct.finish_at > ec.compare_at)
), evaluation_criteria_tree_tag as (
SELECT ect.plan_id, ect.compare_at, ect.plan_name, ect.plan_status,
ect.executed_start_at, ect.executed_finish_at, ect.evaluation_object_category,
ect.evaluation_criteria_name, ect.evaluation_criteria_id, ect.focus_period_id,
ect.indicator_id, ect.parent_indicator_id, ect.seq, ti.name as tag_name,
sto.code as tag_code, ti.id as tag_id, ect.evaluation_criteria_tree_id
FROM evaluation_criteria_tree ect
LEFT JOIN st_tag_ownership_relationship_history tor on ect.evaluation_criteria_tree_id = tor.resource_id
and tor.resource_category = 'EVALUATION_CRITERIA_TREE'
and (tor.begin_at < ect.compare_at and tor.end_at > ect.compare_at)
LEFT JOIN st_tag_ownership sto on sto.id = tor.tag_ownership_id
LEFT JOIN st_tag_info ti on ti.id = sto.tag_id
)SELECT ectt.plan_id, ectt.compare_at, ectt.plan_name, ectt.plan_status,
ectt.evaluation_criteria_name, ectt.focus_period_id, ectt.evaluation_criteria_id,
ectt.tag_name, ectt.tag_code, ectt.tag_id, ectt.executed_start_at, ectt.seq,
ectt.executed_finish_at, ectt.evaluation_object_category, ectt.evaluation_criteria_tree_id,
ectt.parent_indicator_id, si.begin_at, si.end_at, si.id, si.name, si.comments
FROM evaluation_criteria_tree_tag ectt
INNER JOIN st_indicator_history si on ectt.indicator_id = si.id
and (si.begin_at < ectt.compare_at and si.end_at > ectt.compare_at);


-- 2023-09-08 创建物化视图
DROP MATERIALIZED VIEW mv_benchmark_clac_node;

CREATE MATERIALIZED VIEW mv_benchmark_clac_node AS (
WITH evaluation_criteria_plan AS (
         SELECT st_evaluation_criteria_plan.id AS plan_id,
            st_evaluation_criteria_plan.name AS plan_name,
            st_evaluation_criteria_plan.evaluation_criteria_id,
            st_evaluation_criteria_plan.executed_start_at,
            st_evaluation_criteria_plan.executed_finish_at,
            st_evaluation_criteria_plan.focus_period_id,
                CASE
                    WHEN ((st_evaluation_criteria_plan.status)::text = 'ABOLISHED'::text) THEN st_evaluation_criteria_plan.handled_at
                    ELSE st_evaluation_criteria_plan.executed_finish_at
                END AS compare_at,
                CASE
                    WHEN ((st_evaluation_criteria_plan.status)::text = 'ABOLISHED'::text) THEN 'ABOLISHED'::text
                    ELSE 'ARCHIVED'::text
                END AS plan_status
           FROM st_evaluation_criteria_plan
          WHERE ((((st_evaluation_criteria_plan.status)::text = 'ABOLISHED'::text) AND (st_evaluation_criteria_plan.handled_at > st_evaluation_criteria_plan.executed_start_at) AND (st_evaluation_criteria_plan.handled_at < st_evaluation_criteria_plan.executed_finish_at)) OR (((st_evaluation_criteria_plan.status)::text = 'PUBLISHED'::text) AND (st_evaluation_criteria_plan.executed_finish_at < now())) OR ((st_evaluation_criteria_plan.status)::text = 'ARCHIVED'::text))
        UNION ALL
         SELECT st_evaluation_criteria_plan.id AS plan_id,
            st_evaluation_criteria_plan.name AS plan_name,
            st_evaluation_criteria_plan.evaluation_criteria_id,
            st_evaluation_criteria_plan.executed_start_at,
            st_evaluation_criteria_plan.executed_finish_at,
            st_evaluation_criteria_plan.focus_period_id,
            st_evaluation_criteria_plan.executed_finish_at AS compare_at,
            'IN_PROGRESS'::text AS plan_status
           FROM st_evaluation_criteria_plan
          WHERE (((st_evaluation_criteria_plan.status)::text = 'PUBLISHED'::text) AND (now() > st_evaluation_criteria_plan.executed_start_at) AND (now() <= st_evaluation_criteria_plan.executed_finish_at))
        ), evaluation_criteria AS (
         SELECT cp.plan_id,
            cp.compare_at,
            cp.plan_name,
            cp.plan_status,
            cp.executed_start_at,
            cp.executed_finish_at,
            cp.focus_period_id,
            ec.evaluation_object_category,
            ec.name AS evaluation_criteria_name,
            ec.id AS evaluation_criteria_id,
            rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
           FROM (evaluation_criteria_plan cp
             JOIN st_evaluation_criteria_history ec ON ((((cp.evaluation_criteria_id)::text = (ec.id)::text) AND (ec.begin_at < cp.compare_at) AND (ec.end_at > cp.compare_at))))
        ), evaluation_criteria_tree AS (
         SELECT ec.plan_id,
            ec.compare_at,
            ec.plan_name,
            ec.plan_status,
            ec.evaluation_criteria_name,
            ec.focus_period_id,
            ec.evaluation_criteria_id,
            ec.executed_start_at,
            ec.executed_finish_at,
            ec.evaluation_object_category,
            ct.id AS evaluation_criteria_tree_id,
            ct.indicator_id,
            rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
           FROM (evaluation_criteria ec
             JOIN st_evaluation_criteria_tree ct ON ((((ec.evaluation_criteria_id)::text = (ct.evaluation_criteria_id)::text) AND (ct.start_at < ec.compare_at) AND (ct.finish_at > ec.compare_at))))
          WHERE (ec.seq = 1)
        ), evaluation_criteria_tree_tag AS (
         SELECT ect.plan_id,
            ect.compare_at,
            ect.plan_name,
            ect.indicator_id,
            ect.plan_status,
            ect.executed_start_at,
            ect.executed_finish_at,
            ect.evaluation_object_category,
            ect.evaluation_criteria_name,
            ect.evaluation_criteria_id,
            ect.focus_period_id,
            ti.name AS tag_name,
            sto.code AS tag_code,
            ti.id AS tag_id,
            rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
           FROM (((evaluation_criteria_tree ect
             LEFT JOIN st_tag_ownership_relationship_history tor ON ((((ect.evaluation_criteria_tree_id)::text = (tor.resource_id)::text) AND ((tor.resource_category)::text = 'EVALUATION_CRITERIA_TREE'::text) AND (tor.begin_at < ect.compare_at) AND (tor.end_at > ect.compare_at))))
             LEFT JOIN st_tag_ownership sto ON (((sto.id)::text = (tor.tag_ownership_id)::text)))
             LEFT JOIN st_tag_info ti ON (((ti.id)::text = (sto.tag_id)::text)))
          WHERE (ect.seq = 1)
        ), indicator_info AS (
         SELECT ectt.plan_id,
            ectt.compare_at,
            ectt.plan_name,
            ectt.indicator_id,
            ectt.plan_status,
            ectt.evaluation_criteria_name,
            ectt.focus_period_id,
            ectt.evaluation_criteria_id,
            ectt.tag_name,
            ectt.tag_code,
            ectt.tag_id,
            si.name AS indicator_name,
            ectt.executed_start_at,
            ectt.executed_finish_at,
            ectt.evaluation_object_category,
            rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
           FROM (evaluation_criteria_tree_tag ectt
             JOIN st_indicator_history si ON ((((ectt.indicator_id)::text = (si.id)::text) AND (si.begin_at < ectt.compare_at) AND (si.end_at > ectt.compare_at))))
          WHERE (ectt.seq = 1)
        ), benchmark_info AS (
         SELECT ii.plan_id,
            ii.compare_at,
            ii.plan_name,
            ii.indicator_id,
            ii.evaluation_criteria_name,
            ii.indicator_name,
            sb.id AS benchmark_id,
            sb.name AS benchmark_name,
            ii.evaluation_criteria_id,
            ii.plan_status,
            ii.tag_name,
            ii.tag_code,
            ii.tag_id,
            ii.focus_period_id,
            ii.executed_start_at,
            ii.executed_finish_at,
            ii.evaluation_object_category,
            sb.benchmark_strategy_id,
            rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
           FROM (indicator_info ii
             JOIN st_benchmark sb ON ((((ii.indicator_id)::text = (sb.indicator_id)::text) AND (sb.start_at < ii.compare_at) AND (sb.finish_at > ii.compare_at))))
          WHERE (ii.seq = 1)
        ), benchmark_with_strategy AS (
         SELECT bi.plan_id,
            bi.compare_at,
            bi.plan_name,
            bi.indicator_id,
            bi.evaluation_criteria_name,
            bi.indicator_name,
            bi.benchmark_id,
            bi.benchmark_name,
            bi.evaluation_criteria_id,
            bi.plan_status,
            bi.tag_name,
            bi.tag_code,
            bi.tag_id,
            bi.focus_period_id,
            bi.executed_start_at,
            bi.executed_finish_at,
            bi.evaluation_object_category,
            sbs.source_category AS benchmark_source_category,
            rank() OVER (PARTITION BY sbs.id, bi.plan_id ORDER BY sbs.start_at DESC) AS seq
           FROM (benchmark_info bi
             JOIN st_benchmark_strategy sbs ON ((((bi.benchmark_strategy_id)::text = (sbs.id)::text) AND (sbs.start_at < bi.compare_at) AND (sbs.finish_at > bi.compare_at))))
          WHERE (bi.seq = 1)
        )
 SELECT DISTINCT bcn.id,
    bcn.handler_category,
    bcn.handler_id,
    bcn.handled_at,
    bcn.remark,
    bcn.version,
    bcn.benchmark_execute_node_id,
    bcn.input_score_symbol_id,
    bcn.output_score_symbol_id,
    bcn.calc_method,
    bws.evaluation_criteria_name,
    bws.evaluation_criteria_id,
    bws.indicator_id,
    bws.indicator_name,
    bws.benchmark_id,
    bws.plan_status,
    bws.plan_name,
    bws.plan_id,
    bws.benchmark_name,
    bws.executed_start_at,
    bws.executed_finish_at,
    bws.evaluation_object_category,
    bws.tag_name,
    bws.tag_code,
    bws.tag_id,
    bws.focus_period_id,
    bws.compare_at,
    ss.name AS score_symbol_name,
    bws.benchmark_source_category,
    ss.code AS score_symbol_code,
    ss.value_type AS score_symbol_value_type,
    ss.numeric_precision AS score_symbol_numeric_precision,
    ss.string_options AS score_symbol_string_options,
    uuid_generate_v4() AS idx
   FROM (((benchmark_with_strategy bws
     JOIN st_benchmark_execute_node ben ON (((bws.benchmark_id)::text = (ben.benchmark_id)::text)))
     JOIN st_benchmark_calc_node bcn ON (((ben.id)::text = (bcn.benchmark_execute_node_id)::text)))
     JOIN st_score_symbol ss ON (((ss.id)::text = (bcn.output_score_symbol_id)::text)))
  WHERE (bws.seq = 1));

create unique index on mv_benchmark_clac_node (idx);

CREATE INDEX idx_mv_benchmark_clac_id ON public.mv_benchmark_clac_node USING btree (id);
CREATE INDEX idx_mv_benchmark_clac_benchmark_id ON public.mv_benchmark_clac_node USING btree (benchmark_id);

DROP MATERIALIZED VIEW mv_benchmark_input_node;

CREATE MATERIALIZED VIEW mv_benchmark_input_node AS (
WITH evaluation_criteria_plan AS (
         SELECT st_evaluation_criteria_plan.id AS plan_id,
            st_evaluation_criteria_plan.name AS plan_name,
            st_evaluation_criteria_plan.evaluation_criteria_id,
            st_evaluation_criteria_plan.executed_start_at,
            st_evaluation_criteria_plan.executed_finish_at,
            st_evaluation_criteria_plan.focus_period_id,
                CASE
                    WHEN ((st_evaluation_criteria_plan.status)::text = 'ABOLISHED'::text) THEN st_evaluation_criteria_plan.handled_at
                    ELSE st_evaluation_criteria_plan.executed_finish_at
                END AS compare_at,
                CASE
                    WHEN ((st_evaluation_criteria_plan.status)::text = 'ABOLISHED'::text) THEN 'ABOLISHED'::text
                    ELSE 'ARCHIVED'::text
                END AS plan_status
           FROM st_evaluation_criteria_plan
          WHERE ((((st_evaluation_criteria_plan.status)::text = 'ABOLISHED'::text) AND (st_evaluation_criteria_plan.handled_at > st_evaluation_criteria_plan.executed_start_at) AND (st_evaluation_criteria_plan.handled_at < st_evaluation_criteria_plan.executed_finish_at)) OR (((st_evaluation_criteria_plan.status)::text = 'PUBLISHED'::text) AND (st_evaluation_criteria_plan.executed_finish_at < now())) OR ((st_evaluation_criteria_plan.status)::text = 'ARCHIVED'::text))
        UNION ALL
         SELECT st_evaluation_criteria_plan.id AS plan_id,
            st_evaluation_criteria_plan.name AS plan_name,
            st_evaluation_criteria_plan.evaluation_criteria_id,
            st_evaluation_criteria_plan.executed_start_at,
            st_evaluation_criteria_plan.executed_finish_at,
            st_evaluation_criteria_plan.focus_period_id,
            st_evaluation_criteria_plan.executed_finish_at AS compare_at,
            'IN_PROGRESS'::text AS plan_status
           FROM st_evaluation_criteria_plan
          WHERE (((st_evaluation_criteria_plan.status)::text = 'PUBLISHED'::text) AND (now() > st_evaluation_criteria_plan.executed_start_at) AND (now() <= st_evaluation_criteria_plan.executed_finish_at))
        ), evaluation_criteria AS (
         SELECT cp.plan_id,
            cp.compare_at,
            cp.plan_name,
            cp.plan_status,
            cp.executed_start_at,
            cp.executed_finish_at,
            cp.focus_period_id,
            ec.evaluation_object_category,
            ec.name AS evaluation_criteria_name,
            ec.id AS evaluation_criteria_id,
            rank() OVER (PARTITION BY ec.id, cp.plan_id ORDER BY ec.begin_at DESC) AS seq
           FROM (evaluation_criteria_plan cp
             JOIN st_evaluation_criteria_history ec ON ((((cp.evaluation_criteria_id)::text = (ec.id)::text) AND ((ec.begin_at < cp.compare_at) AND (ec.end_at > cp.compare_at)))))
        ), evaluation_criteria_tree AS (
         SELECT ec.plan_id,
            ec.compare_at,
            ec.plan_name,
            ec.plan_status,
            ec.evaluation_criteria_name,
            ec.focus_period_id,
            ec.evaluation_criteria_id,
            ec.executed_start_at,
            ec.executed_finish_at,
            ec.evaluation_object_category,
            ct.id AS evaluation_criteria_tree_id,
            ct.indicator_id,
            rank() OVER (PARTITION BY ct.id, ec.plan_id ORDER BY ct.start_at DESC) AS seq
           FROM (evaluation_criteria ec
             JOIN st_evaluation_criteria_tree ct ON ((((ec.evaluation_criteria_id)::text = (ct.evaluation_criteria_id)::text) AND ((ct.start_at < ec.compare_at) AND (ct.finish_at > ec.compare_at)))))
          WHERE (ec.seq = 1)
        ), evaluation_criteria_tree_tag AS (
         SELECT ect.plan_id,
            ect.compare_at,
            ect.plan_name,
            ect.indicator_id,
            ect.plan_status,
            ect.executed_start_at,
            ect.executed_finish_at,
            ect.evaluation_object_category,
            ect.evaluation_criteria_name,
            ect.evaluation_criteria_id,
            ect.focus_period_id,
            ti.name AS tag_name,
            sto.code AS tag_code,
            ti.id AS tag_id,
            rank() OVER (PARTITION BY tor.id, ect.plan_id ORDER BY tor.begin_at DESC) AS seq
           FROM (((evaluation_criteria_tree ect
             LEFT JOIN st_tag_ownership_relationship_history tor ON ((((ect.evaluation_criteria_tree_id)::text = (tor.resource_id)::text) AND ((tor.resource_category)::text = 'EVALUATION_CRITERIA_TREE'::text) AND ((tor.begin_at < ect.compare_at) AND (tor.end_at > ect.compare_at)))))
             LEFT JOIN st_tag_ownership sto ON (((sto.id)::text = (tor.tag_ownership_id)::text)))
             LEFT JOIN st_tag_info ti ON (((ti.id)::text = (sto.tag_id)::text)))
          WHERE (ect.seq = 1)
        ), indicator_info AS (
         SELECT ectt.plan_id,
            ectt.compare_at,
            ectt.plan_name,
            ectt.indicator_id,
            ectt.plan_status,
            ectt.evaluation_criteria_name,
            ectt.focus_period_id,
            ectt.evaluation_criteria_id,
            ectt.tag_name,
            ectt.tag_code,
            ectt.tag_id,
            si.name AS indicator_name,
            ectt.executed_start_at,
            ectt.executed_finish_at,
            ectt.evaluation_object_category,
            rank() OVER (PARTITION BY si.id, ectt.plan_id ORDER BY si.begin_at DESC) AS seq
           FROM (evaluation_criteria_tree_tag ectt
             JOIN st_indicator_history si ON ((((ectt.indicator_id)::text = (si.id)::text) AND ((si.begin_at < ectt.compare_at) AND (si.end_at > ectt.compare_at)))))
          WHERE (ectt.seq = 1)
        ), benchmark_info AS (
         SELECT ii.plan_id,
            ii.compare_at,
            ii.plan_name,
            ii.indicator_id,
            ii.evaluation_criteria_name,
            ii.indicator_name,
            sb.id AS benchmark_id,
            sb.name AS benchmark_name,
            ii.evaluation_criteria_id,
            ii.plan_status,
            ii.tag_name,
            ii.tag_code,
            ii.tag_id,
            ii.focus_period_id,
            ii.executed_start_at,
            ii.executed_finish_at,
            ii.evaluation_object_category,
            sb.benchmark_strategy_id,
            rank() OVER (PARTITION BY sb.id, ii.plan_id ORDER BY sb.start_at DESC) AS seq
           FROM (indicator_info ii
             JOIN st_benchmark sb ON ((((ii.indicator_id)::text = (sb.indicator_id)::text) AND ((sb.start_at < ii.compare_at) AND (sb.finish_at > ii.compare_at)))))
          WHERE (ii.seq = 1)
        ), benchmark_with_strategy AS (
         SELECT bi.plan_id,
            bi.compare_at,
            bi.plan_name,
            bi.indicator_id,
            bi.evaluation_criteria_name,
            bi.indicator_name,
            bi.benchmark_id,
            bi.benchmark_name,
            bi.evaluation_criteria_id,
            bi.plan_status,
            bi.tag_name,
            bi.tag_code,
            bi.tag_id,
            bi.focus_period_id,
            bi.executed_start_at,
            bi.executed_finish_at,
            bi.evaluation_object_category,
            sbs.source_category AS benchmark_source_category,
            rank() OVER (PARTITION BY sbs.id, bi.plan_id ORDER BY sbs.start_at DESC) AS seq
           FROM (benchmark_info bi
             JOIN st_benchmark_strategy sbs ON ((((bi.benchmark_strategy_id)::text = (sbs.id)::text) AND ((sbs.start_at < bi.compare_at) AND (sbs.finish_at > bi.compare_at)))))
          WHERE (bi.seq = 1)
        )
 SELECT DISTINCT bin.id,
    bin.handler_category,
    bin.handler_id,
    bin.handled_at,
    bin.remark,
    bin.version,
    bin.benchmark_execute_node_id,
    bin.source_category,
    bin.source_benchmark_id,
    bin.source_exec_mode,
    bin.scheduler_expression,
    bin.filler_calc_method,
    bin.filler_calc_context,
    bin.score_symbol_id,
    bin.numeric_min_score,
    bin.numeric_max_score,
    bin.limited_string_options,
    bin.start_at,
    bin.finish_at,
    bws.evaluation_criteria_name,
    bws.evaluation_criteria_id,
    bws.indicator_id,
    bws.indicator_name,
    bws.benchmark_id,
    bws.plan_status,
    bws.plan_name,
    bws.plan_id,
    bws.benchmark_name,
    bws.executed_start_at,
    bws.executed_finish_at,
    bws.evaluation_object_category,
    bws.tag_name,
    bws.tag_code,
    bws.tag_id,
    bws.focus_period_id,
    bws.compare_at,
    bws.benchmark_source_category,
    ss.name AS score_symbol_name,
    ss.code AS score_symbol_code,
    ss.value_type AS score_symbol_value_type,
    ss.numeric_precision AS score_symbol_numeric_precision,
    ss.string_options AS score_symbol_string_options,
    uuid_generate_v4() AS idx
   FROM (((benchmark_with_strategy bws
     JOIN st_benchmark_execute_node ben ON (((bws.benchmark_id)::text = (ben.benchmark_id)::text)))
     JOIN st_benchmark_input_node bin ON (((ben.id)::text = (bin.benchmark_execute_node_id)::text)))
     JOIN st_score_symbol ss ON (((ss.id)::text = (bin.score_symbol_id)::text)))
  WHERE (bws.seq = 1));

create unique index on mv_benchmark_input_node (idx);
CREATE INDEX idx_mv_benchmark_input_node_id ON public.mv_benchmark_input_node USING btree (id);

