# HBnB Evolution - Part 1: Technical Documentation

## 📘 Introduction

Welcome to the **HBnB Evolution** project! This document provides a comprehensive technical overview of the application's architecture, design, and system interactions. The goal of this documentation is to establish a solid foundation for the implementation phases by clearly detailing the application’s layered architecture, business logic, and interaction flow.

## 📌 Project Objective

Design and document the architecture of an AirBnB-like application. The application will allow users to:

- Manage users (registration, updates, roles)
- Manage place listings and amenities
- Submit and view reviews
- Persist all data in a structured database (to be implemented in Part 3)

---

## 🧩 Problem Description

The application allows the following primary operations:

- **User Management**  
  Users can register, update their profiles, and be marked as administrators.

- **Place Management**  
  Users can list properties with metadata and associate amenities.

- **Review Management**  
  Users can leave ratings and comments on places they've visited.

- **Amenity Management**  
  The system supports creating, updating, and listing amenities.

---

## 📐 Architecture and Layers

The application is divided into a **Three-Layer Architecture**:

1. **Presentation Layer**  
   Exposes APIs and services for external interaction.

2. **Business Logic Layer**  
   Encapsulates core logic and data validation using models.

3. **Persistence Layer**  
   Handles data access, storage, and retrieval.

The **Facade Design Pattern** is used to streamline communication between layers.

---

## 📁 Tasks Overview

### ✅ 0. High-Level Package Diagram

**Objective:** Illustrate the application's three-layer structure and component communication.

**Diagram (Mermaid.js):**

```mermaid
classDiagram
class PresentationLayer {
    <<Interface>>
    +ServiceAPI
}
class BusinessLogicLayer {
    +ModelClasses
}
class PersistenceLayer {
    +DatabaseAccess
}
PresentationLayer --> BusinessLogicLayer : Facade Pattern
BusinessLogicLayer --> PersistenceLayer : Database Operations


classDiagram
class User {
    +str id
    +str first_name
    +str last_name
    +str email
    +str password
    +bool is_admin
    +datetime created_at
    +datetime updated_at
}

class Place {
    +str id
    +str title
    +str description
    +float price
    +float latitude
    +float longitude
    +User owner
    +List~Amenity~ amenities
    +datetime created_at
    +datetime updated_at
}

class Review {
    +str id
    +Place place
    +User user
    +int rating
    +str comment
    +datetime created_at
    +datetime updated_at
}

class Amenity {
    +str id
    +str name
    +str description
    +datetime created_at
    +datetime updated_at
}

User "1" --> "*" Place : owns
Place "1" --> "*" Review : has
Place "*" --> "*" Amenity : includes
Review "*" --> "1" User : written by


sequenceDiagram
participant User
participant APIService
participant Facade
participant UserDAO
participant DB

User->>APIService: POST /register
APIService->>Facade: handle_user_creation()
Facade->>UserDAO: save_user()
UserDAO->>DB: INSERT INTO users
DB-->>UserDAO: Success
UserDAO-->>Facade: user_id
Facade-->>APIService: User created
APIService-->>User: 201 Created


sequenceDiagram
participant User
participant APIService
participant Facade
participant PlaceDAO
participant DB

User->>APIService: POST /places
APIService->>Facade: create_place()
Facade->>PlaceDAO: save_place()
PlaceDAO->>DB: INSERT INTO places
DB-->>PlaceDAO: Success
PlaceDAO-->>Facade: place_id
Facade-->>APIService: Place created
APIService-->>User: 201 Created


sequenceDiagram
participant User
participant APIService
participant Facade
participant ReviewDAO
participant DB

User->>APIService: POST /reviews
APIService->>Facade: add_review()
Facade->>ReviewDAO: save_review()
ReviewDAO->>DB: INSERT INTO reviews
DB-->>ReviewDAO: Success
ReviewDAO-->>Facade: review_id
Facade-->>APIService: Review created
APIService-->>User: 201 Created


sequenceDiagram
participant User
participant APIService
participant Facade
participant PlaceDAO
participant DB

User->>APIService: GET /places
APIService->>Facade: fetch_places()
Facade->>PlaceDAO: get_all_places()
PlaceDAO->>DB: SELECT * FROM places
DB-->>PlaceDAO: List of places
PlaceDAO-->>Facade: List
Facade-->>APIService: Place list
APIService-->>User: 200 OK + Data



