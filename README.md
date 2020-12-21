# Shows API
#### Welcome to the Shows API. Search, sort and filter your favorite Movies and TV Shows. Go to /docs to see full list of available endpoints.

## Setup

#### [Dependencies](https://github.com/jubins/Netflix-Shows/blob/master/netflix-shows/requirements.txt)
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
4. From your terminal go `~/Netflix-Shows/netflix-shows` directory, you should be in the directory that contains [`requirements.txt`](https://github.com/jubins/Netflix-Shows/blob/master/netflix-shows/requirements.txt).
5. Install all the requirements using below command and make sure your virtual environment is active.
    ```shell script
    $ pip install requirements.txt
    ```
6. Start the Fast API server using below command. You should see
    ```shell script
    $ python main.py
    ```
7. Go to your browser and copy-paste `http://localhost:9001`. If you see a welcome message then you've successfully setup the server and ready to start using the API.

#### Database setup
1. Once your API server is setup start your Postgresql server.
2. Go to `~/Netflix-Shows/netflix-shows` and run `python backfill.py` to import all the data into the database.
 
## API Documentation
- Go to `http://localhost:9001/docs` to view full list of endpoints.

## [Tests](https://github.com/jubins/Netflix-Shows/blob/master/netflix-shows/unittests.py)
To run the test cases go to `~/Netflix-Shows/netflix-shows` from your terminal window and type below command. Make sure your Fast API server is running.
   ```
    $ python unittests.py 
   ```
If you get `requests` module import error make sure you install it using below command.
   ```
    $ pip3 install requests==2.25.1
   ```

### Contact
- Jubin Soni
- jubinsoni27@gmail.com

### API 
![](https://github.com/jubins/Netflix-Shows/blob/master/img/api-endpoinds.png)
