import uvicorn
from src.bot import run
from src.config import ENV
import asyncio


def test():
    run(
        "https://www.temu.com/search_result.html?search_key=birthday%20gift",
        3,
    )


# Launch API
def main():
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=ENV == "dev",
    )


if __name__ == "__main__":
    test()
    # main()
