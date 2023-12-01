
.. .. image:: https://readthedocs.org/projects/gh-action-open-id-in-aws/badge/?version=latest
    :target: https://gh-action-open-id-in-aws.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/workflows/test_github_action_open_id_in_aws/badge.svg
    :target: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/actions?query=workflow:test_github_action_open_id_in_aws

.. .. image:: https://codecov.io/gh/MacHu-GWU/gh_action_open_id_in_aws-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/gh_action_open_id_in_aws-project

.. image:: https://img.shields.io/pypi/v/gh-action-open-id-in-aws.svg
    :target: https://pypi.python.org/pypi/gh-action-open-id-in-aws

.. image:: https://img.shields.io/pypi/l/gh-action-open-id-in-aws.svg
    :target: https://pypi.python.org/pypi/gh-action-open-id-in-aws

.. image:: https://img.shields.io/pypi/pyversions/gh-action-open-id-in-aws.svg
    :target: https://pypi.python.org/pypi/gh-action-open-id-in-aws

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project

------

.. .. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://gh-action-open-id-in-aws.readthedocs.io/en/latest/

.. .. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://gh-action-open-id-in-aws.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-Install-blue.svg
    :target: `install`_

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/gh-action-open-id-in-aws#files


Welcome to ``gh_action_open_id_in_aws`` Documentation
==============================================================================
.. image:: https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/assets/6800411/b490626c-ef2f-4b86-850b-575dbe18c57e


Overview
------------------------------------------------------------------------------
To use GitHub Actions to deploy applications to AWS, we have to setup the permission properly.

The old school method is to use `Secret Environment Variable <https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions>`_ to store the `AWS IAM User <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html>`_ credentials. You can store `access key abd secret key <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html>`_ to the `AWS_ACCESS_KEY_ID 和 AWS_SECRET_ACCESS_KEY <https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html>`_ environment variables. This is also the solution used by CircleCI.

Around Nov 2021, AWS and GitHub made the official Open ID Connection (OIDC) available. It simplifies the process of granting AWS permissions to GitHub Actions. This is the AWS recommended way, and AWS explicitly mentioned that it is `NOT recommended to use long term IAM user credential for CI/CD <https://github.com/aws-actions/configure-aws-credentials#long-term-credentials-warning-10323>`_.

**This Python tool automates the process of setting up the GitHub action open id connection in AWS**.

Reference:

- `Configuring OpenID Connect in Amazon Web Services <https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services>`_: GitHub official doc.
- `Sample IAM OIDC CloudFormation Template <https://github.com/aws-actions/configure-aws-credentials#sample-iam-oidc-cloudformation-template>`_: AWS maintained github action.


How to Use
------------------------------------------------------------------------------
To setup GitHub action open id connection in AWS the first time, you can do the following. This code snippet creates the necessary resources using AWS CloudFormation:

.. code-block:: python

    from gh_action_open_id_in_aws.impl import setup_github_action_open_id_connection_in_aws

    setup_github_action_open_id_connection_in_aws(
        aws_profile="your_aws_profile_here",
        stack_name="cloudformation-stack-name-here",
        github_org="your-github-organization-name",
        github_repo="your_github_repo_name",
        role_name="the_iam_role_name_to_be_assumed_by_github_actions",
    )

If you have more Github repo need to access the same AWS accounts, and you want to give them different permission, you can do this. This code snippet reuse the OIDC Provider you created before and create a different IAM role, and configure IAM policy permission for the new GitHub repo:

.. code-block:: python

    from boto_session_manager import BotoSesManager
    from gh_action_open_id_in_aws.impl import setup_github_action_open_id_connection_in_aws

    aws_profile = "your_aws_profile_here"
    bsm = BotoSesManager(profile_name=aws_profile)
    role_name = "the_new_iam_role_name_to_be_assumed_by_github_actions"

    setup_github_action_open_id_connection_in_aws(
        aws_profile=aws_profile,
        stack_name="cloudformation-stack-name-here",
        github_org="your-github-organization-name",
        github_repo="another_github_repo_name",
        role_name=role_name,
        oidc_provider_arn=f"arn:aws:iam::{bsm.aws_account_id}:oidc-provider/token.actions.githubusercontent.com",
    )

    # let's say you want to give the new GitHub repo admin permission
    bsm.iam_client.attach_role_policy(
        RoleName=role_name,
        PolicyArn="arn:aws:iam::aws:policy/AdministratorAccess",
    )


GitHub Actions for Multi-AWS Accounts CI/CD IAM Permission Best Practice
------------------------------------------------------------------------------
If you have multiple GitHub Repositories using GitHub Actions to deploy applications to multiple environments in multiple AWS accounts, here is the best practice:

1. Supposes that you have three workload AWS Accounts ``dev_aws``, ``test_aws``, ``prod_aws``, and a ``devops_aws`` AWS account to store versioned code artifacts. These accounts could be different AWS accounts, either could be the same AWS account isolated by naming convention.
2. Supposes that you have one ``admin_repo`` GitHub repo to setup and test the cross AWS account IAM permission, and have multiple project GitHub repo ``project1_repo``, ``project2_repo``, etc ...
3. Run the following code to setup the GitHub Action OIDC provider in ``devops_aws`` account.

