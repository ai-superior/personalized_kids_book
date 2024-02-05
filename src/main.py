import uvicorn
from dotenv import load_dotenv

from api.setup import create_fastapi_app
from settings import SETTINGS

load_dotenv()

app = create_fastapi_app()
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=SETTINGS.webserver.host,
        port=SETTINGS.webserver.port,
        reload=SETTINGS.debug,
        timeout_keep_alive=1000,
    )
