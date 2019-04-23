Diagram Sources:
Store your source files in ../src (this directory is deprecated and will be removed)
so that, as the architecture evolves, the diagrams can change and updated renderings
can replace previous versions in ../src and ../out.


• Store your source code (as .wsd files) in the /docs/diagrams/src directory.

• Store your rendered source code (as .svg images) in the /docs/diagrams/src directory.

• Use lightblue to color elements/microservices that we own and control:
    ex:
        – rethinkdb
        – ledger-sync
        – rbac-server

• Use lightgrey to color elements/microservices that we use but do not control:
    ex:
        – sawtooth
        – the sawtooth validator

• Use stereotypes for <<NEXT>> and <<HYPERLEDGER>> to differentiate between the 
  former and latter, respectively.

• Use default colors and no stereotypes for external entities:
    ex:
        – various human users
        – LDAP
        – Azure AD

• Sequences and architecture diagrams should be high level.
    – Only go as deep as individual microservices or modules for sequence and
      architecture diagrams when possible.
    – Source code should be self documenting, docstrings, and general good 
      practices will result in self explanatory code. As such high level 
      documents should be sufficient.
    – Every major product feature should have a linked sequence diagram.
    – Whenever a PR adds or changes the flow of a feature or data contracts the
      relevant PlantUML diagrams much be updated and re-rendered as an implicit
      success requirement.
