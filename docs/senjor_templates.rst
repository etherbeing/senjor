Senjor Templates
==========================

Senjor templates is a django template processor built over django, the main goal of this is to make the page reactive and modern by integrating django along with ReactJS.

Main features:

* django components now become react components
* scripts and assets are now loaded per demand (like qwik does) to avoid bandwith consumption
* You can either migrate your django model to use react or keep using django default templates syntax to program with the same features that react does.
* You're now able to import ReactJS styles, and components into your Django project
* Supports GraphQL over Socket.IO out of the box, with a TS/JS api to do your queries
* By default `{% url '' %}` django template tags now load your pages in a reactive form.

.. note::
    `Senjor is the framework for senjors built over django for perfeccionist with deadlines.`

Example Usage
--------------

.. code:: django

    {% comment 'home.html' %}
    {% extends 'myapp/base.html' %}
    {% include 'myapp/header.html' %}
    <div> Hello world </div>
    <a href="{% url 'myurl' %}"></a>
    {% include 'myapp/footer.html' %}

Imagine a code as above, that would translate into a folder called: `_frontend` on the root of your project containing a typical react structure and furthermore you should notice the next folders:

1. layouts: Contains the base.html definition in the react form, is extracted from the extends block, and it contains stuff like head and other things that is usually referenced on each file, `Senjor` generates components used in the extends directive with the same path relative to the templates root to avoid conflicts, the resulting name for the file would be something like base.tsx.
2. components: Contains the components of the project typically obtained from the include directive, and as the layouts the name and path are equal for example `header.tsx` and `footer.tsx` for the previous example. The remaining code creates a component with the name of the template that used all of the layouts and components, for example would be something like `home.tsx`.
3. utils: Here goes some utility tools that senjor determines should be used in the frontend project, for example api integrations and more.

In the example above url templatetag would use react-router-dom and make the page reactive.

Engine Behaviour
------------------

Let's not complicate things instead of integrating directly with something like webpack and django and some kind of tricky binding between nodejs and python, we are just going to write the snippets of codes into the files generated with the Vite framework, this way when we integrate with the dev ecosystem of vite. When a template of django is modified, we write the corresponding file in vite, for this we use a middle point that is a json object that contains, all components, links, layouts and utilities as well as file linking, when a file changes we drops the linked files and rebuild it again, then let vite live reload to do its job and such the dev could have a very fancy and integrated dev environment using django+react.

ReactJS to Django, won't be implemented in version 2.0.x but instead in 3.0.x