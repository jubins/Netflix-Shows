from requests import request
import unittest

# BASE_URL = "http://localhost:9001"
BASE_URL = 'https://netflix-shows-api.herokuapp.com'


class TestShowsAPI(unittest.TestCase):

    def test_index(self):
        response = request(method='GET', url=BASE_URL)
        self.assertEqual(response.status_code, 200)

    def test_search_by_id(self):
        response = request(method='GET', url=f"{BASE_URL}/api/searchShows/by/show_id/80169755")
        self.assertEqual(response.status_code, 200)
        expected = 1
        self.assertEqual(response.json().get('length'), expected)

    def test_search_by_title(self):
        response = request(method='GET', url=f"{BASE_URL}/api/searchShows/by/title?text=Transformers")
        self.assertEqual(response.status_code, 200)
        expected = 1
        self.assertGreaterEqual(response.json().get('length'), expected)

    def test_search_by_description(self):
        response = request(method='GET', url=f"{BASE_URL}/api/searchShows/by/description?text=music")
        self.assertEqual(response.status_code, 200)
        expected = 1
        self.assertGreaterEqual(response.json().get('length'), expected)

    def test_search_api_invalid_query_params(self):
        response = request(method='GET', url=f"{BASE_URL}/api/searchShows/by/description?id=80169755")
        self.assertEqual(response.status_code, 422)
        expected = {
            "detail": [
                {
                    "loc": [
                        "query",
                        "text"
                    ],
                    "msg": "field required",
                    "type": "value_error.missing"
                }
            ]
        }
        self.assertEqual(response.json(), expected)

    def test_search_api_invalid_path_params(self):
        response = request(method='GET', url=f"{BASE_URL}/api/searchShows/by/shows?text=Music")
        self.assertEqual(response.status_code, 400)
        expected = {
            "detail": "Bad request: {title_or_description} must be one of [\"title\", \"description\"] columns."
        }
        self.assertEqual(response.json(), expected)

    def test_filter_by_date_and_sorting(self):
        response = request(method='GET', url=f"{BASE_URL}/api/filterShows/by/dateAdded?start_date=2019-09-20&end_date=2019-10-12&sort_by=listed_in&limit=100&offset=0")
        self.assertEqual(response.status_code, 200)
        expected = 1
        self.assertGreaterEqual(response.json().get('length'), expected)

    def test_filter_by_date_pagination(self):
        response = request(method='GET', url=f"{BASE_URL}/api/filterShows/by/dateAdded?start_date=2019-09-20&end_date=2019-10-12&limit=100&offset=0")
        self.assertEqual(response.status_code, 200)
        expected = 100
        self.assertGreaterEqual(response.json().get('length'), expected)
        response = request(method='GET', url=f"{BASE_URL}/api/filterShows/by/dateAdded?start_date=2019-09-20&end_date=2019-10-12&limit=100&offset=100")
        expected = 50
        self.assertGreaterEqual(response.json().get('length'), expected)

    def test_filter_by_release_year(self):
        response = request(method='GET', url=f"{BASE_URL}/api/filterShows/by/releaseYear?year=2019&limit=100&offset=0")
        self.assertEqual(response.status_code, 200)
        expected = 1
        self.assertGreaterEqual(response.json().get('length'), expected)

    def test_delete_show(self):
        show_id = 81145628
        response = request(method='DELETE', url=f'{BASE_URL}/api/deleteShowById/{show_id}')
        if response.status_code == 403:
            expected = {"detail": f"show_id: {show_id} not found"}
            self.assertEqual(response.json(), expected)
        else:
            self.assertEqual(response.status_code, 202)
            expected = {"message": f"show_id: {show_id} deleted."}
            self.assertEqual(response.json(), expected)

    def test_create_new_show(self):
        data = {'show_id': '81145629', 'type': 'Movie', 'title': 'Norm of the North: King Sized Adventure', 'director': 'Richard Finn, Tim Maltby', 'cast': 'Alan Marriott, Andrew Toth, Brian Dobson, Cole Howard, Jennifer Cameron, Jonathan Holmes, Lee Tockar, Lisa Durupt, Maya Kay, Michael Dobson', 'country': 'United States, India, South Korea, China', 'date_added': '2020-09-19', 'release_year': '2019', 'rating': 'TV-PG', 'duration': '90 min', 'listed_in': 'Children & Family Movies, Comedies', 'description': 'Before planning an awesome wedding for his grandfather, a polar bear king must take back a stolen artifact from an evil archaeologist first.'}
        response = request(method='POST', url=f'{BASE_URL}/api/addShow', json=data)
        if response.status_code == 403:
            expected = {"detail":"duplicate key value violates unique constraint \"shows_pkey\"\nDETAIL:  Key (show_id)=(81145629) already exists."}
            self.assertEqual(response.json(), expected)
        else:
            self.assertEqual(response.status_code, 201)
            expected = {"message": f"show_id: 81145629 created."}
            self.assertEqual(response.json(), expected)

    def test_modify_show(self):
        show_id = 80117401
        data = {'type': 'Movie', 'title': 'Norm of the North: King Sized Adventure', 'director': 'Richard Finn, Tim Maltby', 'cast': 'Alan Marriott, Andrew Toth, Brian Dobson, Cole Howard, Jennifer Cameron, Jonathan Holmes, Lee Tockar, Lisa Durupt, Maya Kay, Michael Dobson', 'country': 'United States, India, South Korea, China', 'date_added': '2020-09-19', 'release_year': '2019', 'rating': 'TV-PG', 'duration': '90 min', 'listed_in': 'Children & Family Movies, Comedies', 'description': 'Before planning an awesome wedding for his grandfather, a polar bear king must take back a stolen artifact from an evil archaeologist first.'}
        response = request(method='PUT', url=f'{BASE_URL}/api/modifyShow/{show_id}', json=data)
        if response.status_code == 404:
            expected = {"detail": f"show_id: {show_id} not found"}
            self.assertEqual(response.json(), expected)
        else:
            self.assertEqual(response.status_code, 204)


if __name__ == '__main__':
    unittest.main()
