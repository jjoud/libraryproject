from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Q
from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models.functions import Coalesce

from .forms import (
    Address2Form,
    AddressForm,
    BookForm,
    Student2Form,
    StudentActivityForm,
    StudentForm,
)
from .models import Address, Address2, Book, Publisher, Student, Student2, StudentActivity
#python manage.py runserver

def __getBooksList():
    book1 = {'id': 12344321, 'title': 'Continuous Delivery', 'author': 'J.Humble and D. Farley'}
    book2 = {'id': 56788765, 'title': 'Reversing: Secrets of Reverse Engineering', 'author': 'E. Eilam'}
    book3 = {'id': 43211234, 'title': 'The Hundred-Page Machine Learning Book', 'author': 'Andriy Burkov'}
    return [book1, book2, book3]


def index(request):
    return render(request, 'bookmodule/index.html')

def list_books(request):
    return render(request, 'bookmodule/list_books.html')

def viewbook(request, bookId):
    return render(request, 'bookmodule/one_book.html')

def aboutus(request):
    return render(request, 'bookmodule/aboutus.html')

def html5_links(request):
    return render(request, "bookmodule/links.html")

def html5_text_formatting(request):
    return render(request, "bookmodule/text_formatting.html")

def html5_listing(request):
    return render(request, "bookmodule/listing.html")

def html5_tables(request):
    return render(request, "bookmodule/tables.html")


def search_books(request):
    if request.method == "POST":
        string = request.POST.get('keyword', '').lower()
        isTitle = request.POST.get('option1')
        isAuthor = request.POST.get('option2')
        books = __getBooksList()
        newBooks = []

        for item in books:
            contained = False
            if isTitle and string in item['title'].lower():
                contained = True
            if not contained and isAuthor and string in item['author'].lower():
                contained = True

            if contained:
                newBooks.append(item)

        return render(request, 'bookmodule/bookList.html', {'books': newBooks})

    return render(request, "bookmodule/search.html")


def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='ea')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})


def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False).filter(
        title__icontains='and'
    ).filter(
        edition__gte=2
    ).exclude(price__lte=100)[:10]

    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')


def insert_book(request):
    mybook = Book(
        title='Continuous Delivery',
        author='J.Humble and D. Farley',
        edition=1,
    )
    mybook.save()
    all_books = Book.objects.all()
    return render(request, 'bookmodule/bookList.html', {'books': all_books})


def lab8_task1(request):
    books = Book.objects.filter(Q(price__lte=80))
    return render(request, 'bookmodule/lab8_task1.html', {'books': books})


