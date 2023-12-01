# -*- coding: utf-8 -*-

from cross_aws_account_iam_role.impl import (
    mask_aws_account_id,
    mask_iam_principal_arn,
)


def test_mask_aws_account_id():
    assert mask_aws_account_id("123456789012") == "12********12"


def test_mask_iam_principal_arn():
    assert (
        mask_iam_principal_arn("arn:aws:iam::123456789012:role/role-name")
        == "arn:aws:iam::12********12:role/role-name"
    )


if __name__ == "__main__":
    from cross_aws_account_iam_role.tests import run_cov_test

    run_cov_test(__file__, "cross_aws_account_iam_role.impl", preview=False)
