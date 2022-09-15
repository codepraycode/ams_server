from rest_framework.test import APITestCase
from django.urls import reverse
import io
from PIL import Image
from time import time
from association.models import Association
from api.models import AssociationAuthToken
class TestSetup(APITestCase):
    
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')

        file.name = str(time())+'.png'
        file.seek(0)
        return file
    

    def setUp(self) -> None:
        self.login_url = reverse('association_auth')
        self.register_url = reverse('create_association')
        self.association_url = lambda pk: reverse('rud_association', kwargs={"pk":pk})

        


        logo = self.generate_photo_file()

        self.complete_association_data = {
            "logo": logo,
            "name": "Izian Landlord association",
            "contact": "+23 9249987823",
            "town": "Oreta",
            "city": "Lagos",
            "local_government": "Ikorodu",
            "country": "Nigeria",
            "email": "izian@mail.com",
            "password":"olusola70308"
        }

        self.incomplete_association_data = {
            "name": "Izian Landlord association",
            "contact": "+23 9249987823",
            "town": "Oreta",
            "city": "Lagos",
            "local_government": "Ikorodu",
            "country": "Nigeria",
            "email": "izian@mail.com",
            "password":"olusola70308"
        }


        self.correct_association_login_data = {
            "email": "izian@mail.com",
            "password":"olusola70308"
        }

        self.incorrect_association_login_data = {
            "email": "izian@mails.com",
            "password":"olusola70308"
        }

        # try:
        #     self.association = Association.objects.create_association(
        #         **self.complete_association_data)

        #     self.association_token, created = AssociationAuthToken.objects.get_or_create(
        #         association=self.association)
        # except:
        #     pass
        return super().setUp()
    

    def tearDown(self) -> None:
        return super().tearDown()
