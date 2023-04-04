from django.test import TestCase
from .models import Rental, Product, Genre, Book, Film, CD, ProductIndex
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse


class ProductModelTestCase(TestCase):
    def setUp(self):
        file = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        rental = Rental.objects.create(name="TestName",
                                       city="TestCity",
                                       zip_code="TestZipCode",
                                       street="TestStreet",
                                       building_number="TestBuildingNumber")
        genre_book = Genre.objects.create(name="TestGenreBook",
                                          category="book")
        genre_film = Genre.objects.create(name="TestGenreFilm",
                                          category="film")
        genre_cd = Genre.objects.create(name="TestGenreCD",
                                        category="cd")
        Book.objects.create(pk=1,
                            title="TestTitleBook",
                            image=file,
                            genre=genre_book,
                            author="TestAuthorBook",
                            isbn=123,
                            )
        Film.objects.create(pk=2,
                            title="TestTitleFilm",
                            image=file,
                            genre=genre_film,
                            director="TestDirector",
                            duration=233,
                            )
        CD.objects.create(pk=3,
                          title="TestTitleCD",
                          image=file,
                          genre=genre_cd,
                          band="TestBand",
                          tracklist="track1, track2")

    def create_product_index(self, inventory_number, product):
        return ProductIndex.objects.create(
            inventory_number=inventory_number,
            product=product,
            rental=Rental.objects.get(name="TestName"),
        )

    # Checking that objects are created according to PolymorphicModel
    def test_polymorphism_model(self):
        book_obj = Product.objects.get(title="TestTitleBook")
        self.assertEqual(book_obj.title, "TestTitleBook")
        film_obj = Film.objects.get(director="TestDirector")
        self.assertEqual(film_obj.director, "TestDirector")
        cd_obj = CD.objects.get(band="TestBand")
        self.assertEqual(cd_obj.band, "TestBand")

        self.assertEqual(book_obj.model_name, "book")
        self.assertEqual(film_obj.model_name, "film")
        self.assertEqual(cd_obj.model_name, "cd")

    # Checking whether the save() method itself saves the quantity of a given product
    def test_automatic_quantity(self):
        book_obj = Product.objects.get(pk=1)
        self.create_product_index("test1", book_obj)
        book_obj.save()
        self.assertEqual(book_obj.quantity, 1)

        film_obj = Product.objects.get(pk=2)
        self.create_product_index("test2", film_obj)
        self.create_product_index("test3", film_obj)

        film_obj.save()
        self.assertEqual(film_obj.quantity, 2)

        cd_obj = Product.objects.get(pk=3)
        self.assertEqual(cd_obj.quantity, 0)

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
        book_obj = Product.objects.get(pk=1)
        response_book = self.client.get(book_obj.get_absolute_url())
        self.assertEqual(response_book.status_code, 200)

        film_obj = Product.objects.get(pk=2)
        response_film = self.client.get(film_obj.get_absolute_url())
        self.assertEqual(response_film.status_code, 200)

        cd_obj = Product.objects.get(pk=3)
        response_cd = self.client.get(cd_obj.get_absolute_url())
        self.assertEqual(response_cd.status_code, 200)
