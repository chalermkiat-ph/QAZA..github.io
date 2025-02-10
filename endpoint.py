import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apis import PersonalAPI
from apis.api import personal_api

# mariadb_host = os.getenv("MARIADB_HOST")
# mariadb_port = int(os.getenv("MARIADB_PORT"))
# mariadb_user = os.getenv("MARIADB_USER")
# mariadb_password = os.getenv("MARIADB_PASSWORD")
# mariadb_dbname = os.getenv("MARIADB_DBNAME")


# GrafanaUISAPI(host='mariadb', port=3306, user='pmuser', password='passw0rd', database_name='pmdb')

PersonalAPI('./databases/people.db')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(personal_api.router)


@app.get("/")
def root():
    return {"message": "Hello QA ZA API"}


if __name__ == "__main__":
    uvicorn.run("endpoint:app")
