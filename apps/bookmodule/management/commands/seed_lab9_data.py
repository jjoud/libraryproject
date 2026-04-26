import random
from datetime import date, datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.bookmodule.models import Author, Book, Publisher


class Command(BaseCommand):
    help = "Seed Publisher, Author, and Book tables with fake lab data."

    def add_arguments(self, parser):
        parser.add_argument(
            "--publishers",
            type=int,
            default=6,
            help="Number of publishers to create.",
        )
        parser.add_argument(
            "--authors",
            type=int,
            default=18,
            help="Number of authors to create.",
        )
        parser.add_argument(
            "--books",
            type=int,
            default=30,
            help="Number of books to create.",
        )
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing publishers, authors, and books before seeding.",
        )

    def handle(self, *args, **options):
        if options["reset"]:
            Book.objects.all().delete()
            Author.objects.all().delete()
            Publisher.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing lab 9 data deleted."))

        publishers = self._create_publishers(options["publishers"])
        authors = self._create_authors(options["authors"])
        books = self._create_books(options["books"], publishers, authors)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {len(publishers)} publishers, {len(authors)} authors, and {len(books)} books."
            )
        )

    def _create_publishers(self, count):
        locations = [
            "Doha, Qatar",
            "Riyadh, Saudi Arabia",
            "Dubai, UAE",
            "Cairo, Egypt",
            "Amman, Jordan",
            "Muscat, Oman",
            "London, UK",
            "New York, USA",
        ]
        labels = [
            "Horizon Press",
            "Falcon House",
            "Maple Books",
            "Lighthouse Publishing",
            "Scholars Hub",
            "Blue Ink Media",
            "Golden Page Works",
            "Cedar Publications",
        ]

        publishers = []
        for index in range(count):
            publisher, _ = Publisher.objects.get_or_create(
                name=f"{labels[index % len(labels)]} {index + 1}",
                defaults={"location": locations[index % len(locations)]},
            )
            publishers.append(publisher)
        return publishers

    def _create_authors(self, count):
        first_names = [
            "Omar",
            "Lina",
            "Maya",
            "Noah",
            "Layla",
            "Adam",
            "Sara",
            "Yousef",
            "Nora",
            "Zaid",
        ]
        last_names = [
            "Hassan",
            "Faris",
            "Khaled",
            "Nasser",
            "Rahman",
            "Saleh",
            "Karim",
            "Mahmoud",
            "Saeed",
            "Hamdan",
        ]

        authors = []
        for index in range(count):
            full_name = (
                f"{first_names[index % len(first_names)]} "
                f"{last_names[(index * 2) % len(last_names)]}"
            )
            dob = date(1965, 1, 1) + timedelta(days=365 * (index % 30))
            author, _ = Author.objects.get_or_create(
                name=full_name,
                defaults={"DOB": dob},
            )
            authors.append(author)
        return authors

    def _create_books(self, count, publishers, authors):
        topics = [
            "Data Science",
            "Networks",
            "Cloud Systems",
            "Python",
            "Cyber Security",
            "Machine Learning",
            "Algorithms",
            "Databases",
            "Web Development",
            "Software Testing",
        ]
        subtitles = [
            "Essentials",
            "Foundations",
            "in Practice",
            "Handbook",
            "Workshop",
            "Guide",
        ]

        books = []
        aware_now = timezone.now()
        for index in range(count):
            title = (
                f"{topics[index % len(topics)]} "
                f"{subtitles[index % len(subtitles)]} {index + 1}"
            )
            publisher = publishers[index % len(publishers)]
            main_author = authors[index % len(authors)]
            pubdate = aware_now - timedelta(days=60 * (index + 1))
            book, created = Book.objects.get_or_create(
                title=title,
                defaults={
                    "author": main_author.name,
                    "price": round(random.uniform(45, 220), 2),
                    "quantity": random.randint(2, 25),
                    "pubdate": pubdate,
                    "rating": random.randint(1, 5),
                    "edition": random.randint(1, 5),
                    "publisher": publisher,
                },
            )
            if created:
                author_count = random.randint(1, min(3, len(authors)))
                book.authors.set(random.sample(authors, author_count))
            else:
                if not book.publisher:
                    book.publisher = publisher
                if not book.pubdate:
                    book.pubdate = pubdate
                if not book.author:
                    book.author = main_author.name
                if book.quantity is None:
                    book.quantity = 1
                book.save()
                if book.authors.count() == 0:
                    author_count = random.randint(1, min(3, len(authors)))
                    book.authors.set(random.sample(authors, author_count))
            books.append(book)
        return books
