A fictional api for patients of medicinal organisation.

It's depend on employees_api cause table definition are written by its orm (I now, now very good idea).
Both apis are similar. The main differences are: 
- Using stored procedures to communicate with database, instead of orm;
- Using JWT token, it is probably some less secure than bearer token, but do not need such many database querying;
- Make domain section, for validating data, and adding business logic.


Project architecture:

routers - related to HTTP thing, handling requests, adding headers and status code.

services - preparing data, authentication, sort of other programing things

domain - place for models, and business services, implementing business logic

repositories - a containers for related stored procedures

database - handling db connection

exceptions - some custom exceptions to decrease coupling between services, and router layer


Approach to tests is slightly better than in employees_api
There are unit test, and less E2E tests
The coverage is very poor and I need to write more tests.
Also, its lack of integration tests, but I found them hard to implement.
