#    Copyright 2023 SECTRA AB
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Module for getting test data."""

from pathlib import Path
from typing import List

from wsidicom.codec import (
    Channels,
    Jpeg2kSettings,
    JpegLosslessSettings,
    JpegLsLosslessSettings,
    JpegSettings,
    NumpySettings,
    RleSettings,
    Settings,
    Subsampling,
)
from PIL.Image import Image as PILImage
from PIL import Image


class TestData:
    test_data_path = Path(__file__).parent.joinpath("data")

    @classmethod
    def get_test_tile_path(cls) -> Path:
        return cls.test_data_path.joinpath("test_tile.png")

    @classmethod
    def rgb(cls) -> PILImage:
        return Image.open(cls.get_test_tile_path())

    @classmethod
    def grayscale_8(cls) -> PILImage:
        return cls.rgb().convert("L")

    @classmethod
    def grayscale_12(cls) -> PILImage:
        return cls._scale_bits(cls._grayscale_32(), 8, 12).convert("I;16L")

    @classmethod
    def grayscale_16(cls) -> PILImage:
        return cls._scale_bits(cls._grayscale_32(), 8, 16).convert("I;16L")

    @classmethod
    def image(cls, bits: int, samples_per_pixel: int) -> PILImage:
        if samples_per_pixel == 1:
            if bits == 8:
                return cls.grayscale_8()
            elif bits == 12:
                return cls.grayscale_12()
            elif bits == 16:
                return cls.grayscale_16()
        elif samples_per_pixel == 3 and bits == 8:
            return cls.rgb()
        raise ValueError(
            f"Unsupported bit depth {bits} or samples_per_pixel {samples_per_pixel}."
        )

    @classmethod
    def _grayscale_32(cls) -> PILImage:
        return cls.rgb().convert("I")

    @classmethod
    def _scale_bits(cls, image: PILImage, from_bits: int, to_bits: int) -> PILImage:
        return image.point(lambda x: 2 ** (to_bits - from_bits) * x)


class EncodedTestData:
    test_data_path = Path(__file__).parent.joinpath("data", "encoded")

    @classmethod
    def get_filepath_for_encoder_settings(cls, settings: Settings):
        filename = "-".join(
            (
                settings.transfer_syntax.name.replace(" ", "_"),
                settings.channels.name,
                str(settings.bits),
            )
        )
        return cls.test_data_path.joinpath(filename).with_suffix(settings.extension)


defined_encoder_settings: List[Settings] = [
    JpegSettings(95, 8, Channels.GRAYSCALE),
    JpegSettings(95, 8, Channels.YBR, Subsampling.R444),
    JpegSettings(95, 8, Channels.RGB, Subsampling.R444),
    JpegSettings(95, 12, Channels.GRAYSCALE),
    JpegLosslessSettings(7, 8, Channels.GRAYSCALE),
    JpegLosslessSettings(7, 8, Channels.YBR),
    JpegLosslessSettings(7, 8, Channels.RGB),
    JpegLosslessSettings(7, 16, Channels.GRAYSCALE),
    JpegLosslessSettings(1, 8, Channels.GRAYSCALE),
    JpegLosslessSettings(1, 8, Channels.YBR),
    JpegLosslessSettings(1, 8, Channels.RGB),
    JpegLosslessSettings(1, 16, Channels.GRAYSCALE),
    JpegLsLosslessSettings(0, 8),
    JpegLsLosslessSettings(0, 16),
    JpegLsLosslessSettings(1, 8),
    JpegLsLosslessSettings(1, 16),
    Jpeg2kSettings(80, 8, Channels.GRAYSCALE),
    Jpeg2kSettings(80, 8, Channels.YBR),
    Jpeg2kSettings(80, 8, Channels.RGB),
    Jpeg2kSettings(80, 16, Channels.GRAYSCALE),
    Jpeg2kSettings(0, 8, Channels.GRAYSCALE),
    Jpeg2kSettings(0, 8, Channels.YBR),
    Jpeg2kSettings(0, 8, Channels.RGB),
    Jpeg2kSettings(0, 16, Channels.GRAYSCALE),
    RleSettings(8, Channels.GRAYSCALE),
    RleSettings(8, Channels.RGB),
    RleSettings(16, Channels.GRAYSCALE),
    NumpySettings(8, Channels.GRAYSCALE, True, True),
    NumpySettings(8, Channels.GRAYSCALE, True, False),
    NumpySettings(8, Channels.GRAYSCALE, False, True),
    NumpySettings(16, Channels.GRAYSCALE, True, True),
    NumpySettings(16, Channels.GRAYSCALE, True, False),
    NumpySettings(16, Channels.GRAYSCALE, False, True),
    NumpySettings(8, Channels.RGB, True, True),
    NumpySettings(8, Channels.RGB, True, False),
    NumpySettings(8, Channels.RGB, False, True),
]
