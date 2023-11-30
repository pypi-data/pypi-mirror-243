# *wsidicom-data*

Test data for [wsidicom](https://github.com/imi-bigpicture/wsidicom).

## Install

Install from pypi:

```terminal
pip install wsidicom-data
```

## Re-creating encoded test data

```terminal
python .\wsidicom_data\create_encoded_test_files.py
```

## Accessing test data

```python
from wsidicom_data import TestData, EncodedTestData, defined_encoder_settings

test_tile_path = TestData.get_test_tile_path()

settings = defined_encoder_settings[0]
encoded_test_file_path = EncodedTestData.get_filepath_for_encoder_settings(settings)

```

## Description of data

* `test_tile.png` is extracted from `CMU-1-Small-Region.svs` in the [OpenSlide test data set](https://openslide.cs.cmu.edu/download/openslide-testdata/Aperio/)
* Encoded test data is created from the `test_tile.png` using different encoders. The target transfer syntax, color, and bits per pixel is given in the filename.
