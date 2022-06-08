import uuid
import unittest


class ServiceRequestTestCase(unittest.TestCase):
    def test_contacts_service(self):
        from ts.services.contacts_service import gen_random_contact

        print("\n\nTest contacts_service")
        print("Test gen_random_contact")
        print(gen_random_contact(str(uuid.uuid4()), str(uuid.uuid4())).__dict__)

    def test_auth_service(self):
        from ts.services.auth_service import login_user_request

        print("\n\nTest auth_service")
        print("Test login_user_request")
        request_id = str(uuid.uuid4())
        admin_bearer, user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )
        print(admin_bearer)
        print(user_id)
        self.assertIsInstance(admin_bearer, str)
        self.assertIsInstance(user_id, str)

    def test_station_service(self):
        from ts.services.auth_service import login_user_request
        from ts.services.station_service import (
            get_all_stations_request,
            add_one_new_station_request,
            update_one_station_request,
            delete_one_station_request,
        )

        print("\n\nTest station_service")
        print("Test get_all_stations_request")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )
        stations = get_all_stations_request(admin_user_id, admin_bearer)
        print(stations)
        self.assertIsInstance(stations, list)

        print("\nTest add_one_new_station_request")
        added_station = add_one_new_station_request(
            admin_bearer, admin_user_id, "Lugano", 5
        )
        print(added_station)
        self.assertIsInstance(added_station, dict)

        print("\nTest update_one_station_request")
        updated_station = update_one_station_request(
            admin_bearer, admin_user_id, "lugano", "New Lugano", 10
        )
        print(updated_station)
        self.assertIsInstance(updated_station, dict)

        print("\nTest delete_one_station_request")
        deleted_station = delete_one_station_request(
            admin_bearer, admin_user_id, "lugano", "New Lugano"
        )
        print(deleted_station)
        self.assertIsInstance(deleted_station, dict)


if __name__ == "__main__":
    unittest.main()
