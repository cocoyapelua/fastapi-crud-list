from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Text, Optional
from datetime import datetime

app = FastAPI()

posts = []


# Post Model
class Post(BaseModel):
    id: Optional[int]
    title: str
    author: str
    content: Text
    created_at: datetime = datetime.now()
    published_at: Optional[datetime]
    published: bool = False


@app.get('/')
def read_root():
    return {"welcome": "welcome to my rest api"}


@app.get('/posts')
def get_posts():
    return posts


@app.post('/posts')
def save_post(post: Post):
    posts.append(post.dict())
    return posts[-1]


@app.get('/posts/{post_id}')
def get_post(post_id: int):
    for post in posts:
        if post['id'] == post_id:
            return post
    return HTTPException(status_code=404, detail=f"post {post_id} not found")


@app.put('/posts/{post_id}')
def update_post(post_id: int, updated_post: Post):
    for index, post in enumerate(posts):
        if post["id"] == post_id:
            posts[index]["title"] = updated_post.title
            posts[index]["author"] = updated_post.author
            posts[index]["content"] = updated_post.content
            return {"message": "the post has been updated"}
    return HTTPException(status_code=404, detail=f"post {post_id} not found")


@app.delete('/posts/{post_id}')
def delete_post(post_id: int):
    for index, post in enumerate(posts):
        if post['id'] == post_id:
            posts.pop(index)
            return {"message": "the post has been deleted"}
    return HTTPException(status_code=404, detail=f"post {post_id} not found")
