# Yalantis Lecture FastAPI Template

## What can be done?
1. Makefile which will simplify run & etc
2. JWT Auth
3. User model extension
4. Create Postman Collections with auth jwt request https://www.postman.com/
5. Add CI to github/gitlab repository
6. Docker


## Run

```python
python3 main.py --env local|dev|prod --debug
```

## Dependencies
https://pipenv.pypa.io/en/latest/

## Date base PostgresSQL 

### Migrations
```
alembic revision -m "create account table"  # Make migrations
alembic upgrade head  # do migration
alembic history
alembic downgrade 005ce6e94401
```

SQLAlchemy for asyncio context

```python
from core.db import Transactional, session


@Transactional()
async def create_user(self):
    session.add(User(email="test@test.com"))
```

Do not use explicit `commit()`. `Transactional` class automatically do.

### Standalone session

According to the current settings, the session is set through middleware.

However, it doesn't go through middleware in tests or background tasks.

So you need to use the `@standalone_session` decorator.

```python
from core.db import standalone_session


@standalone_session
def test_something():
    ...
```

## Custom user for authentication

```python
from fastapi import Request


@home_router.get("/")
def home(request: Request):
    return request.user.id
```

**Note. you have to pass jwt token via header like `Authorization: Bearer 1234`**

Custom user class automatically decodes header token and store user information into `request.user`

If you want to modify custom user class, you have to update below files.

1. `core/fastapi/schemas/current_user.py`
2. `core/fastapi/middlewares/authentication.py`

### CurrentUser

```python
class CurrentUser(BaseModel):
    id: int = Field(None, description="ID")
```

Simply add more fields based on your needs.

### AuthBackend

```python
current_user = CurrentUser()
```

After line 18, assign values that you added on `CurrentUser`.

## Dependencies for specific permissions

Permissions `IsAdmin`, `IsAuthenticated`, `AllowAll` have already been implemented.
 
```python
from core.fastapi.dependencies import (
    PermissionDependency,
    IsAdmin,
)


user_router = APIRouter()


@user_router.get(
    "",
    response_model=List[GetUserListResponseSchema],
    response_model_exclude={"id"},
    responses={"400": {"model": ExceptionResponseSchema}},
    dependencies=[Depends(PermissionDependency([IsAdmin]))],  # HERE
)
async def get_user_list(
    limit: int = Query(10, description="Limit"),
    prev: int = Query(None, description="Prev ID"),
):
    pass
```
Insert permission through `dependencies` argument.

If you want to make your own permission, inherit `BasePermission` and implement `has_permission()` function.

**Note. In order to use swagger's authorize function, you must put `PermissionDependency` as an argument of `dependencies`.**



#### Used template https://github.com/teamhide/fastapi-boilerplate