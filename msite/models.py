from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.

    

class Category(models.Model):
    cate=models.CharField(max_length=50)

    def __str__(self):
        return self.cate

    
    

class Actors(models.Model):
    actor_name=models.TextField(max_length=50)
    actors_photo=models.ImageField(upload_to='actors_ph',null=True)
    
    def __str__(self):
        return self.actor_name

    class Meta:
        ordering= ['actor_name']

    
    





class MainMovie(models.Model):
    name=models.CharField(max_length=100)
    poster=models.ImageField(upload_to='posters',null=True)
    poster2=models.ImageField(upload_to='posters2',null=True,blank=True)
    category=models.ManyToManyField(Category,related_name='category')
    about=models.CharField(max_length=1000,null=True)
    actors=models.ManyToManyField(Actors,related_name='actors')
    trailer=models.FileField(upload_to='trailer',null=True,blank=True)
    movie=models.FileField(upload_to='movie',null=True,blank=True)
    def __str__(self):
        return self.name

    


class Userprofile(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE)
    image = models.ImageField(default='def.png',upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} profile'




class Episode(models.Model):
    episode_name=models.CharField(max_length=100,null=True,blank=True)
    episode_poster=models.ImageField(upload_to='episode_ph',null=True)
    episode_poster2=models.ImageField(upload_to='episode_ph2',null=True)
    episode=models.FileField(upload_to='episodes',null=True)

    def __str__(self):
        return self.episode_name



class Part(models.Model):
    part_name=models.CharField(max_length=100,null=True,blank=True)
    poster=models.ImageField(upload_to='season_ph',null=True)
    episodes=models.ManyToManyField(Episode,related_name='epi')
    
    def __str__(self):
        return self.part_name
    

class TvShows(models.Model):
    name=models.CharField(max_length=100)
    poster=models.ImageField(upload_to='posters',null=True)
    poster2=models.ImageField(upload_to='posters',null=True,blank=True)
    about=models.CharField(max_length=500,null=True,blank=True)
    category=models.ManyToManyField(Category,related_name='TVcategory')
    actors=models.ManyToManyField(Actors,related_name='TVactors')
    season=models.ManyToManyField(Part,related_name='part')


    def __str__(self):
        return self.name


class MyList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(MainMovie, on_delete=models.CASCADE)
    watch = models.BooleanField(default=False)
    
class MyTvList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tv = models.ForeignKey(TvShows, on_delete=models.CASCADE)
    watch = models.BooleanField(default=False)

class Myrating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(MainMovie, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5), MinValueValidator(0)])
    def __str__(self):
        return self.movie.name


class SiteRecom(models.Model):
    movie=models.ForeignKey(MainMovie, on_delete=models.CASCADE,null=True,blank=True)

    
    
    

