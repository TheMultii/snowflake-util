# snowflake-util

A Python library for generating Discord, Twitter, Instagram and custom snowflakes.

A snowflake is a unique identifier for a resource that includes, among other things, a timestamp of when such a snowflake was created. Snowflakes are used by Twitter, Discord or Instagram. They were created by Twitter in 2010.

Developed by TheMultii (c) 2022-present

## Installing
```bash
# Linux/macOS
python3 -m pip install -U snowflake-util

# Windows
py -3 -m pip install -U snowflake-util
```

## Examples of How To Use

Creating a custom snowflake

```python
from datetime import datetime
import snowflake

config = snowflake.SnowflakeConfig(
    epoch=snowflake.Epoch.discord, # or Unix timestamp in milliseconds with maximum length of 13 digits.
    leading_bit=False,
    timestamp_length=42,
    param1_length=5,
    param2_length=5,
    sequence_length=12
)

SnowClass = snowflake.Snowflake(config)

custom_snowflake = SnowClass.generate_snowflake(param1=11, param2=3, sequence=753)
custom_snowflake_TS = SnowClass.generate_snowflake(param1=14, param2=9, sequence=357, date=datetime(2021, 8, 8, 8, 8, 0, 0))

print(custom_snowflake, SnowClass.parse_snowflake(custom_snowflake))
print(custom_snowflake_TS, SnowClass.parse_snowflake(custom_snowflake_TS))
```

Creating a Discord snowflake
```python
SnowClass = snowflake.Snowflake()

discord_snowflake = SnowClass.generate_discord_snowflake(worker=5, process=5, sequence=222, date=datetime(2022, 1, 1, 16, 15, 0, 0))

print(discord_snowflake, SnowClass.parse_discord_snowflake(discord_snowflake))
```

Creating a Twitter snowflake
```python
SnowClass = snowflake.Snowflake()

twitter_snowflake = SnowClass.generate_twitter_snowflake(machine=333, sequence=666, date=datetime(2022, 1, 1, 16, 15, 0, 0))

print(twitter_snowflake, SnowClass.parse_twitter_snowflake(twitter_snowflake))
```

Creating an Instagram snowflake
```python
SnowClass = snowflake.Snowflake()

instagram_snowflake = SnowClass.generate_instagram_snowflake(shard=1605, sequence=420, date=datetime(2020, 6, 11, 8 ,13))

print(instagram_snowflake, SnowClass.parse_instagram_snowflake(instagram_snowflake))
```

## IMPORTANT INFO:
- Generating any snowflakes does not require sending the date as an argument - the snowflake will be generated based on the current time.
- `snowflake.SnowflakeConfig` is not required if you want to use any of the ready-made templates for generating/reading snowflakes (Twitter, Discord, Instagram)
- You can edit and read the current configuration settings using the `Snowflake.set_config()` and `Snowflake.get_config()` methods.
- All methods are documented in the code.
- The `leading_bit` is used by Twitter to generate snowflakes.
- For custom configuration, sum of `leading_bit, timestamp_length, param1_length, param2_length, sequence_length` must be exactly 64.
- Snowflakes can only be generated for dates that are after the set epoch.
- There must be a 64-bit representation for each snowflake.


## References
- https://en.wikipedia.org/wiki/Snowflake_ID
- https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake

## License
MIT