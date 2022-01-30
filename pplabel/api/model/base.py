from datetime import datetime

from pplabel.config import db
from pplabel.api.util import nncol
from ..util import abort

# TODO: nn string col cant be ""
class BaseModel(db.Model):
    __abstract__ = True
    __tablename__ = ""
    __table_args__ = {"comment": ""}
    created = nncol(db.DateTime, default=datetime.utcnow)
    modified = nncol(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    _immutables = ["created", "modified", "immutables"]

    def __repr__(self):
        s = f"Object: {self.__tablename__}\n"
        for att in dir(self):
            if att[0] != "_":
                s += f"{att}: {getattr(self, att)}  "
        s += "\n"
        return s

    @classmethod
    def _exists(cls, item_id, throw=True):
        item = cls.query.filter(
            getattr(cls, cls.__tablename__ + "_id") == item_id
        ).one_or_none()
        if item is None:
            if throw:
                abort(f"No {cls.__tablename__} with id : {item_id}", 404)
            else:
                return False
        return True
