from django.db import models


class Category(models.Model):
    type = models.CharField(max_length=32, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def delete(self, *args, **kwargs):
        if self.product_set.count() > 0:
            raise ValueError("Category not empty")
        else:
            super(Category, self).delete(*args, **kwargs)

    def __str__(self):
        return self.type


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=16, decimal_places=2)
    categories = models.ManyToManyField(Category)
    is_published = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.save()
