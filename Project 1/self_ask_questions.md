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

## Idempotency

**What does “the same request” mean in my system?**

In my system, “the same request” means an operation that targets the same resource with the same intent, such that repeating it should result in the same final system state.

Examples:

Create user

- Creating a user with the same unique identifier (e.g., email) multiple times results in exactly one user record. Repeated attempts do not create additional users.

Delete user

- Deleting an already-deleted user leaves the system in the same state. Repeating the delete does not change anything further.

In idempotency, the final state of the system is the same whether the request is executed once or multiple times.

**Why must the key be unique?**

> The idempotency key must be unique so the system can distinguish a retry of the same logical request from a new request and ensure that the operation is applied only once.

**Why tie it to a user?**

> The idempotency key is tied to a user to scope the operation correctly. The same key used by different users represents different logical actions and should not be treated as duplicates.

**What should be returned on duplicate?**

> On a duplicate request, the server should not re-execute the operation and should return the same response as the original successful request, ensuring retries are safe and transparent to the client.

**What happens if the resource is created, but the idempotency key insert fails?**
