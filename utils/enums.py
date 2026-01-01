from enum import Enum 


class Role(str, Enum):
    QA = 'QA'
    DEV = 'DEV'
    PM = 'PM'


class Status(str, Enum):
    O = "Open"
    R = "Review"
    W = "Working"
    AR = "Awaiting Release"
    WQA = "Waiting QA"


class EventType(str, Enum):
    C = "Created"
    U = "Updated"
    D = "Deleted"
