from django.db import models

class ExtraInfo(models.Model):
    KIND = {
        (0,"unknown"),
        (1,"horror"),
        (2,"comedy"),
        (3,"drama")
    }
    time = models.IntegerField()
    kind = models.IntegerField(choices=KIND, default=0)

class Movie (models.Model):
    title = models.CharField(max_length=40)
    content = models.TextField()
    after_prem = models.BooleanField(default=False)
    premiere = models.DateField(null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    imdb_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    extra_info = models.OneToOneField(ExtraInfo, on_delete=models.CASCADE, null=True, blank=True)
    def __str__(self):
        return self.name()
    def name (self):
        return self.title + " (" + str(self.year) + ")"

class Rate (models.Model):
    descript = models.TextField(default='')
    stars = models.IntegerField(default=3)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='rates')

class Actor (models.Model):
    name = models.CharField(max_length=40)
    surname = models.CharField(max_length=40)
    movies = models.ManyToManyField(Movie)






