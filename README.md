# HBnB Evolution Project 🏠

A comprehensive **AirBnB clone** application developed as part of the Holberton School curriculum. This project demonstrates the complete software development lifecycle from architectural design to implementation, featuring a modern **three-layer architecture** with RESTful APIs, object-oriented programming, and scalable design patterns.

## 🌟 Project Overview

**Repository:** `holbertonschool-hbnb`  
**School:** Holberton School  
**Track:** Backend Web Development  
**Architecture:** Three-Layer Architecture with Facade Pattern  
**Framework:** Flask + Flask-RESTx  
**Status:** Complete Multi-Part Implementation (Parts 1-4: Design → Backend → Database → Full-Stack)

## 🎯 Project Objectives

This project creates a simplified AirBnB application that allows users to:

- 👤 **User Management**: Registration, authentication, profile management, and role-based access
- 🏘️ **Place Management**: Property listings with detailed metadata and amenity associations  
- ⭐ **Review System**: User ratings and comments for places with validation
- 🛠️ **Amenity Management**: Create, update, and manage property amenities
- 💾 **Data Persistence**: Scalable storage architecture (in-memory → database)

## 🏗️ Architecture & Design

### Three-Layer Architecture

```mermaid
graph TB
    subgraph "Presentation Layer"
        API[RESTful API Endpoints]
        DOC[API Documentation]
    end
    
    subgraph "Business Logic Layer"
        MODELS[Data Models]
        SERVICES[Business Services]
        FACADE[Facade Pattern]
    end
    
    subgraph "Persistence Layer"
        REPO[Repository Pattern]
        STORAGE[Data Storage]
    end
    
    API --> FACADE
    FACADE --> MODELS
    FACADE --> SERVICES
    SERVICES --> REPO
    REPO --> STORAGE
```

### Core Design Patterns

- **🎭 Facade Pattern**: Simplifies communication between layers
- **📦 Repository Pattern**: Abstracts data access and storage
- **🏭 Factory Pattern**: Creates and manages object instances
- **🔧 Dependency Injection**: Loose coupling between components

## 📁 Project Structure

