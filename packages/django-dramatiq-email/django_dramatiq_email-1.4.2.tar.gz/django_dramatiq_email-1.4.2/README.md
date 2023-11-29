# Django Dramatiq Email

Email backend for Django sending emails via Dramatiq.

This package is tested up to Django 4.2.

[![Pipeline Status](https://gitlab.com/sendcloud-public/django-dramatiq-email/badges/master/pipeline.svg)](https://gitlab.com/sendcloud-public/django-dramatiq-email/-/pipelines)
[![Code coverage Status](https://gitlab.com/sendcloud-public/django-dramatiq-email/badges/master/coverage.svg)](https://gitlab.com/sendcloud-public/django-dramatiq-email/-/pipelines)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://pypi.org/project/black/)

## Installation

To enable `django-dramatiq-email`, modify your project `settings.py`:

- Add `"django_dramatiq_email"` to `INSTALLED_APPS` below `"django_dramatiq"`,
- Set `EMAIL_BACKEND` to `"django_dramatiq_email.backends.DramatiqEmailBackend"`,
- Set `DRAMATIQ_EMAIL_BACKEND` to the actual email backend you want to use (SMTP, Anymail, etc),
- Optionally, add the `DRAMATIQ_EMAIL_TASK_CONFIG` dict as shown below.

## Configuration

The `dramatiq.actor` args ([reference](https://dramatiq.io/reference.html#dramatiq.actor), [user guide](https://dramatiq.io/guide.html)) for `send_email` can be set via the `DRAMATIQ_EMAIL_TASK_CONFIG` dict in your `settings.py`.

The default args are [here](django_dramatiq_email/tasks.py) - most notably, the default `queue_name` is `django_email`.

Example configuration (using the Retry middleware):

```python
DRAMATIQ_EMAIL_TASK_CONFIG = {
    "max_retries": 20,
    "min_backoff": 15000,
    "max_backoff": 86400000,
    "queue_name": "my_custom_queue"
}
```

## Bulk emails
Bulk emails are send using individual Dramatiq tasks. Doing so these tasks can be restarted individually.

## Maintainer
[Tim Drijvers](https://gitlab.com/timdrijvers)
