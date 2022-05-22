# train-ticket-analysis

## 1 Dependency Inspection

### 1.1 Services Without Login

We can call service API without visiting pages. For example, we can call login service without getting login page.

#### Visit Pages

1. Home Page by `GET /index.html`
2. Login Page by `GET /client_login.html`

#### Call Service API

1. Search Ticket by `POST /api/v1/travelservice/trips/left`
2. Login by `POST /api/v1/users/login`

### 1.2 Services With Login

#### Visit Pages

1. Book Page by `GET /client_ticket_book.html`

#### Call Service API

1. Add User by `POST /api/v1/adminuserservice/users` only with admin user
2. Get Assurance by `GET /api/v1/assuranceservice/assurances/types`
3. Get Food Order by `GET /api/v1/foodservice/foods`
4. GET Contact Information by `GET /api/v1/contactservice/contacts/account`
5. Add Contact Information by `POST /api/v1/contactservice/contacts`
6. Reserve Ticket by `POST /api/v1/preserveservice/preserve` requires Contact ID
7. Select Order by `POST /api/v1/orderservice/order/refresh`
8. Pay Order by `POST /api/v1/inside_pay_service/inside_payment` requires Order ID
9. Cancel Order by `GET /api/v1/cancelservice/cancel` requires Order ID
10. Generate Reimbursement Voucher by `POST /getVoucher` requires Order ID
11. Query Consign Order by `GET /api/v1/consignservice/consigns/order` requires Order ID
12. Update Consign Order by `PUT /api/v1/consignservice/consigns` requires Order ID
