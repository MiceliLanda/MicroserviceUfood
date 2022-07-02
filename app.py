from fastapi import FastAPI
from routes.user import userRoute
import uvicorn

app = FastAPI()
app.include_router(userRoute)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=9000, reload=True)