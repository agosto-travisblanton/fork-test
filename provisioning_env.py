"""
Enhances the ``agar.env`` module to support a more environments
"""
from agar.env import on_server, appid, on_integration_server, on_development_server

on_test_harness = not on_server and not on_development_server

on_continuous_integration_server = on_server and appid.lower().endswith('-ci')

on_qa_server = on_server and appid.lower().endswith('-qa')

on_stage_server = on_server and appid.lower().endswith('-stage')

on_gamestop_server = on_server and appid.lower().endswith('-gamestop')

on_production_server = (on_server
                        and not on_continuous_integration_server
                        and not on_integration_server
                        and not on_qa_server
                        and not on_stage_server
                        and not on_gamestop_server)
