# -*- coding: utf-8 -*-

from cross_aws_account_iam_role import api


def test():
    _ = api
    _ = api.IamRootArn
    _ = api.IamUserArn
    _ = api.IamRoleArn
    _ = api.T_GRANTEE_ARN
    _ = api.Grantee
    _ = api.Owner
    _ = api.deploy
    _ = api.mask_aws_account_id
    _ = api.mask_iam_principal_arn
    _ = api.get_account_info
    _ = api.print_account_info
    _ = api.validate
    _ = api.delete


if __name__ == "__main__":
    from cross_aws_account_iam_role.tests import run_cov_test

    run_cov_test(__file__, "cross_aws_account_iam_role.api", preview=False)
