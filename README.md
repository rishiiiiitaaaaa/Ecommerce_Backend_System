**E-commerce Backend API**
A robust FastAPI-based e-commerce backend system with comprehensive features including authentication, product management, shopping cart, and order processing.

**Features**
**🔐 Authentication & User Management**
•	User signup/signin with JWT tokens
•	Role-based access control (Admin/User)
•	Password reset functionality with email integration
•	Secure password hashing with bcrypt

**📦 Product Management**
•	Admin Features: CRUD operations for products
•	Public Features: Product listing, search, filtering, and detail views
•	Category-based filtering and price range filtering

**🛒 Shopping Cart**
•	Add/remove/update cart items
•	Real-time stock validation
•	Cart persistence per user
•	Quantity & Cart management

**💳 Checkout & Orders**
•	Dummy payment processing
•	Order creation with detailed line items
•	Stock management during checkout
•	Order history and detailed order views

**🛡️ Security & Best Practices**
•	JWT-based authentication
•	Input validation with Pydantic
•	Comprehensive error handling
•	Request/response logging
•	Email uniqueness and validation

**Tech Stack**
•	Framework: FastAPI
•	Database: PostgreSQL with SQLAlchemy ORM
•	Authentication: JWT tokens with PyJWT
•	Validation: Pydantic schemas
•	Password Hashing: bcrypt via passlib
•	Email: SMTP integration for password reset

**Installation & Setup**
Prerequisites
•	Python
•	PostgreSQL database

1. Clone and Setup Environment
```bash
Create project directory
mkdir ecommerce-backend cd ecommerce-backend
Create virtual environment
python -m venv venv source venv/bin/activate # On Windows: venv\Scripts\activate
Install dependencies
pip install -r requirements.txt ```

2. Database Setup
```bash
Create PostgreSQL database
createdb ecommerce_db
Update DATABASE_URL in .env file
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db ```

3. Environment Configuration
Create a .env file in the root directory:
```env 
DATABASE_URL=postgresql://username:password@localhost:5432/ecommerce_db SECRET_KEY=your-super-secret-jwt-key 
SMTP_USERNAME=your-email@gmail.com 
SMTP_PASSWORD=your-app-password ```

4. Run the Application
```bash python -m uvicorn app.main:app --reload ```
The API will be available at:
•	API: http://127.0.0.1:8000
•	Documentation: http://127.0.0.1:8000/docs

API Endpoints:
Authentication
•	POST /auth/signup - User registration
•	POST /auth/signin - User login
•	POST /auth/forgot-password - Request password reset
•	POST /auth/reset-password - Reset password with token

Admin Product Management
•	POST /admin/products - Create product (Admin only)
•	GET /admin/products - List all products with pagination (Admin only)
•	GET /admin/products/{id} - Get product details (Admin only)
•	PUT /admin/products/{id} - Update product (Admin only)
•	DELETE /admin/products/{id} - Delete product (Admin only)
Public Product APIs (can be accessed by both)
•	GET /products - List products with filters and pagination
•	GET /products/search - Search products by keyword
•	GET /products/{id} - Get product details

Cart Management
•	POST /cart - Add item to cart (User only)
•	GET /cart - View cart (User only)
•	PUT /cart/{product_id} - Update cart item quantity (User only)
•	DELETE /cart/{product_id} - Remove item from cart (User only)
Checkout & Orders
•	POST /checkout - Process checkout (User only)
•	GET /orders - Get order history (User only)
•	GET /orders/{order_id} - Get order details (User only)

Testing
Manual Testing with Postman and Swagger
1.	Import the API endpoints from the OpenAPI documentation at /docs
2.	Sign in to get JWT tokens
3.	Use the access_token in the Authorization header: Bearer <token>
4.	Test all endpoints according to the role-based access control

Other checkpoints covered :
•	Stock management 
•	Empty cart should not be checkout
•	Quantity should always range between 1 to stock available
  	  ( i.e only positive values are allowed)
•	Admin can’t delete the product for which order is  been placed 
•	Unique , Valid mail id required

Error Handling
All errors follow a consistent format:
```json { "error": true, "message": "Error description", "code": 400 } ```

Logging
The application logs:
•	Authentication attempts
•	Errors and exceptions
Logs are written to both console and app.log file.

Security Features
•	Password hashing with bcrypt
•	JWT token-based authentication
•	Role-based access control
•	Input validation 
•	Secure password reset tokens

API Documentation
•	Swagger UI documention :http://127.0.0.1:8000/docs
•	Postman API Collection :https://crimson-sunset-302038.postman.co/workspace/Team-Workspace~b97f4b2f-5a0a-48d0-846f-a5e48568c0e8/collection/43331568-3fcf2e59-b226-4246-add0-c4a4637f369b?action=share&creator=43331568
