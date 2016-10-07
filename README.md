[![Stories in Ready](https://badge.waffle.io/wearhacks/hardwarelab2.0.png?label=ready&title=Ready)](https://waffle.io/wearhacks/hardwarelab2.0)
# HardwareLab
Django based hardware inventory management system
# Installation

## Requirements

* `pip` - instructions [here](https://pip.pypa.io/en/latest/installing.html)
* `virtualenvwrapper` - instructions [here](https://virtualenvwrapper.readthedocs.org/en/latest/install.html)
* `npm` - instructions [here](https://docs.npmjs.com/getting-started/installing-node)
* `bower` - instructions [here](http://bower.io/#install-bower)

## Quick setup


```bash
$ mkvirtualenv hardwarelab
$ workon hardwarelab
(hardwarelab) $ pip install -r requirements.txt
(hardwarelab) $ bower install

(hardwarelab) $ python manage.py makemigrations
(hardwarelab) $ python manage.py migrate
(hardwarelab) $ python manage.py createsuperuser

(hardwarelab) $ python manage.py runserver
```

Now, open <http://127.0.0.1:8000/admin>.

## Usage 

* To run on [localhost](http://127.0.0.1:8000/):

    ```bash
    $ workon hardwarelab
    (hardwarelab) $ python manage.py runserver
    ```
    
