from django.db import models
from django.conf import settings


class Posts(models.Model):
    title = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    category = models.ForeignKey('Categories', models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = "post"

    def __str__(self):
        return self.title


class Categories(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField()
    is_root = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_root:
            try:
                root = Categories.objects.get(is_root=True)
                if self != root:
                    self.is_root = False
            except Categories.DoesNotExist:
                pass
        if self.parent_category is None:
            try:
                root = Categories.objects.get(is_root=True)
                if self != root:
                    self.parent_category = root
                else:
                    self.parent_category = None
            except Categories.DoesNotExist:
                pass
        super(Categories, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('slug', 'parent_category',)
        verbose_name_plural = "categories"

    def __str__(self):
        full_path = [self.name]
        k = self.parent_category
        while k is not None:
            full_path.append(k.name)
            k = k.parent_category
        return ' -> '.join(full_path[::-1])
