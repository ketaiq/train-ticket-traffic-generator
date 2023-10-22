from enum import Enum


class Role(Enum):
    Irregular_Budget = 0
    Irregular_Normal = 1
    Irregular_Comfort = 2
    Regular = 3
    Cancel_No_Refund = 4
    Cancel_With_Refund = 5
    Sales_Add_Order = 6
    Sales_Add_Update_Order = 7
    Sales_Delete_Order = 8
