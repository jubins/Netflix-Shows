# [Shows API](https://netflix-shows-api.herokuapp.com/)
#### Welcome to the Shows API. Search, sort and filter your favorite Movies and TV Shows. Go to https://netflix-shows-api.herokuapp.com/docs/ to see full list of available endpoints.

## API Usage Examples
- Search: Search shows that contain `Music` in the title
    ```
    curl -XGET -H "Content-type: application/json" 'https://netflix-shows-api.herokuapp.com/api/searchShows/by/title?&text=Music&limit=2&offset=0'
    ```
- Sort: Search shows that contain `Music` in the description and sort by `date_added`
    ```
    curl -XGET -H "Content-type: application/json" 'https://netflix-shows-api.herokuapp.com/api/searchShows/by/title?&text=Music&sort_by=date_added&limit=2&offset=0'
    ```
- Paginate: Search shows that contain `Music` in the description and sort by `duration` and go to page 2
    ```
    curl -XGET -H "Content-type: application/json" 'https://netflix-shows-api.herokuapp.com/api/searchShows/by/title?&text=music&sort_by=date_added&limit=10&offset=10'
    ```
- Create: Create new show
    ```
    curl -XPOST -H "Content-type: application/json" -d '{'show_id': '81145629', 'type': 'Movie', 'title': 'Norm of the North: King Sized Adventure', 'director': 'Richard Finn, Tim Maltby', 'cast': 'Alan Marriott, Andrew Toth, Brian Dobson, Cole Howard, Jennifer Cameron, Jonathan Holmes, Lee Tockar, Lisa Durupt, Maya Kay, Michael Dobson', 'country': 'United States, India, South Korea, China', 'date_added': '2020-09-19', 'release_year': '2019', 'rating': 'TV-PG', 'duration': '90 min', 'listed_in': 'Children & Family Movies, Comedies', 'description': 'Before planning an awesome wedding for his grandfather, a polar bear king must take back a stolen artifact from an evil archaeologist first.'}' 'https://netflix-shows-api.herokuapp.com/api/addShow'
    ```
- Update: Modify existing show
    ```
    curl -XPUT -H "Content-type: application/json" -d '{'type': 'TV Show'}' 'https://netflix-shows-api.herokuapp.com/api/modifyShowTypeById/80117401'
    ```
- Delete: Remove a show
    ```
    curl -XDELETE -H "Content-type: application/json" 'https://netflix-shows-api.herokuapp.com/api/deleteShowById/81145628'
    ```
 
## [API Documentation](https://netflix-shows-api.herokuapp.com/docs)
- Go to [`https://netflix-shows-api.herokuapp.com/docs`](https://netflix-shows-api.herokuapp.com/docs) to view full list of endpoints.

## [Tests](https://github.com/jubins/Netflix-Shows/blob/master/netflix-shows/unittests.py)
To run the test cases go to `~/Netflix-Shows/netflix-shows` from your terminal window and type below command. Make sure your Fast API server is running.
   ```
    $ python unittests.py 
   ```
If you get `requests` module import error make sure you install it using below command.
   ```
    $ pip3 install requests==2.25.1
   ```

## Setup
Follow below steps to setup your environment locally. You can use also clone [`dev`](https://github.com/jubins/Netflix-Shows/tree/dev) branch or clone it for reference as other branches have production related changes and dev branch should work if you have docker running.

#### [Dependencies](https://github.com/jubins/Netflix-Shows/blob/master/requirements.txt)
- Python 3
- Docker/Docker-Compose (Optional)
- All the python dependencies are listed in `requirements.txt`.

#### Docker: Setting up the server
1. If you have docker/docker-compose installed and running this setup is recommended, otherwise follow non-dockerized setup.
2. From your terminal go to main project directory i.e. the Netflix-Shows project directory that contains the `docker-compose.yml` file.
3. Type `docker-compose up --build` to start the server. You will see docker building the service and starting the Fast API server.
4. Go to your browser and copy-paste `http://localhost:9001`. If you see a welcome message then you've successfully setup the server and ready to start using the API.

#### Non-dockerized: Setting up the server
1. Create a virtual environment using below command.
    ```shell script
    $ python3 -m venv venv
    ```
2. Activate your virtual environment.
    ```shell script
    $ source/venv/bin/active
    ```
3. If you are on Windows or need more help with virtual environments follow this [link.](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments)
4. From your terminal go `~/Netflix-Shows/` directory, you should be in the directory that contains [`requirements.txt`](https://github.com/jubins/Netflix-Shows/blob/master/requirements.txt).
5. Install all the requirements using below command and make sure your virtual environment is active.
    ```shell script
    $ pip install requirements.txt
    ```
6. Start the Fast API server using below command. You should see
    ```shell script
    $ python main.py
    ```
7. Go to your browser and copy-paste `http://localhost:9001`. If you see a welcome message then you've successfully setup the server and ready to start using the API.

#### [Database setup](https://data.heroku.com/dataclips/llzjpvexielskjurztdntndfttah)
1. This project uses Postgres server hosted on Heroku. You can view the data clip here: https://data.heroku.com/dataclips/llzjpvexielskjurztdntndfttah
2. These are setups to setup database locally. Comment the Heroku DB variables in [`database.py`](https://github.com/jubins/Netflix-Shows/blob/master/netflix-shows/database.py) and uncomment local DB variables. Once your API server is setup start your Postgresql server.
2. Go to `~/Netflix-Shows/netflix-shows` and run `python backfill.py` to import all the data into your database.

### Contact
- Jubin Soni
- jubinsoni27@gmail.com

### API 
![](https://github.com/jubins/Netflix-Shows/blob/master/netflix-shows/img/api-endpoinds.png)
