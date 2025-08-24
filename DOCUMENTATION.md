- [1 Coding CRUD](#1-coding-crud)
  - [1.2 Using Pydantic](#12-using-pydantic)
  - [1.3 Creating a global variable and retrieving the info stored in the variable (GET)](#13-creating-a-global-variable-and-retrieving-the-info-stored-in-the-variable-get)
  - [1.4 Getting post by id (GET)](#14-getting-post-by-id-get)
  - [1.5 Creating/adding a post with random id (POST)](#15-creatingadding-a-post-with-random-id-post)
  - [1.6 Returning a personalizaed Http status with and without HTTPException (GET)](#16-returning-a-personalizaed-http-status-with-and-without-httpexception-get)
  - [1.7 Delete post old/ new find post fucntion (DELETE)](#17-delete-post-old-new-find-post-fucntion-delete)
  - [1.8 Updating posts (PUT)](#18-updating-posts-put)
- [2 Data Base implementation](#2-data-base-implementation)
  - [Response pydantic v1.1.3](#response-pydantic-v113)
    - [We need to define the schema and serializer:](#we-need-to-define-the-schema-and-serializer)
    - [And update the code](#and-update-the-code)
      - [Multipole posts](#multipole-posts)
- [3 User  and password hashing v1.1.4](#3-user--and-password-hashing-v114)
  - [Creating user table](#creating-user-table)
  - [Creating api-endpoint/function add user](#creating-api-endpointfunction-add-user)
  - [Creating the pydantic schema for request and response](#creating-the-pydantic-schema-for-request-and-response)
  - [Hashing User Password](#hashing-user-password)
  - [Adding *Utils.py* file function call.](#adding-utilspy-file-function-call)
- [4 Splitting main.py using routers v1.1.5](#4-splitting-mainpy-using-routers-v115)
  - [Routing Prefix and tags](#routing-prefix-and-tags)

# 1 Coding CRUD

```python
 from fastapi import FastAPI #import the library
 from fastapi.params import Body

 app=FastAPI() #create instance of fastapi

 @app.get("/fran")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
 def root(): #root=funtion name (does not matter)
     return {"message": "Hello World"}

 @app.get("/posts")
 def get_posts():
     return{"data": "this is your posts"}

 @app.post("/createpost")
 def create_posts(payload: dict =Body(...)): #this gets the body from the post ,convert into a python dictionary and print save it into variable
     print (payload)
     return{"new_post": f"title: {payload['title']}"+" , succesfully created post"}


```

## 1.2 Using Pydantic

- Pydantic allows to define a schema for data validation, additionally, performs error handling

```python
from typing import Optional
from fastapi import FastAPI #import the library
from fastapi.params import Body
from pydantic import BaseModel

app=FastAPI() #create instance of fastapi

class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true
    rating: Optional[int]= None #Optional filed with no default value , type integer
    
    

@app.get("/fran")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
def root(): #root=funtion name (does not matter)
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return{"data": "this is your posts"}

@app.post("/createpost")
def create_posts(new_post: Post): #We are refenrcing the Post class that validates if the post meets the scheme requirements(pydantic)
    print (new_post)# print is internal, we are not retunring info to the client.
    print (new_post.dict()) #Converting  the Pydantic model into a dict
    return{"message_from_server": "new post added, " f"title: {new_post.title}"} # accessing the title attribute of  new_poost

#title str, content str, category

```


## 1.3 Creating a global variable and retrieving the info stored in the variable (GET)

- At this moment the variable will act as DDBB
```python
from typing import Optional
from fastapi import FastAPI #import the library
from fastapi.params import Body
from pydantic import BaseModel

app=FastAPI() #create instance of fastapi

class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true
    rating: Optional[int]= None #Optional filed with no default value , type integer
    
my_posts= [{"id":1,"title": "this is the post 1","content":"content of post"},{"id":2,"title": "this is the post 2","content":"pizza"}] #creating a global variable for storing the posts in memory (not using ddbb)  it's an array/dict  

@app.get("/")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
def root(): #root=funtion name (does not matter)
    return {"message": "Hello World"}

@app.get("/posts")
def get_posts():
    return{"data": my_posts} #passing the variable

@app.post("/posts")
def create_posts(new_post: Post): #We are refenrcing the Post class that validates if the post meets the scheme requirements(pydantic)
    print (new_post)# print is internal, we are not retunring info to the client.
    print (new_post.dict()) #Converting  the Pydantic model into a dict
    return{"message_from_server": "new post added, " f"title: {new_post.title}"} # accessing the title attribute of  new_poost

#title str, content str, category
```
## 1.4 Getting post by id (GET)

```python

# function to find post

my_posts= [{"id":1,"title": "this is the post 1","content":"content of post"},
           {"id":2,"title": "this is the post 2","content":"pizza"}] #creating a global variable for storing the posts in memory (not using ddbb) its an array of dictionaries

def find_post(id):
    for i in my_posts:  # Iterates over dictionaries and returns the matching dictionary
        if i['id'] == id:
            return i  # Returns the matching dictionary if the condition is true
    print(id)
    return None  # In case no matching id is found

#retrieving post by id

@app.get("/posts/{id}")  # Get post per id (decorator/path parameter)
def get_post(id: int):#performing validation with fast api we are saying I want an integer.
    post = find_post(id)
    if post: #in python not empty values are considered as true same as: if post != {} (si no esta vacio... damelo else error)
        return {"post_info": post}  # Returns the entire post if found
    else:
        return {"error": f"Post not found. ID: {id}"}  # Returns an error message if no matching post is found

```
## 1.5 Creating/adding a post with random id (POST)

```python
my_posts= [{"id":1,"title": "this is the post 1","content":"content of post"},
           {"id":2,"title": "this is the post 2","content":"pizza"}]

@app.post("/posts") #adding the post to a dict and to the my_post array of dict
def create_posts(new_post: Post): #function expects new_post param. compliance with pydantic Post class
    post_dict=new_post.model_dump()# We create a dict witht the info we are gonna get
    post_dict['id']=randrange(0, 100000)#from that info the id is gonna be rand adding to the dictionary
    my_posts.append(post_dict)#here we are adding the new post with the rand id to the variable, addind the dictionary to the variable
    title=post_dict['title']
    return {"message_from_server": f"New post added: {post_dict}. Title: {title}"}
```

## 1.6 Returning a personalizaed Http status with and without HTTPException (GET)

 
```python
from fastapi import FastAPI, Response, status 

my_posts= [{"id":1,"title": "this is the post 1","content":"content of post"},
           {"id":2,"title": "this is the post 2","content":"pizza"}]

def find_post(id):
    for i in my_posts:  # Iterates over dictionaries and returns the matching dictionary
        if i['id'] == id:
            return i  # Returns the matching dictionary if the condition is true
    print(id)
    return None  # In case no matching id is found

#retrieving post by id

@app.get("/posts/{id}")  # Get post per id (decorator/path parameter)
def get_post(id: int,response: Response):#This generates an instance of Response class called "response"
    post = find_post(id)
    if post: #in python not empty values are considered as true same as: if post != {} (si no esta vacio... damelo else error)
        return {"post_info": post}  # Returns the entire post if found
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post not found ID: {id}"})
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"error": f"Post not found ID: {id}"}  # Returns an error message if no matching post is found

  # Returns an error message if no matching post is found

```
**Adding it at decorator**
- useful for default operations
``@app.post("/posts", status_code=status.HTTP_201_CREATED)`` 

## 1.7 Delete post old/ new find post fucntion (DELETE)

- Variable

```Python
my_posts= [{"id":1,"title": "this is the post 1","content":"content of post"},
           {"id":2,"title": "this is the post 2","content":"pizza"}]
```

*Deleting post by **id***

```Python

#deleting post by id

@app.delete("/posts/{id}")
def delete_post(id: int,response: Response):
    del_post=find_post(id)
    
    if del_post: 
        title=del_post['title'] #this way we make sure it exsists before accessing title
        my_posts.remove(del_post)
        return {"message":f"Post: {title} Deleted succesfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post not found ID: {id}"})
```
- Function find  post **by id (field)**:

```Python
def find_post(id):
    for i in my_posts:  # Iterates over dictionaries and returns the matching dictionary
        if i['id'] == id:
            return i  # Returns the matching dictionary if the condition is true
    print(id)
    return None  # In case no matching id is found

```

*Deleting post by **Index***


```Python

#deleting post by index

app.delete("/posts/{id}")
def delete_post(id: int, response : Response):
    index,post=find_index(id)
    if index:
        title=post['title']
        my_posts.pop(index)
        return {"info": f"Post: {title} , Succesfully deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with {id} not found"} )


```


- Function find post **by index**:

```Python

def find_index(id):
    for i,p in enumerate(my_posts):#i is index
        if p['id']==id:
            return i,p #returning the index and the array
    return None , None

```


## 1.8 Updating posts (PUT) 

- Same as above, 2 examples one using the **ID** and the othe using the **index ,ID**

- Using the **ID**

```Python

@app.put("/posts/{id}")
def update_post(id: int, response: Response, entry: Post): #Adding the Pydantic schema
    post=find_post(id)
    entry_dict=entry.model_dump()
    if post:
        post.update(entry_dict)# updating the post found above with the given id
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"info": f"Post: {id} , Succesfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with {id} not found"})


```
- Function find  post **by id (field)**:

```Python
def find_post(id):
    for i in my_posts:  # Iterates over dictionaries and returns the matching dictionary
        if i['id'] == id:
            return i  # Returns the matching dictionary if the condition is true
    print(id)
    return None  # In case no matching id is found

```

- Using the **index** and the **ID**

```Python
@app.put("/posts/{id}")
def update_post(id: int, entry: Post):
    index,post=find_index(id)
    entry_dict=entry.model_dump() # important converting into a dictionary
    if post:
        my_posts[index].update(entry_dict)# update the dictionary(post) based on the [index] that matches
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"info": f"Post: {id} , Succesfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"})

```
- *find_index()* function
```Python

def find_index(id):
    for i,p in enumerate(my_posts):#i is index
        if p['id']==id:
            return i,p #returning the index and the array
    return None , None

```

# 2 Data Base implementation

## Response pydantic v1.1.3
As we have Pydantic modelt to define the requst there are also pydantic models to difne the response

Currently base in our Pydantic schemas the request only is processed if acoomplish what is defines (tittle, content.. boleean.)

But the response is returned as it follows no control :


```Python
{
    "title": "test pydantic",
    "content": "third post from dell",
    "created_at": "2025-08-12T19:45:27.258204+02:00",
    "published": true,
    "id": 4
}
```
### We need to define the schema and serializer:
Additionally we have used a ``serializer`` to modify the datetime format for the **created_at** value before returning it to the user.
```Python
    class PostResponse (BaseModel): #This model defines the response that the user will get
    title: str
    content: str
    id: int
    created_at: datetime
    @field_serializer("created_at")
    def format_created_at(self, dt: datetime, _) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")

 
```
### And update the code
We have added the ``response_code`` decorator so , FastApi will Update the response based in the Pydantic Shcema before fowarding it to the user.

```Python
   @app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse) #adding the post to a dict and to the my_post array of dict
   def create_posts(new_post: schemas.Post, db: Session = Depends(get_db)): #function expects new_post param. compliance with pydantic Post class


    #post = models.PostORM(title=new_post.title, content=new_post.content, published=new_post.published)
    post=models.PostORM(**new_post.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    db.add(post)
    db.commit()
    db.refresh(post)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return post
 
```
#### Multipole posts
This aproach works well when the output is only one post but when returning multiple poosts we need to modify more stuff

This happens because we are returning a list of posts and is trying to fit it in one individual post

```Python
@app.get("/posts",response_model=schemas.PostResponse) # 2. Trying to fit it in one unique posts (not list)
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.PostORM).all() # 1.Here we are returning a list of posts
    
    return posts #removing the dict and retunr the stuff  no data keyword
   
```

**Updated Code**
```Python
from typing import List

@app.get("/posts",response_model=List[schemas.PostResponse]) # 2. Now is handling a  List
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.PostORM).all() # 1.Here we are returning a list of posts
    
    return posts #removing the dict and retunr the stuff  no data keyword
   
```
# 3 User  and password hashing v1.1.4


## Creating user table 
This table will allow us to save all the user information we create the model
````python
class Users(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, nullable= False)
    email= Column(String, nullable=False, unique=True)
    password= Column(String, nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), server_default=text('now()'))
````
## Creating api-endpoint/function add user
```python
@app.post("/useradd", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) 
def create_user(new_user: schemas.Useradd, db: Session = Depends(get_db)):
    
    
    user=models.Users(**new_user.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    db.add(user)
    db.commit()
    db.refresh(user)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return user

```
## Creating the pydantic schema for request and response 

**REQUEST**
```python
class Useradd(BaseModel):
    email:EmailStr
    password:str
```
**RESPONSE**
In this Schema additionally to the serilaizer for the date time there is one for sending a message in the response.

```python
class UserResponse (BaseModel):
    email:str
    created_at: datetime

    @field_serializer("created_at")
    def format_created_at(self, dt: datetime, _) -> str:
        return dt.strftime("%Y-%m-%d %H:%M")
    

    @computed_field # This is for sending  a message
    @property
    def message(self) -> str:
        # now you can refer to self.email
        return f"User {self.email!r} created successfully" # !r is for obtaining the mail between quotes
   
```

## Hashing User Password

For hashing the passwrod we need *passlib* and the *Bcrypt* algorithm for hashing
``pip install passlib[bcrypt]``

```python
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"], deprecated="auto")

@app.post("/useradd", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse) 
def create_user(new_user: schemas.Useradd, db: Session = Depends(get_db)):

    #hash the password - new_user.password
    hashed_password=pwd_context.hash(new_user.password)
    new_user.password=hashed_password

    user=models.Users(**new_user.dict())# This way we unpack the dictionary and put it in the same format the line above automatically
    db.add(user)
    db.commit()
    db.refresh(user)

    #return {"message_from_server": f"New post added!  Title: {post.title}"}
    return user

```
## Adding *Utils.py* file function call.
In order to heave a more clean **main.py**  we create the **utils.py** file
We send the password filed from pydantic and it returns the hash that later is added to the ddbb.

# 4 Splitting main.py using routers v1.1.5

We are gonna split the **main.py** in two files one for users and the other for posts

1. Created a  folder named *routers* that contains 2 files *postst.py* and *users.py* .
2. These are acting now as independent files so we need to add the imports and the **ROUTER** object

*Posts example*


```Python
from fastapi import FastAPI, Response, status, HTTPException, Depends,APIRouter
from .. import schemas,models,utils,database
from  sqlalchemy.orm import Session
from typing import Optional, List

router= APIRouter()

@router.get("/posts",response_model=List[schemas.PostResponse]) #to retrieve all posts
def get_posts(db: Session = Depends(database.get_db)):
    posts=db.query(models.PostORM).all() #models=tables
    
    return posts #removing the dict and retunr the stuff  no data keyword

```
We need to update the *main.py*

```Python
from . routers import users,posts
models.Base.metadata.create_all(bind=engine)

app=FastAPI() #create instance of fastapi

app.include_router(posts.router)
app.include_router(users.router)

```
## Routing Prefix and tags
- The idea is to remove the need of copying the same path in each api endpoint such as "/posts/*something...*"
  ```Python
    router= APIRouter(
        prefix="/posts"
    )

  ```
  With this modification endpoint : **"/posts"** is converted to **"/"**