# train-ticket-analysis

Run `locust` to start sending requests.

## Environment Configuration

1. Install all required packages by running `conda create -n train-ticket-test --channel=conda-forge python locust`.
2. Activate the conda environment by running `conda activate train-ticket-test`.

## Dependency Inspection

We can call service API without visiting pages. For example, we can call login service without getting login page.

### 1. visit pages

| Operation        | Method | API                        | Return     | Require     | Dependency          |
| ---------------- | ------ | -------------------------- | ---------- | ----------- | ------------------- |
| Visit Home Page  | GET    | `/index.html`              | Home Page  | None        | None                |
| Visit Login Page | GET    | `/client_login.html`       | Login Page | None        | None                |
| Visit Book Page  | GET    | `/client_ticket_book.html` | Book Page  | Login Token | **ts-auth-service** |


### 2. ts-travel-service

| Operation       | Method   | API                                | Return                | Require |
| --------------- | -------- | ---------------------------------- | --------------------- | ------- |
| Search Ticket   | POST     | `/api/v1/travelservice/trips/left` | Ticket Info           | None    |
| ~~Create Trip~~ | ~~POST~~ | ~~`/api/v1/travelservice/trips`~~  | Service Not Available |
| ~~Update Trip~~ | ~~PUT~~  | ~~`/api/v1/travelservice/trips`~~  | Service Not Available |
| ~~Get Trip~~    | ~~GET~~  | ~~`/api/v1/travelservice/trips`~~  | Service Not Available |

### 3. ts-auth-service

| Operation | Method | API                   | Return      | Require |
| --------- | ------ | --------------------- | ----------- | ------- |
| Login     | POST   | `/api/v1/users/login` | Login Token | None    |

### 4. ts-admin-user-service

| Operation | Method | API                              | Return | Require               | Dependency          |
| --------- | ------ | -------------------------------- | ------ | --------------------- | ------------------- |
| Add User  | POST   | `/api/v1/adminuserservice/users` | None   | **Admin** Login Token | **ts-auth-service** |

### 5. ts-assurance-service

| Operation     | Method | API                                         | Return          | Require     | Dependency          |
| ------------- | ------ | ------------------------------------------- | --------------- | ----------- | ------------------- |
| Get Assurance | GET    | `/api/v1/assuranceservice/assurances/types` | Assurance Types | Login Token | **ts-auth-service** |

### 6. ts-food-service

| Operation     | Method | API                         | Return    | Require     | Dependency          |
| ------------- | ------ | --------------------------- | --------- | ----------- | ------------------- |
| Get Food Menu | GET    | `/api/v1/foodservice/foods` | Food Menu | Login Token | **ts-auth-service** |


### 7. ts-contacts-servic

| Operation                             | Method | API                                       | Return                      | Require     | Dependency          |
| ------------------------------------- | ------ | ----------------------------------------- | --------------------------- | ----------- | ------------------- |
| GET Contact Information Of An Account | GET    | `/api/v1/contactservice/contacts/account` | Contact ID                  | Login Token | **ts-auth-service** |
| Add Contact Information               | POST   | `/api/v1/contactservice/contacts`         | Contact ID                  | Login Token | **ts-auth-service** |
| Update Contact Information            | PUT    | `api/v1/contactservice/contacts`          | Deleted Contact Information | Login Token | **ts-auth-service** |

### 8. ts-preserve-service

| Operation      | Method | API                                | Return | Require                 | Dependency                                   |
| -------------- | ------ | ---------------------------------- | ------ | ----------------------- | -------------------------------------------- |
| Reserve Ticket | POST   | `/api/v1/preserveservice/preserve` | None   | Login Token, Contact ID | **ts-auth-service**, **ts-contacts-service** |

### 9. ts-order-service

| Operation        | Method | API                                  | Return   | Require     | Dependency                                   |
| ---------------- | ------ | ------------------------------------ | -------- | ----------- | -------------------------------------------- |
| Get Ticket Order | POST   | `/api/v1/orderservice/order/refresh` | Order ID | Login Token | **ts-auth-service**, **ts-preserve-service** |

### 10. ts-inside-payment-service

| Operation        | Method | API                                         | Return | Require               | Dependency                                |
| ---------------- | ------ | ------------------------------------------- | ------ | --------------------- | ----------------------------------------- |
| Pay Ticket Order | POST   | `/api/v1/inside_pay_service/inside_payment` | None   | Login Token, Order ID | **ts-auth-service**, **ts-order-service** |

