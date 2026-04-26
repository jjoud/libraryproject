from django.shortcuts import render
from django.db.models import Q
from django.db.models import Avg, Count, Max, Min, Sum
from django.db.models.functions import Coalesce

from .models import Book, Publisher, Student
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
