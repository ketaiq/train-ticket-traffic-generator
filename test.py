import uuid
import unittest


class ServiceRequestTestCase(unittest.TestCase):
    @unittest.skip("skipping")
    def test_contacts_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_contacts_service import test_all

        print("\n\nTest contacts_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_all(request_id, admin_bearer, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_auth_service(self):
        from test.test_auth_service import test_all

        print("\n\nTest auth_service")
        test_all(self.assertIsInstance)

    @unittest.skip("skipping")
    def test_station_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_station_service import test_all

        print("\n\nTest station_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_all(
            admin_bearer,
            admin_user_id,
            self.assertIsInstance,
            self.assertEqual,
        )

    @unittest.skip("skipping")
    def test_admin_route_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_admin_route_service import test_all

        print("\n\nTest admin_route_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_all(
            admin_bearer,
            admin_user_id,
            request_id,
            self.assertIsInstance,
            self.assertEqual,
        )

    @unittest.skip("skipping")
    def test_admin_travel_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_admin_travel_service import test_all

        print("\n\nTest admin_travel_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_all(admin_bearer, request_id, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_train_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_train_service import test_all

        print("\n\nTest train_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_all(admin_bearer, request_id, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_admin_basic_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_admin_basic_service import test_all

        print("\n\nTest admin_basic_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_all(admin_bearer, request_id, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_food_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_food_service import test_all

        print("\n\nTest food_service")
        request_id = str(uuid.uuid4())
        bearer, user_id = login_user_request(
            username="fdse_microservice", password="111111", request_id=request_id
        )

        test_all(bearer, request_id, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_food_map_service(self):
        from test.test_food_map_service import test_all

        print("\n\nTest food_map_service")
        request_id = str(uuid.uuid4())

        test_all(request_id, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_preserve_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_preserve_service import test_all

        print("\n\nTest preserve_service")
        request_id = str(uuid.uuid4())
        bearer, user_id = login_user_request(
            username="fdse_microservice", password="111111", request_id=request_id
        )

        test_all(request_id, bearer, user_id, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_admin_user_service(self):
        from ts.services.auth_service import login_user_request
        from test.test_admin_user_service import test_all

        print("\n\nTest admin_user_service")
        request_id = str(uuid.uuid4())
        bearer, user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_all(request_id, bearer, self.assertIsInstance, self.assertEqual)

    @unittest.skip("skipping")
    def test_visit_page(self):
        from ts.services.auth_service import login_user_request
        from test.test_visit_page import test_all

        print("\n\nTest visit_page")
        request_id = str(uuid.uuid4())
        bearer, user_id = login_user_request(
            username="fdse_microservice", password="111111", request_id=request_id
        )

        test_all(request_id, bearer, self.assertIsInstance, self.assertEqual)


if __name__ == "__main__":
    unittest.main()
