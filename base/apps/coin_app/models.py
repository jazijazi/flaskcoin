from timeit import default_timer
from base import db
from sqlalchemy import Column , Integer , String , Boolean , Float , DateTime , ForeignKey
from sqlalchemy.sql import func

class coin(db.Model):
    __tablename__ = 'Coin'
    id = Column(Integer, primary_key=True)
    currency = Column(String(128) , nullable=False)
    name = Column(String(128) , nullable=False)
    fullName = Column(String(128) , nullable=False)
    precision = Column(Integer , nullable=True)
    confirms = Column(Integer , nullable=True)
    contractAddress = Column(String(128) , nullable=True)
    withdrawalMinSize = Column(String(128) , nullable=False)
    withdrawalMinFee = Column(String(128) , nullable=False)
    isWithdrawEnabled = Column(Boolean , nullable=False)
    isDepositEnabled = Column(Boolean , nullable=False)
    isMarginEnabled = Column(Boolean , nullable=False)
    isDebitEnabled = Column(Boolean , nullable=False)
    prices = db.relationship('price' , backref='coin' , lazy=True)

    def __repr__(self) -> str:
        return f'{self.fullName}'
        #return super().__repr__()

class price(db.Model):
    __tablename__ = "Price"
    id = Column(Integer, primary_key=True)
    coin_id = Column(Integer , ForeignKey('Coin.id' , ondelete='cascade'))
    price = Column(Float , nullable=False)
    date = Column(DateTime(timezone=True) , server_default=func.now())