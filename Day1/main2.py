from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel, EmailStr, field_validator
from typing import List

app = FastAPI()


users_db: List["User"] = []
emails_set = set()

ALLOWED_DOMAINS = {"@gmail.com", "@yahoo.com", "@outlook.com"}


def get_domain(email: str) -> str:
    return "@" + email.split("@")[-1]


class User(BaseModel):
    id: int
    name: str
    email: EmailStr

    # model_config = {
    #     "json_schema_extra": {
    #         "example": {
    #             "id": 1,
    #             "name": "Kapil Rokaya",
    #             "email": "kapil123@gmail.com",
    #         }
    #     }
    # }


class UserCreate(BaseModel):
    name: str
    email: EmailStr

    model_config = {
        "extra": "forbid",
        # "json_schema_extra": {
        #     "example": {
        #         "name": "Kapil Rokaya",
        #         "email": "kapil123@gmail.com",
        #     }
        # },
        # "strict": True,
        # "validate_assignment": True
    }

    @field_validator("email", mode="before")
    @classmethod
    def preprocess_email(cls, value):
        return value.replace(" ", "").lower()

    @field_validator("email")
    @classmethod
    def validate_email_domain(cls, value):
        domain = get_domain(value)
        if domain not in ALLOWED_DOMAINS:
            raise ValueError(
                f"Email domain '{domain}' is not allowed. Allowed domains: {ALLOWED_DOMAINS}"
            )
        return value


def get_next_id() -> int:
    if users_db:
        return users_db[-1].id + 1
    return 1


def find_user_index(id: int) -> int | None:
    for index, user in enumerate(users_db):
        if user.id == id:
            return index
    return None

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=User, status_code=201, operation_id="createUser")
def create_user(user: UserCreate):
    if user.email in emails_set:
        raise HTTPException(status_code=409, detail="Email is already registered")

    new_user = User(id=get_next_id(), name=user.name, email=user.email)
    users_db.append(new_user)
    emails_set.add(user.email)
    return new_user


@user_router.get("/", response_model=List[User], operation_id="listUsers")
def get_users():
    return users_db


@user_router.get("/{id}", response_model=User, operation_id="getUser")
def get_user(id: int):
    index = find_user_index(id)
    if index is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[index]


@user_router.delete("/{id}", response_model=User, operation_id="deleteUser")
def delete_user(id: int):
    index = find_user_index(id)
    if index is None:
        raise HTTPException(status_code=404, detail="User not found")

    user = users_db.pop(index)
    emails_set.remove(user.email)
    return user


@user_router.put("/{id}", response_model=User, operation_id="updateUser")
def update_user(id: int, user_update: UserCreate):
    index = find_user_index(id)
    if index is None:
        raise HTTPException(status_code=404, detail="User not found")

    existing_user = users_db[index]

    if user_update.email in emails_set and user_update.email != existing_user.email:
        raise HTTPException(status_code=409, detail="Email is already registered")

    updated_user = User(id=id, name=user_update.name, email=user_update.email)
    users_db[index] = updated_user

    emails_set.remove(existing_user.email)
    emails_set.add(user_update.email)

    return updated_user


@app.get("/", tags=["Root"])
def root():
    return {"message": "Hello!. Go to /docs"}


app.include_router(user_router)
