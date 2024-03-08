from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime
# Create your models here.

#my models

class Genre(models.Model):
    genre_text = models.CharField(max_length=20)
    def __str__(self):
        return self.genre_text

class Musician(models.Model):
    musician_name = models.CharField(max_length=40)
    musician_photo = models.ImageField(null=True, upload_to='musician_images/')
    musician_bio = models.TextField(blank=True)
    musician_followers = models.ManyToManyField(User)
    
    musician_genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    def __str__(self):
        return self.musician_name

class Post(models.Model):
    post_text = models.CharField(max_length=100)
    post_pubdate = models.DateTimeField('Date Published', auto_now_add=True)
    post_image = models.ImageField(null=True, upload_to='comment_images/')
    post_likers = models.ManyToManyField(User, related_name='post_likers')
    post_musician = models.ForeignKey(Musician, on_delete=models.CASCADE)
    post_author = models.ForeignKey(User,  on_delete=models.DO_NOTHING, related_name='post_author')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.post_text


class Comment(models.Model):
    comment_text = models.CharField(max_length=80)
    comment_pubdate = models.DateTimeField('Date Published',  auto_now_add=True)
    comment_author = models.ForeignKey(User, on_delete=models.DO_NOTHING,related_name='comment_author' )
    comment_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.comment_text



    

# userprofile --> extra info about every user (how many followers, pictures etc.
# upcomingcocerts --> manytomany relationship with artist
# recentreleases --> manytomany relationship with artist
# for itmes in subreddits:
#     print the itmes with the most followers 