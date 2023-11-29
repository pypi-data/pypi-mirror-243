|pypi| |actions| |codecov| |downloads|

edc-form-runners
----------------

Classes to manually run modelform validation for clinicedc/edc projects.

Rerun modelform validation
==========================

You can use the ``FormRunner`` to rerun modelform validation on all instances for a model. 

You could do this:

.. code-block:: python

    runner = FormRunner(modelform)
    runner.run()

If modelform validation does not validate, the validation message is captures in model ``Issue``.

You could also run for every model in your EDC deployment by getting the ``ModelForm`` class
from the ``admin`` registry and running ``FormRunner``:

.. code-block:: python

    from django.apps import apps as django_apps
    from edc_form_runners.form_runners import (
        FormRunner,
        FormRunnerError,
        get_modelform_cls,
        )

    for app_config in django_apps.get_app_configs():
        if app_config.name.startswith("edc_"):
            continue
        for model_cls in app_config.get_models():
            if model_cls == Appointment:
                continue
            print(model_cls._meta.label_lower)
            try:
                modelform = get_modelform_cls(model_cls._meta.label_lower)
            except FormRunnerError as e:
                print(e)
            else:
                print(modelform)
                try:
                    runner = FormRunner(modelform)
                except AttributeError as e:
                    print(f"{e}. See {model_cls._meta.label_lower}.")
                else:
                    try:
                        runner.run()
                    except (AttributeError, FieldError) as e:
                        print(f"{e}. See {model_cls._meta.label_lower}.")


You could also create a custom ``FormRunner`` for your model to add extra fields and ignore others.

For example:

.. code-block:: python

    class AppointmentFormRunner(FormRunner):
        def __init__(self, modelform_cls: ModelForm = None, **kwargs):
            modelform_cls = modelform_cls or AppointmentForm
            extra_fieldnames = ["appt_datetime"]
            ignore_fieldnames = ["appt_close_datetime"]
            super().__init__(
                modelform_cls=modelform_cls,
                extra_formfields=extra_fieldnames,
                ignore_formfields=ignore_fieldnames,
                **kwargs,
            )


.. |pypi| image:: https://img.shields.io/pypi/v/edc-form-runners.svg
  :target: https://pypi.python.org/pypi/edc-form-runners

.. |actions| image:: https://github.com/clinicedc/edc-form-runners/workflows/build/badge.svg?branch=develop
  :target: https://github.com/clinicedc/edc-form-runners/actions?query=workflow:build

.. |codecov| image:: https://codecov.io/gh/clinicedc/edc-form-runners/branch/develop/graph/badge.svg
  :target: https://codecov.io/gh/clinicedc/edc-form-runners

.. |downloads| image:: https://pepy.tech/badge/edc-form-runners
   :target: https://pepy.tech/project/edc-form-runners

