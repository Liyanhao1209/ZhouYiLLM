# 生成access_key
根据百度ocr的技术文档(https://ai.baidu.com/ai-doc/REFERENCE/Ck3dwjhhu)，首先我们要先在创建应用后获取access_key

这个过程没有GUI，只能请求百度ocr的一个鉴权接口获得，这一部分我已经放在了./authorize/Gen_Access_Key中

当你运行这个脚本前，首先前往./config/auth_config.json中配置自己的API_Key，Secret_Key以及AppID

随后运行脚本，脚本会在./config/auth_config中写入access_token以及它的过期时间。