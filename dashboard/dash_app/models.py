from django.db import models

class Data_table(models.Model):
    end_year = models.CharField(max_length=4, blank=True, null=True)
    intensity = models.IntegerField(default=0)  # Set a default value to avoid null issues
    sector = models.CharField(max_length=100, blank=True, null=True)
    topic = models.CharField(max_length=100, blank=True, null=True)
    insight = models.TextField(blank=True, null=True)
    url = models.URLField(blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    start_year = models.CharField(max_length=4, blank=True, null=True)
    impact = models.TextField(blank=True, null=True)
    added = models.DateTimeField(blank=True, null=True)  # Allow nulls for optional dates
    published = models.DateTimeField(blank=True, null=True)  # Allow nulls for optional dates
    country = models.CharField(max_length=100, blank=True, null=True)
    relevance = models.IntegerField(blank=True, null=True)  # Allow nulls if required
    pestle = models.CharField(max_length=100, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    likelihood = models.IntegerField(default=0)  # Set a default value to avoid null issues

    def __str__(self):
        return self.title
