#!/usr/bin/env bash
cd examples/requirements/
pip-compile base.in "$@" --upgrade
pip-compile code_style.in "$@" --upgrade
pip-compile common.in "$@" --upgrade
pip-compile coreapi_coreschema.in "$@" --upgrade
pip-compile debug.in "$@" --upgrade
pip-compile deployment.in "$@" --upgrade
pip-compile dev.in "$@" --upgrade
pip-compile django_2_2.in "$@" --upgrade
pip-compile django_2_2_and_elastic_6x.in "$@" --upgrade
pip-compile django_2_2_and_elastic_7x.in "$@" --upgrade
pip-compile django_3_1.in "$@" --upgrade
pip-compile django_3_1_and_elastic_6x.in "$@" --upgrade
pip-compile django_3_1_and_elastic_7x.in "$@" --upgrade
pip-compile django_3_2.in "$@" --upgrade
pip-compile django_3_2_and_elastic_6x.in "$@" --upgrade
pip-compile django_3_2_and_elastic_7x.in "$@" --upgrade
pip-compile docs.in "$@" --upgrade
pip-compile documentation.in "$@" --upgrade
pip-compile elastic.in "$@" --upgrade
pip-compile elastic_6x.in "$@" --upgrade
pip-compile elastic_7x.in "$@" --upgrade
pip-compile test.in "$@" --upgrade
pip-compile testing.in "$@" --upgrade
