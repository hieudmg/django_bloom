from django.db import models
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.TextField(default='')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, blank=True, null=True)
    category = models.ManyToManyField('post.Category')
    slug = models.SlugField(unique=True)
    pinned = models.BooleanField(default=False)
    views = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "posts"

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(default='')
    parent_category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    slug = models.SlugField()
    is_root = models.BooleanField(default=False)
    string = models.TextField(default='')

    def save(self, *args, **kwargs):
        parent_string = ''
        delimiter = ' -> '
        if self.is_root:
            try:
                root = Category.objects.get(is_root=True)
                if self != root:
                    self.is_root = False
            except Category.DoesNotExist:
                pass
        if self.parent_category is None:
            try:
                root = Category.objects.get(is_root=True)
                if self != root:
                    self.parent_category = root
                    parent_string = 'root' + delimiter
                else:
                    parent_string = ''
            except Category.DoesNotExist:
                pass
        else:
            parent_string = self.parent_category.string + delimiter
        self.string = parent_string + self.name
        super(Category, self).save(*args, **kwargs)
        for child in self.category_set.all():
            child.save()

    class Meta:
        unique_together = ('slug', 'parent_category',)
        verbose_name_plural = "categories"

    def get_parent_categories(self):
        result = [self]
        parent = self.parent_category
        while parent is not None:
            result.insert(0, parent)
            parent = parent.parent_category
        return result

    def get_child_categories(self):
        result = []
        children = self.category_set.all()
        while len(children) > 0:
            for child in children:
                result.extend(child.get_child_categories())
        return result

    def get_post_set(self):
        result = []
        result.extend(self.post_set.all())
        children = self.category_set.all()
        if len(children) > 0:
            for child in children:
                result.extend(child.get_post_set())
        return result

    def __str__(self):
        return self.string
