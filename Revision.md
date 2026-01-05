## Day 1 FastAPI Introduction

> Why is returning correct HTTP status codes important?

Status codes allow clients (frontend, other services, monitoring tools) to programmatically understand outcomes without parsing response bodies.

> What happens if user_id is a string?

FastAPI will reject the request automatically with a 422 Unprocessable Entity

Why?

user_id: int triggers request validation

The request never reaches your function

> Why does FastAPI auto-generate docs?

Documentation helps to see and test all the endpoints at one place. Docs are generated from your code contracts (types, routes, responses), not manually written.

## Day 2 Pydantic, Request and Response Models

> Why is validation at the API boundary better than validation inside functions?

- **Separation of Concerns:** It decouples the "business logic" (what the function does) from the "interface logic" (ensuring data is correct).<br>
  **Automatic Documentation:** Validations at the boundary are automatically reflected in the OpenAPI (Swagger) documentation. If you hide validation inside the function, the API user won’t know the requirements until they try (and fail) to use it.<br>
  **Fail-Fast Security:** Invalid data is rejected before your code even starts running. This prevents your database or logic from processing potentially malicious or broken payloads.<br>
  **Cleaner Code:** You remove repetitive if not data or isinstance(x, int) checks from your core logic, keeping functions small and readable.

> What problem does response_model solve?

- While you are correct that it filters sensitive data like passwords, it solves several other critical problems:<br>
  **Data Integrity (Outbound Validation):** It ensures your server doesn't accidentally send a response that violates its own contract. If your code tries to return a string where the model expects an integer, FastAPI will catch it and raise a 500 Internal Server Error (instead of sending broken data to the client).<br>
  **Type Casting:** It automatically converts Python objects (like ORM database models) into clean JSON-serializable dictionaries based on the model.<br>
  **Response Documentation:** It tells the frontend developer exactly what the response body will look like in the Swagger UI, making the API much easier to consume.<br>
  **Technical Doubt Answer:** You can filter manually in the code, but you lose the automatic JSON schema generation and contract enforcement that makes FastAPI powerful.<br>

> What HTTP status code do you expect for invalid request data?

> **Standard FastAPI Response:** 422 Unprocessable Entity.<br> > **Reasoning:** While many older APIs used 400 Bad Request for everything, modern REST standards (and FastAPI/Pydantic by default) use 422 to indicate that the request was syntactically correct (valid JSON) but semantically incorrect (e.g., a missing field, wrong data type, or value out of range).<br> > **Note:** You can still manually return a 400 Bad Request using HTTPException if you prefer, but 422 is the framework's automated standard.<br>

## Day-3 Database Integration

**Why do we use Depends(get_db) instead of creating session inside function?**

> Depends(get_db) centralizes session creation and cleanup, ensures one DB session per request, enables safe reuse across endpoints, and guarantees cleanup even if an exception occurs.

**What would happen if we forget db.close()?**

> If db.close() is not called, database connections are not returned to the connection pool, leading to connection leaks.

**Why is email marked unique=True?**

> unique=True enforces data integrity at the database level, preventing race conditions that API-level checks cannot reliably handle.
> “Application checks are advisory; database constraints are authoritative.”

## Day 4

**Why do we return 404 instead of 200 with empty body?**

> 404 Not Found is returned because the requested resource does not exist. Returning 200 OK would falsely indicate that the resource exists and was successfully retrieved, even though it wasn’t found.

**Why must we call rollback() after DB errors?**

> When a database error occurs, the current transaction enters a failed state. `rollback()` is required to undo any partial changes and to reset the session, otherwise the session becomes unusable for further operations.

**Why is 409 Conflict better than 400 here?**

> 409 Conflict is used when the request is syntactically valid but cannot be processed because it conflicts with the current state of the resource (e.g., duplicate email).
> 400 Bad Request is for malformed or invalid input.

## Day 5 Pagination and Limiting

**Why is default limit = 10?**

> To provide a safe default page size that prevents accidental large queries and ensures predictable performance.

**Why cap limit at 100?**

> To prevent excessive database load, memory usage, and network transfer that could degrade performance under concurrent traffic.

**Why should ordering use an indexed column?**

> Because indexed ordering avoids full table scans and expensive sort operations, enabling the database to return results efficiently at scale.

---

🔒 One rule to remember

Pagination limits protect the database, indexing protects performance, and defaults protect you from mistakes.

## Day 6 PATCH Vs PUT, Delete - Idempotent

**Why is PATCH safer than PUT?**

> PATCH is safer because it updates only the fields explicitly provided in the request, whereas PUT replaces the entire resource. Sending partial data with PUT can unintentionally overwrite or nullify fields that were not included in the request.

**Why do real systems prefer soft deletes?**

> Real systems prefer soft deletes to allow data recovery, auditing, and historical analysis, and to avoid breaking references or relationships that depend on the deleted data.

**Why must DELETE be idempotent?**

> An operation is idempotent if making the same request multiple times has the same effect as making it once.
> DELETE must be idempotent so that repeated delete requests do not cause additional side effects. Deleting a resource multiple times should result in the same final state: the resource is gone.

---

## Day 7 Pytest

**Why do tests reduce fear while refactoring?**

> Tests reduce fear during refactoring because they act as a safety net that verifies existing behavior remains unchanged, allowing internal code structure to be modified with confidence.

**Why is testing failure cases critical?**

> Testing failure cases is critical because it validates how the system behaves under invalid input, edge cases, and error conditions, ensuring predictable, safe, and secure behavior.

**What would break if tests didn’t exist?**

> Without tests, changes can introduce regressions that silently break existing functionality, making refactoring and feature development risky and causing failures in production environments.

## Day 8 Authorization and Authentication

**Why doesn’t the backend trust the frontend?**

> The backend does not trust the frontend because the frontend runs in the user’s environment and can be modified, bypassed, or manipulated. All security-critical checks—such as authentication, authorization, and data validation—must be enforced on the backend, which is under the system’s control.

**Why do we hash passwords?**

> Passwords are hashed so that even if the database is compromised, plaintext passwords are not exposed. Hashing is a one-way process, meaning passwords cannot be reconstructed from their stored values, reducing the impact of data breaches.

**Why is JWT stateless?**

> JWT is stateless because the server does not store any session information. All necessary authentication data is contained within the token itself, allowing the server to verify requests without maintaining session state.

## Day 9 Roles and Ownership

**Where does authorization logic belong?**

> Authorization logic belongs on the backend and is evaluated after authentication but before executing the endpoint’s business logic. It determines whether an authenticated user is allowed to perform a specific action on a resource.

**What would break if roles were handled only in frontend?**

> If roles were enforced only on the frontend, users could modify client-side code or requests to assign themselves higher privileges. This would completely bypass authorization and allow unauthorized access to protected actions.

**Why is ownership harder than authentication?**

> Authentication verifies the identity of a user, while ownership requires validating that the authenticated user is associated with a specific resource. Ownership checks are harder because they depend on runtime context (which resource is being accessed) and require additional database lookups and business rules.

## Day 10 Background Tasks

**Why shouldn’t email sending block user creation?**

> User creation is a critical business operation, while email sending is a non-critical side effect. Blocking user creation on email delivery tightly couples the core workflow to an unreliable external dependency and reduces system reliability.

**What would happen if background tasks fail silently?**

> Silent failures cause important side effects to be missed without detection, leading to degraded user experience and operational blind spots unless errors are logged and monitored.

**When does BackgroundTasks stop being enough?**

> Silent failures cause important side effects to be missed without detection, leading to degraded user experience and operational blind spots unless errors are logged and monitored.
