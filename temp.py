from functions import ComputeHandler, get_results
import pandas as pd


uid = "123"
path = r""
col = ""


x = ComputeHandler(
    user_id= uid,
    file_name= "temp.csv",
    df = pd.read_excel(path),
    column_name= col,
    operation= "average"
)
x.workflow()



y = get_results(uid)
print(y)