### 11. ts-cancel-service

| Operation        | Method | API                                     | Return         | Require               | Dependency                                |
| ---------------- | ------ | --------------------------------------- | -------------- | --------------------- | ----------------------------------------- |
| Cancel Order     | GET    | `/api/v1/cancelservice/cancel`          | None           | Login Token, Order ID | **ts-auth-service**, **ts-order-service** |
| Calculate Refund | GET    | `/api/v1/cancelservice/cancel/refound/` | Refound Amount | Login Token, Order ID | **ts-auth-service**, **ts-order-service** |

### 12. ts-voucher-service

| Operation        | Method | API           | Return       | Require               | Dependency                                |
| ---------------- | ------ | ------------- | ------------ | --------------------- | ----------------------------------------- |
| Generate Voucher | POST   | `/getVoucher` | Voucher Info | Login Token, Order ID | **ts-auth-service**, **ts-order-service** |

### 13. ts-consign-service

| Operation            | Method | API                                     | Return       | Require               | Dependency                                |
| -------------------- | ------ | --------------------------------------- | ------------ | --------------------- | ----------------------------------------- |
| Add Consign Order    | POST   | `/api/v1/consignservice/consigns/order` | Consign Info | Login Token, Order ID | **ts-auth-service**, **ts-order-service** |
| Get Consign Order    | GET    | `/api/v1/consignservice/consigns/order` | Consign Info | Login Token, Order ID | **ts-auth-service**, **ts-order-service** |
| Update Consign Order | PUT    | `/api/v1/consignservice/consigns`       | Consign Info | Login Token, Order ID | **ts-auth-service**, **ts-order-service** |

### 14. ts-travel-plan-service

| Operation                         | Method   | API                                                      | Return                 | Require | Dependency |
| --------------------------------- | -------- | -------------------------------------------------------- | ---------------------- | ------- | ---------- |
| Get cheapest travel plans         | POST     | `/api/v1/travelplanservice/travelPlan/cheapest`          | Cheapest Plans         | None    | None       |
| Get quickest travel plans         | POST     | `/api/v1/travelplanservice/travelPlan/quickest`          | Quickest Plans         | None    | None       |
| Get minimum stations travel plans | POST     | `/api/v1/travelplanservice/travelPlan/minStation`        | Minimum Stations Plans | None    | None       |
| ~~Get transfer search result~~    | ~~POST~~ | ~~`api/v1/travelplanservice/travelPlan/transferResult`~~ | Service Not Available  |

### 15. ts-station-service

| Operation            | Method | API                               | Return         | Require               | Dependency          |
| -------------------- | ------ | --------------------------------- | -------------- | --------------------- | ------------------- |
| Get train stations   | GET    | `/api/v1/stationservice/stations` | Train Stations | **Admin** Login Token | **ts-auth-service** |
| Add train station    | POST   | `/api/v1/stationservice/stations` | Train Station  | **Admin** Login Token | **ts-auth-service** |
| Update train station | PUT    | `/api/v1/stationservice/stations` | Train Station  | **Admin** Login Token | **ts-auth-service** |
| Delete train station | DELETE | `/api/v1/stationservice/stations` | Train Station  | **Admin** Login Token | **ts-auth-service** |

### 16. ts-admin-route-service

| Operation        | Method | API                                              | Return | Require               | Dependency                                |
| ---------------- | ------ | ------------------------------------------------ | ------ | --------------------- | ----------------------------------------- |
| Get routes       | GET    | `/api/v1/adminrouteservice/adminroute`           | Routes | **Admin** Login Token | **ts-auth-service**, **ts-route-service** |
| Add one route    | POST   | `/api/v1/adminrouteservice/adminroute`           | Routes | **Admin** Login Token | **ts-auth-service**, **ts-route-service** |
| Delete one route | DELETE | `/api/v1/adminrouteservice/adminroute/{routeId}` | Routes | **Admin** Login Token | **ts-auth-service**, **ts-route-service** |

### 17. ts-admin-travel-service

| Operation              | Method | API                                      | Return  | Require               | Dependency                                 |
| ---------------------- | ------ | ---------------------------------------- | ------- | --------------------- | ------------------------------------------ |
| Get travel information | GET    | `/api/v1/admintravelservice/admintravel` | Travels | **Admin** Login Token | **ts-auth-service**, **ts-travel-service** |
| Add one travel         | POST   | `/api/v1/admintravelservice/admintravel` | None    | **Admin** Login Token | **ts-auth-service**, **ts-travel-service** |