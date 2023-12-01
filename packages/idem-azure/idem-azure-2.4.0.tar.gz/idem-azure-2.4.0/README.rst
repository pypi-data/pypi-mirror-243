===============
idem-azure
===============

.. image:: https://img.shields.io/badge/made%20with-pop-teal
   :alt: Made with pop, a Python implementation of Plugin Oriented Programming
   :target: https://pop.readthedocs.io/

.. image:: https://img.shields.io/badge/made%20with-idem-teal
   :alt: Made with idem, a Python implementation of Plugin Oriented Programming
   :target: https://www.idemproject.io/

.. image:: https://img.shields.io/badge/docs%20on-docs.idemproject.io-blue
   :alt: Documentation is published with Sphinx on docs.idemproject.io
   :target: https://docs.idemproject.io/idem-azure/en/latest/index.html

.. image:: https://img.shields.io/badge/made%20with-python-yellow
   :alt: Made with Python
   :target: https://www.python.org/

Idem plugin to manage Azure cloud resources

About
=====

``idem-azure`` helps manage Azure with ``idem``.

* `idem-azure source code <https://gitlab.com/vmware/idem/idem-azure>`__
* `idem-azure documentation <https://docs.idemproject.io/idem-azure/en/latest/index.html>`__

What is POP?
------------

This project is built with `pop <https://pop.readthedocs.io/>`__, a Python-based
implementation of *Plugin Oriented Programming (POP)*. POP seeks to bring
together concepts and wisdom from the history of computing in new ways to solve
modern computing problems.

For more information:

* `Intro to Plugin Oriented Programming (POP) <https://pop-book.readthedocs.io/en/latest/>`__
* `pop-awesome <https://gitlab.com/saltstack/pop/pop-awesome>`__
* `pop-create <https://gitlab.com/saltstack/pop/pop-create/>`__

What is Idem?
-------------

This project is built with `idem <https://www.idemproject.io/>`__, an idempotent,
imperatively executed, declarative programming language written in Python. This project extends
idem!

For more information:

* `Idem Project Website <https://www.idemproject.io/>`__
* `Idem Project docs portal <https://docs.idemproject.io/>`__

Getting Started
===============

Prerequisites
-------------

* Python 3.8+
* git *(if installing from source, or contributing to the project)*
* Idem

.. note::
  It is recommended that you install Idem using Poetry. Poetry is a tool for virtual environment and dependency management. See the `Idem Getting Started guide <https://docs.idemproject.io/getting-started/en/latest/topics/gettingstarted/installing.html>`_ for more information.

Installation
------------

Install from PyPI
+++++++++++++++++
You can install ``idem-azure`` from PyPI, a source repository, or a local directory.

Before you install ``idem-azure``, ensure that you are in the same directory as your ``pyproject.toml`` file. Optionally, you can specify the directory containing your ``pyproject.toml`` file by using the ``--directory=DIRECTORY (-C)`` option.

Install from PyPI
+++++++++++++++++

To install ``idem-azure`` from PyPI, run the following command:

.. code-block:: bash

  poetry add idem-azure

Install from source
+++++++++++++++++++

You can also install ``idem-azure`` directly from the source repository:

.. code-block:: bash

  poetry add git+https://gitlab.com/vmware/idem/idem-azure.git

If you don't specify a branch, Poetry uses the latest commit on the ``master`` branch.

Install from a local directory
++++++++++++++++++++++++++++++

Clone the ``idem-zure`` repository. Then run the following command to install from the cloned directory:

.. code-block:: bash

  poetry add ~/path/to/idem-azure


Usage
=====

Credentials Setup
-----------------

After installation, the Azure Idem execution and state modules will be accessible to the pop `hub`.
In order to use them, we need to set up our credentials.

Create a new file called `credentials.yaml` and populate it with credentials.
The `default` profile will be picked up automatically by `idem`.

There are multiple authentication backends for `idem-azure` which each have their own unique set of parameters.
The following examples show the parameters that can be used to define credential profiles.

credentials.yaml:

..  code:: sls

    azure:
       default:
          client_id: "12345678-1234-1234-1234-aaabc1234aaa"
          secret: "76543210-4321-4321-4321-bbbb3333aaaa"
          subscription_id: "ZzxxxXXXX11xx-aaaaabbbb-k3xxxxxx"
          tenant: "bbbbbca-3333-4444-aaaa-cddddddd6666"

Next step is to encrypt the credentials file, and add the encryption key and encrypted file
path to the ENVIRONMENT.

Encrypt the credential file:

.. code:: bash

    Idem encrypt credentials.yaml

This will generate a credentials.yaml.fernet file and a command line output token::

    -AXFSEFSSEjsfdG_lb333kVhCVSCDyOFH4eABCDEFNwI=

Add these to your environment:

.. code:: bash

    export ACCT_KEY="-AXFSEFSSEjsfdG_lb333kVhCVSCDyOFH4eABCDEFNwI="
    export ACCT_FILE=$PWD/credentials.yaml.fernet


You are ready to use idem-azure!!!

STATES
--------
Idem states are used to make sure resources are in a desired state.
The desired state of a resource can be specified in sls file.
In Idem-azure, three states are supported: `present`, `absent`, `describe`

present state
+++++++++++++
`present` state makes sure a resource exists in a desired state. If a resource does
not exist, running `present` will create the resource on the provider. If a resource
exists, running `present` will update the resource on the provider. (Only the values
that the Azure REST api supports can be updated.)

absent state
++++++++++++
`absent` state makes sure a resource does not exist. If a resource exits, running
`absent` will delete the resource. If a resource does not exist, running `absent`
is a no-operation.

describe state
++++++++++++++
`describe` state lists all the current resources of the same resource type
under the subscription id specified in the credential profile.

States can be accessed by their relative location in `idem-azure/idem_azure/states`.
For example, in the state sls yaml file below, Azure resource group state can be created with the `present` function.

my_resource_group_state.sls:

.. code:: sls

    my-azure-resource-group:
      azure.resource_management.resource_groups.present:
      - resource_group_name: my-azure-resource-group
      - location: eastus

The state sls file can be executed with:

.. code:: bash

    idem state $PWD/my_resource_group_state.sls

Example of creating an Azure virtual network:

.. code:: sls

    my-virtual-network:
      azure.network.virtual_networks.present:
      - resource_group_name: my-azure-resource-group
      - virtual_network_name: my-virtual-network
      - location: eastus
      - address_space:
            - 10.0.0.0/16

The resource parameters in an sls yaml file follow the exact structure as
what's in the `Azure REST api doc <https://docs.microsoft.com/en-us/rest/api/azure/>`__ . URI Parameters
should be specified in snake case with "- " in front. All parameters of the api request body
should be specified in exactly the same way as what's in the Azure REST api.

Current Supported Resources states
++++++++++++++++++++++++++++++++++

authorization
"""""""""""""
role_definitions, role_assignments

resource_management
"""""""""""""""""""
resource_groups

policy
""""""
policy_definitions, policy_assignments

management_groups
"""""""""""""""""""
management_groups

subscription
"""""""""""""""""""
subscription

network
""""""""""""""""""""""""
firewall, firewall_policies, network_interfaces, network_security_groups, public_ip_addresses, route_tables, routes, security_rules, subnets, virtual_networks

compute
""""""""""""""""""""""""
virtual_machines, log_analytics_workspace

storage_resource_provider
"""""""""""""""""""""""""
storage_accounts
