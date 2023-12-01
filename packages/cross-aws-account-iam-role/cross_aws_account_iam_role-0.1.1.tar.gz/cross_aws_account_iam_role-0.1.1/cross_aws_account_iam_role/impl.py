# -*- coding: utf-8 -*-

"""
This automation scripts can quickly set up a delegated cross AWS Account access
using IAM Role.

Assuming you have a grantee AWS Account and multiple owner AWS Accounts.
The grantee AWS Account has an identity (IAM User or IAM Role) that needs to
assume IAM Role in the owner AWS Accounts to perform some tasks on owner
AWS Accounts.

Please scroll to the bottom (below the ``if __name__ == "__main__":`` section)
to see the example usage.

Requirements:

- Python3.7+
- Dependencies::

    # content of requirements.txt
    cached-property>=1.5.2; python_version < '3.8'
    boto_session_manager>=1.5.2,<2.0.0
    aws_cloudformation>=1.5.1,<2.0.0
"""

import typing as T
import json
import dataclasses

try:
    from functools import cached_property
except ImportError:  # pragma: no cover
    from cached_property import cached_property

from boto_session_manager import BotoSesManager
from aws_cloudformation import deploy_stack, remove_stack

# ------------------------------------------------------------------------------
# IAM Arn data models
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class _IamArn:
    account: str

    @property
    def arn(self) -> str:
        raise NotImplementedError


@dataclasses.dataclass
class IamRootArn(_IamArn):
    @property
    def arn(self) -> str:
        return f"arn:aws:iam::{self.account}:root"

    @classmethod
    def parse_arn(cls, arn: str):
        return cls(account=arn.split(":")[4])


@dataclasses.dataclass
class _IamNamedArn(_IamArn):
    name: str

    def _make_arn(self, type: str) -> str:
        return f"arn:aws:iam::{self.account}:{type}/{self.name}"

    @classmethod
    def parse_arn(cls, arn: str):
        _, _, _, _, account, type_and_name = arn.split(":")
        name = type_and_name.split("/", 1)[1]
        return cls(account=account, name=name)


@dataclasses.dataclass
class IamUserArn(_IamNamedArn):
    @property
    def arn(self) -> str:
        return self._make_arn("user")


@dataclasses.dataclass
class IamRoleArn(_IamNamedArn):
    @property
    def arn(self) -> str:
        return self._make_arn("role")


@dataclasses.dataclass
class IamPolicyArn(_IamNamedArn):
    @property
    def arn(self) -> str:
        return self._make_arn("policy")


T_GRANTEE_ARN = T.Union[IamRootArn, IamUserArn, IamRoleArn]

# ------------------------------------------------------------------------------
# Grantee and Owner data models
# ------------------------------------------------------------------------------
@dataclasses.dataclass
class AwsContext:
    """
    :param bsm: the boto session manager for this AWS context.
    """

    bsm: BotoSesManager = dataclasses.field()


def get_managed_policy_property_name(iam_arn: T.Union[IamUserArn, IamRoleArn]) -> str:
    """
    Get the CloudFormation IamManagedPolicy property name for the given IAM ARN.
    """
    if isinstance(iam_arn, IamRoleArn):
        return "Roles"
    elif isinstance(iam_arn, IamUserArn):
        return "Users"
    else:
        raise TypeError


@dataclasses.dataclass
class Grantee(AwsContext):
    """
    Represents an AWS entity that needs to assume IAM Role in the owner AWS account.

    :param bsm: the boto session manager for this AWS context, it is used to
        provision necessary AWS resources for cross account access via CloudFormation.
    :param stack_name: cloudformation stack name to set up necessary resource
        for this grantee.
    :param iam_arn: the IAM ARN object of this grantee, could be one of
        :class:`IamRootArn`, :class:`IamUserArn`, :class:`IamRoleArn`.
        IAM Group cannot be a grantee.
    :param policy_name: the name of the IAM policy to attach to the grantee,
        which allows the grantee to assume the owner's IAM role.
    :param test_bsm: optional, the boto session manager represents the grantee
        for cross account access testing.
    """

    stack_name: str = dataclasses.field()
    iam_arn: T_GRANTEE_ARN = dataclasses.field()
    policy_name: str = dataclasses.field()
    test_bsm: T.Optional[BotoSesManager] = dataclasses.field(default=None)
    _owners: T.Dict[str, "Owner"] = dataclasses.field(default_factory=dict)

    @property
    def id(self) -> str:
        """
        A unique identifier for this grantee.
        """
        return self.iam_arn.arn

    @property
    def policy_arn(self) -> str:
        """
        The ARN of the IAM policy attached to this grantee.
        """
        return IamRoleArn(account=self.bsm.aws_account_id, name=self.policy_name).arn

    @property
    def policy_document(self) -> dict:
        """
        The IAM policy document attached to this grantee.
        """
        resource = [owner.role_arn for owner in self._owners.values()]
        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": "sts:AssumeRole",
                    "Resource": resource,
                },
            ],
        }

    def is_need_deploy(self) -> bool:
        """
        Do we need to deploy cloudformation for this grantee?
        """
        if len(self._owners) == 0:
            return False
        if isinstance(self.iam_arn, IamRootArn):
            return False
        return True

    @property
    def cft(self) -> dict:
        """
        The cloudformation template that defines the necessary AWS resources
        for cross account access.
        """
        tpl = {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {},
        }
        if isinstance(self.iam_arn, IamRootArn):
            pass
        else:
            managed_policy_properties = {
                "ManagedPolicyName": self.policy_name,
                "PolicyDocument": self.policy_document,
            }
            property_name = get_managed_policy_property_name(self.iam_arn)
            managed_policy_properties[property_name] = [self.iam_arn.name]
            tpl["Resources"]["GranteeIamPolicy"] = {
                "Type": "AWS::IAM::ManagedPolicy",
                "Properties": managed_policy_properties,
            }
        return tpl


