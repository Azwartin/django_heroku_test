from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
import datetime
from django.urls import reverse, reverse_lazy

from .forms import RenewBookForm
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# Create your views here.
@login_required
def index(request):
  """
    Show index page
  """
  num_books = Book.objects.all().count()
  num_instances = BookInstance.objects.all().count()
  num_instances_available = BookInstance.objects.filter(status__exact='a').all().count()
  num_authors = Author.objects.count()
  num_genres = Genre.objects.filter(name__contains='test').count()

  num_visits = request.session.get('num_visits', 0)
  request.session['num_visits'] = num_visits + 1

  return render(
    request,
    'index.html',
    context={
      'num_genres': num_genres,
      'num_books':num_books,
      'num_instances':num_instances,
      'num_instances_available':num_instances_available,
      'num_authors':num_authors,
      'num_visits': num_visits
    }
  )

class BookListView(LoginRequiredMixin, ListView):
  model = Book
  paginate_by = 1

class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed_user.html'
  paginate_by = 2

  def get_queryset(self):
    return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class BorrowedBooksListView(PermissionRequiredMixin, ListView):
  permission_required = ('catalog.can_see_borrowed')
  model = BookInstance
  template_name = 'catalog/bookinstance_list_borrowed.html'
  paginate_by = 2

  def get_queryset(self):
    return BookInstance.objects.filter(status__exact='o').exclude(borrower__isnull=True).order_by('due_back')

class BookDetailView(LoginRequiredMixin, DetailView):
  model = Book

class AuthorListView(LoginRequiredMixin, ListView):
  model = Author
  paginate_by = 10

class AuthorDetailView(LoginRequiredMixin, DetailView):
  model = Author

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
  book_inst = get_object_or_404(BookInstance, pk=pk)

  if request.method == 'POST':
    form = RenewBookForm(request.POST)

    if form.is_valid():
      book_inst.due_back = form.cleaned_data['renewal_date']
      book_inst.save()

      return HttpResponseRedirect(reverse('all-borrowed'))
  else:
    proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
    form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

  return render(request, 'catalog/book_renew_librarian.html', {'form': form, 'bookinst':book_inst})

class AuthorCreate(PermissionRequiredMixin, CreateView):
  permission_required = 'catalog.can_author_edit'
  model = Author
  fields = '__all__'
  initial = {'date_of_death' : '11/11/2016'}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
  permission_required = 'catalog.can_author_edit'
  model = Author
  fields = ['first_name','last_name','date_of_birth','date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
  permission_required = 'catalog.can_author_edit'
  model = Author
  success_url = reverse_lazy('authors')

class BookCreate(PermissionRequiredMixin, CreateView):
  permission_required = 'catalog.can_author_edit'
  model = Book
  fields = '__all__'

class BookUpdate(PermissionRequiredMixin, UpdateView):
  permission_required = 'catalog.can_author_edit'
  fields = ['title','author','summary','isbn','genre']
  model = Book

class BookDelete(PermissionRequiredMixin, DeleteView):
  permission_required = 'catalog.can_author_edit'
  model = Book
  success_url = reverse_lazy('books')