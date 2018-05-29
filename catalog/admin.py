from django.contrib import admin

# Register your models here.

from .models import Author, Genre, Book, BookInstance

class BooksInstanceInline(admin.TabularInline):
    model = BookInstance

class BooksInline(admin.TabularInline):
    model = Book

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
  list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
  fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
  inlines = [BooksInline]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BooksInstanceInline]

    def display_genre(i, self):
      """
        Return a string of Genre
      """    
      return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
  list_display = ('book_title', 'status', 'due_back', 'borrower')
  list_filter = ('status', 'due_back')
  def book_title(i, self):
    """
      Return a string of Book Name
    """
    return self.book.title

  fieldsets = (
        (None, {
            'fields': ('book','imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back', 'borrower')
        }),
    )

admin.site.register(Genre)