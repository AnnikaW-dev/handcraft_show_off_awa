import os
import django
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from handcrafts.models import Post, Comment, Favorite
from django.utils import timezone


class HandcraftModelsTest(TestCase):
    """Test the handcraft models for proper relationships and constraints"""

    def setUp(self):
        """Set up test data"""
        self.user1 = User.objects.create_user(
            username='testuser1',
            email='test1@example.com',
            password='testpass123'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='testpass123'
        )

        self.post = Post.objects.create(
            title='Test Handcraft',
            content='This is a test handcraft post',
            author=self.user1,
            status=1,  # Published
            handcraft_type='knitting'
        )

    def test_post_creation(self):
        """Test that posts are created correctly"""
        self.assertEqual(self.post.title, 'Test Handcraft')
        self.assertEqual(self.post.author, self.user1)
        self.assertEqual(self.post.status, 1)
        self.assertTrue(self.post.created_on)
        self.assertTrue(self.post.updated_on)

    def test_post_str_method(self):
        """Test the string representation of Post"""
        expected = f"{self.post.title} | written by {self.user1.username}"
        self.assertEqual(str(self.post), expected)

    def test_post_slug_generation(self):
        """Test that slugs are generated automatically"""
        self.assertTrue(self.post.slug)
        self.assertIn('test-handcraft', self.post.slug)

    def test_comment_creation(self):
        """Test comment creation and relationship to post and user"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user2,
            body='Great handcraft!'
        )

        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user2)
        self.assertEqual(comment.body, 'Great handcraft!')
        self.assertFalse(comment.approved)  # Should default to False

    def test_comment_str_method(self):
        """Test the string representation of Comment"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user2,
            body='Great handcraft!'
        )
        expected = f"Comment {comment.body} by {self.user2.username}"
        self.assertEqual(str(comment), expected)

    def test_favorite_creation(self):
        """Test favorite creation and relationship"""
        favorite = Favorite.objects.create(
            user=self.user2,
            post=self.post
        )

        self.assertEqual(favorite.user, self.user2)
        self.assertEqual(favorite.post, self.post)
        self.assertTrue(favorite.created_on)

    def test_favorite_unique_constraint(self):
        """Test that a user can't favorite the same post twice"""
        Favorite.objects.create(user=self.user2, post=self.post)

        with self.assertRaises(IntegrityError):
            Favorite.objects.create(user=self.user2, post=self.post)

    def test_post_deletion_cascade(self):
        """Test that deleting a post deletes related comments and favorites"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user2,
            body='Great handcraft!'
        )
        favorite = Favorite.objects.create(
            user=self.user2,
            post=self.post
        )

        post_id = self.post.id
        self.post.delete()

        # Check that comment and favorite are also deleted
        self.assertFalse(Comment.objects.filter(post_id=post_id).exists())
        self.assertFalse(Favorite.objects.filter(post_id=post_id).exists())

    def test_user_deletion_cascade(self):
        """Test what happens when a user is deleted"""
        comment = Comment.objects.create(
            post=self.post,
            author=self.user2,
            body='Great handcraft!'
        )
        favorite = Favorite.objects.create(
            user=self.user2,
            post=self.post
        )

        user2_id = self.user2.id
        self.user2.delete()

        # Check that user's comments and favorites are deleted
        self.assertFalse(Comment.objects.filter(author_id=user2_id).exists())
        self.assertFalse(Favorite.objects.filter(user_id=user2_id).exists())

        # But the post should still exist
        # (assuming CASCADE is not set for author)
        self.assertTrue(Post.objects.filter(id=self.post.id).exists())

    def test_handcraft_types_validation(self):
        """Test that only valid handcraft types are accepted"""
        valid_types = [
            'knitting', 'crochet',
            'sewing', 'embroidery',
            'quilting', 'other']

        for craft_type in valid_types:
            post = Post.objects.create(
                title=f'Test {craft_type}',
                content='Test content',
                author=self.user1,
                handcraft_type=craft_type
            )
            self.assertEqual(post.handcraft_type, craft_type)

    def test_post_ordering(self):
        """Test that posts are ordered by creation date"""
        post2 = Post.objects.create(
            title='Second Post',
            content='Second post content',
            author=self.user1,
            status=1
        )

        posts = Post.objects.all()
        # Should be ordered by created_on descending
        self.assertEqual(posts.first(), post2)  # Most recent first

    def test_published_posts_only(self):
        """Test filtering for published posts only"""
        # Create a draft post
        draft_post = Post.objects.create(
            title='Draft Post',
            content='Draft content',
            author=self.user1,
            status=0  # Draft
        )

        published_posts = Post.objects.filter(status=1)
        all_posts = Post.objects.all()

        self.assertEqual(published_posts.count(), 1)
        self.assertEqual(all_posts.count(), 2)
        self.assertNotIn(draft_post, published_posts)
