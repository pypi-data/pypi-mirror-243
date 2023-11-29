#!/usr/bin/env python3
# pylint: disable=wildcard-import,unused-wildcard-import

""" A minimal viable monitor"""

from minimon import *
from minimon.plugins import df, ps

with Monitor("MVM"):

    @view(("host", [Host("localhost")]))
    async def local_resources(host: Host) -> AInsights:
        """This async generator will be invoked by the above `view` and run continuously to
        gather and yield monitoring data"""
        async for insight in Bundler(
            ps=ps.generate(host) | ps.parse() | ps.check(),
            df=df.generate(host) | df.parse() | df.check(),
        ):
            yield insight
