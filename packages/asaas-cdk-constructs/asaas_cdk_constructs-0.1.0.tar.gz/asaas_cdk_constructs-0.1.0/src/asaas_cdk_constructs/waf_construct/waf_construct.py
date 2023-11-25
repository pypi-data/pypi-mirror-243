import sys
import boto3

from aws_cdk import (
    Stack,
    aws_wafv2 as waf,
)
from constructs import Construct


class WafConstructStack(Stack):

    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            aws_profile: str,
            rate_limit: int,
            search_string_block_outside_access: list,
            is_allowed_asaas_ips: bool = True,
            addresses: list = [],
            ip_set_id: str = None,
            **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #
        # Define application name
        #
        application_name = self.stack_name.replace('WafConstructStack', '')

        try:
            if len(addresses) == 0 and is_allowed_asaas_ips is False:
                raise Exception
            elif is_allowed_asaas_ips is True and ip_set_id is None:
                raise Exception

            if is_allowed_asaas_ips is False:
                ipv4_arn = waf.CfnIPSet(
                    self,
                    f"{application_name}_Site_Api_Jobs",
                    name=f"{application_name}_Site_Api_Jobs",
                    addresses=addresses,
                    description=f"Allowed {application_name} IPs",
                    ip_address_version="IPV4",
                    scope="CLOUDFRONT",
                ).attr_arn
            else:
                session = boto3.Session(profile_name=aws_profile)
                wafv2 = session.client("wafv2")

                ip_set = wafv2.get_ip_set(
                    Name='Asaas_Site_Api_Jobs',
                    Scope='CLOUDFRONT',
                    Id=ip_set_id,
                )

                ipv4_arn = ip_set['IPSet']['ARN']

            #
            # WAF
            #
            rules = list()

            global_ip_rate_limit_rule = waf.CfnWebACL.RuleProperty(
                name='GlobalIpRateLimit',
                priority=1,
                action=waf.CfnWebACL.RuleActionProperty(
                    block=waf.CfnWebACL.BlockActionProperty()
                ),
                statement=waf.CfnWebACL.StatementProperty(
                    rate_based_statement=waf.CfnWebACL.RateBasedStatementProperty(
                        limit=rate_limit,
                        aggregate_key_type='IP'
                    )
                ),
                visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                    cloud_watch_metrics_enabled=True,
                    metric_name='GlobalIpRateLimit',
                    sampled_requests_enabled=True
                ),
            )

            rules.append(global_ip_rate_limit_rule)

            for block_outside_access in search_string_block_outside_access:
                block_api_outside_access = waf.CfnWebACL.RuleProperty(
                    name='BlockApiOutsideAccess',
                    priority=2,
                    action=waf.CfnWebACL.RuleActionProperty(
                        block=waf.CfnWebACL.BlockActionProperty()
                    ),
                    statement=waf.CfnWebACL.StatementProperty(
                        and_statement=waf.CfnWebACL.AndStatementProperty(
                            statements=[
                                waf.CfnWebACL.StatementProperty(
                                    not_statement=waf.CfnWebACL.NotStatementProperty(
                                        statement=waf.CfnWebACL.StatementProperty(
                                            ip_set_reference_statement=waf.CfnWebACL.IPSetReferenceStatementProperty(
                                                arn=ipv4_arn
                                            )
                                        )
                                    )
                                ),
                                waf.CfnWebACL.StatementProperty(
                                    byte_match_statement=waf.CfnWebACL.ByteMatchStatementProperty(
                                        field_to_match=waf.CfnWebACL.FieldToMatchProperty(uri_path={}),
                                        positional_constraint='STARTS_WITH',
                                        search_string=f'{block_outside_access}',
                                        text_transformations=[
                                            waf.CfnWebACL.TextTransformationProperty(
                                                type='NONE',
                                                priority=0
                                            )
                                        ]
                                    )
                                ),
                            ]
                        )
                    ),
                    visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                        cloud_watch_metrics_enabled=True,
                        metric_name='BlockApiOutsideAccess',
                        sampled_requests_enabled=True
                    ),
                )

                rules.append(block_api_outside_access)

            self.asaas_waf = waf.CfnWebACL(
                self, f'{application_name}-Waf',
                name=f'WAF-{application_name}-CloudFront',
                default_action=waf.CfnWebACL.DefaultActionProperty(allow={}),
                scope='CLOUDFRONT',
                visibility_config=waf.CfnWebACL.VisibilityConfigProperty(
                    cloud_watch_metrics_enabled=True,
                    metric_name=f'WAF-{application_name}-CloudFront',
                    sampled_requests_enabled=True
                ),
                rules=rules,
            )
        except Exception:
            if is_allowed_asaas_ips is False:
                print("A lista de endereços IP permitidos não foi fornecida, o padrão será PERMITIR todos os IPs através do WAF")
            elif is_allowed_asaas_ips is True:
                print("O id do recurso IP Set é obrigatório, quando a flag is_allowed_asaas_ips for TRUE")
            sys.exit(1)
