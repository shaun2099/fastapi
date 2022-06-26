from typing import Optional, List
from fastapi import Body, Depends, FastAPI, Response, HTTPException, status
from pydantic import BaseModel, BaseSettings
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas, utils
from .database import Base, engine, get_db
from sqlalchemy.orm import Session
from .routers import post, user, auth
from .config import settings

print(settings)
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get('/')
async def root():
    return {"message": "Hello to my new World"}


# try:
#     conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                             password='123456', cursor_factory=RealDictCursor)
#     cursor = conn.cursor()
#     print('db connected ...')
# except Exception as e:
#     print('db connection error: ', e)
#     # print(e)
#     exit()


# @app.get('/posts')
# async def get_posts():
#     cursor.execute("""SELECT * FROM post""")
#     posts = cursor.fetchall()
#     return posts


# @app.get('/posts/{post_id}')
# async def get_post(post_id: int, response: Response):
#     cursor.execute(f"""SELECT * FROM post WHERE id = {post_id}""")
#     post = cursor.fetchone()
#     if not post:
#         # response.status_code = 404
#         raise HTTPException(status_code=404, detail=f"Post not found for id: {post_id}")
#     return post


# @app.post("/posts", response_model=Post, status_code=201)
# async def create_post(post: Post):
#     cursor.execute(""" insert into post (title, content, published) values (%s, %s, %s) returning * """,
#                    [post.title, post.content, post.published])
#     post = cursor.fetchone()
#     conn.commit()
#     return post

# @app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(post_id: int):
#     cursor.execute("""DELETE FROM post WHERE id = %s returning * """, [post_id])
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if not deleted_post:
#         raise HTTPException(status_code=404, detail=f"Post not found for id: {post_id}")

#     # return {"message": "Post deleted"}
#     return Response(status_code=204)


# @app.put("/posts/{post_id}", status_code=status.HTTP_200_OK)
# async def update_post(post_id: int, post: Post):
#     cursor.execute("""UPDATE post SET title = %s, content = %s, published = %s WHERE id = %s returning * """,
#                    [post.title, post.content, post.published, post_id])
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if not updated_post:
#         raise HTTPException(status_code=404, detail=f"Post not found for id: {post_id}")

#     return updated_post
