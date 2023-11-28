## yatbaf

Asynchronous [Telegram Bot API](https://core.telegram.org/bots/api) framework.

## Requirements

Python 3.11+

## Installation

```shell
$ pip install yatbaf
```

## Simple echo bot

```python
from yatbaf import Bot, on_message


@on_message
async def echo(message):
    await message.answer(message.text)


Bot("<REPLACE-WITH-YOUR-TOKEN>", [echo]).run()
```

## License
[MIT](./LICENSE)
