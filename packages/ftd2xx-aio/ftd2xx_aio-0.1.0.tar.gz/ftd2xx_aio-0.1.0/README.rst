==========
ftd2xx-aio
==========

|python|
|black|
|pdm|

ftd2xx-aio is an extension of `ftd2xx`_ (a wrapper around the `D2XX drivers`_ for FTDI devices)
that adds a transport/protocol layer (similar to `pyserial-asyncio`_). This allows the user to
take advantage of asynchronous callbacks on connections, rather than polling for data themselves.


------
Thanks
------

Parts of this code are inspired by or directly copied from the work of the pyserial team
(`pyserial-asyncio`_) which is under BSD3 license. This project is possible because of their
good work for the open source community. Thank you!

And, of coarse, thank you Satya for your work on `ftd2xx`_! I have truly enjoyed contributing
to your project here and there. You are so great to work with!


.. _ftd2xx: https://github.com/snmishra/ftd2xx

.. _pyserial-asyncio: https://github.com/pyserial/pyserial-asyncio

.. _D2XX drivers: http://www.ftdichip.com/Drivers/D2XX.htm


.. |black|
    image:: https://img.shields.io/badge/code%20style-black-000000.svg
        :target: https://github.com/psf/black
.. |python|
    image:: https://img.shields.io/badge/python-3.9%2B-blue.svg
        :target: https://www.python.org/
.. |pdm|
    image:: https://img.shields.io/badge/pdm-managed-blueviolet
        :target: https://pdm.fming.dev
