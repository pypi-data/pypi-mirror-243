# 掘金量化的简化函数包（第三方）

个人自用包，出问题了欢迎提 Issue。

## 功能列表

### A 股

1. 获取所有指数（股票市场、当前有效）：get_all_index
2. 获取所有股票（股票市场、当前有效）：get_all_security
3. ~~获取龙虎榜股票列表：get_dragon_tiger_list~~

## 打包

1. 更新 [pyproject.toml](pyproject.toml) 文件
2. 执行 `python -m build`
3. 执行 `python -m twine upload dist/*`
4. 对输入框，输入账号：`__token__` 并回车
5. 最后输入 API token 即可