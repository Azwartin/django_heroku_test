from django.db import models
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date
import uuid

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as __

# Create your models here.

class Genre(models.Model):
  """
    Model representing a book genre
  """
  name = models.CharField(verbose_name="Жанр", max_length=100, help_text="Enter a book genre")

  def __str__(self):
    """
      String representing the Model object
    """
    return self.name  

class Book(models.Model):
  """
    Model representing a book (but not instance)
  """

  title = models.CharField(verbose_name="Название", max_length=128)
  author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
  summary = models.TextField(verbose_name="Описание", max_length=1000)
  isbn = models.CharField(verbose_name="ISBN", max_length=13)
  genre = models.ManyToManyField(Genre, help_text="Выберите жанр") 

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('book-detail', args=[str(self.id)])

class BookInstance(models.Model):
  """
    Model representing a book instance
  """
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="UUID")
  book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
  imprint=models.CharField(max_length=100)
  due_back=models.DateField(null=True, blank=True)
  borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
  @property
  def is_overdue(self):
    return self.due_back and date.today() > self.due_back


  
  LOAN_STATUS = (
    ('m', 'Maintenance'),
    ('o', 'On loan'),
    ('a', 'Available'),
    ('r', 'Reserved'),
  )

  status = models.CharField(max_length=1, choices=LOAN_STATUS)

  class Meta:
    ordering = ["due_back"]
    permissions = (("catalog.can_mark_returned", "Set book as returned"),('catalog.can_see_borrowed', 'Can see borrowed'),)

  def __str__(self):
    return '{0} {1}'.format(self.id, self.book.title)

class Author(models.Model):
  """
    Model representing an author
  """

  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  date_of_birth = models.DateField(null=True, blank=True)
  date_of_death = models.DateField(null=True, blank=True, verbose_name='died')

  class Meta:
    permissions = (('catalog.can_author_edit', 'Can author edit'),)

  def get_absolute_url(self):
    return reverse('author-detail', args=[str(self.id)])

  def __str__(self):
    return '{0}, {1}'.format(self.last_name, self.first_name)