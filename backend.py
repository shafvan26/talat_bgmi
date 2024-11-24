from fastapi import FastAPI, Form
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = FastAPI()

# Database configuration
DATABASE_URL = "mysql+pymysql://root:nixon_97.talat@localhost:3306/bgmiacc"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the table
class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_name = Column(String, index=True)
    price = Column(Integer)
    details = Column(String)
    contact_email = Column(String)

Base.metadata.create_all(bind=engine)

# API Endpoint to handle form submissions
@app.post("/sell-account")
async def sell_account(
    account_name: str = Form(...),
    price: int = Form(...),
    details: str = Form(...),
    contact_email: str = Form(...)
):
    db = SessionLocal()
    new_account = Account(
        account_name=account_name,
        price=price,
        details=details,
        contact_email=contact_email
    )
    db.add(new_account)
    db.commit()
    db.close()
    return {"message": "Account submitted successfully!"}


@app.get("/accounts")
def get_accounts():
    db = SessionLocal()
    accounts = db.query(Account).all()
    db.close()
    return accounts
