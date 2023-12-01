
.. .. image:: https://readthedocs.org/projects/cross-aws-account-iam-role/badge/?version=latest
    :target: https://cross-aws-account-iam-role.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/workflows/test_cross_aws_account_iam_role/badge.svg
    :target: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/actions?query=workflow:test_cross_aws_account_iam_role

.. .. image:: https://codecov.io/gh/MacHu-GWU/cross_aws_account_iam_role-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/cross_aws_account_iam_role-project

.. image:: https://img.shields.io/pypi/v/cross-aws-account-iam-role.svg
    :target: https://pypi.python.org/pypi/cross-aws-account-iam-role

.. image:: https://img.shields.io/pypi/l/cross-aws-account-iam-role.svg
    :target: https://pypi.python.org/pypi/cross-aws-account-iam-role

.. image:: https://img.shields.io/pypi/pyversions/cross-aws-account-iam-role.svg
    :target: https://pypi.python.org/pypi/cross-aws-account-iam-role

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://cross-aws-account-iam-role.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://cross-aws-account-iam-role.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/cross-aws-account-iam-role#files


Welcome to ``cross_aws_account_iam_role`` Documentation
==============================================================================
.. image:: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/assets/6800411/5feed272-4d59-49b1-9e19-a6e465e88128

The best practice to setup AWS Account is using IAM assumed roles. You can grant an AWS Account (IAM root), an IAM User or an IAM Role to assume an IAM Role in another AWS Account. This is the most secure way to access AWS resources across AWS Accounts.

.. image:: https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/assets/6800411/598966ae-36ec-436a-a88e-c3e3135e7cc5

This Python tool can setup / modify / cleanup cross AWS account IAM permission at scale. See usage example below:

- `Grant IAM Root (entire AWS account) cross account IAM permission <https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/blob/main/example/use_iam_root_on_laptop.py>`_
- `Grant IAM User cross account IAM permission <https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/blob/main/example/use_iam_user_on_laptop.py>`_
- `Grant IAM Role cross account IAM permission <https://github.com/MacHu-GWU/cross_aws_account_iam_role-project/blob/main/example/use_iam_role_on_laptop.py>`_


.. _install:

Install
------------------------------------------------------------------------------

``cross_aws_account_iam_role`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install cross-aws-account-iam-role

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade cross-aws-account-iam-role