.. code-block:: python

    from gh_action_open_id_in_aws.impl import setup_github_action_open_id_connection_in_aws

    setup_github_action_open_id_connection_in_aws(
        # this AWS principal should have permission to deploy CloudFormation and IAM
        aws_profile="aws_profile_for_devops_aws",
        stack_name="admin-repo-with-hyphen",
        github_org="your-github-org",
        github_repo="admin_repo",
        role_name="admin_repo_role_name",
    )

4. For each project GitHub repo, run the following code to setup the IAM role in ``devops_aws`` AWS account, only for the given GitHub repo. Of course you can use ``${GitHubOrg}/*`` to give all GitHub repos in the same GitHub org the same permission, but this is not recommended.

.. code-block:: python

    from gh_action_open_id_in_aws.impl import setup_github_action_open_id_connection_in_aws

    setup_github_action_open_id_connection_in_aws(
        # this AWS principal should have permission to deploy CloudFormation and IAM
        aws_profile="aws_profile_for_devops_aws",
        stack_name="project1-repo-with-hyphen",
        github_org="your-github-org",
        github_repo="project1_repo",
        role_name="project1_repo_role_name",
    )

5. Then refer to the `cross_aws_account_iam_role <https://github.com/MacHu-GWU/cross_aws_account_iam_role-project>`_ Python library to setup the cross AWS account IAM roles for the ``project1_repo_role_name`` in ``devops_aws`` AWS Account.

**Note**:

In general, there are two ways to setup cross AWS account IAM permission in GitHub actions:

1. ONLY setup OIDC provider and IAM role in ``devops_aws`` account, and let the IAM role in ``devops_aws`` account to assume IAM role in ``dev_aws``, ``test_aws``, ``prod_aws`` account. This is the **recommended way**.
2. Setup OIDC provider and IAM role in ``devops_aws``, ``dev_aws``, ``test_aws``, ``prod_aws`` account. And use `aws-actions/configure-aws-credentials <https://github.com/aws-actions/configure-aws-credentials>`_ GitHub Action to switch between them. This is **NOT recommended**, because it introduce more complexity and more IAM permission to manage in workload AWS accounts, which increases the risk.

.. code-block:: yaml

    name: ...
    on: ...
    jobs:
      job_id:
        runs-on: ubuntu-latest
        steps:
          ..
          - name: Configure AWS credentials for DEVOPS
            uses: aws-actions/configure-aws-credentials@v3
            with:
              role-to-assume: arn:aws:iam::${{ secrets.DEVOPS_AWS_ACCOUNT_ID }}:role/devops_aws_iam_role
              role-session-name: sample_role_session
              aws-region: ${{ env.AWS_REGION }}
          - name: Configure AWS credentials for DEV
            uses: aws-actions/configure-aws-credentials@v3
            with:
              role-to-assume: arn:aws:iam::${{ secrets.DEV_AWS_ACCOUNT_ID }}:role/dev_aws_iam_role
              role-session-name: sample_role_session
              aws-region: ${{ env.AWS_REGION }}
          - name: Configure AWS credentials for TEST
            uses: aws-actions/configure-aws-credentials@v3
            with:
              role-to-assume: arn:aws:iam::${{ secrets.TEST_AWS_ACCOUNT_ID }}:role/test_aws_iam_role
              role-session-name: sample_role_session
              aws-region: ${{ env.AWS_REGION }}
          - name: Configure AWS credentials for PROD
            uses: aws-actions/configure-aws-credentials@v3
            with:
              role-to-assume: arn:aws:iam::${{ secrets.PROD_AWS_ACCOUNT_ID }}:role/prod_aws_iam_role
              role-session-name: sample_role_session
              aws-region: ${{ env.AWS_REGION }}


Developer Guide
------------------------------------------------------------------------------
This section is for developers who want to contribute to this project.

What under the hood is a CloudFormation template. The `gh_action_open_id_in_aws/cf.py <https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/blob/main/gh_action_open_id_in_aws/cf.py>`_ file contains the AWS CDK source code. The `cdk/cdk_synth.py <https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/blob/main/cdk/cdk_synth.py>`_ script can generate the JSON CloudFormation template using AWS CDK. The developer then can copy the output template to the `gh_action_open_id_in_aws/cft-{year}-{month}-{day}.json <https://github.com/MacHu-GWU/gh_action_open_id_in_aws-project/tree/main/gh_action_open_id_in_aws>`_ file and do local testing.


.. _install:

Install
------------------------------------------------------------------------------

``gh_action_open_id_in_aws`` is released on PyPI, so all you need is to:

.. code-block:: console

    $ pip install gh-action-open-id-in-aws

To upgrade to latest version:

.. code-block:: console

    $ pip install --upgrade gh-action-open-id-in-aws