def lab8_task2(request):
    books = Book.objects.filter(
        Q(edition__gt=3) & (Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_task2.html', {'books': books})


def lab8_task3(request):
    books = Book.objects.filter(
        Q(edition__lte=3) & ~(Q(title__icontains='qu') | Q(author__icontains='qu'))
    )
    return render(request, 'bookmodule/lab8_task3.html', {'books': books})


def lab8_task4(request):
    books = Book.objects.order_by('title')
    return render(request, 'bookmodule/lab8_task4.html', {'books': books})


def lab8_task5(request):
    stats = Book.objects.aggregate(
        book_count=Count('id'),
        total_price=Sum('price'),
        average_price=Avg('price'),
        max_price=Max('price'),
        min_price=Min('price'),
    )
    return render(request, 'bookmodule/lab8_task5.html', {'stats': stats})


def lab8_task7(request):
    city_student_counts = Student.objects.values('address__city').annotate(
        student_count=Count('id')
    ).order_by('address__city')
    return render(
        request,
        'bookmodule/lab8_task7.html',
        {'city_student_counts': city_student_counts},
    )


def lab9_task1(request):
    books = list(
        Book.objects.select_related('publisher').prefetch_related('authors').order_by('title')
    )
    total_stock = Book.objects.aggregate(total_stock=Coalesce(Sum('quantity'), 0))[
        'total_stock'
    ]

    for book in books:
        if total_stock > 0:
            book.availability_percentage = round((book.quantity / total_stock) * 100)
        else:
            book.availability_percentage = 0

    return render(
        request,
        'bookmodule/lab9_task1.html',
        {'books': books, 'total_stock': total_stock},
    )


def lab9_task2(request):
    publishers = Publisher.objects.annotate(
        total_book_stock=Coalesce(Sum('book__quantity'), 0),
        book_count=Count('book', distinct=True),
    ).prefetch_related('book_set').order_by('name')

    return render(
        request,
        'bookmodule/lab9_task2.html',
        {'publishers': publishers},
    )


def lab9_task3(request):
    publishers = Publisher.objects.annotate(
        oldest_book_pubdate=Min('book__pubdate')
    ).filter(oldest_book_pubdate__isnull=False).prefetch_related('book_set').order_by('name')

    for publisher in publishers:
        publisher.oldest_book = publisher.book_set.filter(
            pubdate=publisher.oldest_book_pubdate
        ).order_by('title').first()

    return render(
        request,
        'bookmodule/lab9_task3.html',
        {'publishers': publishers},
    )


def lab9_task4(request):
    publishers = Publisher.objects.annotate(
        average_price=Avg('book__price'),
        min_price=Min('book__price'),
        max_price=Max('book__price'),
    ).filter(book__isnull=False).distinct().order_by('name')

    return render(
        request,
        'bookmodule/lab9_task4.html',
        {'publishers': publishers},
    )


def lab9_task5(request):
    publishers = Publisher.objects.annotate(
        highly_rated_books_count=Count('book', filter=Q(book__rating__gte=4), distinct=True),
        highly_rated_books_quantity=Coalesce(
            Sum('book__quantity', filter=Q(book__rating__gte=4)),
            0,
        ),
    ).filter(highly_rated_books_count__gt=0).order_by('name')

    return render(
        request,
        'bookmodule/lab9_task5.html',
        {'publishers': publishers},
    )


def lab9_task6(request):
    qualifying_filter = Q(book__price__gt=50) & Q(book__quantity__lt=5) & Q(book__quantity__gte=1)
    publishers = Publisher.objects.annotate(
        qualifying_books_count=Count('book', filter=qualifying_filter, distinct=True),
    ).prefetch_related('book_set').order_by('name')

    for publisher in publishers:
        publisher.filtered_books = publisher.book_set.filter(
            price__gt=50,
            quantity__lt=5,
            quantity__gte=1,
        ).order_by('title')

    return render(
        request,
        'bookmodule/lab9_task6.html',
        {'publishers': publishers},
    )


def lab9_part1_listbooks(request):
    books = Book.objects.select_related('publisher').order_by('id')
    return render(
        request,
        'bookmodule/lab9_part1_listbooks.html',
        {'books': books},
    )


def __lab9_part1_save_book_from_post(book, post_data):
    book.title = post_data.get('title', '').strip()
    book.author = post_data.get('author', '').strip()
    book.price = float(post_data.get('price') or 0)
    book.edition = int(post_data.get('edition') or 1)
    book.quantity = int(post_data.get('quantity') or 1)
    book.rating = int(post_data.get('rating') or 1)

    publisher_id = post_data.get('publisher')
    book.publisher = Publisher.objects.filter(id=publisher_id).first() if publisher_id else None
    book.save()


def lab9_part1_addbook(request):
    publishers = Publisher.objects.order_by('name')

    if request.method == 'POST':
        try:
            __lab9_part1_save_book_from_post(Book(), request.POST)
            return redirect('books.lab9_part1_listbooks')
        except ValueError:
            return render(
                request,
                'bookmodule/lab9_part1_book_form.html',
                {
                    'book': request.POST,
                    'publishers': publishers,
                    'page_title': 'Add Book',
                    'button_text': 'Add Book',
                    'error': 'Please enter valid numeric values for price, edition, quantity, and rating.',
                },
            )

    return render(
        request,
        'bookmodule/lab9_part1_book_form.html',
        {
            'publishers': publishers,
            'page_title': 'Add Book',
            'button_text': 'Add Book',
        },
    )


def lab9_part1_editbook(request, id):
    book = get_object_or_404(Book, id=id)
    publishers = Publisher.objects.order_by('name')

    if request.method == 'POST':
        try:
            __lab9_part1_save_book_from_post(book, request.POST)
            return redirect('books.lab9_part1_listbooks')
        except ValueError:
            return render(
                request,
                'bookmodule/lab9_part1_book_form.html',
                {
                    'book': book,
                    'publishers': publishers,
                    'page_title': 'Edit Book',
                    'button_text': 'Update Book',
                    'error': 'Please enter valid numeric values for price, edition, quantity, and rating.',
                },
            )

    return render(
        request,
        'bookmodule/lab9_part1_book_form.html',
        {
            'book': book,
            'publishers': publishers,
            'page_title': 'Edit Book',
            'button_text': 'Update Book',
        },
    )


def lab9_part1_deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books.lab9_part1_listbooks')


def lab9_part2_listbooks(request):
    books = Book.objects.select_related('publisher').order_by('id')
    return render(
        request,
        'bookmodule/lab9_part2_listbooks.html',
        {'books': books},
    )


def lab9_part2_addbook(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab9_part2_listbooks')
    else:
        form = BookForm()

    return render(
        request,
        'bookmodule/lab9_part2_book_form.html',
        {
            'form': form,
            'page_title': 'Add Book',
            'button_text': 'Add Book',
        },
    )


def lab9_part2_editbook(request, id):
    book = get_object_or_404(Book, id=id)

    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)      #instance dont creat anouther book just edit the book u have
        if form.is_valid():
            form.save()
            return redirect('books.lab9_part2_listbooks')
    else:
        form = BookForm(instance=book)

    return render(
        request,
        'bookmodule/lab9_part2_book_form.html',
        {
            'form': form,
            'book': book,
            'page_title': 'Edit Book',
            'button_text': 'Update Book',
        },
    )


def lab9_part2_deletebook(request, id):
    book = get_object_or_404(Book, id=id)
    book.delete()
    return redirect('books.lab9_part2_listbooks')


def lab10_task1_students(request):
    students = Student.objects.select_related('address').order_by('name')
    addresses = Address.objects.order_by('city')
    return render(
        request,
        'bookmodule/lab10_task1_students.html',
        {'students': students, 'addresses': addresses},
    )


def lab10_task1_add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task1_students')
    else:
        form = AddressForm()

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Add Address', 'button_text': 'Save Address'},
    )


def lab10_task1_edit_address(request, id):
    address = get_object_or_404(Address, id=id)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task1_students')
    else:
        form = AddressForm(instance=address)

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Edit Address', 'button_text': 'Update Address'},
    )