```
holbertonschool-hbnb/
├── 📋 README.md                     # This comprehensive guide
├── 📊 part1/                        # Architecture & Design Phase
│   ├── 📖 README.md                 # Technical documentation
│   └── 📈 DIAGRAMASFINAL/           # UML diagrams and visuals
│       ├── class_diagram.png
│       ├── sequence_diagrams.png
│       └── architecture_overview.png
├── 🚀 part2/                        # Basic Implementation Phase
│   ├── 📖 README.md                 # Implementation documentation
│   ├── ⚙️ config.py                 # Application configuration
│   ├── 📦 requirements.txt          # Python dependencies
│   ├── 🎯 run.py                    # Application entry point
│   ├── 📝 server.log                # Server logs
│   ├── 🔧 app/                      # Main application package
│   │   ├── 🌐 api/v1/               # Presentation Layer (REST API)
│   │   │   ├── users.py             # User management endpoints
│   │   │   ├── places.py            # Place management endpoints
│   │   │   ├── reviews.py           # Review management endpoints
│   │   │   └── amenities.py         # Amenity management endpoints
│   │   ├── 📊 models/               # Business Logic Layer (Data Models)
│   │   │   ├── base_model.py        # Abstract base class
│   │   │   ├── user.py              # User entity model
│   │   │   ├── place.py             # Place entity model
│   │   │   ├── review.py            # Review entity model
│   │   │   └── amenity.py           # Amenity entity model
│   │   ├── 🎯 services/             # Business Logic Layer (Services)
│   │   │   └── facade.py            # Facade pattern implementation
│   │   └── 💾 persistence/          # Persistence Layer (Data Access)
│   │       └── repository.py        # In-memory repository
│   ├── 🧪 tests/                    # Comprehensive test suite
│   │   ├── test_user_endpoints.py   # User API tests
│   │   ├── test_amenity_creation.py # Amenity tests
│   │   ├── test_put_endpoint.py     # Update operation tests
│   │   └── example_*.py             # Usage examples
│   └── 🐍 venv/                     # Python virtual environment
├── 🗄️ part3/                        # Database Integration & Advanced Features
│   ├── 📖 README.md                 # Database implementation documentation
│   ├── ⚙️ config.py                 # Multi-environment configuration
│   ├── 📦 requirements.txt          # Enhanced dependencies (SQLAlchemy, JWT, etc.)
│   ├── 🎯 run.py                    # Application entry point
│   ├── 🔧 init_db.py                # Database initialization script
│   ├── 🔧 app/                      # Enhanced application package
│   │   ├── __init__.py              # Flask app factory with extensions
│   │   ├── 🌐 api/v1/               # Enhanced REST API with authentication
│   │   │   ├── auth.py              # JWT authentication endpoints
│   │   │   ├── users.py             # User management with admin features
│   │   │   ├── places.py            # Place management with ownership
│   │   │   ├── reviews.py           # Review management with validation
│   │   │   ├── amenities.py         # Amenity management (admin only)
│   │   │   └── protected.py         # Protected route examples
│   │   ├── 📊 models/               # SQLAlchemy ORM Models
│   │   │   ├── base_model.py        # SQLAlchemy base model
│   │   │   ├── user.py              # User model with password hashing
│   │   │   ├── place.py             # Place model with relationships
│   │   │   ├── review.py            # Review model with constraints
│   │   │   └── amenity.py           # Amenity model
│   │   ├── 🎯 services/             # Business Logic with Repository Pattern
│   │   │   ├── facade.py            # In-memory facade (backward compatibility)
│   │   │   ├── facade_db.py         # Database-ready facade
│   │   │   ├── facade_sqlalchemy.py # Complete SQLAlchemy facade
│   │   │   └── repositories/        # Specialized repositories
│   │   │       └── user_repository.py # User-specific operations
│   │   └── 💾 persistence/          # Enhanced persistence layer
│   │       └── repository.py        # Abstract repository with SQLAlchemy
│   ├── 📚 documentations/           # Comprehensive documentation
│   │   ├── ADMIN_ENDPOINTS_GUIDE.md         # Admin functionality guide
│   │   ├── APPLICATION_FACTORY_COMPLETED.md # App factory pattern
│   │   ├── JWT_AUTHENTICATION_COMPLETED.md  # JWT implementation
│   │   ├── PASSWORD_HASHING_COMPLETED.md    # Bcrypt integration
│   │   ├── RELATIONSHIPS_DOCUMENTATION.md   # Database relationships
│   │   ├── SQLALCHEMY_INTEGRATION.md        # ORM integration
│   │   └── USER_MODEL_MAPPING.md            # User model mapping
│   ├── 📊 database_diagrams/        # ER diagrams and database design
│   │   ├── hbnb_er_diagram.md       # Core database schema
│   │   ├── hbnb_extended_er_diagram.md # Extended schema
│   │   ├── relationship_types_diagram.md # Relationship examples
│   │   ├── diagram_examples.md      # Practical examples
│   │   ├── view_diagrams.sh         # Safe diagram viewer
│   │   └── README.md                # Diagram documentation
│   ├── 🔧 sql_scripts/              # Database setup and testing
│   │   ├── 00_execute_all.sql       # Master execution script
│   │   ├── 01_create_tables.sql     # Schema creation
│   │   ├── 02_insert_initial_data.sql # Test data insertion
│   │   ├── 03_test_crud_operations.sql # CRUD testing
│   │   ├── generate_uuids.py        # UUID generation utility
│   │   ├── test_sql_scripts.py      # Script validation
│   │   ├── README.md                # SQL scripts guide
│   │   └── SQL_SCRIPTS_DOCUMENTATION.md # Comprehensive SQL docs
│   ├── 🧪 tests/                    # Enhanced test suite
│   │   ├── test_*.py                # Various test modules
│   │   └── example_*.py             # Usage examples
│   ├── 📝 BCRYPT_USAGE.md           # Password hashing guide
│   ├── 📝 SQLALCHEMY_IMPLEMENTATION_SUMMARY.md # Database summary
│   ├── 💾 instance/                 # SQLite database files
│   └── 🐍 venv/                     # Python virtual environment
└── 🌐 part4/                        # Full-Stack Integration
    ├── 📖 README.md                 # Full-stack documentation
    ├── 📖 LOGIN_README.md           # Login functionality guide
    ├── 🔧 BackEnd/                  # Complete Flask API Backend
    │   ├── 📖 README.md             # Backend documentation
    │   ├── ⚙️ config.py             # Production configuration
    │   ├── 📦 requirements.txt      # Backend dependencies
    │   ├── 🎯 run.py                # Backend entry point
    │   ├── 🔧 init_db.py            # Database initialization
    │   ├── 🔧 app/                  # Production-ready Flask app
    │   │   ├── __init__.py          # App factory with CORS
    │   │   ├── 🌐 api/v1/           # Production API endpoints
    │   │   │   ├── auth.py          # JWT authentication
    │   │   │   ├── users.py         # User management
    │   │   │   ├── places.py        # Place management
    │   │   │   ├── reviews.py       # Review management
    │   │   │   ├── amenities.py     # Amenity management
    │   │   │   └── protected.py     # Protected routes
    │   │   ├── 📊 models/           # Production ORM models
    │   │   ├── 🎯 services/         # Production business logic
    │   │   └── 💾 persistence/      # Production persistence
    │   ├── 📚 documentations/       # Backend documentation
    │   ├── 📊 database_diagrams/    # Database design docs
    │   ├── 🔧 sql_scripts/          # Production SQL scripts
    │   ├── 🧪 tests/                # Backend test suite
    │   └── 💾 instance/             # Production database
    └── 🎨 FrontEnd/                 # Responsive Web Interface
        ├── 📖 README.md             # Frontend documentation
        ├── 🏠 index.html            # Main page - Places listing
        ├── 🔐 login.html            # Login form with JWT
        ├── 🏘️ place.html            # Generic place details
        ├── 🏘️ place2.html           # Modern City Apartment
        ├── 🏘️ place3.html           # Beachfront Villa
        ├── 🏘️ place4.html           # Historic Downtown Loft
        ├── 🏘️ place5.html           # Countryside Cottage
        ├── 🏘️ place6.html           # Luxury Penthouse
        ├── ⭐ add_review.html        # Add review form
        ├── 🎨 styles.css             # Responsive CSS styling
        ├── ⚡ scripts.js             # JavaScript functionality
        ├── ⚙️ config.js              # Frontend API configuration
        └── 🖼️ images/                # Image assets
            ├── logo.png             # Application logo
            ├── icon.png             # Favicon
            ├── background.png       # Header background
            ├── Cozy Mountain Cabin.png      # Property images
            ├── Modern City Apartment.png    # Property images
            ├── Beachfront Villa.png         # Property images
            ├── Historic Downtown Loft.png   # Property images
            ├── Countryside Cottage.png      # Property images
            └── Luxury Penthouse.png         # Property images
```

