# train-ticket-analysis

## 1 Dependency Inspection

### 1.1 Services Without Login

We can call service API without visiting pages. For example, we can call login service without getting login page.

#### (1) Visit Pages

1. Home Page by `GET /index.html`
2. Login Page by `GET /client_login.html`

#### (2) Call Service API

1. Search Ticket by `POST /api/v1/travelservice/trips/left` provided by **ts-travel-service** microservice
2. Login by `POST /api/v1/users/login` provided by **ts-auth-service** microservice

### 1.2 Services With Login

#### (1) Visit Pages

1. Book Page by `GET /client_ticket_book.html`

#### (2) Call Service API

1. Add User by `POST /api/v1/adminuserservice/users` only with login of *admin user* provided by **ts-admin-user-service** microservice
2. Get Assurance by `GET /api/v1/assuranceservice/assurances/types` provided by **ts-assurance-service** microservice
3. Get Food Order by `GET /api/v1/foodservice/foods` provided by **ts-food-service** microservice
4. GET Contact Information Of An Account by `GET /api/v1/contactservice/contacts/account` provided by **ts-contacts-service** microservice
5. Add Contact Information by `POST /api/v1/contactservice/contacts` provided by **ts-contacts-service** microservice
6. Reserve Ticket by `POST /api/v1/preserveservice/preserve` requires *Contact ID* provided by **ts-preserve-service** microservice
7. Select Order by `POST /api/v1/orderservice/order/refresh` provided by **ts-order-service** microservice
8. Pay Order by `POST /api/v1/inside_pay_service/inside_payment` requires *Order ID* provided by **ts-inside-payment-service** microservice
9. Cancel Order by `GET /api/v1/cancelservice/cancel` requires *Order ID* provided by **ts-cancel-service** microservice
10. Generate Reimbursement Voucher by `POST /getVoucher` requires *Order ID* provided by **ts-voucher-service** microservice
11. Add Consign Order by `POST /api/v1/consignservice/consigns/order` requires *Order ID* provided by **ts-consign-service** microservice
12. Query Consign Order by `GET /api/v1/consignservice/consigns/order` requires *Order ID* provided by **ts-consign-service** microservice
13. Update Consign Order by `PUT /api/v1/consignservice/consigns` requires *Order ID* provided by **ts-consign-service** microservice
