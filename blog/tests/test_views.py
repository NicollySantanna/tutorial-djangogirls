from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Post


class PostListViewTest(TestCase):
    def setUp(self):  # Método para criar dados de teste(usuário, post...)
        self.client = Client()  # simula a requisicao
        self.user = User.objects.create_user(
            username='test', password='testpassword')
        self.post = Post.objects.create(
            author=self.user, title='Test Post', text='Texto teste',
            published_date=timezone.now()
        )

    def test_post_list_view_returns_200(self):
        url = reverse('post_list')  # pega a url pelo nome
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_list_view_uses_correct_template(self):
        url = reverse('post_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post_list.html')


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword'
        )
        self.post = Post.objects.create(
            author=self.user, title='Test Post', text='Test Text',
            published_date=timezone.now()
        )

    def test_post_detail_view_returns_200(self):
        url = reverse('post_detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_detail_view_uses_correct_template(self):
        url = reverse('post_detail', args=[self.post.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post_detail.html')

    def test_post_detail_view_returns_404_for_invalid_pk(self):
        url = reverse('post_detail', args=[999])  # Um pk que não existe
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class PostNewViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

    def test_post_new_view_returns_200(self):
        url = reverse('post_new')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_new_view_uses_correct_template(self):
        url = reverse('post_new')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post_edit.html')

    def test_post_new_view_creates_post(self):
        url = reverse('post_new')
        data = {'title': 'New Post', 'text': 'New Text'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        self.assertEqual(Post.objects.count(), 1)  # Um post é criado no teste
        new_post = Post.objects.last()
        self.assertEqual(new_post.title, 'New Post')
        self.assertEqual(new_post.text, 'New Text')
        self.assertIsNotNone(new_post.published_date)
        self.assertEqual(new_post.author, self.user)


class PostEditViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.post = Post.objects.create(
            author=self.user, title='Test Post', text='Test Text',
            published_date=timezone.now()
        )
        self.client.login(username='testuser', password='testpassword')

    def test_post_edit_view_returns_200(self):
        url = reverse('post_edit', args=[self.post.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_post_edit_view_uses_correct_template(self):
        url = reverse('post_edit', args=[self.post.pk])
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'blog/post_edit.html')

    def test_post_edit_view_returns_404_for_invalid_pk(self):
        url = reverse('post_edit', args=[999])  # Um pk que não existe
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_post_edit_view_updates_post(self):
        url = reverse('post_edit', args=[self.post.pk])
        data = {'title': 'Edited Post', 'text': 'Edited Text'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirecionamento
        self.post.refresh_from_db()  # Atualiza o objeto com os dados do banco
        self.assertEqual(self.post.title, 'Edited Post')
        self.assertEqual(self.post.text, 'Edited Text')
