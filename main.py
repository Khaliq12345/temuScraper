import uvicorn
from src.bot import run
from src.config import ENV


def test():
    result = run(
        "https://www.temu.com/search_result.html?search_key=birthday%20gift",
        3,
    )
    print(result)


# Launch API
def main():
    uvicorn.run(
        "src.api:app",
        host="localhost",
        port=8000,
        reload=ENV == "dev",
    )


if __name__ == "__main__":
    # test()
    main()
