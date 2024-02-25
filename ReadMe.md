# Note Finder API
#### This is created using python (FastAPI)

Step 1:
install required python libs
Run in terminal
```
pip install fastapi uvicorn[standard]
pip install libroa,asyncio,os
```
If you are facing any error installing fastapi try using this :
```
pip install fastapi "uvicorn[standard]"
```

once all the lib are installed then run the main.py

```
uvicorn main:app --reload
```
This should run the server at http://127.0.0.1:8000

To access the API documentation or to test it use : http://127.0.0.1:8000/docs

