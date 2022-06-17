import requests
import uuid
from json import JSONDecodeError
from pymongo import MongoClient
import random
from ts.util import gen_random_phone_number

FOOD_MAP_SERVICE_URL = "http://35.222.140.129:18855/api/v1/foodmapservice"


def get_all_food_stores_request(
    request_id: str,
) -> list:
    operation = "get food stores"
    r = requests.get(
        url=FOOD_MAP_SERVICE_URL + "/" + "foodstores",
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            food_stores = r.json()["data"]
            return food_stores
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def get_train_food_in_one_trip_request(request_id: str, trip_id: str) -> list:
    operation = "get train food in one trip"
    r = requests.get(
        url=FOOD_MAP_SERVICE_URL + "/" + "trainfoods" + "/" + trip_id,
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    try:
        key = "msg"
        msg = r.json()["msg"]
        if msg != "Success":
            print(
                f"request {request_id} tries to {operation} but gets wrong response {msg}"
            )
        else:
            key = "data"
            train_food = r.json()["data"]
            return train_food
    except JSONDecodeError:
        print("Response could not be decoded as JSON")
    except KeyError:
        print(f"Response did not contain expected key '{key}'")


def _gen_random_food_list(food_choices) -> list:
    food_names = random.sample(food_choices, k=random.randint(1, len(food_choices)))
    return [
        {"foodName": name, "price": round(random.uniform(5, 20), 1)}
        for name in food_names
    ]


def _gen_random_train_food_record(food_choices, travel) -> dict:
    return {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.TrainFood",
        "tripId": travel.trip_id,
        "foodList": _gen_random_food_list(food_choices),
    }


def _gen_random_store_record(food_choices, store_choices, station) -> dict:
    business_start_time_choices = ["06:00", "07:00", "08:00", "09:00", "10:00"]
    business_end_time_choices = ["18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    business_time = (
        random.choice(business_start_time_choices)
        + "-"
        + random.choice(business_end_time_choices)
    )
    return {
        "_id": str(uuid.uuid4()),
        "_class": "food.entity.FoodStore",
        "stationId": station.id,
        "storeName": random.choice(store_choices),
        "telephone": gen_random_phone_number(),
        "businessTime": business_time,
        "deliveryFee": round(random.uniform(5, 15), 1),
        "foodList": _gen_random_food_list(food_choices),
    }


def add_food(all_travels, all_stations):
    client = MongoClient("mongodb://35.188.139.242:27017/")
    db = client["ts"]
    trainfoods = db["trainfoods"]
    trainfoods.delete_many({})
    stores = db["stores"]
    stores.delete_many({})
    print("Food is clear")
    for train_food in trainfoods.find():
        print(train_food)
    for store in stores.find():
        print(store)
    food_choices = [
        "Pork Chop with rice",
        "Egg Soup",
        "Beef with rice",
        "Soup",
        "Pork pickled mustard green noodles",
        "Seafood noodles",
        "Glutinous rice",
        "Dumplings",
        "Spring rolls",
        "Vegetable soup",
        "Rice and vegetable roll",
        "Spicy hot noodles",
        "Soup",
        "Oily bean curd",
        "Hamburger",
        "Cola",
        "Chicken",
        "Rice",
        "Chicken Soup",
        "Big Burger",
        "Bone Soup",
        "Big Burger",
        "Bone Soup",
        "Big Mac",
        "McChicken",
        "Big Burger",
        "Bone Soup",
        "French Fries",
        "Vegetable Seafood Soup",
        "Hot Chocolate",
        "Pineapple Pie",
        "Karubi Beef",
        "Low Fat Yogurt Blackberry",
    ]
    store_choices = [
        "KFC",
        "Good Taste",
        "Burger King",
        "Pizza Hut",
        "McDonald's",
        "Roman Holiday",
        "Perfect",
        "Delicious",
        "16 Handles",
        "Tequila Mockingbird",
        "Of Rice & Men",
        "Planet of the Crepes",
        "The Codfather",
        "The Breakfast Club",
        "Custard's Last Stand",
        "Happy Grillmore",
        "Café Jack",
        "Life of Pie",
        "Filled of Dreams",
        "Lord of the Wings",
        "Eat Pray Love",
        "Frying Nemo",
        "Grillenium Falcon",
        "Pita Pan",
        "Earth, Wind and Flour",
        "Wok This Way",
        "Gochew Grill",
    ]
    all_train_food_records = [
        _gen_random_train_food_record(food_choices, travel) for travel in all_travels
    ]
    all_store_records = [
        _gen_random_store_record(food_choices, store_choices, station)
        for station in all_stations
    ]
    trainfoods.insert_many(all_train_food_records)
    stores.insert_many(all_store_records)

    for train_food in trainfoods.find():
        print(train_food)
    for store in stores.find():
        print(store)
