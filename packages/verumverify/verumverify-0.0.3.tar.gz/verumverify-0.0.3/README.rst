Verum Verify: Authenticity Verifier for VerumJourno
========================================
.. image:: https://github.com/Ethosym/verumverify/actions/workflows/ci.yml/badge.svg
    :target: https://travis-ci.org/cgdeboer/verumverify

.. image:: https://img.shields.io/pypi/v/verumverify.svg
    :target: https://pypi.org/project/verumverify/

.. image:: https://img.shields.io/conda/vn/conda-forge/verumverify.svg
    :target: https://anaconda.org/conda-forge/verumverify

Verum Verify is a public, open-source library that provides tools for verifying the authenticity
of content posted to verumjourno.com

.. image:: https://github.com/Ethosym/verumverify/blob/main/docs/verumverify.png?raw=true


Example Code:

.. code-block::

    $ verumverify --hash_id 7708e5e103f71fd65af14a33747755836690545b8873f228dd43bbf17ee42a21

    Verify Authenticity of Hash: 7a06d927e5f16f96d22f681b6ceaf6c8b12aab14523012bd3c215c7f11b19ae2

    Locating and retrieving files...OK
    Loading data and signature files...OK
    Loading public key files...OK

            Video 'A bright and sunny day' was recording on
            an Android T2Q on Samsung
            called Chris's Android
            at around 2023-11-16 23:05:54.

    Verifying Timestamps Authenticity
    2023-11-16 23:05:54...OK
    Verifying Sensor Authenticity
    | TEMPERATURE |...OK
    | PROXIMITY |...OK
    | ACCELEROMETER |...OK
    | GPS |...OK
    | GYROSCOPE |...OK
    | HUMIDITY |...OK
    | LIGHT |...OK
    | DATE |...OK
    | PRESSURE |...OK
    Verifying Recording Authenticity
    | recording |...OK
    Verifying Device Authenticity
    | device |...OK


How It Works
---------------
Verum Verify provides a single command line callable, :code:`verumverify` that takes one of
of the following inputs:

hash_id:
    The hash value of a recording from verumjourno.com

id:
    The ID of a recording from verumjourno.com

url:
	The full URL of a recording from verumjourno.com

zipfile:
    A zipfile of all recorded sensor data (downloadable from verumjourno.com)

videofile:
    A original full-resolution MP4 video

The :code:`verumverify` command will verify the authenticity of the recording, the device that
made the recording, all sensor data associated with the recording, and an external timestamp
of when the recording occurred.

Verum Verify officially supports Python 3.6+.

Installation
------------

To install Verum Verify, use:
-  `pipenv <http://pipenv.org/>`_ (or pip, of course)
- `conda <https://docs.conda.io/en/latest/>`_ (or anaconda, or course)
- or wherever you get your python packages.

.. code-block:: bash

    $ pip install verumverify

    $ verumverify --hash_id <hash>

    $ verumverify --videofile /path/to/your/video.mp4

Documentation
-------------

See https://verumjourno/posts/faq for more information.

Verum Verify relies on these open-source libraries for cryptography and timestamping:
-  `cryptography <https://github.com/pyca/cryptography>`_
-  `rfc3161ng <https://github.com/trbs/rfc3161ng>`_


How to Contribute
-----------------

#. Check for open issues or open a fresh issue to start a discussion around a feature idea or a bug.
#. Fork `the repository`_ on GitHub to start making your changes to the **main** branch (or branch off of it).
#. Send a pull request. Make sure to add yourself to AUTHORS_.

.. _`the repository`: https://github.com/cgdeboer/verumverify
.. _AUTHORS: https://github.com/cgdeboer/verumverify/blob/master/AUTHORS.rst
