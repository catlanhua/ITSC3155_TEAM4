import unittest
#import requests


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
        self.assertEqual('<form action="new" method="post">' in response.text, True)

    def test_update(self):
        response = requests.get("http://127.0.0.1:5000/posts/edit/1")
        statuscode = response.status_code
        self.assertEqual(statuscode, 200)
        self.assertEqual('Update Post' in response.text, True)

    def test_delete(self):
        response = requests.get("http://127.0.0.1:5000/posts/delete")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)


    def test_reply(self):
        response = requests.get("http://127.0.0.1:5000/posts/<post_id>/reply")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)

    def test_report(self):
        response = requests.get("http://127.0.0.1:5000/index/<post_id>/report")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)

    def test_like(self):
        response = requests.get("http://127.0.0.1:5000/posts/<post_id>/like_unlike")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)

    def test_dislike(self):
        response = requests.get("http://127.0.0.1:5000/posts/<post_id>/dislike_undislike")
        statuscode = response.status_code
        self.assertEqual(statuscode, 500)


if __name__ == " __main__":
    unittest.main()
