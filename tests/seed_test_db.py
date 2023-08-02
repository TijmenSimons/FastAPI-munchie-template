from app.user.utils import get_password_hash
from core.db.models import User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def seed_db():
    # we can now construct a Session() without needing to pass the
    # engine each time
    engine = create_engine("sqlite:///./test.db")

    # a sessionmaker(), also in the same scope as the engine
    Session = sessionmaker(engine)

    with Session() as session:
        # Add your things here

        admin_user = User(
            display_name="admin",
            username="admin",
            password=get_password_hash("admin"),
            is_admin=True,
        )

        normal_user = User(
            display_name="normal_user",
            username="normal_user",
            password=get_password_hash("normal_user"),
        )

        session.add_all([admin_user, normal_user])
        session.commit()

    # needed to call this because test.db couldnt be deleted anymore
    engine.dispose()
