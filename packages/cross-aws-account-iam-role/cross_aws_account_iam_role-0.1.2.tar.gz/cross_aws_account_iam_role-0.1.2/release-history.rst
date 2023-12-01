.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.2 (2023-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- By default the ``validate()`` method will mask AWS account id and IAM principal ARN.

**Bugfixes**

- Fix a bug that the masked aws account id doesn't looks right.


0.1.1 (2023-11-30)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Add the following public API:
    - ``cross_aws_account_iam_role.api.IamRootArn``
    - ``cross_aws_account_iam_role.api.IamUserArn``
    - ``cross_aws_account_iam_role.api.IamRoleArn``
    - ``cross_aws_account_iam_role.api.T_GRANTEE_ARN``
    - ``cross_aws_account_iam_role.api.Grantee``
    - ``cross_aws_account_iam_role.api.Owner``
    - ``cross_aws_account_iam_role.api.deploy``
    - ``cross_aws_account_iam_role.api.mask_aws_account_id``
    - ``cross_aws_account_iam_role.api.mask_iam_principal_arn``
    - ``cross_aws_account_iam_role.api.get_account_info``
    - ``cross_aws_account_iam_role.api.print_account_info``
    - ``cross_aws_account_iam_role.api.validate``
    - ``cross_aws_account_iam_role.api.delete``
