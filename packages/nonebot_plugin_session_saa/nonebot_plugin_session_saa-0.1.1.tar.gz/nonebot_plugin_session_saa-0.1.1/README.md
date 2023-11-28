## nonebot-plugin-session-saa

- 提供从 [session](https://github.com/noneplugin/nonebot-plugin-session) 获取 [saa](https://github.com/MountainDash/nonebot-plugin-send-anything-anywhere) 发送对象 [PlatformTarget](https://github.com/MountainDash/nonebot-plugin-send-anything-anywhere/blob/main/nonebot_plugin_saa/utils/platform_send_target.py) 的方法


### 安装

- 使用 nb-cli

```
nb plugin install nonebot_plugin_session_saa
```

- 使用 pip

```
pip install nonebot_plugin_session_saa
```

### 使用

```python
from nonebot import require

require("nonebot_plugin_session_saa")

from nonebot_plugin_session import EventSession
from nonebot_plugin_session_saa import get_saa_target

@matcher.handle()
async def handle(session: EventSession):
    target = get_saa_target(session)
```