@dataclasses.dataclass
class Owner(AwsContext):
    """
    Represents an AWS account that will allow an IAM entity from another AWS account
    to assume an IAM role on this account for some tasks.

    :param bsm: the boto session manager for this AWS context, it is used to
        provision necessary AWS resources for cross account access via CloudFormation.
    :param stack_name: cloudformation stack name to set up necessary resource
        for this owner.
    :param role_name: the name of the IAM role to be assumed by the IAM entity
        from another AWS account.
    :param policy_name: the name of the IAM policy to attach to the IAM role,
        this policy defines the permissions that the IAM entity from another AWS
        account can perform on this AWS account.
    :param policy_document: the policy document that defines the permissions
        that the IAM entity from another AWS account can perform on this AWS account.
    """

    stack_name: str = dataclasses.field()
    role_name: str = dataclasses.field()
    policy_name: str = dataclasses.field()
    policy_document: dict = dataclasses.field()
    _grantees: T.Dict[str, "Grantee"] = dataclasses.field(default_factory=dict)

    @property
    def id(self) -> str:
        """
        The unique identifier for this owner.
        """
        return self.role_arn

    @property
    def role_arn(self) -> str:
        """
        The ARN of the IAM role that will be assumed by the IAM entity from
        another AWS account.
        """
        return IamRoleArn(account=self.bsm.aws_account_id, name=self.role_name).arn

    @property
    def policy_arn(self) -> str:
        """
        The ARN of the IAM policy attached to the IAM role.
        """
        return IamRoleArn(account=self.bsm.aws_account_id, name=self.policy_name).arn

    def grant(self, grantee: "Grantee"):
        """
        Grant the given grantee to assume the IAM role.
        """
        if grantee.id not in self._grantees:
            self._grantees[grantee.id] = grantee
            grantee._owners[self.id] = self

    def revoke(self, grantee: "Grantee"):
        """
        Revoke the permission of given grantee to assume the IAM role.
        """
        if grantee.id in self._grantees:
            self._grantees.pop(grantee.id)
            grantee._owners.pop(self.id)

    @property
    def trusted_entities_document(self) -> dict:
        """
        The IAM policy document that defines the trusted entities that who
        can assume the IAM role.
        """
        arn_list = [grantee.iam_arn.arn for grantee in self._grantees.values()]
        arn_list.sort()
        return {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"AWS": arn_list},
                    "Action": "sts:AssumeRole",
                },
            ],
        }

    def is_need_deploy(self) -> bool:
        """
        Do we need to deploy cloudformation for this owner?
        """
        if len(self._grantees) == 0:
            return False
        return True

    @property
    def cft(self) -> dict:
        """
        The cloudformation template that defines the necessary AWS resources
        for cross account access.
        """
        return {
            "AWSTemplateFormatVersion": "2010-09-09",
            "Resources": {
                "OwnerIamRole": {
                    "Type": "AWS::IAM::Role",
                    "Properties": {
                        "AssumeRolePolicyDocument": self.trusted_entities_document,
                        "RoleName": self.role_name,
                        "Policies": [
                            {
                                "PolicyName": f"{self.role_name}-policy",
                                "PolicyDocument": self.policy_document,
                            },
                        ],
                    },
                }
            },
        }


def ensure_no_duplicate_accounts(
    grantee_list: T.List[Grantee],
    owner_list: T.List[Owner],
):
    grantee_account_list = [grantee.bsm.aws_account_id for grantee in grantee_list]
    owner_account_list = [owner.bsm.aws_account_id for owner in owner_list]
    if len(set(grantee_account_list)) != len(grantee_account_list):
        raise ValueError("Duplicate account IDs in grantee list")
    if len(set(owner_account_list)) != len(owner_account_list):
        raise ValueError("Duplicate account IDs in owner list")


