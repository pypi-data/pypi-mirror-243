# -*- coding: utf-8 -*-

import aws_cdk as cdk
import aws_cdk.aws_iam as iam
from constructs import Construct


class Stack(cdk.Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.declare_params()
        self.declare_conditions()
        self.declare_resources()

    def declare_params(self):
        self.param_github_org = cdk.CfnParameter(
            self,
            "GithubOrg",
            type="String",
            description="Name of GitHub organization/user (case sensitive)",
        )
        self.param_github_repository_name = cdk.CfnParameter(
            self,
            "GithubRepoName",
            type="String",
            description="Name of GitHub repository (case sensitive)",
        )
        self.param_oidc_provider_arn = cdk.CfnParameter(
            self,
            "OIDCProviderArn",
            type="String",
            description="Arn for the GitHub OIDC Provider. (optional)",
            default="",
        )
        self.param_oidc_audience = cdk.CfnParameter(
            self,
            "OIDCAudience",
            type="String",
            description="Audience supplied to configure-aws-credentials",
            default="sts.amazonaws.com",
        )
        self.param_iam_role_name = cdk.CfnParameter(
            self,
            "RoleName",
            type="String",
            description="Name of the IAM role to be assumed by GitHub Actions",
        )

    def declare_conditions(self):
        self.cond_create_oidc_provider = cdk.CfnCondition(
            self,
            "CreateOIDCProvider",
            expression=cdk.Fn.condition_equals(
                self.param_oidc_provider_arn.value_as_string,
                "",
            ),
        )

    def declare_resources(self):
        self.github_oidc_provider = iam.CfnOIDCProvider(
            self,
            "GitHubOIDCProvider",
            url="https://token.actions.githubusercontent.com",
            client_id_list=[
                "sts.amazonaws.com",
            ],
            thumbprint_list=[
                "ffffffffffffffffffffffffffffffffffffffff",
            ],
        )
        self.github_oidc_provider.cfn_options.condition = self.cond_create_oidc_provider

        self.github_action_iam_role = iam.CfnRole(
            self,
            "GitHubActionRole",
            role_name=self.param_iam_role_name.value_as_string,
            assume_role_policy_document={
                "Version": "2008-10-17",
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {
                            "Federated": cdk.Fn.condition_if(
                                self.cond_create_oidc_provider.logical_id,
                                self.github_oidc_provider.ref,
                                self.param_oidc_provider_arn.value_as_string,
                            ),
                        },
                        "Action": "sts:AssumeRoleWithWebIdentity",
                        "Condition": {
                            "StringEquals": {
                                "token.actions.githubusercontent.com:aud": self.param_oidc_audience.value_as_string,
                            },
                            "StringLike": {
                                "token.actions.githubusercontent.com:sub": cdk.Fn.sub(
                                    "repo:${github_org}/${github_repo_name}:*",
                                    {
                                        "github_org": self.param_github_org.value_as_string,
                                        "github_repo_name": self.param_github_repository_name.value_as_string,
                                    },
                                )
                            },
                        },
                    }
                ],
            },
        )
