from rest_framework.test import APITestCase
from rest_framework import status as s
from django.test import TestCase
import datetime as dt
from uuid import uuid4
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

User = get_user_model()


class PostModelTest(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(
            username='test', password='password')

    def test_post_create(self):
        p = Post.objects.create(
            text='post',
            author=self.author,
            pins=0,
            visible=True,
            edited=False)
        self.assertEqual(p.text, 'post')
        self.assertEqual(p.author.uuid, self.author.uuid)
        self.assertEqual(p.pins, 0)
        self.assertEqual(p.edited, False)
        self.assertEqual(p.visible, True)

    def test_post_comment_count_none(self):
        p = Post.objects.create(text='post', author=self.author)
        self.assertEqual(p.get_comment_count(), 0)

    def test_post_comment_count_one(self):
        p = Post.objects.create(text='post', author=self.author)
        Comment.objects.create(text='comment', author=self.author, post=p)
        self.assertEqual(p.get_comment_count(), 1)


class PostListCreateTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Post.objects.create(text='post1', author=user)
        Post.objects.create(text='post2', author=user)
        Post.objects.create(text='post3', author=user)
        return super().setUpTestData()

    def setUp(self):
        res = self.client.post(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)

    def test_post_list(self):
        res = self.client.get(reverse('post_list_create'),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        posts = PostSerializer(
            instance=Post.objects.filter(author=self.author), many=True)

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertListEqual(posts.data, res.data)

    def test_post_list_unauth(self):
        res = self.client.get(reverse('post_list_create'))

        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_post_list_filter(self):
        user2 = User.objects.create_user(username='test2', password='password')
        Post.objects.create(text='post', author=user2)

        res = self.client.get(reverse('post_list_create'),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        posts = PostSerializer(
            instance=Post.objects.filter(author=self.author), many=True)

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertListEqual(posts.data, res.data)

    def test_create_new_post(self):
        res = self.client.post(
            reverse('post_list_create'),
            data={'text': 'My new post'},
            HTTP_AUTHORIZATION=f'Bearer {self.token}'
        )
        self.assertEqual(res.status_code, s.HTTP_201_CREATED)

        new_post = PostSerializer(
            instance=Post.objects.get(text='My new post'))
        self.assertDictEqual(new_post.data, res.data)


class PostDetailView(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Post.objects.create(text='post1', author=user)
        Post.objects.create(text='post2', author=user)
        Post.objects.create(text='post3', author=user)
        User.objects.create_user(username='test2', password='password')

    def setUp(self):
        res = self.client.post(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)

        res = self.client.post(reverse('token_login'), data={
            'username': 'test2',
            'password': 'password',
        })
        self.token2 = res.data.get('access')

    def test_detail_view_unauth(self):
        p = Post.objects.get(pk=1)
        ps = PostSerializer(instance=p)

        res = self.client.get(reverse('post_detail', kwargs={'uuid': p.uuid}))

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertDictEqual(ps.data, res.data)

    def test_detail_view_auth(self):
        p = Post.objects.get(pk=1)
        ps = PostSerializer(instance=p)

        res = self.client.get(reverse('post_detail', kwargs={'uuid': p.uuid}),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertDictEqual(ps.data, res.data)

    def test_delete_no_user(self):
        p = Post.objects.get(pk=1)
        res = self.client.delete(
            reverse('post_detail', kwargs={'uuid': p.uuid}))

        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.get(pk=1).id, p.id)

    def test_delete_wrong_user(self):
        p = Post.objects.get(pk=1)
        res = self.client.delete(reverse('post_detail', kwargs={'uuid': p.uuid}),
                                 HTTP_AUTHORIZATION=f'Bearer {self.token2}')

        self.assertEqual(res.status_code, s.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.get(pk=1).id, p.id)

    def test_delete(self):
        p = Post.objects.get(pk=1)
        res = self.client.delete(reverse('post_detail', kwargs={'uuid': p.uuid}),
                                 HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_204_NO_CONTENT)
        with self.assertRaises(Post.DoesNotExist):
            Post.objects.get(pk=1)

    def test_update(self):
        p = Post.objects.get(pk=1)
        self.assertFalse(p.edited)

        res = self.client.put(reverse('post_detail', kwargs={'uuid': p.uuid}),
                              data={'text': 'edited text'},
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_200_OK)

        p = Post.objects.get(pk=1)
        self.assertEqual(p.text, 'edited text')
        self.assertTrue(p.edited)

    def test_update_no_user(self):
        p = Post.objects.get(pk=1)
        res = self.client.put(reverse('post_detail', kwargs={'uuid': p.uuid}),
                              data={'text': 'edited text'})

        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

    def test_update_wrong_user(self):
        p = Post.objects.get(pk=1)
        res = self.client.put(reverse('post_detail', kwargs={'uuid': p.uuid}),
                              data={'text': 'edited text'},
                              HTTP_AUTHORIZATION=f'Bearer {self.token2}')

        self.assertEqual(res.status_code, s.HTTP_403_FORBIDDEN)

    def test_bad_update(self):
        p = Post.objects.get(pk=1)
        self.assertEqual(p.pins, 0)

        res = self.client.put(reverse('post_detail', kwargs={'uuid': p.uuid}),
                              data={'pins': 1000},
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.assertEqual(res.status_code, s.HTTP_400_BAD_REQUEST)

        p = Post.objects.get(pk=1)
        self.assertEqual(p.pins, 0)


class PinPostViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Post.objects.create(text='post1', author=user)
        Post.objects.create(text='post2', author=user)
        Post.objects.create(text='post3', author=user)
        User.objects.create_user(username='test2', password='password')

    def setUp(self):
        res = self.client.post(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)

        res = self.client.post(reverse('token_login'), data={
            'username': 'test2',
            'password': 'password',
        })
        self.token2 = res.data.get('access')

    def test_pin(self):
        p = Post.objects.get(pk=1)
        self.assertEqual(p.pins, 0)

        res = self.client.put(reverse('pin_post', kwargs={'uuid': p.uuid}),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(res.status_code, s.HTTP_200_OK)

        p = Post.objects.get(pk=1)
        self.assertEqual(p.pins, 1)

    def test_pin_unauth(self):
        p = Post.objects.get(pk=1)
        self.assertEqual(p.pins, 0)

        res = self.client.put(reverse('pin_post', kwargs={'uuid': p.uuid}))
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

        p = Post.objects.get(pk=1)
        self.assertEqual(p.pins, 0)

    def test_pin_404(self):
        res = self.client.put(reverse('pin_post', kwargs={'uuid': uuid4()}),
                              HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(res.status_code, s.HTTP_404_NOT_FOUND)


class CommentDetailViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Post.objects.create(text='post1', author=user)

    def setUp(self):
        res = self.client.post(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)

        self.post = Post.objects.get(pk=1)

    def test_create_comment(self):
        self.assertEqual(self.post.comments.count(), 0)

        res = self.client.post(
            reverse('comment_list_create', kwargs={'uuid': self.post.uuid}),
            data={'text': 'Nice Post'},
            HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(res.status_code, s.HTTP_201_CREATED)

        p = Post.objects.get(pk=1)
        self.assertEqual(p.comments.count(), 1)

    def test_create_comment_unauth(self):
        self.assertEqual(self.post.comments.count(), 0)

        res = self.client.post(
            reverse('comment_list_create', kwargs={'uuid': self.post.uuid}),
            data={'text': 'Nice Post'})
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)

        p = Post.objects.get(pk=1)
        self.assertEqual(p.comments.count(), 0)

    def test_list_comments(self):
        Comment.objects.create(
            text='comment', post=self.post, author=self.author)
        Comment.objects.create(
            text='comment2', post=self.post, author=self.author)
        comments = CommentSerializer(instance=Comment.objects.order_by('-date_created').filter(
            post__uuid=self.post.uuid), many=True)

        res = self.client.get(
            reverse('comment_list_create', kwargs={'uuid': self.post.uuid}))
        self.assertEqual(res.status_code, s.HTTP_200_OK)
        self.assertDictEqual(comments.data[0], res.data[0])
        self.assertDictEqual(comments.data[1], res.data[1])


class CommentRetrieveDestroyViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        post = Post.objects.create(text='post1', author=user)
        User.objects.create_user(username='test2', password='password')
        Comment.objects.create(text='comment', author=user, post=post)

    def setUp(self):
        res = self.client.post(reverse('token_login'), data={
            'username': 'test',
            'password': 'password',
        })
        self.token = res.data.get('access')
        self.author = User.objects.get(pk=1)
        self.post = Post.objects.get(pk=1)
        self.comment = Comment.objects.get(pk=1)

        res = self.client.post(reverse('token_login'), data={
            'username': 'test2',
            'password': 'password',
        })
        self.token2 = res.data.get('access')

        self.url = reverse('delete_comment', kwargs={
            'post_uuid': self.post.uuid,
            'comment_uuid': self.comment.uuid})

    def test_delete_comment(self):
        res = self.client.delete(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token}')
        self.assertEqual(res.status_code, s.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.get(pk=1).get_comment_count(), 0)

    def test_delete_comment_unauth(self):
        res = self.client.delete(self.url)
        self.assertEqual(res.status_code, s.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.get(pk=1).get_comment_count(), 1)

    def test_delete_comment_wrong_user(self):
        res = self.client.delete(self.url, HTTP_AUTHORIZATION=f'Bearer {self.token2}')
        self.assertEqual(res.status_code, s.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.get(pk=1).get_comment_count(), 1)

    def test_get_comment(self):
        comment = CommentSerializer(instance=self.comment)
        res = self.client.get(self.url)
        self.assertDictEqual(comment.data, res.data)


class UserPostListAPIViewTest(APITestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='password')
        Post.objects.create(text='post1', author=user)
        Post.objects.create(text='post2', author=user)
        Post.objects.create(text='post3', author=user)
        user = User.objects.create_user(username='test2', password='password')

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.user2 = User.objects.get(pk=2)

    def test_list_posts(self):
        posts = PostSerializer(instance=Post.objects.order_by('-date_created').filter(
            author__uuid=self.user.uuid), many=True)
        res = self.client.get(
            reverse('get_user_posts', kwargs={'uuid': self.user.uuid}))

        self.assertDictEqual(posts.data[0], res.data[0])
        self.assertDictEqual(posts.data[1], res.data[1])
        self.assertDictEqual(posts.data[2], res.data[2])

    def test_no_posts(self):
        res = self.client.get(
            reverse('get_user_posts', kwargs={'uuid': self.user2.uuid}))

        self.assertEqual(res.data, [])

    def test_bad_uuid(self):
        res = self.client.get(
            reverse('get_user_posts', kwargs={'uuid': uuid4()}))
        self.assertEqual(res.data, [])
