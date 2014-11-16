

from clocked.config import allow_thread_unsafe_uuid


# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    import libuuid
    uuid1 = libuuid.uuid1
except:
    import uuid
    uuid1 = uuid.uuid1

    if allow_thread_unsafe_uuid:
        counter = 0

        def new_uid():
            global counter
            counter += 1
            return counter

        uuid1 = new_uid
