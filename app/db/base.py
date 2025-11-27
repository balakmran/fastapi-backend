# Import all the models, so that Base has them before being
# imported by Alembic
from sqlmodel import SQLModel  # noqa

# Import models here
from app.modules.user.models import User  # noqa