## 🔧 Technical Stack

### Backend Technologies
- **🐍 Python 3.8+**: Core programming language
- **🌶️ Flask**: Lightweight web framework
- **📝 Flask-RESTx**: RESTful API development with auto-documentation
- **🏗️ Object-Oriented Programming**: Clean architecture with inheritance

### Development Tools
- **🧪 Unit Testing**: Comprehensive test coverage
- **📚 Auto-Documentation**: Swagger/OpenAPI integration
- **🔧 Virtual Environment**: Isolated dependency management
- **📊 Logging**: Application monitoring and debugging

### Architecture Patterns
- **🏛️ Three-Layer Architecture**: Separation of concerns
- **🎭 Facade Pattern**: Simplified layer communication  
- **📦 Repository Pattern**: Abstract data access
- **🔄 RESTful Design**: Standard HTTP methods and status codes

## 🚀 Getting Started

### Prerequisites

#### Backend Requirements (Parts 2-4)
- Python 3.8 or higher
- pip (Python package manager)
- Git for version control
- SQLite (for Part 3+ database functionality)

#### Frontend Requirements (Part 4)
- A modern web browser (Chrome 60+, Firefox 55+, Safari 10+, Edge 16+)
- Local web server (optional, for development):
  - Python 3.x (for `python -m http.server`)
  - Node.js (for `npx serve`)
  - PHP (for `php -S localhost:8000`)
  - Or any other local development server

