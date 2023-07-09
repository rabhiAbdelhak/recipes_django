#test for the user api

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    #creating a user
   return get_user_model().objects.create_user(**params)



class PublicUserAPITest(TestCase):
   
   def setUp(self):
      self.client = APIClient
    
   def test_create_user_success(self):
      #test creating a user is successful
      payload = {
         'email': "abdelwahed@gmail.com",
         'password': 'abdou1234',
         'name': 'abdelwahed'
      }
      res = self.client.post(CREATE_USER_URL, payload)
      self.assertEqual(res.status_code, status.HTTP_201_CREATED)
      user = get_user_model().objects.get(payload['email'])
      self.assertTrue(user.check_password(payload['password']))
      self.assertNotIn('password', res.data)

   def test_email_already_existed(self):
      #test that email is already existed error works
      payload = {
         'email': "abdelwahed@gmail.com",
         'password': 'abdou1234',
         'name': 'abdelwahed'
      }

      create_user(**payload)
      res = self.client.post(CREATE_USER_URL, payload)
      self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
   def test_password_to_short_error(self):
      #test the password is too short error works
      payload = {
         'email': "abdelwahed@gmail.com",
         'password': 'pw',
         'name': 'abdelwahed'
      }

      res = self.cliant.post(CREATE_USER_URL, payload)
      self.assertEqual(res.status, status.HTTP_400_BAD_REQUEST)

      #test that the users didnt get added to the database
      user_exists = get_user_model().objects.filter(email = payload['email']).exists()
      self.assertFalse(user_exists)

      

