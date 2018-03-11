# GSS Metadata

## Authentication

Go to [Google developer console](https://console.developers.google.com/), and follow these [directions](http://gspread.readthedocs.org/en/latest/oauth2.html).

You should end up with a `credentials.json` file in the project directory. By default, gspread
expects this file to be there in order to authenticate. Don't forget to share your directories or documents with the service account user! The service account user's email address is specified in
the `client_email` field of the credentials file.

## Installation

```
mkvirtualenv --python=python3 gss
pipenv install
```
