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

from typing import Optional, Union
from .enums import Epoch


class SnowflakeConfig:
    """
    Represents the configuration for a snowflake.
    """

    def __init__(self, epoch: Union[Epoch, int], leading_bit: bool = False, timestamp_length: int = 42, param1_length: int = 5, param2_length: Optional[int] = 5, sequence_length: int = 5):
        """
        Initializes a new instance of the SnowflakeConfig class.

        Parameters:
        -----------

        epoch: Union[snowflake.Epoch, int]
            The epoch to use for the snowflake. Must be a snowlake.Epoch or a valid Unix timestamp in milliseconds with maximum length of 13 digits.
        leading_bit: bool = False
            Whether or not to use the leading bit for the snowflake.
        timestamp_length: int = 42
            The length of the timestamp in bits. Sum of leading_bit, timestamp_length, param1_length, param2_length, sequence_length must be exactly 64.
        param1_length: int = 5
            The length of the first parameter in bits. Sum of leading_bit, timestamp_length, param1_length, param2_length, sequence_length must be exactly 64.
        param2_length: Optional[int] = 5
            The length of the second parameter in bits. It is optional argument and can be omitted. Sum of leading_bit, timestamp_length, param1_length, param2_length, sequence_length must be exactly 64.
        sequence_length: int = 12
            The length of the sequence in bits. Sum of leading_bit, timestamp_length, param1_length, param2_length, sequence_length must be exactly 64.
        
        
        Methods:
        --------

        Public:

        get_config: Returns the configuration as a dictionary.


        Raises:
        -------

        ValueError:
            If the snowflake.Epoch or a valid Unix timestamp in milliseconds with maximum length of 13 digits is invalid.
        AssertionError:
            If the sum of leading_bit, timestamp_length, param1_length, param2_length, sequence_length is not exactly 64.
        """
        if isinstance(epoch, Epoch):
            self.epoch = epoch
        elif len(str(epoch)) <= 13 and epoch >= 0:
            self.epoch = epoch
        else:
            raise ValueError("Must be a snowlake.Epoch or a valid Unix timestamp in milliseconds with maximum length of 13 digits.")
        
        assert (1 if leading_bit else 0) + timestamp_length + param1_length + (param2_length or 0) + sequence_length == 64, "Sum of leading_bit, timestamp_length, param1_length, param2_length, sequence_length must be exactly 64."

        self.leading_bit = leading_bit
        self.timestamp_length = timestamp_length
        self.param1_length = param1_length
        self.param2_length = param2_length
        self.sequence_length = sequence_length

    def get_config(self) -> dict:
        """
        Returns the configuration as a dictionary.
        """
        return {
            "epoch": self.epoch,
            "leading_bit": self.leading_bit,
            "timestamp_length": self.timestamp_length,
            "param1_length": self.param1_length,
            "param2_length": self.param2_length,
            "sequence_length": self.sequence_length
        }