def lab10_task1_delete_address(request, id):
    address = get_object_or_404(Address, id=id)
    if request.method == 'POST':
        address.delete()
        return redirect('books.lab10_task1_students')

    return render(
        request,
        'bookmodule/lab10_confirm_delete.html',
        {'object': address, 'cancel_url': 'books.lab10_task1_students'},
    )


def lab10_task1_add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task1_students')
    else:
        form = StudentForm()

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Add Student', 'button_text': 'Save Student'},
    )


def lab10_task1_edit_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task1_students')
    else:
        form = StudentForm(instance=student)

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Edit Student', 'button_text': 'Update Student'},
    )


def lab10_task1_delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('books.lab10_task1_students')

    return render(
        request,
        'bookmodule/lab10_confirm_delete.html',
        {'object': student, 'cancel_url': 'books.lab10_task1_students'},
    )


def lab10_task2_students(request):
    students = Student2.objects.prefetch_related('addresses').order_by('name')
    addresses = Address2.objects.order_by('city', 'street')
    return render(
        request,
        'bookmodule/lab10_task2_students.html',
        {'students': students, 'addresses': addresses},
    )


def lab10_task2_add_address(request):
    if request.method == 'POST':
        form = Address2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task2_students')
    else:
        form = Address2Form()

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Add Many-to-Many Address', 'button_text': 'Save Address'},
    )


def lab10_task2_edit_address(request, id):
    address = get_object_or_404(Address2, id=id)
    if request.method == 'POST':
        form = Address2Form(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task2_students')
    else:
        form = Address2Form(instance=address)

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Edit Many-to-Many Address', 'button_text': 'Update Address'},
    )


def lab10_task2_delete_address(request, id):
    address = get_object_or_404(Address2, id=id)
    if request.method == 'POST':
        address.delete()
        return redirect('books.lab10_task2_students')

    return render(
        request,
        'bookmodule/lab10_confirm_delete.html',
        {'object': address, 'cancel_url': 'books.lab10_task2_students'},
    )


def lab10_task2_add_student(request):
    if request.method == 'POST':
        form = Student2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task2_students')
    else:
        form = Student2Form()

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Add Many-to-Many Student', 'button_text': 'Save Student'},
    )


def lab10_task2_edit_student(request, id):
    student = get_object_or_404(Student2, id=id)
    if request.method == 'POST':
        form = Student2Form(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task2_students')
    else:
        form = Student2Form(instance=student)

    return render(
        request,
        'bookmodule/lab10_form.html',
        {'form': form, 'title': 'Edit Many-to-Many Student', 'button_text': 'Update Student'},
    )


def lab10_task2_delete_student(request, id):
    student = get_object_or_404(Student2, id=id)
    if request.method == 'POST':
        student.delete()
        return redirect('books.lab10_task2_students')

    return render(
        request,
        'bookmodule/lab10_confirm_delete.html',
        {'object': student, 'cancel_url': 'books.lab10_task2_students'},
    )


def lab10_task3_activities(request):
    activities = StudentActivity.objects.order_by('-created_at')
    return render(
        request,
        'bookmodule/lab10_task3_activities.html',
        {'activities': activities},
    )


def lab10_task3_add_activity(request):
    if request.method == 'POST':
        form = StudentActivityForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task3_activities')
    else:
        form = StudentActivityForm()

    return render(
        request,
        'bookmodule/lab10_file_form.html',
        {'form': form, 'title': 'Add Student Activity', 'button_text': 'Save Activity'},
    )


def lab10_task3_edit_activity(request, id):
    activity = get_object_or_404(StudentActivity, id=id)
    if request.method == 'POST':
        form = StudentActivityForm(request.POST, request.FILES, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('books.lab10_task3_activities')
    else:
        form = StudentActivityForm(instance=activity)

    return render(
        request,
        'bookmodule/lab10_file_form.html',
        {'form': form, 'title': 'Edit Student Activity', 'button_text': 'Update Activity'},
    )


def lab10_task3_delete_activity(request, id):
    activity = get_object_or_404(StudentActivity, id=id)
    if request.method == 'POST':
        activity.delete()
        return redirect('books.lab10_task3_activities')

    return render(
        request,
        'bookmodule/lab10_confirm_delete.html',
        {'object': activity, 'cancel_url': 'books.lab10_task3_activities'},
    )
