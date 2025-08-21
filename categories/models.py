from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        db_table = 'categories'

    def __str__(self) -> str:  # noqa: D401
        return self.name


