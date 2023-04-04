from django.test import TestCase
from .models import Rental, Product, Genre, Book, Film, CD, ProductIndex
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .admin import BookForm, FilmForm, CDForm
from django.core.exceptions import ValidationError


class ProductModelTestCase(TestCase):
    def setUp(self):
        self.file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        self.rental = Rental.objects.create(name="TestName", city="TestCity", zip_code="TestZipCode", street="TestStreet",
                                            building_number="TestBuildingNumber")

        self.genre_book = Genre.objects.create(name="TestGenreBook", category="book")
        self.genre_film = Genre.objects.create(name="TestGenreFilm", category="film")
        self.genre_cd = Genre.objects.create(name="TestGenreCD", category="cd")

        self.book = Book.objects.create(pk=1, title="TestTitleBook", image=self.file, genre=self.genre_book, author="TestAuthorBook", isbn=123)
        self.film = Film.objects.create(pk=2, title="TestTitleFilm", image=self.file, genre=self.genre_film, director="TestDirector",
                                        duration=233)
        self.cd = CD.objects.create(pk=3, title="TestTitleCD", image=self.file, genre=self.genre_cd, band="TestBand",
                                    tracklist="track1, track2")

    def create_product_index(self, inventory_number, product):
        return ProductIndex.objects.create(inventory_number=inventory_number, product=product,
                                           rental=Rental.objects.get(name="TestName"))

    # Checking that objects are created according to PolymorphicModel
    def test_polymorphism_model(self):
        self.assertEqual(self.book.title, "TestTitleBook")
        self.assertEqual(self.film.director, "TestDirector")
        self.assertEqual(self.cd.band, "TestBand")

        self.assertEqual(self.book.model_name, "book")
        self.assertEqual(self.film.model_name, "film")
        self.assertEqual(self.cd.model_name, "cd")

    # Checking whether the save() method itself saves the quantity of a given product
    def test_automatic_quantity(self):
        self.create_product_index("test1", self.book)
        self.book.save()
        self.assertEqual(self.book.quantity, 1)

        self.create_product_index("test2", self.film)
        self.create_product_index("test3", self.film)

        self.film.save()
        self.assertEqual(self.film.quantity, 2)

        cd_obj = Product.objects.get(pk=3)
        self.assertEqual(self.cd.quantity, 0)

    # Checking if listviews are working
    def test_listView(self):
        list_url_home = reverse('Home')
        response = self.client.get(list_url_home)
        self.assertEqual(response.status_code, 200)

        list_url_book = reverse('BookListView')
        response = self.client.get(list_url_book)
        self.assertEqual(response.status_code, 200)

        list_url_film = reverse('FilmListView')
        response = self.client.get(list_url_film)
        self.assertEqual(response.status_code, 200)

        list_url_cd = reverse('CDListView')
        response = self.client.get(list_url_cd)
        self.assertEqual(response.status_code, 200)

    # Checks that detailview and get_absolute_url are working properly
    def test_detailView(self):
        response_book = self.client.get(self.book.get_absolute_url())
        self.assertEqual(response_book.status_code, 200)

        response_film = self.client.get(self.film.get_absolute_url())
        self.assertEqual(response_film.status_code, 200)

        response_cd = self.client.get(self.cd.get_absolute_url())
        self.assertEqual(response_cd.status_code, 200)

    # testing whether filtering by genre, alphabetically and by popularity works
    def test_filter(self):
        url = reverse('Home') + f'?genre=alphabetical'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestTitleBook')
        self.assertContains(response, 'TestTitleFilm')
        self.assertContains(response, 'TestTitleCD')

        url = reverse('Home') + f'?genre=popularity'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestTitleBook')
        self.assertContains(response, 'TestTitleFilm')
        self.assertContains(response, 'TestTitleCD')

        url = reverse('BookListView') + f'?genre={self.genre_book.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestTitleBook')

        url = reverse('FilmListView') + f'?genre={self.genre_film.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestTitleFilm')

        url = reverse('CDListView') + f'?genre={self.genre_cd.pk}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'TestTitleCD')

