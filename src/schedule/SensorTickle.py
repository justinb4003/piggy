import db.EqFetch as eqfetch
import asyncio


def execute():
    """
    Here we "tickle" every sensor in the system to keep their values
    up to date.

    Currently the BaseSensor class forces all sensors to implement a
    _refresh_value() method to update that value.  An optional
    _arefresh_value() method will the the convention used to specify an
    asyncio compatible version of _refresh_value().

    As implemented right now sensors will update in the sum of time it takes
    to update all of the non-async methods plus the time it takes the longest
    async method to complete.

    For a greenhouse enviromental control system that'll work just fine but
    something more sophisticated is desired... just not sure what yet.
    """

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    async_methods = []
    sync_methods = []
    for sid, s in eqfetch.get_all_sensors():
        if hasattr(s, '_arefresh_value'):
            # print("found aysnc refresh")
            async_methods.append(s._arefresh_value)
        else:
            # print("found NON_aysnc refresh")
            sync_methods.append(s._refresh_value)

    for m in sync_methods:
        m()

    async_tasks = [f() for f in async_methods]
    fin, unfin = loop.run_until_complete(
                    asyncio.wait(async_tasks,
                                 return_when=asyncio.ALL_COMPLETED))
    loop.close()
