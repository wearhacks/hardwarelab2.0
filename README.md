# HardwareLab
Django based hardware inventory management system
# Installation

## Requirements

* `pip` - instructions [here](https://pip.pypa.io/en/latest/installing.html)
* `virtualenvwrapper` - instructions [here](https://virtualenvwrapper.readthedocs.org/en/latest/install.html)
* `npm` - instructions [here](https://docs.npmjs.com/getting-started/installing-node)

## Quick setup


```bash
$ mkvirtualenv hardwarelab
$ workon hardwarelab
(hardwarelab) $ pip install -r requirements.txt

(hardwarelab) $ python manage.py makemigrations
(hardwarelab) $ python manage.py migrate
(hardwarelab) $ python manage.py runserver
```

Now, open <http://127.0.0.1:8000/>.

## Usage

* To run on [localhost](http://127.0.0.1:8000/):

    ```bash
    $ workon hardwarelab
    (hardwarelab) $ python manage.py runserver
    ```
    
