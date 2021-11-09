import unittest
import requests

class FlaskTest(unittest.TestCase):

    def test_index(self):
        response = requests.get("http://127.0.0.1:5000/index")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<h2>Use this site to post, reply and rate questions.</h2>' in response.text, True)

    def test_posts(self):
        response = requests.get("http://127.0.0.1:5000/posts")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Title' and 'Date' in response.text, True)

    def test_post(self):
        response = requests.get("http://127.0.0.1:5000/posts/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('First Post' in response.text, True)

    def test_new(self):
        response = requests.get("http://127.0.0.1:5000/posts/new")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('<form action="new" name = "form" method="post">' in response.text, True)

if __name__ == " __main__":
    unittest.main()
