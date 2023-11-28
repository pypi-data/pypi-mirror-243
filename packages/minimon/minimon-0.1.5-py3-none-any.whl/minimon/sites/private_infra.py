#!/usr/bin/env python3

""" Monitor my private infrastructure
Todo
- wth: monitor networks
"""

from minimon.builder import AInsights, Bundler, ConfigBase, Host, Monitor, view
from minimon.plugins import df, dmesg, ps


class HostConfig(ConfigBase):
    """Individual Host configuration"""

    df_parse: None | df.ParseOptions = None
    df_check: None | df.CheckOptions = None


hostconfigs = HostConfig.create_multiple((
    {"host": Host("localhost", ssh_user="root")},
    # {"host": {"name": "localhost", "ssh_user": "root"}},
    {"host": Host("om-office.de", ssh_port=2222, ssh_user="root")},
    {"host": Host("zentrale", ssh_user="pi"),
        "df_parse": {"mountpoint_opt_in": "^/$"}},
    # Host("reMarkable"),
    {"host": Host("SHIFT6mq", ssh_port=2222),
        "df_parse": {"mountpoint_opt_in": "^/storage/.*$"},
    },
))

with Monitor("Private infra"):

    @view(("config", hostconfigs))
    async def local_resources(config: HostConfig) -> AInsights:
        """Provides quick summary of system sanity"""
        async for insight in Bundler(
            df=df.generate(config.host) | df.parse(config.df_parse) | df.check(config.df_check),
            ps=ps.generate(config.host) | ps.parse() | ps.check(),
            dmesg=dmesg.generate(config.host) | dmesg.parse() | dmesg.check(),
            # process_output(host, "ss --oneline --numeric --resolve --processes --info", "3"),
            # dos=Pipeline(process_output(host, "while true; do date; done", "1")),
        ):
            yield insight
