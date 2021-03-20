from django.test import TestCase, Client
from .models import Post, User, Group
from django.urls import reverse
from django.core.cache import cache


class ProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            email='test@test.com',
            password='12345678'
        )
        self.not_auth_client = Client()
        self.auth_client = Client()
        self.auth_client.force_login(self.user)
        self.group = Group.objects.create(
            title='test group',
            slug='test_group',
            description='test description'
        )

    def _get_urls(self, post):
        urls = [reverse('index'),
                reverse('profile', kwargs={'username': post.author.username}),
                reverse('post', kwargs={'username': post.author.username, 'post_id': post.id}),
                reverse('group_posts', kwargs={'slug': post.group.slug})
                ]
        return urls

    def _check_post_on_page(self, url, post):
        response = self.auth_client.get(url)
        if "page" in response.context:
            post_list = response.context['page'].object_list
            self.assertEqual(len(post_list), 1)
            self.assertEqual(post_list[0], post)
        else:
            self.assertEqual(response.context['post'], post)

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
        self.assertEqual(response.context['page'][0].text, 'test text')

    def test_newpost_loggeduser2(self):
        self.auth_client.post(reverse('new_post'),
                              data={'text': 'test text',
                                    'group': self.group.pk})
        post = Post.objects.first()
        urls = self._get_urls(post=post)
        for url in urls:
            self._check_post_on_page(url=url, post=post)

    def test_edit_post(self):
        self.auth_client.post(reverse('new_post'),
                              data={'text': 'test text'})
        self.auth_client.post(reverse('post_edit',
                                      kwargs={
                                          'username': self.user.username,
                                          'post_id': 1}),
                                      data={'text': 'edit test text',
                                            'group': self.group.pk})
        post = Post.objects.first()
        urls = self._get_urls(post)
        for url in urls:
            self._check_post_on_page(url, post)

    def test_image_in_posts(self):
        cache.clear()
        with open('media/posts/test_img.png', 'rb') as img:
            self.auth_client.post(reverse('new_post'),
                                  data={'text': 'post with image', 'group': self.group.pk, 'image': img},
                                  follow=True)
            post = Post.objects.first()
            urls = self._get_urls(post=post)
            for url in urls:
                response = self.auth_client.get(url)
                self.assertContains(response, "<img")
