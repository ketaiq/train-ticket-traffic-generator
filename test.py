import uuid
import unittest


class ServiceRequestTestCase(unittest.TestCase):
    @unittest.skip("skipping")
    def test_contacts_service(self):
        from ts.services.contacts_service import gen_random_contact

        def test_gen_random_contact():
            print("Test gen_random_contact")
            print(gen_random_contact(str(uuid.uuid4()), str(uuid.uuid4())).__dict__)

        print("\n\nTest contacts_service")
        test_gen_random_contact()

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
                    delete_one_station_request(
                        admin_bearer, admin_user_id, station["id"], station["name"]
                    )
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
            gen_random_route_from_original_stations,
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
            route = gen_random_route_from_original_stations()
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
