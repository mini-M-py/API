from fastapi import FastAPI
from .routers import post, user, auth, vote, comments
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

#model.Base.metadata.create_all(bind=engine)
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#app.add_middleware(HTTPSRedirectMiddleware)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(comments.router)
@app.get("/")
async def root():
    return {"message":"welcome to my api!!!!!!!!!!"}


