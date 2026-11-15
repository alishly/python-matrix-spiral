
import asyncio

from matrix_spiral.matrix import get_matrix


URL = (
    "https://raw.githubusercontent.com/"
    "avito-tech/python-trainee-assignment/main/matrix.txt"
)


async def main():
    result = await get_matrix(URL)
    print("Результат:", result)


if __name__ == "__main__":
    asyncio.run(main())
