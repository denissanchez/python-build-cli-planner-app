from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Iterable
from dateutil.parser import parse
from datetime import datetime


class DeadlinedMetaReminder(Iterable, metaclass=ABCMeta):
    @abstractmethod
    def is_due(self):
        pass


class DeadlinedReminder(Iterable, ABC):
    @classmethod
    def __subclasshook__(cls, subclass: type) -> bool:
        if cls is not DeadlinedReminder:
            return NotImplemented
        
        def attr_in_hierarchy(attr):
            return any(attr in SuperClass.__dict__ for SuperClass in subclass.__mro__)
        
        if not all(attr_in_hierarchy(attr) for attr in ('__iter__', 'is_due')):
            return NotImplemented
        
        return True

    @abstractmethod
    def is_due(self):
        pass

class DateReminder(DeadlinedReminder):
    def __init__(self, text: str, date: str) -> None:
        self.text = text
        self.date = parse(date, dayfirst=True)

    def is_due(self):
        return self.date <= datetime.now()
    
    def __iter__(self):
        return iter([self.text, self.date.isoformat()])
 