from django.test import TestCase, Client
from .models import Post, User


class ProfileTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@test.com', password='12345678')
        self.post = Post.objects.create(text='test text', author=self.user)

    def test_profile(self):
        response = self.client.get('/test_user/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["page"]), 1)
        self.assertIsInstance(response.context["profile"], User)
        self.assertEqual(response.context["profile"].username, self.user.username)


class NewPostTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='test_user', email='test@test.com', password='12345678')
        self.post = Post.objects.create(text='test text', author=self.user)

    def test_newpost_notlogged(self):
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, 'login.html')

    def test_newpost_loggeduser(self):
        self.client.login(username='test_user', password='12345678')
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        self.post = Post.objects.create(text='test text', author=self.user)
        response = self.client.get('/index/')
        self.assertEqual(response.context['paginator'][0].text, 'test text')



