# Technical test

Prisma has considered developing an expense management and control system to help its employees control their monthly budget. control system so that they can control their monthly budget. For this purpose, it is requested to develop the
Back-end layer services using the necessary technologies (you can use the technology that you best handle, but preferably technology, but preferably Python).

## Technologies
 - Python
 - Flask
 - SQLAlchemy
 - Marshmallow
 - Flask-JWT
 - Flask-Restful
 - Blueprint

## Installation
1. We start with the installation of the virtual environment by executing the following command.
```bash
py -3 -m venv venv
```
2. Activate the Virtual enviroment
```bash
venv\Scripts\activate
```
3. Install the dependencies by executing the following command:
```bash
pip install -r requirements.txt
```
4. Run the project by executing the following command:
```bash
py entrypoint.py
```
## Architecture
The architecture used for the development of the backend and construction of the API is REST, used mainly for being light in interactions between client and server. 
It is a type of web development architecture that relies entirely on the HTTP standard. 

Two modules are managed, an authentication module and a user module, the authentication module allows the user to log in by returning a jwt token that will be used as bearer token in the API to make requests to the user module. The user module allows the user to insert, update, delete and view his bills.

![alt text](https://github.com/GenesisDaniela/test-prisma/blob/master/arquitectura.jpeg)

### Flask-Restful

A library called flaskrestful was used to build the API in a simple and more efficient way, Flask-RESTful encourages best practices with minimal setup.

For the management of routes, the resources.py files are managed inside the "api" directory, the 2 URLs are defined
> test-prisma/financialControl/routes/auth/api/resource.py
```bash
api.add_resource(AuthResource, '/login', endpoint='login_resource')
```
> test-prisma/financialControl/routes/user/api/resource.py
```bash
api.add_resource(UserBillsIdResource, '/<string:user>/bills/<int:bill_id>', endpoint='user_bill_resource')
api.add_resource(UserBillsResource, '/<string:user>/bills', endpoint='user_list_resource')
```
then the implementation of the GET, POST, DELETE, PUT methods respective to the 2 urls is done by means of a class.

> test-prisma/financialControl/routes/user/api/resources/UserBillsResource.py
```bash
class UserBillsResource(Resource):
    @cross_origin()
    @token_required
    def get(self,user): 
        try:
            user_found = User.simple_filterByOne(username=user)
            bills = Bill.simple_filter(user_id=user_found.id)
        except NoResultFound:
            return {f"user {user} not found"}, 404
        response = billsSchema.dump(bills)
        return response
    
    @cross_origin()
    @token_required
    def post(self,user):
        try:
            user_found = User.simple_filterByOne(username=user)
            data = request.get_json()
            bill = Bill(None, user_found.id, data["value"], data["type"], data["observation"])
        except Exception:
            return {'mgs': 'Incorrect fields, try again'}, 400
        Bill.save(bill)
        return billSchema.dump(bill)
```

> test-prisma/financialControl/routes/user/api/resources/UserBillsResource.py
```bash
class UserBillsIdResource(Resource):
    @cross_origin()
    @token_required
    def get(self, user, bill_id):
        try:
            user = User.simple_filterByOne(username=user)
        except NoResultFound:
            return {'msg':f'user with username: \'{user}\' not found'}, 404
        try:
            bill = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':'bill not found'}, 404
        if(user.id != bill.user_id):
            return {'msg':'user can only get their own bills'}, 401
        return billSchema.dump(bill)
    
    @cross_origin()
    @token_required
    def delete(self, user, bill_id):
        try:
            user = User.simple_filterByOne(username=user) 
        except NoResultFound:
            return {'msg':f'user with username: \'{user}\' not found'}, 404
        try: 
            bill = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':'bill not found'}, 404
        if(user.id != bill.user_id):
            return {'msg':'user can only delete their own bills'}, 401
        Bill.delete(bill)
        return billsSchema.dump(Bill.get_all())
    
    @cross_origin()
    @token_required
    def put(self, user, bill_id): 

        try:
            user = User.simple_filterByOne(username=user) 
        except NoResultFound:
            return {'msg':f'user with username: \'{user}\' not found'}, 404
        try: 
            billFound = Bill.simple_filterByOne(id = bill_id)
        except NoResultFound:
            return {'msg':f'bill with id: \'{bill_id}\' of the user \'{user}\' not found'}, 404
        try:
            data = request.get_json()
            if "type" in data:
                billFound.type_ = data["type"]
            if "observation" in data:
                billFound.observation = data["observation"]
            if "value" in data:
                billFound.value = data["value"]
        except:
            return {'mgs': 'Incorrect fields, try again'}, 400
        Bill.update(billFound)
        return billSchema.dump(billFound)
```
