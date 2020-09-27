from fastapi import FastAPI

from .routers import index, recaptcha, submit_recaptcha

app = FastAPI()

app.include_router(index.router)
app.include_router(recaptcha.router, prefix="/recaptcha")
app.include_router(submit_recaptcha.router, prefix="/recaptcha")
