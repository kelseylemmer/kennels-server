import json
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import (get_all_animals, get_single_animal, create_animal, delete_animal, update_animal, get_animal_by_location, get_animal_by_status,
                   get_all_customers, get_single_customer, get_customer_by_email, create_customer, delete_customer, update_customer,
                   get_all_employees, get_single_employee, get_employee_by_location, create_employee, delete_employee, update_employee,
                   get_all_locations, get_single_location, create_location, delete_location, update_location)

# Here's a class. It inherits from another class.
# For now, think of a class as a container for functions that
# work together for a common purpose. In this case, that
# common purpose is to respond to HTTP requests from a client.


class HandleRequests(BaseHTTPRequestHandler):
    # replace the parse_url function in the class
    def parse_url(self, path):
        """Parse the url into the resource and id"""
        parsed_url = urlparse(path)
        path_params = parsed_url.path.split('/')  # ['', 'animals', 1]
        resource = path_params[1]

        if parsed_url.query:
            query = parse_qs(parsed_url.query)
            return (resource, query)

        pk = None
        try:
            pk = int(path_params[2])
        except (IndexError, ValueError):
            pass
        return (resource, pk)

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        self._set_headers(200)
        response = {}  # Default response

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            (resource, id) = parsed

            if resource == "animals":
                if id is not None:
                    response = get_single_animal(id)
                else:
                    response = get_all_animals()
            if resource == "locations":
                if id is not None:
                    response = get_single_location(id)
                else:
                    response = get_all_locations()
            if resource == "customers":
                if id is not None:
                    response = get_single_customer(id)
                else:
                    response = get_all_customers()
            if resource == "employees":
                if id is not None:
                    response = get_single_employee(id)
                else:
                    response = get_all_employees()

        else:  # There is a ? in the path, run the query param functions
            (resource, query) = parsed

            # see if the query dictionary has an email key
            if query.get('email') and resource == 'customers':
                response = get_customer_by_email(query['email'][0])
            if query.get('location_id') and resource == 'animals':
                response = get_animal_by_location(query['location_id'][0])
            if query.get('location_id') and resource == 'employees':
                response = get_employee_by_location(query['location_id'][0])
            if query.get('status') and resource == 'animals':
                response = get_animal_by_status(query['status'][0])

        self.wfile.write(json.dumps(response).encode())

    # Here's a method on the class that overrides the parent's method.
    # It handles any POST request.
    def do_POST(self):
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        # Convert JSON string to a Python dictionary
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Initialize new resource
        new_resource = None

        # Add a new animal to the list. Don't worry about
        # the orange squiggle, you'll define the create function next.
        if resource == "animals":
            new_resource = create_animal(post_body)
        if resource == "customers":
            new_resource = create_customer(post_body)
        if resource == "employees":
            new_resource = create_employee(post_body)
        if resource == "locations":
            new_resource = create_location(post_body)

        # Encode the new resource and send in response
        self.wfile.write(json.dumps(new_resource).encode())

    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        # Delete a single animal from the list
        if resource == "animals":
            delete_animal(id)
        # Delete a single customer from the list
        if resource == "customers":
            delete_customer(id)
        # Delete a single employee from the list
        if resource == "employees":
            delete_employee(id)
        # Delete a single location from the list
        if resource == "locations":
            delete_location(id)

        # Encode the new and send in response
        self.wfile.write("".encode())

    # A method that handles any PUT request.
    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "animals":
            success = update_animal(id, post_body)
        # if resource == "customers":
        #     success = update_customer(id, post_body)
        # if resource == "employees":
        #     success = update_employee(id, post_body)
        # if resource == "locations":
        #     success = update_location(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # sets up a basic HTTP server that listens on port 8088.
    # The server handles HTTP OPTIONS requests and responds with the appropriate headers
    # for CORS support, allowing requests from any domain and specifying allowed methods
    # and headers. The server will run indefinitely, listening for incoming requests until it is manually stopped.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        # This header specifies which origins are allowed to access the server's resources.
        # In this case, the * wildcard means that any origin is allowed
        # (i.e., the server allows requests from any domain).
        self.send_header('Access-Control-Allow-Origin', '*')
        # This header indicates which HTTP methods are allowed for the resource.
        # The server is allowing GET, POST, PUT, and DELETE requests.
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        # This header specifies which request headers can be used during the actual request.
        # The server allows the 'X-Requested-With', 'Content-Type', and 'Accept' headers.
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        # This line ends the response headers and sends an empty line,
        # indicating that the response headers are complete.
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    # This line creates an instance of the HTTPServer class, specifying the host and port number
    # (in this case, an empty host and port 8088).
    # The HandleRequests class is used as the request handler, indicating that it will handle incoming HTTP requests.
    HTTPServer((host, port), HandleRequests).serve_forever()


# This block ensures that if the script is executed directly (not imported as a module),
# it calls the main() function, starting the server.
if __name__ == "__main__":
    main()