def deploy(
    grantee_list: T.List[Grantee],
    owner_list: T.List[Owner],
    tags: T.Optional[T.Dict[str, str]] = None,
    skip_prompt: bool = True,
    verbose: bool = True,
):
    """
    Deploy the cross account access resources for the given grantee and owner

    :param grantee_list: The list of :class:`Grantee`.
    :param owner_list: The list of :class:`Owner`.
    :param tags: The tags to be attached to the cloudformation stack, it will be
        propagated to the IAM role and IAM policy.
    :param skip_prompt: default True; if False, you have to enter "Yes"
        in prompt to do deployment; if True, then execute the deployment directly.
    :param verbose: Whether to print verbose information.
    """
    # ensure_no_duplicate_accounts(grantee_list, owner_list)
    final_tags = {"tech:machine_creator": "cross_aws_account_iam_role"}
    if tags is not None:
        final_tags.update(tags)

    for grantee in grantee_list:
        if grantee.is_need_deploy():
            deploy_stack(
                bsm=grantee.bsm,
                stack_name=grantee.stack_name,
                template=json.dumps(grantee.cft),
                include_iam=True,
                include_named_iam=True,
                tags=final_tags,
                skip_plan=False,
                skip_prompt=skip_prompt,
                wait=True,
                timeout=60,
                on_failure_delete=True,
                verbose=verbose,
            )

    for owner in owner_list:
        if owner.is_need_deploy():
            deploy_stack(
                bsm=owner.bsm,
                stack_name=owner.stack_name,
                template=json.dumps(owner.cft),
                include_iam=True,
                include_named_iam=True,
                tags=final_tags,
                skip_plan=False,
                skip_prompt=skip_prompt,
                wait=True,
                timeout=60,
                on_failure_delete=True,
                verbose=verbose,
            )


def mask_aws_account_id(aws_account_id: str) -> str:
    """
    Example:

        >>> mask_aws_account_id("123456789012")
        '12*********12'
    """
    return aws_account_id[4][:2] + "*" * 8 + aws_account_id[4][-2:]


def mask_iam_principal_arn(arn: str) -> str:
    parts = arn.split(":")
    parts[4] = mask_aws_account_id(parts[4])
    masked_arn = ":".join(parts)
    return masked_arn


def get_account_info(
    bsm: BotoSesManager,
    masked_aws_account_id: bool = True,
) -> T.Tuple[str, str, str]:
    """
    Get the account ID, account alias and ARN of the given boto session.
    """
    res = bsm.sts_client.get_caller_identity()
    account_id = res["Account"]
    arn = res["Arn"]
    res = bsm.iam_client.list_account_aliases()
    account_alias = res.get("AccountAliases", ["unknown-account-alias"])[0]
    if masked_aws_account_id:
        account_id = mask_aws_account_id(account_id)
        arn = mask_iam_principal_arn(arn)
    return account_id, account_alias, arn


def print_account_info(
    bsm: BotoSesManager,
    masked_aws_account_id: bool = True,
):
    """
    Display the account ID, account alias and ARN of the given boto session.
    """
    account_id, account_alias, arn = get_account_info(bsm, masked_aws_account_id)
    print(
        f"now we are on account {account_id} ({account_alias}), using principal {arn}"
    )


def validate(
    grantee_list: T.List[Grantee],
    call_api: T.Callable,
    verbose: bool = True,
):
    """
    Validate the cross account permission of the grantee by calling the given API
    on the owner AWS account.

    :param grantee_list: The list of :class:`Grantee`
    :param call_api: The callable that will be called on the owner AWS account,
        it takes a :class:`BotoSesManager` as the only argument.
    :param verbose: Whether to print verbose information.
    """
    if verbose:
        print("Verify cross account assume role ...")
    for grantee in grantee_list:
        if verbose:
            account_id, account_alias, arn = get_account_info(grantee.test_bsm)
            print(
                f"We are on grantee account {grantee.bsm.aws_account_id} ({account_alias}), "
                f"using principal {arn}"
            )
        for owner in grantee._owners.values():
            if verbose:
                print(f"  Try to assume role {owner.role_arn} on owner account ...")
            bsm_new = grantee.test_bsm.assume_role(role_arn=owner.role_arn)
            call_api(bsm_new)


def delete(
    grantee_list: T.List[Grantee],
    owner_list: T.List[Owner],
    skip_prompt: bool = True,
    verbose: bool = True,
):
    """
    Delete the cross account access resources for the given grantee and owner.

    :param grantee_list: The list of :class:`Grantee`.
    :param owner_list: The list of :class:`Owner`.
    :param skip_prompt: default True; if False, you have to enter "Yes"
        in prompt to do deployment; if True, then execute the deployment directly.
    :param verbose: Whether to print verbose information.
    """
    for grantee in grantee_list:
        remove_stack(
            bsm=grantee.bsm,
            stack_name=grantee.stack_name,
            skip_prompt=skip_prompt,
            wait=True,
            timeout=60,
            verbose=verbose,
        )

    for owner in owner_list:
        remove_stack(
            bsm=owner.bsm,
            stack_name=owner.stack_name,
            skip_prompt=skip_prompt,
            wait=True,
            timeout=60,
            verbose=verbose,
        )