### Installation & Setup

1. **Clone the Repository**
```bash
git clone https://github.com/holbertonschool/holbertonschool-hbnb.git
cd holbertonschool-hbnb/part2
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Application**
```bash
python run.py
```

5. **Access the API**
- **Application**: http://localhost:5001
- **API Documentation**: http://localhost:5001/api/v1/
- **Interactive Docs**: Swagger UI available at the docs endpoint

## 📡 API Endpoints

### 👤 User Management
```http
POST   /api/v1/users           # Create new user
GET    /api/v1/users           # List all users  
GET    /api/v1/users/{id}      # Get specific user
PUT    /api/v1/users/{id}      # Update user
DELETE /api/v1/users/{id}      # Delete user
```

### 🏘️ Place Management
```http
POST   /api/v1/places          # Create new place
GET    /api/v1/places          # List all places
GET    /api/v1/places/{id}     # Get specific place  
PUT    /api/v1/places/{id}     # Update place
DELETE /api/v1/places/{id}     # Delete place
```

### ⭐ Review Management
```http
POST   /api/v1/reviews         # Create new review
GET    /api/v1/reviews         # List all reviews
GET    /api/v1/reviews/{id}    # Get specific review
PUT    /api/v1/reviews/{id}    # Update review
DELETE /api/v1/reviews/{id}    # Delete review
```

### 🛠️ Amenity Management
```http
POST   /api/v1/amenities       # Create new amenity
GET    /api/v1/amenities       # List all amenities
GET    /api/v1/amenities/{id}  # Get specific amenity
PUT    /api/v1/amenities/{id}  # Update amenity
DELETE /api/v1/amenities/{id}  # Delete amenity
```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_user_endpoints.py

# Run with verbose output
python -m pytest -v tests/

# Run with coverage report
python -m pytest --cov=app tests/
```

### Test Examples
```bash
# Test user creation
python tests/test_user_endpoints.py

# Test amenity management
python tests/test_amenity_creation.py

# Test update operations
python tests/test_put_endpoint.py
```

## 📊 Data Models

