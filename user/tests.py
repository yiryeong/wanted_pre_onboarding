import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserRegistrationTest(APITestCase):
    url = reverse('user:signup')

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            'username': 'test_user',
            'password': 'password',
            'password_check': 'password_check',
            'email': 'test_user@gmail.com',
            'is_staff': 1
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_invalid_email(self):
        """
        Test to verify that a post call with invalid email
        """
        user_data = {
            'username': 'test_user',
            'password': 'password',
            'password_check': 'password_check',
            'email': 'test_user@',
            'is_staff': 1
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
            'username': 'test_user',
            'password': 'test_user',
            'password_check': 'test_user',
            'email': 'test_user@gmail.com',
            'is_staff': 0
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            'username': 'test_user1',
            'email': 'test_user1@testuser.com',
            'password': 'test_user1',
            'password_check': 'test_user1',
            'is_staff': 0
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        user_data_2 = {
            'username': 'test_user1',
            'email': 'test_user1@testuser.com',
            'password': 'test_user1',
            'password_check': 'test_user1',
            'is_staff': 0
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class UserLoginTest(APITestCase):
    url = reverse('user:login')

    def setUp(self):
        self.user_data = {
            'username': 'user_login_test',
            'password': 'user_login_test',
            'password_check': 'user_login_test',
            'email': 'user_login_test@gmail.com',
            'is_staff': 1
        }
        self.user = self.client.post(UserRegistrationTest.url, self.user_data)
        self.assertEqual(status.HTTP_201_CREATED, self.user.status_code)

    def test_authentication_without_username(self):
        """
        Test to verify that a post call without username
        """
        response = self.client.post(self.url, {'password': self.user_data['password']})
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('The username is required.', response_json['msg'])

    def test_authentication_without_password(self):
        """
        Test to verify that a post call without password
        """
        response = self.client.post(self.url, {'username': 'user_login_test'})
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('The password is required.', response_json['msg'])

    def test_authentication_with_wrong_password(self):
        """
        Test to verify that a post call with wrong password
        """
        response = self.client.post(self.url, {'username': self.user_data['username'], 'password': 'password'})
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(400, response.status_code)
        self.assertEqual('The username and/or password is incorrect.', response_json['msg'])

    def test_authentication_with_valid_data(self):
        """
        Test to verify that a post call with valid data
        """
        response = self.client.post(self.url, self.user_data)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(200, response.status_code)
        self.assertTrue('token' in response_json)
        self.assertEqual(self.user_data['username'], response_json['user']['username'])


class UserLogoutTest(APITestCase):
    url = reverse('user:logout')

    def setUp(self):
        self.user_data = {
            'username': 'user_login_test',
            'password': 'user_login_test',
            'password_check': 'user_login_test',
            'email': 'user_login_test@gmail.com',
            'is_staff': 1
        }
        self.user = self.client.post(UserRegistrationTest.url, self.user_data)
        response = self.client.post(UserLoginTest.url, self.user_data)
        response_json = json.loads(response.content.decode('utf-8'))
        self.token = response_json['token']

    def test_logout_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token 123' + self.token)
        response = self.client.post(self.url)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual('토큰이 유효하지 않습니다.', response_json['detail'])

    def test_logout_with_valid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        response = self.client.post(self.url)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual('logout successfully.', response_json['msg'])
