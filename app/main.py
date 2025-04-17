from fastapi import FastAPI,File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from flow import kickoff 
from pydantic import BaseModel

class Query(BaseModel):
    query : str | None = None

origins_all = '*'
app = FastAPI();

#configure fastapi
app.add_middleware(
        CORSMiddleware,
        allow_origins = origins_all,
        allow_credentials = True,
        allow_methods=['*'],
        allow_headers=['*']
        )
# test api
@app.get('/')
def root() :
    return { 'message' : 'Hello world' }

@app.get('/kickoff')
def kickoff_crew_get() :
    result = kickoff('what is a pgwp?')
    return result

@app.post('/kickoff')
def kickoff_crew(query : Query) :
    print('kickoff crew , query :', query)
    result = kickoff(query.query);
    if result.raw :
        return result.raw
    else :
        return result
