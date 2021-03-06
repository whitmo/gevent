import os
import traceback
import gevent


for count in xrange(2):
    for backend in gevent.core.supported_backends():
        hub = gevent.get_hub(backend, default=False)
        assert hub.loop.backend == backend, (hub.loop.backend, backend)
        gevent.sleep(0.001)
        fileno = hub.loop.fileno()
        if fileno is not None:
            print '%s. Testing %r: %r' % (count, backend, hub)
            os.close(fileno)
            try:
                gevent.sleep(0.001)
            except SystemError, ex:
                if '(libev)' in str(ex):
                    print 'The error is expected: %s' % ex
                else:
                    raise
            else:
                raise AssertionError('gevent.sleep() is expected to fail after loop fd was closed')
        else:
            print '%s. %r lacks fileno()' % (count, backend)
        hub.destroy()
        assert 'destroyed' in repr(hub), repr(hub)
