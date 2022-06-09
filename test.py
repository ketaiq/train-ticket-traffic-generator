import uuid
import unittest


class ServiceRequestTestCase(unittest.TestCase):
    def test_contacts_service(self):
        from ts.services.contacts_service import gen_random_contact

        def test_gen_random_contact():
            print("Test gen_random_contact")
            print(gen_random_contact(str(uuid.uuid4()), str(uuid.uuid4())).__dict__)

        print("\n\nTest contacts_service")
        test_gen_random_contact()

    def test_auth_service(self):
        from ts.services.auth_service import login_user_request

        def test_login_user_request():
            print("Test login_user_request")
            request_id = str(uuid.uuid4())
            admin_bearer, user_id = login_user_request(
                username="admin", password="222222", request_id=request_id
            )
            print(admin_bearer)
            print(user_id)
            self.assertIsInstance(admin_bearer, str)
            self.assertIsInstance(user_id, str)

        print("\n\nTest auth_service")
        test_login_user_request()

    def test_station_service(self):
        from ts.services.auth_service import login_user_request
        from ts.services.station_service import (
            get_all_stations_request,
            add_one_new_station_request,
            update_one_station_request,
            delete_one_station_request,
            gen_random_station,
        )

        def test_get_all_stations_request():
            print("Test get_all_stations_request")
            stations = get_all_stations_request(admin_user_id, admin_bearer)
            print(stations)
            self.assertIsInstance(stations, list)

        def test_add_one_new_station_request():
            print("Test add_one_new_station_request")
            added_station = add_one_new_station_request(
                admin_bearer, admin_user_id, "lugano", "Lugano", 5
            )
            print(added_station)
            self.assertIsInstance(added_station, dict)

        def test_update_one_station_request():
            print("Test update_one_station_request")
            updated_station = update_one_station_request(
                admin_bearer, admin_user_id, "lugano", "New Lugano", 10
            )
            print(updated_station)
            self.assertIsInstance(updated_station, dict)

        def test_delete_one_station_request():
            print("Test delete_one_station_request")
            deleted_station = delete_one_station_request(
                admin_bearer, admin_user_id, "lugano", "New Lugano"
            )
            print(deleted_station)
            self.assertIsInstance(deleted_station, dict)

        def test_gen_random_station():
            print("Test gen_random_station")
            print(gen_random_station().__dict__)

        print("\n\nTest station_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_get_all_stations_request()
        test_add_one_new_station_request()
        test_update_one_station_request()
        test_delete_one_station_request()
        test_gen_random_station()


if __name__ == "__main__":
    unittest.main()
