from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from ..models import Post


class PostModelTest(TestCase):
    def setUp(self):
        # Criando um usuário para ser o autor dos posts
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )

    def test_post_creation(self):
        # Criando um post
        post = Post.objects.create(
            author=self.user,
            title="Primeiro post",
            text="primeiro conteudo"
        )

        # Verificando se o post foi criado corretamente
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, 'Primeiro post')
        self.assertEqual(post.text, 'primeiro conteudo')
        self.assertIsNotNone(post.created_date)

    def test_post_published(self):
        # Criando um post
        post = Post.objects.create(
            author=self.user,
            title="Post para publicar",
            text="Esse post será publicado."
        )

        # Publicando o post
        post.publish()

        # Verificando se a data de publicação foi definida
        self.assertIsNotNone(post.published_date)
        self.assertLessEqual(post.published_date, timezone.now())

    def test_post_str_representation(self):
        # Criando um post
        post = Post.objects.create(
            author=self.user,
            title="Poste teste",
            text="texto teste"
        )

        self.assertEqual(str(post), "Poste teste")
