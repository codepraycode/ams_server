import pdb
from api.test.test_setup import TestSetup
from rest_framework import  status

class TestViews (TestSetup):

    def test_association_can_register_with_incomplete_data(self):
        res = self.client.post(
            self.register_url, self.incomplete_association_data, format="multipart")

        self.assertNotEqual(res.status_code, status.HTTP_201_CREATED)
    
    def test_association_can_register_with_complete_data(self):
        res = self.client.post(
            self.register_url, self.complete_association_data, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
    
    
    def test_association_cannot_signin(self):

        # self.client.credentials(
        #     HTTP_AUTHORIZATION='Token ' + self.association_token.key)

        res = self.client.post(
            self.login_url, self.incorrect_association_login_data)

        self.assertNotEqual(res.status_code, status.HTTP_200_OK)

    # def test_association_can_signin_with_correct_data(self):

    #     res = self.client.post(
    #         self.register_url, self.complete_association_data, format="multipart")

    #     self.assertEqual(res.status_code, status.HTTP_201_CREATED)


        
    #     res = self.client.post(
    #         self.login_url, self.correct_association_login_data)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