### 👤 User Model
```python
{
    "id": "string (UUID)",
    "first_name": "string",
    "last_name": "string", 
    "email": "string (unique)",
    "password": "string (hashed)",
    "is_admin": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### 🏘️ Place Model
```python
{
    "id": "string (UUID)",
    "title": "string",
    "description": "string",
    "price": "float",
    "latitude": "float",
    "longitude": "float", 
    "owner_id": "string (User UUID)",
    "amenity_ids": ["string (Amenity UUIDs)"],
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### ⭐ Review Model
```python
{
    "id": "string (UUID)",
    "place_id": "string (Place UUID)",
    "user_id": "string (User UUID)",
    "rating": "integer (1-5)",
    "comment": "string",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### 🛠️ Amenity Model
```python
{
    "id": "string (UUID)",
    "name": "string (unique)",
    "description": "string",
    "created_at": "datetime", 
    "updated_at": "datetime"
}
```

## 🎯 Business Logic & Validation

### Data Validation Rules
- **Email Format**: Valid email address format required
- **Password Security**: Minimum length and complexity requirements
- **Rating Range**: Reviews must be between 1-5 stars
- **Coordinates**: Latitude/longitude within valid geographic ranges
- **Unique Constraints**: Email addresses and amenity names must be unique
- **Required Fields**: All mandatory fields must be provided

### Business Rules
- **User Authentication**: Secure user registration and login
- **Ownership Validation**: Users can only modify their own content
- **Review Restrictions**: Users cannot review their own places
- **Admin Privileges**: Special permissions for administrative users
- **Data Integrity**: Referential integrity between related entities

## 🔮 Future Enhancements (Part 3+)

### Database Integration
- **🗄️ SQLAlchemy ORM**: Replace in-memory storage
- **🐘 PostgreSQL**: Production-ready database
- **📊 Database Migrations**: Version-controlled schema changes
- **🔍 Query Optimization**: Efficient data retrieval

### Advanced Features
- **🔐 JWT Authentication**: Secure token-based auth
- **📤 File Upload**: Image handling for places
- **🔍 Advanced Search**: Filter and search functionality
- **📧 Email Notifications**: User communication system
- **📱 Mobile API**: Mobile app support

### DevOps & Deployment
- **🐳 Docker**: Containerized deployment
- **☁️ Cloud Deployment**: AWS/GCP/Azure integration
- **🔄 CI/CD Pipeline**: Automated testing and deployment
- **📊 Monitoring**: Application performance monitoring

## 🎓 Learning Outcomes

### Software Architecture
- **🏗️ Layered Architecture**: Understanding separation of concerns
- **🎭 Design Patterns**: Practical application of common patterns
- **📡 RESTful APIs**: Standard web service design
- **🔧 Modular Design**: Creating maintainable and scalable code

### Backend Development
- **🐍 Python Mastery**: Advanced Python programming concepts
- **🌶️ Flask Expertise**: Web framework proficiency
- **🗄️ Data Modeling**: Entity relationship design
- **🧪 Testing Strategy**: Comprehensive testing methodologies

### Software Engineering
- **📚 Documentation**: Clear technical documentation
- **🔄 Version Control**: Git workflow and collaboration
- **🎯 Project Structure**: Organizing large-scale applications
- **🚀 Deployment**: Application lifecycle management

## 📚 Resources & References

### Documentation
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/)
- [Python Design Patterns](https://python-patterns.guide/)
- [RESTful API Design Guidelines](https://restfulapi.net/)

### Learning Materials
- [Three-Layer Architecture](https://www.oreilly.com/library/view/software-architecture-patterns/9781491971437/ch01.html)
- [Facade Pattern Tutorial](https://refactoring.guru/design-patterns/facade)
- [Repository Pattern in Python](https://breadcrumbscollector.tech/repository-pattern-in-python/)
- [Flask Best Practices](https://flask.palletsprojects.com/en/stable/patterns/)

## 🤝 Contributing

This repository represents academic work completed as part of the Holberton School curriculum. The project follows a structured learning approach with specific phases:

### Development Phases
1. **📋 Part 1**: Architecture design and documentation
2. **🚀 Part 2**: Core implementation with in-memory storage  
3. **🗄️ Part 3**: Database integration and persistence
4. **🔒 Part 4**: Authentication and advanced features

### Code Standards
- **PEP 8**: Python code style compliance
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Unit test coverage for all components
- **Git Flow**: Structured branching and commit messages

## 📧 Project Information

**Institution**: Holberton School  
**Program**: Full-Stack Software Engineering  
**Project Type**: Backend Web Development  
**Duration**: Multi-part implementation  
**Technologies**: Python, Flask, RESTful APIs, OOP

## 👨‍💻 Author

**Hector Soto**  
- **GitHub**: [@hector17rock](https://github.com/hector17rock)  
- **Institution**: Holberton School  
- **Role**: Full-Stack Developer  
- **Project**: HBnB Evolution - Complete AirBnB Clone Implementation

---

*This project demonstrates the progression from architectural design to full-stack implementation, showcasing modern software engineering practices and design patterns in a real-world application context.*
