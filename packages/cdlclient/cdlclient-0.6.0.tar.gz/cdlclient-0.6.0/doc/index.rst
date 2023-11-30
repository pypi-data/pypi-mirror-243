DataLab Simple Client User Guide
================================

DataLab is a **generic signal and image processing software**
with unique features designed to meet industrial requirements.
It is based on Python scientific libraries (such as NumPy,
SciPy or scikit-image) and Qt graphical user interfaces (thanks to
the powerful `PlotPyStack`_ - mostly the `guidata`_ and `PlotPy`_ libraries).

For more details, see DataLab `Documentation`_.

DataLab Simple Client (``cdlclient`` package) is a Python library providing a
remote proxy to a DataLab application (server). It allows to use DataLab
features from a remote computer, and/or from a third-party application.

It also provides widgets to embed DataLab features in a Qt application
(connection dialog, etc.). For this particular use case, the library relies
on `QtPy`_.

.. figure:: _static/plotpy-stack-powered.png
    :align: center
    :width: 300 px

    DataLab is powered by `PlotPyStack <https://github.com/PlotPyStack>`_,
    the Python-Qt visualization and scientific graphical user interface stack.

External resources:
    .. list-table::
        :widths: 20, 80

        * - `Home`_
          - Project home page
        * - `PyPI`_
          - Python Package Index

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   overview
   api

Copyrights and licensing
------------------------

- Copyright © 2023 `Codra`_, Pierre Raybaut
- Licensed under the terms of the `BSD 3-Clause`_

.. _PlotPyStack: https://github.com/PlotPyStack
.. _guidata: https://pypi.python.org/pypi/guidata
.. _PlotPy: https://pypi.python.org/pypi/PlotPy
.. _QtPy: https://pypi.python.org/pypi/QtPy
.. _PyPI: https://pypi.python.org/pypi/DataLab
.. _Home: https://github.com/Codra-Ingenierie-Informatique/DataLabSimpleClient/
.. _Documentation: https://cdlapp.readthedocs.io/
.. _Codra: https://codra.net/
.. _BSD 3-Clause: https://github.com/Codra-Ingenierie-Informatique/DataLabSimpleClient/blob/master/LICENSE
