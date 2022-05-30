# train-ticket-analysis

## Environment Configuration

1. Install all required packages by running `conda create -n train-ticket-test --channel=conda-forge python locust`.
2. Activate the conda environment by running `conda activate train-ticket-test`.

## 1 Dependency Inspection

### 1.1 Services Without Login

We can call service API without visiting pages. For example, we can call login service without getting login page.

| Operation        | Method | API                                | Service               |
| ---------------- | ------ | ---------------------------------- | --------------------- |
| Visit Home Page  | GET    | `/index.html`                      | None                  |
| Visit Login Page | GET    | `/client_login.html`               | None                  |
| Search Ticket    | POST   | `/api/v1/travelservice/trips/left` | **ts-travel-service** |
| Login            | POST   | `/api/v1/users/login`              | **ts-auth-service**   |

### 1.2 Services With Login

| Operation                             | Method | API                                         | Service                       | Return          | Require                 | Dependency                                   |
| ------------------------------------- | ------ | ------------------------------------------- | ----------------------------- | --------------- | ----------------------- | -------------------------------------------- |
| Visit Book Page                       | GET    | `/client_ticket_book.html`                  | None                          | None            | Login Token             | **ts-auth-service**                          |
| Add User                              | POST   | `/api/v1/adminuserservice/users`            | **ts-admin-user-service**     | None            | **Admin** Login Token   | **ts-auth-service**                          |
| Get Assurance                         | GET    | `/api/v1/assuranceservice/assurances/types` | **ts-assurance-service**      | Assurance Types | Login Token             | **ts-auth-service**                          |
| Get Food Menu                         | GET    | `/api/v1/foodservice/foods`                 | **ts-food-service**           | Food Menu       | Login Token             | **ts-auth-service**                          |
| GET Contact Information Of An Account | GET    | `/api/v1/contactservice/contacts/account`   | **ts-contacts-service**       | Contact ID      | Login Token             | **ts-auth-service**                          |
| Add Contact Information               | POST   | `/api/v1/contactservice/contacts`           | **ts-contacts-service**       | Contact ID      | Login Token             | **ts-auth-service**                          |
| Reserve Ticket                        | POST   | `/api/v1/preserveservice/preserve`          | **ts-preserve-service**       | None            | Login Token, Contact ID | **ts-auth-service**, **ts-contacts-service** |
| Get Ticket Order                      | POST   | `/api/v1/orderservice/order/refresh`        | **ts-order-service**          | Order ID        | Login Token             | **ts-auth-service**, **ts-preserve-service** |
| Pay Ticket Order                      | POST   | `/api/v1/inside_pay_service/inside_payment` | **ts-inside-payment-service** | None            | Login Token, Order ID   | **ts-auth-service**, **ts-order-service**    |
| Cancel Order                          | GET    | `/api/v1/cancelservice/cancel`              | **ts-cancel-service**         | None            | Login, Order ID         | **ts-auth-service**, **ts-order-service**    |
| Generate Voucher                      | POST   | `/getVoucher`                               | **ts-voucher-service**        | Voucher Info    | Login, Order ID         | **ts-auth-service**, **ts-order-service**    |
| Add Consign Order                     | POST   | `/api/v1/consignservice/consigns/order`     | **ts-consign-service**        | Consign Info    | Login, Order ID         | **ts-auth-service**, **ts-order-service**    |
| Get Consign Order                     | GET    | `/api/v1/consignservice/consigns/order`     | **ts-consign-service**        | Consign Info    | Login, Order ID         | **ts-auth-service**, **ts-order-service**    |
| Update Consign Order                  | PUT    | `/api/v1/consignservice/consigns`           | **ts-consign-service**        | Consign Info    | Login, Order ID         | **ts-auth-service**, **ts-order-service**    |