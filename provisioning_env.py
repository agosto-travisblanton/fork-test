"""
Enhances the ``agar.env`` module to support a more environments
"""
from agar.env import on_server, appid, on_integration_server, on_development_server

#: ``True`` if running on a google server and the application ID ends in ``-stage``, ``False`` otherwise.
on_stage_server = on_server and appid.lower().endswith('-stage')

#: ``True`` if running on a google server and the application ID ends in ``-gamestop``, ``False`` otherwise.
on_gamestop_server = on_server and appid.lower().endswith('-gamestop')

on_continuous_integration_server = on_server and appid.lower().endswith('-ci')
on_qa_server = on_server and appid.lower().endswith('-qa')

on_production_server = (on_server and not on_integration_server and not on_stage_server
                        and not on_continuous_integration_server and not on_gamestop_server and not on_qa_server)

on_test_harness = not on_server and not on_development_server

#: ``True`` if running on a google server and the application ID ends in ``-stage``, ``False`` otherwise.
on_stage_server = on_server and appid.lower().endswith('-stage')
