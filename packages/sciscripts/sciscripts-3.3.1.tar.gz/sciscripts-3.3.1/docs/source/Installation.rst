Installation
============


Simple
------

.. code-block:: console

   $ pip install --user 'sciscripts[full]'

Advanced
--------

If you:
- Plan to contribute to the code;
- Want to change the code and see the results on the fly;
- Want the most up-to-date version;

Then run these commands:

.. code-block:: console

   $ git clone https://gitlab.com/malfatti/SciScripts/ -b Dev
   $ cd SciScripts/
   $ pip install --user -e .

This will:

#. Clone the development branch of this repository;
#. Enter the cloned repository;
#. Install software dependencies using pip and install SciScripts as a link to the cloned repository.

Then manually install any missing optional dependencies that you might find while using the code.

If you fix/improve something, pull your changes back here! PRs are always welcome.



