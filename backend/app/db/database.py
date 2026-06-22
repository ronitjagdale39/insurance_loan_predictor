from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

URL='postgresql://postgres:1234@db:5432/insu_premium'
engine=create_engine(URL)
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base=declarative_base()
def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()