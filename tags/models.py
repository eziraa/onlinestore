from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# create tag model


class TeggedItemManager(models.Manager):
    def get_tags_for(self, object_type, obj_id):
        content_type = ContentType.objects.get_for_model(object_type)

        return TaggeItem.objects\
            .select_related('tag')\
            .filter(
                content_type=content_type,
                object_id=1
            )

class Tag(models.Model):
    label = models.CharField(max_length=255)

# create TeggedItem model


class TaggeItem(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey()
    objects = TeggedItemManager()

