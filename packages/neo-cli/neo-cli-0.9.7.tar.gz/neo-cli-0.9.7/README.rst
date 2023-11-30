Don't let all those templates and commands burden your head. Sit back,
relax and let :code:`neo-cli` asks what you need.

:code:`neo-cli` lower the barrier of understanding complicated templates,
memorizing long command and parameters to create your cloud
infrastructure. :code:`neo-cli` will interactively ask what you need.

In addition, :code:`neo-cli` aims to support diverse cloud platforms in near
future. So no matter what your cloud platforms is, :code:`neo-cli` will always be
your friend.

.. end-of-readme-intro

Installation
------------

.. code-block:: bash

    $ pip install neo-cli


Features
--------

* Support common OpenStack operation:
  ``creating vm``, ``listing vm, stack, network, floating ip``, and ``removing and
  updating stacks``.
* Auto-login for previous account.
* Support attaching local standard input, output, and error streams to a running machine.
* Can be used as library for your OpenStack application.

Take the tour
-------------

List your virtual machine
^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ neo ls vm

    +-----------+----------+------------+------------+----------+------- ---+--------+--------------------------+----------+
    | ID        | Name     | Key Pair   | Image      | Flavor   | RAM (GiB) |   vCPU | Addresses                | Status   |
    +===========+==========+============+============+==========+===========+========+========================+============+
    | 1bf4d720  | my-vm-1  | vm-key     | CentOS 7.5 | SS2.1    |         2 |      1 | network : default        | ACTIVE   |
    |           |          |            |            |          |           |        | fixed IP : 192.168.68.5  |          |
    +-----------+----------+------------+------------+----------+-----------+--------+--------------------------+----------+
    | 9ca3e7d10 | my-vm-2  | vm-key     | CentOS 7.5 | SS2.1    |         2 |      1 | network : default        | ACTIVE   |
    |           |          |            |            |          |           |        | fixed IP : 192.168.68.12 |          |
    +-----------------------------------------------------------------------------------------------------------------------


Some info omitted.

Attach local terminal to running machine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: bash

    $ neo attach vm c57a477b-84dc-4ae3-1234-5678
    2020-04-02 01:22:34 INFO Check your key pairs
    2020-04-02 01:22:38 INFO Done...
    2020-04-02 01:22:38 INFO Check username
    Username : centos
    Last login: Wed Jul 31 04:52:07 2019 from 123.456.68.101
    [centos@foo-vm ~]$

Creating stuffs
^^^^^^^^^^^^^^^

.. code-block:: bash

    $ neo create
    2020-04-02 01:25:57 ERROR Can't find neo.yml manifest file!
    Do you want to generate neo.yml manifest?  [y/n]? y

    Select Stack  :
    - clusters
    - networks
    - instances
    - others
    Enter your choice :

.. end-of-readme-usage

Project information
-------------------

* `Documentation <https://neo-cli.readthedocs.io/en/latest/index.html>`_
* `Contributing <https://neo-cli.readthedocs.io/en/latest/project/contributing.html>`_
* `Changelog <https://neo-cli.readthedocs.io/en/latest/project/changelog.html>`_
* `License <https://neo-cli.readthedocs.io/en/latest/project/license.html>`_
