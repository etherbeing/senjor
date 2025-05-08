Senjor Controllers
====================
Perhaps documenting this is a little of stating the facts, but controllers in Senjor are the same that controllers anywhere else (Like controllers in MVC web development), thus controllers are `Functions or methods that control how an input should be processed to create an specific output`, in this case the input is received through socket.io (websockets) and delivered back by the same protocol. 

Example Usage
--------------
Once you install the project you should now be able to quickly set your custom controllers as shown below:

.. code:: python

    from senjor import models
    from django.contrib.auth.models import get_user_model

    User = get_user_model()

    class SingletonExample(models.Model):
        """
        Example of usage in a singleton model
        """
        text = models.CharField(gql_resolve=lambda results: results.first().text) # This is the default behaviour if not gql_resolve is given
        class Schema:
            """
            Senjor Schema declaration, this is not needed unless you want to tweak your senjor API somehow like making this model singleton
            """
            is_singleton = True

    class BareExample(models.Model):
        """
        Example of using normal django integration with no customization
        """
        sender = models.ForeignKey(User, on_delete=models.CASCADE)
        text = models.CharField()

In the code above what could we expect, there we have a graphql schema as below

.. code:: graphql

    query ExampleQuery {
        singletonexample{
            text
        }
        bareexample{
            sender,
            text
        }
    }
    mutation ExampleMutation {
        singletonexample(
            text: "Hello world"
        ){
            _id # The default is to obtain the id of the newly created model in senjor
        }
        bareexample(
            sender: "<my_user_id>",
            text: "Hello world"
        ){
            _id
        }
    }
    subscription ExampleSubscription {
        singletonexample(
            text: "Hello world"
        ){
            _id # The default is to obtain the id of the newly created model in senjor
        }
        bareexample(
            sender: "<my_user_id>",
            text: "Hello world"
        ){
            _id
        }
    }

Filtering is also possible in queries for convenience, also there are some context variables that can be used, the context variables are shown below:

``Global context variable``

* `_user`: ``The current authenticated user``

``Input context variable (Only usable when receiving a query and not when sending a query)``

* `_id`: The _id of the model related mostly useful on mutations that creates and for mutations that queries this is an alias to `id`

You can access `_user` attributes by using `_user.<my_attribute>`.

Advanced Usage Examples
------------------------

.. code:: python
    
    from senjor import models
    from django.contrib.auth.models import get_user_model

    User = get_user_model()

    async def gql_subscribe_example(results):
        """
        The senjor engine sends an update each time the field used here is updated, this it does by listening to the attributes access, in the results object, it registered the access and then if the field is changed it triggers the generator, also for subscriptions purposes you should handle here the end of array if you don't want the subscription to end once the messages array is totally consumed 
        """
        async for message in results.first().messages:
            yield message

    class SenjorMessage(models.Model):
        message = models.CharField()
        sender = models.ForeignKey(User)

    class SenjorAdvancedExamples(models.Model):
        channel_id = models.UUIDField(gql_subscribe=gql_subscribe_example) # for subscriptions non async functions are transformed into async functions and you'd need a generator to deliver the value to the frontend
        messages = models.ManyToManyField(SenjorMessage)

The example above is all you'd need to create an RTC Chat using Senjor, the senjor.fields support the next parameters:

* gql_resolve: The callback used when resolving graphql queries, receives a function that receive the next parameters: 
   * results: The model QuerySet resulting from a query filtering.
* gql_subscribe: The callback used when subscribing to a value in graphql
   * results: The model QuerySet resulting from a subscription filtering.
* gql_mutate: The callback used when trying to mutate a value in graphql
   * results: The model QuerySet resulting from a mutation filtering.
