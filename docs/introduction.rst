============
Introduction
============

NEXT is an approval platform for the enterprise incorporating aspects of identity management, role-based access
control, and SOX compliance recording. Its apis are used to orchestrate changes to an organization (promotions,
terminations, team changes, etc), management of roles (customization of and members in), and tasks (capabilities)
granted. In daily operations, these changes are carried out using a proposal/approval process. In addition, the system
can intake organizational data via one or more connectors to other identity and access providers such as
`Active Directory`_.

The main goal of the project is to supply an immutable log of organizational change events to SOX_ auditors.

Additional goals of NEXT include:
  - Customizable, team-defined-and-managed roles
  - Rapid new hire registration into multiple systems and applications
  - Retroactive integration and bi-directional sync with other identity providers
  - Configurable proposal escalations (scheduled, delegation-based)
  - Customizable approvals (one or more required)
  - Approval delegation
  - Batch approvals

NEXT's underlying blockchain is `Hyperledger SawTooth`_. Since Sawtooth is a permissioned blockchain maintained
by a private cluster of nodes, ledger continuity is supported by disseminating block id hashes over time to external
systems of record (eg: sent in an email). Because new hashes are constructed from the hashes of earlier blocks, and
because the hashes also reflect of contents of the merkle tree content within their blocks, any manipulation of data
stored in the blockchain/ledger will result in a new chain of hash ids. Identical block ids between the current
blockchain and those of the external system is proof that no alterations have been made to the events stored within
the ledger.

The domain model is a graph-like representation of an organizational structure comprising of users, tasks, roles,
and packs (sets of roles). This representation is stored in both a blockchain for immutability, and a nosql database
for access. Running processes manage the data sync between data stores as well as (if active) delta sync between NEXT
and third party identity providers.

.. _SOX: https://en.wikipedia.org/wiki/Sarbanes%E2%80%93Oxley_Act
.. _`Active Directory`: https://en.wikipedia.org/wiki/Active_Directory
.. _`Hyperledger Sawtooth`: https://www.hyperledger.org/
.. _SawTooth: https://www.hyperledger.org/projects/sawtooth