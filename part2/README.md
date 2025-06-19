# HBnB Evolution - Part 2: Project Setup and Package Initialization

## Objective

The goal of this task is to establish the foundational project structure for the HBnB application. This involves organizing the codebase into three main architectural layers—Presentation, Business Logic, and Persistence—while preparing it for integration with the **Facade Design Pattern**. Although a database-backed solution will be implemented in Part 3, this stage uses an **in-memory repository** for object storage and validation.

## Context

A modular and well-organized codebase is key to maintaining scalability, readability, and ease of development. Before diving into the implementation of features and endpoints, this setup ensures:

- A clear separation of concerns across architectural layers.
- A scalable structure ready for enhancements.
- Smooth communication between layers using the Facade pattern.
- Readiness to transition from in-memory to persistent storage (e.g., SQLAlchemy).

## Project Structure Overview



## Tasks Completed

- Created directory structure and `__init__.py` files to define Python packages.
- Organized the application into three core layers:
  - **Presentation Layer** (`api/v1/`): Handles Flask API routes.
  - **Business Logic Layer** (`models/`, `services/`): Defines data models and Facade logic.
  - **Persistence Layer** (`persistence/`): Includes an in-memory repository.
- Implemented an in-memory repository with storage and validation logic.
- Integrated a `facade.py` module to mediate between API and data operations.

## Expected Outcome

By completing this setup, the project is now:

- Structured for modular development and scalability.
- Ready to integrate more complex business rules and API routes.
- Capable of storing and validating data in-memory.
- Prepared for smooth transition to a persistent database layer in the next phase.

## Resources

- [Flask Documentation](https://flask.palletsprojects.com/en/stable/)
- [Flask-RESTx Documentation](https://flask-restx.readthedocs.io/en/latest/)
- [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
- [Facade Design Pattern (Python)](https://refactoring.guru/design-patterns/facade/python/example)

## Repository

- **GitHub**: [holbertonschool-hbnb](https://github.com/holbertonschool-hbnb)
- **Directory**: `part2/`

---


