# Project 1

## Project Goal

Build a backend system that accepts user actions, responds quickly and processes side effects reliably without duplication, even under failures.

## Project Scope

Under a heading “V1 Scope”, write only this list:

- V1 Scope (Must-Have)
- User signup & login (JWT)
- Roles: user, admin
- Submit an action
- Async processing of action
- Idempotency for action submission
- Logs for processing outcome

Then under “Explicitly Out of Scope”, write:

- UI / frontend
- Message brokers (Kafka, RabbitMQ)
- AI features
- Scaling / deployment
- Performance optimization

✔️ Done = both lists written.

## Core Entites

### User

- id
- email
- role

### Action

- id
- user_id
- status (pending / processed / failed)
- created_at

### Event

- id
- type (e.g. action.created)
- payload
- processed_at

### IdempotencyKey

- key
- action_id
- created_at

Do not add extra fields.

### System Flow

```
Client
→ POST /actions
→ validate request
→ check idempotency key
→ create action (pending)
→ create event
→ respond 202 Accepted

Worker (background)
→ pick event
→ process side effect
→ update action status
→ log result
```

## System Invariants

- Idempotency, duplicate requests should not create duplicate records
- Unauthenticated persons should not be able to access the system
- Users can access/update their own accounts only, while admin can access all the accounts.

## Failure Scenario

- User took an action but the side effect failed silently.
- Database connection pool may be exhausted, so the request is not fullfilled.

## Project Description

> In this Project, we are authenticating users and authorizing them based on their roles. We are also sending them signup emails which is a part of Background Tasks. For this, we have used, Python FastAPI web framework, Uvicorn as Web Server and Pydanctic to validate and serialize requests. SQLAlchemy is used to connect to Postgres database.
