

# noinspection PyBroadException
try:
    # noinspection PyUnresolvedReferences
    import libuuid
    _uuid1 = libuuid.uuid1
    uuid1 = _uuid1
except:
    import uuid
    _uuid1 = uuid.uuid1
    uuid1 = _uuid1


_uuid_counter = 0


def toggle_thread_unsafe_uuid(on):
    global uuid1

    if on:
        def uid_gen():
            global _uuid_counter
            _uuid_counter += 1
            return _uuid_counter

        uuid1 = uid_gen
    else:
        uuid1 = _uuid1
