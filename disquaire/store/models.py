from django.db import models

# Create your models here.
# ARTISTS = {
#     "youssou-ndour" : {"name" : "Youssou Ndour"},
#     "wally-seck" : {"name" : "Wally Seck"},
# } 

# ALBUMS = [
#     {"name" : "Bercy", "artists" : [ARTISTS["youssou-ndour"]]},
#     {"name" : "Senegal", "artists" : [ARTISTS["wally-seck"]]}
# ]

class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __str__(self):
        return self.name

class Contact(models.Model):
    email = models.EmailField(max_length=100, verbose_name="Email", unique=True)
    name = models.CharField(max_length=200, verbose_name="Nom")
    def __str__(self):
        return self.name

class Album(models.Model):
    reference = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    picture = models.URLField()   
    artists = models.ManyToManyField(Artist, related_name='albums', blank=True)
    def __str__(self):
        theArtists=", ".join([artist.name for artist in self.artists.all()])
        return "{} / {}".format(self.title, theArtists)

class Booking(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    contacted = models.BooleanField(default=False)
    contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
    album = models.OneToOneField(Album,on_delete=models.CASCADE)
    def __str__(self):
        return self.contact.name