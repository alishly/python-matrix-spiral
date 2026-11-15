import pytest
from aioresponses import aioresponses


from matrix_spiral.matrix import (
    parse_matrix,
    spiral_traversal,
    get_matrix,
    MatrixFormatError,
    MatrixDownloadError,
)


def test_parse_matrix():
    text = """
    | 10 20 30 |
    | 40 50 60 |
    | 70 80 90 |
    """

    expected = [
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90],
    ]

    assert parse_matrix(text) == expected


def test_spiral_traversal():
    matrix = [
        [10, 20, 30, 40],
        [50, 60, 70, 80],
        [90, 100, 110, 120],
        [130, 140, 150, 160],
    ]

    expected = [
        10, 50, 90, 130,
        140, 150, 160,
        120, 80, 40,
        30, 20,
        60, 100, 110, 70,
    ]

    assert spiral_traversal(matrix) == expected


def test_one_element_matrix():
    assert spiral_traversal([[5]]) == [5]


def test_empty_matrix():
    with pytest.raises(MatrixFormatError):
        parse_matrix("")


def test_not_square_matrix():
    text = "1 2 3\n4 5 6"

    with pytest.raises(MatrixFormatError):
        parse_matrix(text)


def test_invalid_matrix():
    text = "1 2\n3 abc"

    with pytest.raises(MatrixFormatError):
        parse_matrix(text)


def test_spiral_traversal_empty_matrix():
    with pytest.raises(MatrixFormatError):
        spiral_traversal([])


@pytest.mark.asyncio
async def test_get_matrix():
    url = "https://example.com/matrix.txt"

    response_text = "1 2\n3 4"

    with aioresponses() as mocked:
        mocked.get(url, status=200, body=response_text)

        result = await get_matrix(url)

    assert result == [1, 3, 4, 2]


@pytest.mark.asyncio
async def test_download_error():
    url = "https://example.com/matrix.txt"

    with aioresponses() as mocked:
        mocked.get(url, status=500)

        with pytest.raises(MatrixDownloadError):
            await get_matrix(url)
