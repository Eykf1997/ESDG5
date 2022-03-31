# test_invoke_http.py
from invokes import invoke_http

# invoke book microservice to get all books
results = invoke_http("http://localhost:5000/login", method='GET')

print( type(results) )
print()
print( results )

# invoke book microservice to create a book
login = 'glennaong'
login_details = {"admin_id" : "1", "password" : "password"}
create_results = invoke_http(
        "http://localhost:5000/login/" + login, method='DELETE', json = login_details
    )

print()
print( create_results )


