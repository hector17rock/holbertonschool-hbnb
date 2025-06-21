# 📘 HBnB Evolution – Part 1: Technical Documentation

## 📌 Overview

This document outlines the technical foundation for the **HBnB Evolution** project, a simplified AirBnB-like application. The goal of this phase is to produce clear, maintainable documentation that will guide the design and implementation of the system in later stages.

---

## 🎯 Context and Objective

In this initial phase, we focus on:

- Structuring the application using a **three-layer architecture**
- Applying the **Facade design pattern** for cleaner communication between components
- Documenting business entities and API flows using **UML diagrams**
- Ensuring alignment with business rules and software engineering principles

---

## 🧩 Problem Description

HBnB Evolution allows users to manage:

- **Users** – Create, update, delete user profiles
- **Places** – Add properties with descriptions, pricing, and geolocation
- **Reviews** – Submit comments and ratings for places
- **Amenities** – Manage services that can be associated with places

---

## 📚 Business Rules and Requirements

### 🔸 User
- Attributes: `first_name`, `last_name`, `email`, `password`, `is_admin`
- Can: register, update profile, be deleted

### 🔸 Place
- Attributes: `title`, `description`, `price`, `latitude`, `longitude`
- Owned by a user; can have amenities
- Can: be created, updated, deleted, and listed

### 🔸 Review
- Attributes: `rating`, `comment`
- Linked to a specific place and user
- Can: be created, updated, deleted, and listed

### 🔸 Amenity
- Attributes: `name`, `description`
- Can: be created, updated, deleted, and listed

**All entities:**
- Must have a unique `id` (UUID)
- Must track `created_at` and `updated_at` timestamps

---

## 🏗 Architecture and Layers

The application is divided into three main layers:

1. **Presentation Layer**: API and services used by end users
2. **Business Logic Layer**: Core models and rules
3. **Persistence Layer**: Data storage and retrieval

**Data will be stored in a database** to be implemented in Part 3.

---

## 📦 Task 0: High-Level Package Diagram

### ✅ Objective
Illustrate the three-layer architecture and the use of the **Facade Pattern** to connect them.

### 🖼️ Diagram (Mermaid.js)
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


📝 Explanatory Notes
Presentation Layer exposes services to the client.
Business Logic Layer applies domain rules via models.
Persistence Layer abstracts data handling.
The Facade simplifies and centralizes logic exposure.
🧱 Task 1: Detailed Class Diagram for Business Logic Layer

✅ Objective
Define entities and their relationships in the core logic of the application.


🖼️ Example Class Diagram (Mermaid.js)
classDiagram
class User {
    +UUID id
    +str first_name
    +str last_name
    +str email
    +str password
    +bool is_admin
    +datetime created_at
    +datetime updated_at
}

class Place {
    +UUID id
    +str title
    +str description
    +float price
    +float latitude
    +float longitude
    +datetime created_at
    +datetime updated_at
}

class Review {
    +UUID id
    +int rating
    +str comment
    +datetime created_at
    +datetime updated_at
}

class Amenity {
    +UUID id
    +str name
    +str description
    +datetime created_at
    +datetime updated_at
}

User "1" --> "0..*" Place : owns >
Place "1" --> "0..*" Review : has >
User "1" --> "0..*" Review : writes >
Place "1" --> "*" Amenity : includes >


📝 Notes
Entities include both identity fields and timestamp tracking
Relationships reflect ownership and interactions:
A user can own multiple places
Places can include multiple amenities
Reviews are linked to both user and place


🔄 Task 2: Sequence Diagrams for API Calls

✅ Objective
Visualize interaction flows across layers for major API calls.

📌 Diagrams (Mermaid.js)
1. User Registration


sequenceDiagram
participant Client
participant API
participant Facade
participant Repo

Client->>API: POST /users
API->>Facade: create_user(data)
Facade->>Repo: add(user)
Repo-->>Facade: success
Facade-->>API: return user
API-->>Client: 201 Created


2. Place Creation


sequenceDiagram
participant Client
participant API
participant Facade
participant Repo

Client->>API: POST /places
API->>Facade: create_place(data)
Facade->>Repo: add(place)
Repo-->>Facade: success
Facade-->>API: return place
API-->>Client: 201 Created


3. Review Submission


sequenceDiagram
participant Client
participant API
participant Facade
participant Repo

Client->>API: POST /reviews
API->>Facade: create_review(data)
Facade->>Repo: add(review)
Repo-->>Facade: success
Facade-->>API: return review
API-->>Client: 201 Created


4. Fetch List of Places


sequenceDiagram
participant Client
participant API
participant Facade
participant Repo

Client->>API: GET /places
API->>Facade: get_all_places()
Facade->>Repo: list()
Repo-->>Facade: [place1, place2, ...]
Facade-->>API: return list
API-->>Client: 200 OK


📑 Task 3: Documentation Compilation

✅ Objective
Compile all deliverables into one complete reference for development.

📘 Contents
Introduction: Goals and scope of documentation
Architecture: Overview of system design
Class Diagram: Core entities and their structure
Sequence Diagrams: How data flows for key use cases
📌 Tools & Formats
Diagrams: Mermaid.js, draw.io (optional)
Format: Markdown for source, export to PDF if needed


🔗 Resources

UML Class Diagram Tutorial
UML Sequence Diagrams
Facade Pattern Guide
Mermaid.js Docs


✅ Expected Outcome

A comprehensive, professional technical document that:

Explains system architecture clearly
Includes detailed UML diagrams for logic and flow
Enables a seamless transition to implementation


📁 Repository Structure


holbertonschool-hbnb/
└── part1/
    ├── diagrams/
    │   ├── package_diagram.mmd
    │   ├── class_diagram.mmd
    │   └── sequence_diagrams.mmd
    ├── README.md
    └── documentation.pdf



