from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Post
from django.urls import reverse

# Create your tests here.
class BlogTests(TestCase):
    @classmethod
    # this tests to make sure the object is added
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username="testuser",email="test@gmail.com",password="secret")
        cls.post = Post.objects.create(
            title="A good title",
            body="Nice body content",
            author=cls.user,
        )
        
    #this tests to make sure the blog post is actually made
    def test_post_model(self):
        self.assertEqual(self.post.title,"A good title")
        self.assertEqual(self.post.body,"Nice body content")
        self.assertEqual(self.post.author.username,"testuser")
        self.assertEqual(str(self.post),"A good title")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")
      
    #this test to make sure the url exists at the correct location  for listview
    def test_url_exists_at_correct_location_listview(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code,200)
      
    #this tests to make sure the correct location for detailview
    def test_url_exists_at_correct_location_detailview(self):
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code,200)
        
    #this tests to make sure the listview post works
    def test_post_listview(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response,"Nice body content")
        self.assertTemplateUsed(response,'home.html')
        
    #this tests to make sure the detailview post works
    def test_post_detailview(self):
        response = self.client.get(reverse('post_detail',kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code,200)
        self.assertEqual(no_response.status_code,404)
        self.assertContains(response,"A good title")
        self.assertTemplateUsed(response,'post_detail.html')
        
    #this tests to make sure the create post by visiting the page works 
    def test_post_createview(self):
        response = self.client.post(
            reverse('post_new'),
            {
                "title":"New Title",
                "body":"New text",
                "author":self.user.id,
            },
        )
        self.assertEqual(response.status_code,302)
        self.assertEqual(Post.objects.last().title,"New Title")
        self.assertEqual(Post.objects.last().body,"New text")
        
    #this tests to make sure the post update works
    def test_post_updateview(self):
        response = self.client.post(
            reverse("post_edit",args="1"),
            {
                "title":"Updated title",
                "body":"Updated text",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Post.objects.last().title,"Updated title")
        self.assertEqual(Post.objects.last().body, "Updated text")
        
    #this tests to make sure the delete post works
    def test_post_deleteview(self):
        response = self.client.post(reverse('post_delete',args="1"))
        self.assertEqual(response.status_code,302)