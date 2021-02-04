from django.db import models
from django.contrib.auth.models import User

def item_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/items/<id>/<filename> 
    return 'items/{0}/{1}'.format(instance.id, filename) 

class Item(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=item_directory_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="item_created_by")
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, related_name="item_updated_by")

    def __str__(self):
        return self.name
    
