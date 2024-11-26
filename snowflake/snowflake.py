"""
The MIT License (MIT)

Copyright (c) 2022-present TheMultii

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""

from datetime import datetime
from typing import Optional

from .enums import Epoch
from .config import SnowflakeConfig

class Snowflake:
    """
    Class for generating and parsing snowflakes.

    Attributes:
    -----------

    Private:

    __default_config: snowflake.SnowflakeConfig
        The default configuration to use for the snowflake.
    __version: str
        The version of the snowflake library.


    Methods:
    --------

    Public:

    set_config: Sets the configuration to use for the snowflake.
    get_config: Gets the configuration to use for the snowflake.
    generate_discord_snowflake: Generates a snowflake in the Discord format.
    parse_discord_snowflake: Parses a snowflake in the Discord format.
    generate_twitter_snowflake: Generates a snowflake in the Twitter format.
    parse_twitter_snowflake: Parses a snowflake in the Twitter format.
    generate_instagram_snowflake: Generates a snowflake in the Instagram format.
    parse_instagram_snowflake: Parses a snowflake in the Instagram format.
    generate_snowflake: Generates a snowflake in the specified format.
    parse_snowflake: Parses a snowflake in the specified format.


    Raises:
    -------

    ValueError:
        If the snowflake.Epoch or a valid Unix timestamp in milliseconds with maximum length of 13 digits is invalid.
    AssertionError:
        If assertion fails for any reason inside any of the methods.
    """
    
    __default_config = SnowflakeConfig(
        epoch=Epoch.discord,
        leading_bit=False,
        timestamp_length=42,
        param1_length=5,
        param2_length=5,
        sequence_length=12
    )
    __version = "1.0.0b4"

    def __init__(self, config: Optional[SnowflakeConfig] = __default_config) -> None:
        """
        Creates a new instance of Snowflake

        Parameters:
        -----------

        config: Optional[snowflake.SnowflakeConfig]
            The configuration to use for the snowflake. If not provided, the default configuration will be used.
        """
        if config is not None:
            self.__config = config

    def set_config(self, config: SnowflakeConfig) -> None:
        """
        Sets the configuration to use for the snowflake.
        
        Parameters:
        -----------

        config: snowflake.SnowflakeConfig
            The configuration to use for the snowflake.
        """
        self.__config = config

    def get_config(self) -> SnowflakeConfig:
        """
        Gets the configuration to use for the snowflake.

        Returns:
        --------

        snowflake.SnowflakeConfig
            The configuration to use for the snowflake.
        """
        return self.__config

    def generate_discord_snowflake(self, worker: int, process: int, sequence: int, date: Optional[datetime] = None) -> str:
        """
        Generates a snowflake in the Discord format.

        Parameters:
        -----------

        worker: int
            The worker ID to use for the snowflake. Must be between 0 and 31.
        process: int
            The process ID to use for the snowflake. Must be between 0 and 31.
        sequence: int
            The sequence ID to use for the snowflake. This is the number of times the snowflake has been generated in one millisecond. Must be between 0 and 4095.
        date: Optional[datetime]
            The date to use for the snowflake. If not provided, the current date will be used.

        Returns:
        --------

        str
            The generated snowflake.

        Raises:
        -------

        AssertionError:
            If provided arguments are somehow invalid.
        ValueError:
            If provided datetime is before the Discord epoch.
        """
        assert 0 <= worker < 32, "Worker must be between 0 and 31."
        assert 0 <= process < 32, "Process must be between 0 and 31."
        assert 0 <= sequence < 4096, "Sequence must be between 0 and 4095."

        if date is None:
            date = datetime.now()

        __dt_calculated = round(date.timestamp() * 1000) - Epoch.discord.value
        if __dt_calculated < 0:
            raise ValueError("Provided date is before the Discord epoch.")

        __binary_dt_calculated = bin(__dt_calculated)[2:].zfill(42)
        __binary_worker = bin(worker)[2:].zfill(5)
        __binary_process = bin(process)[2:].zfill(5)
        __binary_sequence = bin(sequence)[2:].zfill(12)

        return str(int(f"{__binary_dt_calculated}{__binary_worker}{__binary_process}{__binary_sequence}", 2))

    def parse_discord_snowflake(self, snowflake: str) -> 'tuple[datetime, int, int, int]':
        """
        Parses a snowflake in the Discord format.

        Parameters:
        -----------

        snowflake: str
            The snowflake to parse. Must be a valid Discord snowflake within 17-19 digits. If not, a AssertionError will be raised.

        Returns:
        --------

        tuple[datetime, int, int, int]
            The first element is the date of the snowflake.
            The second element is the worker ID of the snowflake.
            The third element is the process ID of the snowflake.
            The fourth element is the sequence ID of the snowflake.

        Raises:
        -------

        AssertionError:
            If provided snowflake is somehow invalid.
        """
        assert 17 <= len(snowflake) <= 19, "Snowflake must be a valid Discord snowflake within 17-19 digits."

        __snowflake = int(snowflake)
        __binary_snowflake = bin(__snowflake)[2:].zfill(64)
        
        __binary_timestamp = __binary_snowflake[:42]
        __binary_worker = __binary_snowflake[42:47]
        __binary_process = __binary_snowflake[47:52]
        __binary_sequence = __binary_snowflake[52:]

        __timestamp = int(__binary_timestamp, 2)
        __worker = int(__binary_worker, 2)
        __process = int(__binary_process, 2)
        __sequence = int(__binary_sequence, 2)

        __timestamp = round((__timestamp + Epoch.discord.value) / 1000)
        __date = datetime.fromtimestamp(__timestamp)

        return __date, __worker, __process, __sequence

    def generate_twitter_snowflake(self, machine: int, sequence: int, date: Optional[datetime] = None) -> str:
        """
        Generates a snowflake in the Twitter format.

        Parameters:
        -----------

        machine: int
            The machine ID to use for the snowflake. Must be between 0 and 1023.
        sequence: int
            The sequence ID to use for the snowflake. This is the number of times the snowflake has been generated in one millisecond. Must be between 0 and 4095.
        date: Optional[datetime]
            The date to use for the snowflake. If not provided, the current date will be used.

        Returns:
        --------

        str
            The generated snowflake.

        Raises:
        -------

        AssertionError:
            If provided arguments are somehow invalid.
        ValueError:
            If provided datetime is before the Twitter epoch.
        """
        assert 0 <= machine < 1024, "Worker must be between 0 and 1023."
        assert 0 <= sequence < 4096, "Sequence must be between 0 and 4095."

        if date is None:
            date = datetime.now()

        __dt_calculated = round(date.timestamp() * 1000) - Epoch.twitter.value
        if __dt_calculated < 0:
            raise ValueError("Provided date is before the Twitter epoch.")

        __binary_dt_calculated = bin(__dt_calculated)[2:].zfill(41)
        __binary_machine = bin(machine)[2:].zfill(10)
        __binary_sequence = bin(sequence)[2:].zfill(12)

        return str(int(f"0{__binary_dt_calculated}{__binary_machine}{__binary_sequence}", 2))

    def parse_twitter_snowflake(self, snowflake: str) -> 'tuple[datetime, int, int]':
        """
        Parses a snowflake in the Twitter format.

        Parameters:
        -----------

        snowflake: str
            The snowflake to parse. Must be a valid Twitter snowflake within 17-19 digits. If not, a AssertionError will be raised.

        Returns:
        --------

        tuple[datetime, int, int, int]
            The first element is the date of the snowflake.
            The second element is the machine ID of the snowflake.
            The third element is the sequence ID of the snowflake.

        Raises:
        -------

        AssertionError:
            If provided snowflake is somehow invalid.
        """
        assert 17 <= len(snowflake) <= 19, "Snowflake must be a valid Twitter snowflake within 17-19 digits."

        __snowflake = int(snowflake)
        __binary_snowflake = bin(__snowflake)[2:].zfill(64)
        
        __binary_timestamp = __binary_snowflake[1:42]
        __binary_machine = __binary_snowflake[42:52]
        __binary_sequence = __binary_snowflake[52:]

        __timestamp = int(__binary_timestamp, 2)
        __machine = int(__binary_machine, 2)
        __sequence = int(__binary_sequence, 2)

        __timestamp = round((__timestamp + Epoch.twitter.value) / 1000)
        __date = datetime.fromtimestamp(__timestamp)

        return __date, __machine, __sequence

    def generate_instagram_snowflake(self, shard: int, sequence: int, date: Optional[datetime] = None) -> str:
        """
        Generates a snowflake in the Instagram format.

        Parameters:
        -----------

        shard: int
            The shard ID to use for the snowflake. Must be between 0 and 8191.
        sequence: int
            The sequence ID to use for the snowflake. This is the number of times the snowflake has been generated in one millisecond. Must be between 0 and 4095.
        date: Optional[datetime]
            The date to use for the snowflake. If not provided, the current date will be used.

        Returns:
        --------

        str
            The generated snowflake.

        Raises:
        -------

        AssertionError:
            If provided arguemnts are somehow invalid.
        ValueError:
            If provided datetime is before the Instagram epoch.
        """
        assert 0 <= shard < 8192, "Shard must be between 0 and 8191."
        assert 0 <= sequence < 1024, "Sequence must be between 0 and 1023."

        if date is None:
            date = datetime.now()

        __dt_calculated = round(date.timestamp() * 1000) - Epoch.instagram.value
        if __dt_calculated < 0:
            raise ValueError("Provided date is before the Instagram epoch.")

        __binary_dt_calculated = bin(__dt_calculated)[2:].zfill(41)
        __binary_shard = bin(shard)[2:].zfill(13)
        __binary_sequence = bin(sequence)[2:].zfill(10)

        return str(int(f"{__binary_dt_calculated}{__binary_shard}{__binary_sequence}", 2))

    def parse_instagram_snowflake(self, snowflake: str) -> 'tuple[datetime, int, int]':
        """
        Parses a snowflake in the Instagram format.

        Parameters:
        -----------

        snowflake: str
            The snowflake to parse. Must be a valid Instagram snowflake within 17-19 digits. If not, a AssertionError will be raised.

        Returns:
        --------

        tuple[datetime, int, int, int]
            The first element is the date of the snowflake.
            The second element is the shard ID of the snowflake.
            The third element is the sequence ID of the snowflake.

        Raises:
        -------

        AssertionError:
            If provided snowflake is somehow invalid.
        """
        assert 17 <= len(snowflake) <= 19, "Snowflake must be a valid Instagram snowflake within 17-19 digits."

        __snowflake = int(snowflake)
        __binary_snowflake = bin(__snowflake)[2:].zfill(64)
        
        __binary_timestamp = __binary_snowflake[:41]
        __binary_shard = __binary_snowflake[41:54]
        __binary_sequence = __binary_snowflake[54:]

        __timestamp = int(__binary_timestamp, 2)
        __shard = int(__binary_shard, 2)
        __sequence = int(__binary_sequence, 2)

        __timestamp = round((__timestamp + Epoch.instagram.value) / 1000)
        __date = datetime.fromtimestamp(__timestamp)

        return __date, __shard, __sequence

    def generate_snowflake(self, param1: int, sequence: int, date: Optional[datetime] = None, **kwargs) -> str:
        """
        Generates a snowflake in the specified format.
        
        Parameters:
        -----------

        param1: int
            The first parameter to use for the snowflake. Must be between 0 and (10**(config.param1_length) - 1)
        sequence: int
            The sequence ID to use for the snowflake. This is the number of times the snowflake has been generated in one millisecond. Must be between 0 and (10**(config.sequence_length) - 1).
        date: Optional[datetime]
            The date to use for the snowflake. If not provided, the current date will be used.
        kwargs: 
            param2: Optional[int]:
                If config.param2_length is provided and greater than 0, the second parameter to use for the snowflake. Must be between 0 and (10**(config.param2_length) - 1)

        Returns:
        --------

        str
            The generated snowflake.

        
        Raises:
        -------

        TypeError:
            If (based on config) required param2 is not provided.
        ValueError:
            If provided datetime is before the epoch.
        AssertionError:
            If provided arguments are somehow invalid.
        """

        if self.__config is None:
            raise TypeError("SnowflakeConfig must be provided.")

        __param2 = kwargs.get("param2", None)
        if __param2 is None and self.__config.param2_length > 0:
            raise TypeError("Required param2 is not provided.")
        
        assert 0 <= param1 < 10 ** self.__config.param1_length, "Param1 must be between 0 and (10**(config.param1_length) - 1)"
        assert 0 <= sequence < 10 ** self.__config.sequence_length, "Sequence must be between 0 and (10**(config.sequence_length) - 1)"

        if date is None:
            date = datetime.now()

        epoch_value = self.__config.epoch.value if isinstance(self.__config.epoch, Epoch) else self.__config.epoch
        __dt_calculated = round(date.timestamp() * 1000) - epoch_value
        if __dt_calculated < 0:
            raise ValueError("Provided date is before the epoch.")
        __binary_dt_calculated = bin(__dt_calculated)[2:].zfill(self.__config.timestamp_length)
        __param1_calculated = bin(param1)[2:].zfill(self.__config.param1_length)
        __param2_calculated = None
        if __param2 is not None:
            __param2_calculated = bin(__param2)[2:].zfill(self.__config.param2_length)
        __sequence_calculated = bin(sequence)[2:].zfill(self.__config.sequence_length)

        __binary_string = f"{0 if self.__config.leading_bit else ''}{__binary_dt_calculated}{__param1_calculated}{__param2_calculated}{__sequence_calculated}"

        assert len(__binary_string) == 64, "Binary string length is incorrect."

        return str(int(__binary_string, 2))

    def parse_snowflake(self, snowflake: str) -> 'tuple[datetime, int, int, Optional[int]]':
        """
        Parses a snowflake in the specified format.

        Parameters:
        -----------

        snowflake: str
            The snowflake to parse. Must be a valid snowflake within 17-19 digits based on provided config. If not, a AssertionError will be raised.

        Returns:
        --------

        tuple[datetime, int, int, Optional[int]]
            The first element is the date of the snowflake.
            The second element is the param1 of the snowflake.
            If param2 is provided, the third element is the param2 of the snowflake. If not, the third element is sequence ID of the snowflake.
            If param2 is provided, the fourth element is sequence ID of the snowflake. If not, the fourth element is not being returned.

        Raises:
        -------

        TypeError:
            If config is not provided.
        AssertionError:
            If provided snowflake is somehow invalid.
        """

        if self.__config is None:
            raise TypeError("SnowflakeConfig must be provided.")

        assert 17 <= len(snowflake) <= 19, "Snowflake must be a valid snowflake within 17-19 digits."

        __snowflake = int(snowflake)
        __binary_snowflake = bin(__snowflake)[2:].zfill(64)
        
        __binary_timestamp = __binary_snowflake[:self.__config.timestamp_length]
        __binary_param1 = __binary_snowflake[self.__config.timestamp_length:(self.__config.timestamp_length + self.__config.param1_length)]
        __binary_param2 = None
        __binary_sequence = __binary_snowflake[(self.__config.timestamp_length + self.__config.param1_length + self.__config.param2_length):]
        if self.__config.param2_length > 0:
            __binary_param2 = __binary_snowflake[(self.__config.timestamp_length + self.__config.param1_length):(self.__config.timestamp_length + self.__config.param1_length + self.__config.param2_length)]
            __binary_sequence = __binary_snowflake[(self.__config.timestamp_length + self.__config.param1_length + self.__config.param2_length):]

        epoch_value = self.__config.epoch.value if isinstance(self.__config.epoch, Epoch) else self.__config.epoch
        __timestamp = round((int(__binary_timestamp, 2) + epoch_value) / 1000)
        __param1 = int(__binary_param1, 2)
        __param2 = int(__binary_param2, 2) if __binary_param2 is not None else None
        __sequence = int(__binary_sequence, 2)

        __date = datetime.fromtimestamp(__timestamp)

        return (__date, __param1, __sequence) if __param2 is None else (__date, __param1, __param2, __sequence)
