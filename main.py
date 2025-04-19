# main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("interfaces.api.endpoints:app", reload=True)
