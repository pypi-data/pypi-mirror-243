.. autosubmit documentation master file, created by
   sphinx-quickstart on Wed Mar 18 16:55:44 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

######################################
Welcome to autosubmit's documentation!
######################################

.. toctree::
   :maxdepth: 1
   :hidden:

   /introduction/index

.. toctree::
   :caption: Quick Start Guide
   :maxdepth: 1
   :hidden:

   /qstartguide/index

.. toctree::
   :caption: Installation
   :maxdepth: 1
   :hidden:

   /installation/index

.. toctree::
   :caption: User Guide
   :maxdepth: 2
   :hidden:

   /userguide/index
   /userguide/create/index
   /userguide/configure/index
   /userguide/defining_workflows/index
   /userguide/wrappers/index
   /userguide/run/index
   /userguide/modifying_workflow/index
   /userguide/manage/index
   /userguide/monitor_and_check/index
   /userguide/set_and_share_the_configuration/index
   /userguide/variables
   /userguide/expids
   /userguide/provenance

.. toctree::
   :caption: Database Documentation
   :maxdepth: 1
   :hidden:

   /database/index

.. toctree::
   :caption: Developer Guide
   :maxdepth: 1
   :hidden:

   /devguide/index

.. toctree::
   :caption: Troubleshooting
   :maxdepth: 1
   :hidden:

   /troubleshooting/index
   /troubleshooting/error-codes
   /troubleshooting/changelog

.. toctree::
   :caption: Module Documentation
   :maxdepth: 1
   :hidden:

   /moduledoc/index


Autosubmit is a Python software to manage complicated workflows on HPC platforms.

Automatization
   Autosubmit manages job submission and dependencies without user intervention
Data Provenance.
   Autosubmit assigns unique ID's to experiments, uses open standards, and
   applies other techniques to enable :doc:`data provenance </userguide/provenance>`
   in the experiments and workflows.
Failure Tolerance
   Autosubmit manages automatic retrials and has the ability to rerun specific parts of
   the experiment in case of failure
Resource Management
   Autosubmit supports a per-platform configuration, allowing users to run their experiments
   without adapting job scripts.
Multiple Platform
   Autosubmit can run jobs of an experiment in different platforms