import uuid
import unittest


class ServiceRequestTestCase(unittest.TestCase):
    # @unittest.skip("skipping")
    def test_contacts_service(self):
        from ts.services.auth_service import login_user_request
        from ts.services.contacts_service import (
            gen_random_contact,
            get_all_contacts_request,
            add_one_contact_request,
            delete_one_contact_request,
            update_one_contact_request,
        )

        def test_gen_random_contact():
            print("Test gen_random_contact")
            print(gen_random_contact(str(uuid.uuid4()), str(uuid.uuid4())).__dict__)

        def test_get_all_contacts_request():
            print("Test get_all_contacts_request")
            contacts = get_all_contacts_request(request_id, admin_bearer)
            print(contacts[:10])
            self.assertIsInstance(contacts, list)

        def test_add_one_contact_request():
            print("Test add_one_contact_request")
            new_contact = gen_random_contact(
                None, "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f"
            )
            added_contact = add_one_contact_request(
                request_id, admin_bearer, new_contact
            )
            print(added_contact)

        def test_update_one_contact_request():
            print("Test update_one_contact_request")
            contacts = get_all_contacts_request(request_id, admin_bearer)
            contact = contacts[-1]
            new_contact = gen_random_contact(contact["id"], contact["accountId"])
            updated_contact = update_one_contact_request(
                request_id, admin_bearer, new_contact
            )
            self.assertEqual(updated_contact["id"], new_contact.id)
            self.assertEqual(updated_contact["accountId"], new_contact.user_id)
            self.assertEqual(updated_contact["name"], new_contact.name)
            self.assertEqual(updated_contact["documentType"], new_contact.document_type)
            self.assertEqual(
                updated_contact["documentNumber"], new_contact.document_number
            )
            self.assertEqual(updated_contact["phoneNumber"], new_contact.phone_number)

        def test_delete_one_contact_request():
            print("Test delete_one_contact_request")
            contacts = get_all_contacts_request(request_id, admin_bearer)
            contact_id = contacts[-1]["id"]
            deleted_contact_id = delete_one_contact_request(
                request_id, admin_bearer, contact_id
            )
            print(deleted_contact_id)
            self.assertEqual(deleted_contact_id, contact_id)

        def restore_original_contacts():
            print("Restore original contacts")
            contacts = get_all_contacts_request(request_id, admin_bearer)
            original_contacts = [
                {
                    "id": "b80f4344-eca8-455e-89c2-82f5f096ce9d",
                    "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
                    "name": "Contacts_One",
                    "documentType": 1,
                    "documentNumber": "DocumentNumber_One",
                    "phoneNumber": "ContactsPhoneNum_One",
                },
                {
                    "id": "c7f61d22-6514-4c81-9dd7-c444b0a42dc4",
                    "accountId": "4d2a46c7-71cb-4cf1-b5bb-b68406d9da6f",
                    "name": "Contacts_Two",
                    "documentType": 1,
                    "documentNumber": "DocumentNumber_Two",
                    "phoneNumber": "ContactsPhoneNum_Two",
                },
            ]
            for contact in contacts:
                if contact not in original_contacts:
                    deleted_contact_id = delete_one_contact_request(
                        request_id, admin_bearer, contact["id"]
                    )
                    self.assertEqual(deleted_contact_id, contact["id"])
                    print(f"Delete contact {deleted_contact_id}")
            print(get_all_contacts_request(request_id, admin_bearer))

        print("\n\nTest contacts_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )
        test_gen_random_contact()
        test_get_all_contacts_request()
        # test_add_one_contact_request()
        # test_update_one_contact_request()
        # test_delete_one_contact_request()
        # restore_original_contacts()

    @unittest.skip("skipping")
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

    @unittest.skip("skipping")
    def test_station_service(self):
        from ts.services.auth_service import login_user_request
        from ts.services.station_service import (
            get_all_stations_request,
            add_one_station_request,
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
            added_station = add_one_station_request(
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

        def restore_original_stations():
            print("Restore original stations")
            stations = get_all_stations_request(admin_user_id, admin_bearer)
            print(stations)
            original_stations = [
                {"id": "shanghai", "name": "Shang Hai", "stayTime": 10},
                {
                    "id": "shanghaihongqiao",
                    "name": "Shang Hai Hong Qiao",
                    "stayTime": 10,
                },
                {"id": "taiyuan", "name": "Tai Yuan", "stayTime": 5},
                {"id": "beijing", "name": "Bei Jing", "stayTime": 10},
                {"id": "nanjing", "name": "Nan Jing", "stayTime": 8},
                {"id": "shijiazhuang", "name": "Shi Jia Zhuang", "stayTime": 8},
                {"id": "xuzhou", "name": "Xu Zhou", "stayTime": 7},
                {"id": "jinan", "name": "Ji Nan", "stayTime": 5},
                {"id": "hangzhou", "name": "Hang Zhou", "stayTime": 9},
                {"id": "jiaxingnan", "name": "Jia Xing Nan", "stayTime": 2},
                {"id": "zhenjiang", "name": "Zhen Jiang", "stayTime": 2},
                {"id": "wuxi", "name": "Wu Xi", "stayTime": 3},
                {"id": "suzhou", "name": "Su Zhou", "stayTime": 3},
            ]
            for station in stations:
                if station not in original_stations:
                    deleted_station = delete_one_station_request(
                        admin_bearer, admin_user_id, station["id"], station["name"]
                    )
                    print(f"Delete station {deleted_station}")
            stations = get_all_stations_request(admin_user_id, admin_bearer)
            print(stations)

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
        restore_original_stations()

    @unittest.skip("skipping")
    def test_admin_route_service(self):
        from ts.services.auth_service import login_user_request
        from ts.services.admin_route_service import (
            get_routes_request,
            add_or_update_one_route_request,
            gen_random_route,
            delete_one_route_request,
            gen_updated_route,
            Route,
        )

        def test_get_routes():
            print("Test get_routes")
            routes = get_routes_request(admin_bearer, request_id)
            print(routes)
            self.assertIsInstance(routes, list)

        def test_add_one_route():
            print("Test add_one_route")
            new_route = add_or_update_one_route_request(
                admin_bearer,
                request_id,
                admin_user_id,
                "e18c9ae5-610b-4cda-a990-65081e64ec8d",
                ["Wu Xi", "Ji Nan", "Nan Jing"],
                [0, 395, 638],
            )
            print(new_route)
            self.assertIsInstance(new_route, dict)
            self.assertEqual(len(new_route["stations"]), len(new_route["distances"]))

        def test_update_one_route():
            print("Test update_one_route")
            updated_route = add_or_update_one_route_request(
                admin_bearer,
                request_id,
                admin_user_id,
                "e18c9ae5-610b-4cda-a990-65081e64ec8d",
                ["Schaffhausen", "Singen", "Konstanz"],
                [0, 100, 200],
            )
            print(updated_route)
            self.assertIsInstance(updated_route, dict)
            self.assertEqual(
                len(updated_route["stations"]), len(updated_route["distances"])
            )

        def test_gen_random_route():
            print("Test gen_random_route")
            route = gen_random_route()
            print(route.__dict__)
            self.assertIsInstance(route, Route)
            self.assertEqual(len(route.stations), len(route.distances))

        def test_delete_one_route():
            print("Test delete_one_route")
            deleted_route_id = delete_one_route_request(
                admin_bearer, request_id, "e18c9ae5-610b-4cda-a990-65081e64ec8d"
            )
            print(deleted_route_id)
            self.assertEqual(deleted_route_id, "e18c9ae5-610b-4cda-a990-65081e64ec8d")

        def test_gen_updated_route():
            print("Test gen_updated_route")
            original_route = Route(
                str(uuid.uuid4()),
                ["Schaffhausen", "Singen", "Konstanz"],
                [0, 100, 200],
            )
            original_stations = [
                {"id": "shanghai", "name": "Shang Hai", "stayTime": 10},
                {
                    "id": "shanghaihongqiao",
                    "name": "Shang Hai Hong Qiao",
                    "stayTime": 10,
                },
                {"id": "taiyuan", "name": "Tai Yuan", "stayTime": 5},
                {"id": "beijing", "name": "Bei Jing", "stayTime": 10},
                {"id": "nanjing", "name": "Nan Jing", "stayTime": 8},
                {"id": "shijiazhuang", "name": "Shi Jia Zhuang", "stayTime": 8},
                {"id": "xuzhou", "name": "Xu Zhou", "stayTime": 7},
                {"id": "jinan", "name": "Ji Nan", "stayTime": 5},
                {"id": "hangzhou", "name": "Hang Zhou", "stayTime": 9},
                {"id": "jiaxingnan", "name": "Jia Xing Nan", "stayTime": 2},
                {"id": "zhenjiang", "name": "Zhen Jiang", "stayTime": 2},
                {"id": "wuxi", "name": "Wu Xi", "stayTime": 3},
                {"id": "suzhou", "name": "Su Zhou", "stayTime": 3},
            ]
            original_stations = [station["name"] for station in original_stations]
            updated_route = gen_updated_route(original_route, original_stations)
            print(updated_route.__dict__)
            self.assertIsInstance(updated_route, Route)
            self.assertEqual(len(updated_route.stations), len(updated_route.distances))

        print("\n\nTest admin_route_service")
        request_id = str(uuid.uuid4())
        admin_bearer, admin_user_id = login_user_request(
            username="admin", password="222222", request_id=request_id
        )

        test_get_routes()
        test_gen_random_route()
        test_add_one_route()
        test_update_one_route()
        test_delete_one_route()
        test_gen_updated_route()


if __name__ == "__main__":
    unittest.main()
