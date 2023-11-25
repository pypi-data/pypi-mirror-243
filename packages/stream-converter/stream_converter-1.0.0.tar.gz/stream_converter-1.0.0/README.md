A simple package for applying transformations to streaming data.

# Stream Conversion

This package can handle stream functions and stream generators.

Here's an example with functions:

```python
from random import randint
from stream_converter.converter import convert_function_stream


def get_random_number() -> int:
    return randint(0, 100)


converted_stream = convert_function_stream(
    stream_function=get_random_number,
    conversion_function=lambda byte: str(byte),
)
for converted_chunk in converted_stream:
    print(converted_chunk)
```

And here's an example with generators:

```python
from random import randint
from typing import Generator
from stream_converter.converter import convert_generator_stream


def get_random_number_generator() -> Generator[int, None, None]:
    while True:
        yield randint(0, 100)


converted_stream = convert_generator_stream(
    stream_generator=get_random_number_generator(),
    conversion_function=lambda int: "odd" if int % 2 else "even"
)
for converted_chunk in converted_stream:
    print(converted_chunk)
```

# Built-In Stream Support

## Microphone via PyAudio

```python
from stream_converter.converter import convert_generator_stream, convert_function_stream
from stream_converter.microphone_stream import get_microphone_stream_generator, MicrophoneStream


# generator
converted_stream = convert_generator_stream(
    stream_generator=get_microphone_stream_generator(),
    conversion_function=lambda byte: str(byte),
)
for converted_chunk in converted_stream:
    print(converted_chunk)


# function
with MicrophoneStream() as microphone_stream:
    converted_stream = convert_function_stream(
        stream_function=microphone_stream.read,
        conversion_function=lambda byte: str(byte),
    )
    for converted_chunk in converted_stream:
        print(converted_chunk)
```
