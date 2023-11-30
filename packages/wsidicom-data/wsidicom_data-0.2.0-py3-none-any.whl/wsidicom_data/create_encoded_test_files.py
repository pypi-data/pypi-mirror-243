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

"""Module for creating encoded test data."""

import hashlib

from wsidicom.codec import Encoder

from wsidicom_data.test_data import EncodedTestData, TestData, defined_encoder_settings


def create_encoded_test_files():
    for settings in defined_encoder_settings:
        image = TestData.image(settings.bits, settings.samples_per_pixel)
        encoder = Encoder.create(settings)
        encoded = encoder.encode(image)
        output_path = EncodedTestData.get_filepath_for_encoder_settings(settings)
        with open(output_path, "wb") as file:
            file.write(encoded)
        print(
            "Created test file for settings:",
            settings,
            hashlib.sha256(encoded).hexdigest(),
        )


create_encoded_test_files()
