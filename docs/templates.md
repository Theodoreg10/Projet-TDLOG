## Templates

Here are the templates for all the pages of the website
### template
main template for all the page 
[full code](ok)

### login page
here the user can login

<details>
  <summary>Expand to see the code</summary>
  
  ```django
    {% extends 'template.html' %}
    {% load static %}
    {% block title %}Se connecter ou s'inscrire{% endblock %}
    {% block styles %}
        <link rel="stylesheet" type="text/css" href="{% static 'css/login.css' %}">
    {% endblock %}
    {% block carrousel %}{% endblock%}
    {% block content %}
        <div class="login">
            <div class="form">
                <form class="login-form" method="post">
                    {% csrf_token %}
                    {{ form.username.label_tag }}
                    {{ form.username }}
                    {{ form.password.label_tag }}
                    {{ form.password }}
                    <button type="submit">Se connecter</button>
                    <p><a href="register">Créer un compte</a></p>
                </form>
                {% if messages %}
                <ul class="messages">
                    {% for message in messages %}
                    <p {% if message.tags %} class="{{ message.tags }}"{% endif %} style="color: crimson;">{{ message }}</p>
                    {% endfor %}
                </ul>
                {% endif %}
            </div>
        </div>
    {% endblock %}
    {% block footer %}
    {% endblock %}
  ```
  

</details>
