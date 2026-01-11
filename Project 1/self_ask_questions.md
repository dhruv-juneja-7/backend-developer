## App Entry Point

**Where does FastAPI() live?**

> FastAPI() is a Python application object defined in the codebase. It implements the ASGI interface.

**How will uvicorn run it?**

> Uvicorn loads the FastAPI app and serves it by binding it to a host and port, handling incoming HTTP requests and passing them to the app.

## Database Setup

**How will endpoints get a DB session?**
Endpoints receive a database session via FastAPI’s dependency injection system using Depends(get_db).

**Who closes it?**
The session is closed by the dependency function itself after the request completes; FastAPI ensures the cleanup code runs.

## First Domain Model

**What does the system need to store first?**

> Domain modeling begins with independent entities like User. Dependent entities such as Action reference users via foreign keys and therefore come later.
