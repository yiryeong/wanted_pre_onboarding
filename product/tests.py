import json
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.tests import UserRegistrationTest, UserLoginTest, UserLogoutTest


class ProductCreateAPITest(APITestCase):
    url = reverse('product:list')
    signup_url = UserRegistrationTest.url
    login_url = UserLoginTest.url
    logout_url = UserLogoutTest.url

    staff_user = {
        'username': 'test_staff',
        'password': 'test_staff',
        'password_check': 'test_staff',
        'email': 'test_staff@gmail.com',
        'is_staff': 1
    }

    normal_user = {
        'username': 'test_normal',
        'password': 'test_normal',
        'password_check': 'test_normal',
        'email': 'test_normal@gmail.com',
        'is_staff': 0
    }

    product = {
        "title": "test_title",
        "description": "test_title",
        "target_amount": 35000,
        "one_time_funding": 10,
        "end_date": "2023-08-27 10:00:00"
    }

    product_invalid = {
        "title": "test_title",
        "description": "test_title",
        "target_amount": 35000,
        "one_time_funding": 10
    }

    def setUp(self) -> None:
        normal_user_signup = self.client.post(self.signup_url, self.normal_user)
        self.assertEqual(status.HTTP_201_CREATED, normal_user_signup.status_code)
        staff_user_signup = self.client.post(self.signup_url, self.staff_user)
        self.assertEqual(status.HTTP_201_CREATED, staff_user_signup.status_code)

    def test_product_create_with_normal_user(self):
        # 로그인
        user = self.client.post(self.login_url, self.normal_user)
        user_json = json.loads(user.content.decode('utf-8'))
        self.assertEqual(status.HTTP_200_OK, user.status_code)
        self.assertTrue('token' in user_json)
        self.assertEqual(self.normal_user['username'], user_json['user']['username'])
        token = user_json['token']
        # 일반사용자 상품 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.url, self.product)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.assertEqual('이 작업을 수행할 권한(permission)이 없습니다.', response_json['detail'])

    def test_product_create_with_staff_user(self):
        # 로그인
        user = self.client.post(self.login_url, self.staff_user)
        user_json = json.loads(user.content.decode('utf-8'))
        self.assertEqual(status.HTTP_200_OK, user.status_code)
        self.assertTrue('token' in user_json)
        self.assertEqual(self.staff_user['username'], user_json['user']['username'])
        token = user_json['token']
        # 스탭 상품 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.url, self.product)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual('create product successful.', response_json['msg'])

    def test_product_create_with_invalid_data(self):
        # 로그인
        user = self.client.post(self.login_url, self.staff_user)
        user_json = json.loads(user.content.decode('utf-8'))
        self.assertEqual(status.HTTP_200_OK, user.status_code)
        self.assertTrue('token' in user_json)
        self.assertEqual(self.staff_user['username'], user_json['user']['username'])
        token = user_json['token']
        # 스탭 상품 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.post(self.url, self.product_invalid)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class ProductListApiTest(APITestCase):
    url = ProductCreateAPITest.url

    product1 = {
        "title": "test_title1",
        "description": "test_title1",
        "target_amount": 50000,
        "one_time_funding": 20,
        "end_date": "2022-05-15 10:00:00"
    }

    product2 = {
        "title": "test_title11",
        "description": "test_title11",
        "target_amount": 30000,
        "one_time_funding": 500,
        "end_date": "2022-07-15 10:00:00"
    }

    def setUp(self) -> None:
        user_signup = self.client.post(ProductCreateAPITest.signup_url, ProductCreateAPITest.staff_user)
        self.assertEqual(status.HTTP_201_CREATED, user_signup.status_code)
        # 로그인
        user = self.client.post(ProductCreateAPITest.login_url, ProductCreateAPITest.staff_user)
        user_json = json.loads(user.content.decode('utf-8'))
        self.token1 = user_json['token']
        # 상품1 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        self.created_product = self.client.post(ProductCreateAPITest.url, ProductCreateAPITest.product)
        self.created_product_json = json.loads(self.created_product.content.decode('utf-8'))
        # 상품2 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        self.client.post(ProductCreateAPITest.url, self.product1)
        # 상품3 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        self.client.post(ProductCreateAPITest.url, self.product2)

        user_signup = self.client.post(ProductCreateAPITest.signup_url, ProductCreateAPITest.normal_user)
        # 로그인
        user = self.client.post(ProductCreateAPITest.login_url, ProductCreateAPITest.normal_user)
        user_json = json.loads(user.content.decode('utf-8'))
        self.token2 = user_json['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)

    def test_product_list_get_all_data(self):
        response = self.client.get(self.url)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(3, len(response_json['data']))

    def test_product_list_search_title_no_data(self):
        response = self.client.get(self.url, {"search": 'no_title'})
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response_json['data'])

    def test_product_list_search_title(self):
        response = self.client.get(self.url, {"search": 'title'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertTrue('title' in response_json['data'][0]['title'])

    def test_product_list_sorting_with_create_date(self):
        response = self.client.get(self.url, {"order_by": 'create_date'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(ProductCreateAPITest.product['title'], response_json['data'][0]['title'])
        self.assertEqual(self.product1['title'], response_json['data'][1]['title'])
        self.assertEqual(self.product2['title'], response_json['data'][2]['title'])

    def test_product_list_sorting_with_total_funding(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)
        self.client.post(reverse('funding:list'), {'p': self.created_product_json['data']['id']})
        response = self.client.get(self.url, {"order_by": 'total_funding'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertTrue(response_json['data'][2]['total_funding'] >= response_json['data'][1]['total_funding'] >= response_json['data'][0]['total_funding'])


class ProductRetrieveAPITest(APITestCase):
    user_data = {
        'username': 'user_login_test',
        'password': 'user_login_test',
        'password_check': 'user_login_test',
        'email': 'user_login_test@gmail.com',
        'is_staff': 1
    }

    def setUp(self) -> None:
        self.user = self.client.post(UserRegistrationTest.url, self.user_data)
        user_response = self.client.post(UserLoginTest.url, self.user_data)
        user_response_json = json.loads(user_response.content.decode('utf-8'))
        self.token = user_response_json['token']
        # 상품 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        product_response = self.client.post(ProductCreateAPITest.url, ProductCreateAPITest.product)
        self.product_response_json = json.loads(product_response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_201_CREATED, product_response.status_code)
        self.assertEqual('create product successful.', self.product_response_json['msg'])

    def test_product_retrieve_non_data(self):
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']+1})
        response = self.client.get(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_product_retrieve_created_data(self):
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']})
        response = self.client.get(url)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(ProductCreateAPITest.product['title'], response_json['title'])


class ProductUpdateAPITest(APITestCase):

    change_target_amount_product = {
        "title": "test_title",
        "description": "test_title",
        "target_amount": 350000,
        "one_time_funding": 10,
        "end_date": "2023-08-27 10:00:00"
    }

    success_product = {
        "title": "test_title_update",
        "description": "test_title_update",
        "target_amount": 35000,
        "one_time_funding": 10,
        "end_date": "2023-08-27 10:00:00"
    }

    staff_user = {
        'username': 'test_staff_1',
        'password': 'test_staff_1',
        'password_check': 'test_staff_1',
        'email': 'test_staff_1@gmail.com',
        'is_staff': 1
    }

    def setUp(self) -> None:
        # user1
        self.user1 = self.client.post(UserRegistrationTest.url, ProductCreateAPITest.staff_user)
        user1_response = self.client.post(UserLoginTest.url, ProductCreateAPITest.staff_user)
        user1_response_json = json.loads(user1_response.content.decode('utf-8'))
        self.token1 = user1_response_json['token']
        # user2
        self.user2 = self.client.post(UserRegistrationTest.url, self.staff_user)
        user2_response = self.client.post(UserLoginTest.url, self.staff_user)
        user2_response_json = json.loads(user2_response.content.decode('utf-8'))
        self.token2 = user2_response_json['token']
        # 상품 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        product_response = self.client.post(ProductCreateAPITest.url, ProductCreateAPITest.product)
        self.product_response_json = json.loads(product_response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_201_CREATED, product_response.status_code)
        self.assertEqual('create product successful.', self.product_response_json['msg'])

    def test_update_no_created_product(self):
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']+1})
        response = self.client.put(url, ProductCreateAPITest.product)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_update_exist_product_with_change_target_amount(self):
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']})
        response = self.client.put(url, self.change_target_amount_product)
        self.assertEqual(status.HTTP_409_CONFLICT, response.status_code)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual("target_amount field can't be modified.", response_json['msg'])

    def test_update_exist_product_successful(self):
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']})
        response = self.client.put(url, self.success_product)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual(self.success_product['title'], response_json['data']['title'])

    def test_update_not_my_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)
        # 본인이 등록하지 않은 상품이 삭제
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']})
        response = self.client.put(url, self.success_product)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual("You do not have permission to modify this product.", response_json['msg'])


class ProductDeleteAPITest(APITestCase):

    def setUp(self) -> None:
        # user1
        self.user1 = self.client.post(UserRegistrationTest.url, ProductCreateAPITest.staff_user)
        user1_response = self.client.post(UserLoginTest.url, ProductCreateAPITest.staff_user)
        user1_response_json = json.loads(user1_response.content.decode('utf-8'))
        self.token1 = user1_response_json['token']
        # user2
        self.user2 = self.client.post(UserRegistrationTest.url, ProductUpdateAPITest.staff_user)
        user2_response = self.client.post(UserLoginTest.url, ProductUpdateAPITest.staff_user)
        user2_response_json = json.loads(user2_response.content.decode('utf-8'))
        self.token2 = user2_response_json['token']
        # 상품 등록
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1)
        product_response = self.client.post(ProductCreateAPITest.url, ProductCreateAPITest.product)
        self.product_response_json = json.loads(product_response.content.decode('utf-8'))
        self.assertEqual(status.HTTP_201_CREATED, product_response.status_code)
        self.assertEqual('create product successful.', self.product_response_json['msg'])

    def test_delete_no_product(self):
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']+1})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_product_successful(self):
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_delete_not_my_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2)
        # 본인이 등록하지 않은 상품이 삭제
        url = reverse('product:detail', kwargs={"pk": self.product_response_json['data']['id']})
        response = self.client.delete(url)
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        response_json = json.loads(response.content.decode('utf-8'))
        self.assertEqual("You do not have permission to delete this product.", response_json['msg'])
