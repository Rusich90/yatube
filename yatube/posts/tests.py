from django.test import TestCase, Client


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@test.com', password='12345678')
        self.post = Post.objects.create(text='test text', author=self.user)

    def test_profile(self):
        response = self.client.get('/test_user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 1)
        self.assertIsInstance(response.context["profile"], User)
        self.assertEqual(response.context["profile"].username, self.user.username)
