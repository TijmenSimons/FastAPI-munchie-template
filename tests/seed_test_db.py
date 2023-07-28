from core.db.models import *
from app.user.utils import get_password_hash
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

        session.add_all(
            []
        )
        session.commit()

    # needed to call this because test.db couldnt be deleted anymore
    engine.dispose()
