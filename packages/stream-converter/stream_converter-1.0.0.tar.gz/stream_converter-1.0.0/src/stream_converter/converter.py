from typing import Generator, Callable, Generator


def convert_function_stream(
    stream_function: Callable,
    conversion_function: Callable,
) -> Generator[str, None, None]:
    while True:
        stream_chunk = stream_function()
        yield conversion_function(stream_chunk)


def convert_generator_stream(
    stream_generator: Generator,
    conversion_function: Callable,
) -> Generator[str, None, None]:
    for stream_chunk in stream_generator:
        yield conversion_function(stream_chunk)
