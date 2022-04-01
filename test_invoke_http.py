# test_invoke_http.py
from invokes import invoke_http

# invoke book microservice to get all books

# results = invoke_http("http://localhost:5000/book", method='GET')

# print( type(results) )
# print()
# print( results )

##################################################################################

# invoke book microservice to create a book
isbn = 'I01'
book_details = { "Quantity": 5, "Details": 213.00, "Expiry_date": "2022-03-18 12:19:01" }
create_results = invoke_http(
        "http://127.0.0.1:5000/inventory/" + isbn, method='POST', 
        json=book_details
    )

print()
print( create_results )

