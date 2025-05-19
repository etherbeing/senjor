Schema
=======
Handles the schema generation.

Architecture
-------------
NOTE: Please setup a UML image here for a better architecture representation

--------------------------
| GQLField               |
|------------------------|
| Description: It handles field args, and field level operations like subscriptions, queries and mutations|
|------------------------|
| Methods:              |
|-----------------------|
| _gql_get_kwargs(void): Gets the arguments of the field |
|-------------------------|
| get_gql_field(type: GQLSchemaType): It returns the expected graphql field for the Schema |
|--------------------------|
