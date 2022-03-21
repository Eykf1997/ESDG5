# # test_invoke_http.py
from invokes import invoke_http

# invoke inventory microservice to get all bouquet
results = invoke_http("http://localhost:5000/inventory", method='GET')

print( type(results) )
print()
print( results )

#invoke inventory microservice to create a bouquet
# Item_Id = '8'
# bouquet_details = {"Quantity": "2", "Details": "Mixture of flowers", "Expiry_Date": "5/05/2022", "Item_Name": "Condolence Stands", "Price": 230 }
# create_results = invoke_http(
#         "http://localhost:5000/inventory/" +Item_Id, method='POST', 
#         json=bouquet_details

# )

# print()
# print(create_results)