from fastapi import FastAPI
app=FastAPI() #create instance of fastapi

@app.get("/hi")
def test():
    return {"hello world"}