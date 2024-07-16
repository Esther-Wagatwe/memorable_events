
from sqlalchemy import Table, Column, Integer, ForeignKey
from . import Base

event_vendor = Table('event_vendor', Base.metadata,
    Column('event_id', Integer, ForeignKey('Event.event_id')),
    Column('vendor_id', Integer, ForeignKey('Vendor.vendor_id'))
)