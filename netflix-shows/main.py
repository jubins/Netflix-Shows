from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from . import models, database, crud
import uvicorn

# Create Connection
app = FastAPI(title="Shows API - search, sort and filter your favorite Movies and TV Shows.")

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

# Connect Database
shows_db = database.ShowsDB().initialize()
shows_crud = crud.CRUDShowsDB(shows_db)


@app.on_event('startup')
async def startup():
    await shows_db.connect()


@app.on_event('shutdown')
async def shutdown():
    await shows_db.disconnect()


# Endpoints

# Index Endpoint
@app.get('/')
def index():
    return {'message': 'Welcome to the Shows API. Go to https://netflix-shows-api.herokuapp.com/docs to see full list of available endpoints.'}


# Search Endpoints
@app.get('/api/searchShows/by/show_id/{show_id}', response_model=models.ShowsSearch, status_code=200)
async def search_shows_by_show_id(show_id: int):
    show = await shows_crud.search_show_by_id(show_id)
    response = {'data': show, 'length': len(show)}
    if not show:
        raise HTTPException(status_code=404, detail=f'show_id: {show_id} not found')
    return response


@app.get('/api/searchShows/by/{title_or_description}', response_model=models.ShowsSearch, status_code=200)
async def search_shows_by_show_title_or_description(title_or_description: str, text: str, sort_by: str = 'date_added', limit: int = 10, offset: int = 0):
    if sort_by not in {'date_added', 'release_year', 'duration', 'listed_in'}:
        raise HTTPException(status_code=400, detail='Bad request: "sort_by" must be one of ["date_added", "release_year", "duration", "listed_in"] columns.')
    if title_or_description == 'title':
        show = await shows_crud.search_show_by_title(text, sort_by, limit, offset)
        response = {'data': show, 'length': len(show)}
    elif title_or_description == 'description':
        show = await shows_crud.search_show_by_description(text, sort_by, limit, offset)
        response = {'data': show, 'length': len(show)}
    else:
        raise HTTPException(status_code=400, detail='Bad request: {title_or_description} must be one of ["title", "description"] columns.')
    if not show:
        raise HTTPException(status_code=404, detail='No matching results found')
    return response


# Filter Endpoints
@app.get('/api/filterShows/by/dateAdded', response_model=models.ShowsSearch, status_code=200)
async def filter_shows_by_date_added(start_date: str = None, end_date: str = None, sort_by: str = 'date_added', limit: int = 10, offset: int = 0):
    if sort_by not in {'date_added', 'release_year', 'duration', 'listed_in'}:
        raise HTTPException(status_code=400, detail='Bad request: "sort_by" must be one of ["date_added", "release_year", "duration", "listed_in"] columns.')
    if not start_date and not end_date:
        raise HTTPException(status_code=400, detail='Bad request: "start_date" or "end_date" is required.')
    if start_date and not shows_crud.valid_date_format(start_date):
        raise HTTPException(status_code=400, detail='Bad request: Specify "start_date" in "YYYY-MM-DD" format.')
    if end_date and not shows_crud.valid_date_format(end_date):
        raise HTTPException(status_code=400, detail='Bad request: Specify "start_date" in "YYYY-MM-DD" format.')
    show = await shows_crud.filter_show_by_date_added(start_date, end_date, sort_by, limit, offset)
    response = {'data': show, 'length': len(show)}
    if not show:
        raise HTTPException(status_code=404, detail='No matching results found')
    return response


@app.get('/api/filterShows/by/releaseYear', response_model=models.ShowsSearch, status_code=200)
async def filter_shows_by_release_year(year: int, sort_by: str = 'date_added', limit: int = 10, offset: int = 0):
    if sort_by not in {'date_added', 'release_year', 'duration', 'listed_in'}:
        raise HTTPException(status_code=400, detail='Bad request: "sort_by" must be one of ["date_added", "release_year", "duration", "listed_in"] columns.')
    show = await shows_crud.filter_show_by_release_year(year, sort_by, limit, offset)
    response = {'data': show, 'length': len(show)}
    if not show:
        raise HTTPException(status_code=404, detail='No matching results found')
    return response


@app.get('/api/filterShows/by/country', response_model=models.ShowsSearch, status_code=200)
async def filter_show_by_country(country: str, sort_by: str = 'date_added', limit: int = 10, offset: int = 0):
    if sort_by not in {'date_added', 'release_year', 'duration', 'listed_in'}:
        raise HTTPException(status_code=400, detail='Bad request: "sort_by" must be one of ["date_added", "release_year", "duration", "listed_in"] columns.')
    show = await shows_crud.filter_show_by_country(country, sort_by, limit, offset)
    response = {'data': show, 'length': len(show)}
    if not show:
        raise HTTPException(status_code=404, detail='No matching results found')
    return response


# POST Endpoint to add data
@app.post('/api/addShow', status_code=201)
async def create_a_new_show(show: models.Shows):
    try:
        await shows_crud.create_show(show)
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))
    return {"message": f"show_id: {show.show_id} created."}


# PUT Endpoint to modify data
@app.put('/api/modifyShow/{show_id}', status_code=204)
async def modify_an_existing_show(show_id: int, shows: models.ShowModify):
    show = await shows_crud.search_show_by_id(show_id)
    if not show:
        raise HTTPException(status_code=404, detail=f'show_id: {show_id} not found')
    await shows_crud.modify_show(show_id, shows)
    return {"message": f"show_id: {show_id} modified."}


# DELETE Endpoint to delete data
@app.delete('/api/deleteShowById/{show_id}', status_code=202)
async def delete_an_existing_show(show_id: int):
    show = await shows_crud.search_show_by_id(show_id)
    if not show:
        raise HTTPException(status_code=403, detail=f'show_id: {show_id} not found')
    await shows_crud.delete_show(show_id)
    return {"message": f"show_id: {show_id} deleted."}

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=9001, reload=True)
