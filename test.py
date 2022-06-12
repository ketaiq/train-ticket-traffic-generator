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


if __name__ == "__main__":
    unittest.main()
