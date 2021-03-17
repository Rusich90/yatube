from django.test import TestCase, Client
from .models import Post, User
from django.urls import reverse



class ProfileTest(TestCase):
    def setUp(self):
        self.not_auth_client = Client()
        self.auth_client = Client()
        self.user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='12345678'
        )
        self.auth_client.login(username='test_user', password='12345678')

        #self.post = Post.objects.create(text='test text', author=self.user)

    def test_profile(self):
        response = self.auth_client.get(reverse('profile', kwargs={'username': 'test_user'}))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["profile"], User)
        self.assertEqual(response.context["profile"].username, self.user.username)

    def test_newpost_notlogged(self):
        self.not_auth_client.post(reverse('new_post'), data={'text': 'test text'})
        response = self.not_auth_client.get(reverse('profile', kwargs={'username': 'test_user'}))
        self.assertEqual(len(response.context["page"]), 0)

    def test_newpost_loggeduser(self):
        self.auth_client.post(reverse('new_post'), data={'text': 'test text'})
        response = self.auth_client.get(reverse('profile', kwargs={'username': 'test_user'}))
        self.assertEqual(len(response.context["page"]), 1)
        self.assertEqual( response.context['page'][0].text, 'test text')

    def test_edit_post(self):
        self.auth_client.post(reverse('new_post'), data={'text': 'test text'})
        self.auth_client.post(reverse('post_edit',
                                      kwargs={
                                          'username': self.user.username,
                                          'post_id': 1}),
                                      data={'text': 'edit test text'})
        response_index = self.client.get('/')
        response_profile = self.client.get('/test_user/')
        response_post = self.client.get('/test_user/1/')
        self.assertEqual(response_index.context['page'][0].text, 'edit test text')
        self.assertEqual(response_profile.context['page'][0].text, 'edit test text')
        self.assertEqual(response_post.context['author_post'].text, 'edit test text')
