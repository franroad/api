
######
#using Pydantic
######

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException #import the library
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange #importing the random for generating th post id

app=FastAPI() #create instance of fastapi

class Post (BaseModel): # here we use pydantic for define the schema
    title: str
    content: str
    published: bool = True # this is an optional/odefault to true
    rating: Optional[int]= None #Optional filed with no default value , type integer
    
my_posts= [{"id":1,"title": "this is the post 1","content":"content of post"},
           {"id":2,"title": "this is the post 2","content":"pizza"}] #creating a global variable for storing the posts in memory (not using ddbb) its an array of dictionaries



@app.get("/")#the route where to find the stuff /fran would be: http://127.0.0.1:8000/fran (decorator , endpoint)
def root(): #root=funtion name (does not matter)
    return {"message": "Hello World"}



@app.get("/posts") #to retrieve all posts
def get_posts():
    return{"data": my_posts} #passing the variable



#creating a post

@app.post("/posts", status_code=status.HTTP_201_CREATED) #adding the post to a dict and to the my_post array of dict
def create_posts(new_post: Post): #function expects new_post param. compliance with pydantic Post class
    post_dict=new_post.model_dump()# We create a dict witht the info we are gonna get
    post_dict['id']=randrange(0, 100000)#from that info the id is gonna be rand adding to the dictionary
    my_posts.append(post_dict)#here we are adding the new post with the rand id to the variable, addind the dictionary to the variable
    title=post_dict['title']
    return {"message_from_server": f"New post added: {post_dict}. Title: {title}"}



# function to find post

def find_post(id):
    for i in my_posts:  # Iterates over dictionaries and returns the matching dictionary
        if i['id'] == id:
            return i  # Returns the matching dictionary if the condition is true
    print(id)
    return None  # In case no matching id is found

#Function to find index
def find_index(id):
    for i,p in enumerate(my_posts):#i is index
        if p['id']==id:
            return i,p #returning the index and the array
    return None , None
         
        
            
       



#retrieving post by id

@app.get("/posts/{id}")  # Get post per id (decorator/path parameter)
def get_post(id: int,response: Response):#performing validation with fast api we are saying I want an integer.
    post = find_post(id)
    if post: #in python not empty values are considered as true same as: if post != {} (si no esta vacio... damelo else error)
        return {"post_info": post}  # Returns the entire post if found
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post not found ID: {id}"})
        # response.status_code= status.HTTP_404_NOT_FOUND
        # return {"error": f"Post not found ID: {id}"}  # Returns an error message if no matching post is found


#deleting post by id 

# @app.delete("/posts/{id}")
# def delete_post(id: int,response: Response):
#     del_post=find_post(id)
    
#     if del_post: 
#         title=del_post['title'] #this way we make sure it exsists before accessing title
#         my_posts.remove(del_post)
#         return {"message":f"Post: {title} Deleted succesfully"}
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"error": f"Post not found ID: {id}"})

#deleting post by index

@app.delete("/posts/{id}")
def delete_post(id: int):
    index, post=find_index(id)
    if post:
        title=post['title']
        my_posts.pop(index)
        raise HTTPException(status_code=status.HTTP_200_OK,detail={"info": f"Post: {title} , Succesfully deleted"})
        #return {"info": f"Post: {title} , Succesfully deleted"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"} )
    
#Updating post
    
# @app.put("/posts/{id}")
# def update_post(id: int, response: Response, entry: Post): #Adding the Pydantic schema/class
#     post=find_post(id)
#     entry_dict=entry.model_dump() # imporatnt converting into a dictionary
#     if post:
#         post.update(entry_dict)# updating the post found above with the given id
#         raise HTTPException(status_code=status.HTTP_200_OK, detail={"info": f"Post: {id} , Succesfully updated"})
#     else:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with {id} not found"})

@app.put("/posts/{id}")
def update_post(id: int, entry: Post):
    index,post=find_index(id)
    entry_dict=entry.model_dump() # important converting into a dictionary to fit our 
    if post:
        my_posts[index].update(entry_dict)# update the dictionary(post) based on the [index] that matches
        raise HTTPException(status_code=status.HTTP_200_OK, detail={"info": f"Post: {id} , Succesfully updated"})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"Error": f"Post with ID: {id} not found"})





