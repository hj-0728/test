# 一些约定

## 关于使用了start_at、finish_at字段的表的一些处理逻辑

- 列表页通常只捞出`start_at < now < finish_at`的数据
- 删除的时候不再物理删除，而是把`finish_at`设置为删除时的时间
- 若需要为这些表简历当前数据的视图，则命名为`cv_`，如`cv_benchmark_strategy`
- 若其他视图需要用到这类表的当前数据，不建议用上述所说的`cv_`开头的视图，宁可在其他视图里面多写几次判断，也尽量避免视图嵌套

## 关于service、repository等类名重复的问题

- 如果存在在biz、backbone等底层包已经命名过的文件名/类名，那么在backend等上层包就加上如app等约定的前缀。可参考AppAbilityPermissionService的做法

# 待讨论确定的约定

- 如service中会引用repository等，添加为self的属性时用`_`还是`__`
- 对前端src/api/xxx结构可以再讨论下，现在这样每个ts建一个文件夹放，似乎显得累赘
- 后端python枚举的使用声明：如EnumRoleCode，除了SYSTEM_ADMIN应该放在role_model中的枚举，其他值应该在biz的包里面定义（如果backbone是一个pypi的包，像我们现在这样随心所欲的写法就不满足啦）
