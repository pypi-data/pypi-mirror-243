# -*- coding: utf-8 -*-

"""
This script automates the GitHub open id connect configuration in AWS.

Python >= 3.7 is required.

Requirements::

    boto_session_manager>=1.5.4,<2.0.0
    aws_cloudformation>=1.5.1,<2.0.0
"""

import typing as T

from boto_session_manager import BotoSesManager
import aws_cloudformation.api as aws_cf

from .paths import path_cft


def setup_github_action_open_id_connection_in_aws(
    aws_profile: str,
    stack_name: str,
    github_org: str,
    github_repo: str,
    role_name: str,
    oidc_provider_arn: str = "",
    tags: T.Optional[T.Dict[str, str]] = None,
    skip_prompt: bool = True,
    verbose: bool = True,
):
    """
    The OpenID Connect (OIDC) identity provider that allows the GitHub Actions
    to assume the role in the target account.

    :param aws_profile: the aws profile to set up the OpenID Connect (OIDC)
        identity provider in the target account.
    :param stack_name: the cloudformation stack name to set up the OpenID Connect
    :param github_org: the GitHub organization name trusted by the IAM role
    :param github_repo: the GitHub repository name trusted by the IAM role,
        could be "*"
    :param role_name: the IAM role name to be assumed by the GitHub Actions
    :param skip_prompt: default False; if False, you have to enter "Yes"
        in prompt to do deployment; if True, then execute the deployment directly.
    :param verbose: whether you want to log information to console
    """
    bsm = BotoSesManager(profile_name=aws_profile)
    final_tags = {
        "tech:human_creator": bsm.sts_client.get_caller_identity()["Arn"],
        "tech:machine_creator": "gh_action_open_id_in_aws",
    }
    if tags is not None:
        final_tags.update(tags)

    aws_cf.deploy_stack(
        bsm=bsm,
        stack_name=stack_name,
        template=path_cft.read_text(),
        parameters=[
            aws_cf.Parameter(key="GithubOrg", value=github_org),
            aws_cf.Parameter(key="GithubRepoName", value=github_repo),
            aws_cf.Parameter(key="RoleName", value=role_name),
            aws_cf.Parameter(key="OIDCProviderArn", value=oidc_provider_arn),
        ],
        skip_prompt=skip_prompt,
        include_named_iam=True,
        tags=final_tags,
        verbose=verbose,
    )
