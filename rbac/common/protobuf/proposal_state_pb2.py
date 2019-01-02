# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proposal_state.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='proposal_state.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x14proposal_state.proto\"2\n\x12ProposalsContainer\x12\x1c\n\tproposals\x18\x01 \x03(\x0b\x32\t.Proposal\"\xba\x05\n\x08Proposal\x12\x13\n\x0bproposal_id\x18\x01 \x01(\t\x12-\n\rproposal_type\x18\x02 \x01(\x0e\x32\x16.Proposal.ProposalType\x12\x11\n\tobject_id\x18\x03 \x01(\t\x12\x12\n\nrelated_id\x18\x04 \x01(\t\x12\x0e\n\x06opener\x18\x05 \x01(\t\x12\x0e\n\x06\x63loser\x18\x06 \x01(\t\x12 \n\x06status\x18\x07 \x01(\x0e\x32\x10.Proposal.Status\x12\x13\n\x0bopen_reason\x18\x08 \x01(\t\x12\x14\n\x0c\x63lose_reason\x18\t \x01(\t\x12\x10\n\x08metadata\x18\n \x01(\t\x12\x1c\n\tapprovals\x18\x0b \x03(\x0b\x32\t.Approval\x12\x1e\n\nrejections\x18\x0c \x03(\x0b\x32\n.Rejection\x12\x14\n\x0c\x63reated_date\x18\r \x01(\x03\x12\x13\n\x0b\x63losed_date\x18\x0e \x01(\x03\"\xa9\x02\n\x0cProposalType\x12\x11\n\rADD_ROLE_TASK\x10\x00\x12\x13\n\x0f\x41\x44\x44_ROLE_MEMBER\x10\x01\x12\x12\n\x0e\x41\x44\x44_ROLE_OWNER\x10\x02\x12\x12\n\x0e\x41\x44\x44_ROLE_ADMIN\x10\x03\x12\x14\n\x10REMOVE_ROLE_TASK\x10\x04\x12\x16\n\x12REMOVE_ROLE_MEMBER\x10\x05\x12\x15\n\x11REMOVE_ROLE_OWNER\x10\x06\x12\x15\n\x11REMOVE_ROLE_ADMIN\x10\x07\x12\x12\n\x0e\x41\x44\x44_TASK_OWNER\x10\x08\x12\x12\n\x0e\x41\x44\x44_TASK_ADMIN\x10\t\x12\x15\n\x11REMOVE_TASK_OWNER\x10\n\x12\x15\n\x11REMOVE_TASK_ADMIN\x10\x0b\x12\x17\n\x13UPDATE_USER_MANAGER\x10\x0c\"/\n\x06Status\x12\x08\n\x04OPEN\x10\x00\x12\x0c\n\x08REJECTED\x10\x01\x12\r\n\tCONFIRMED\x10\x02\"/\n\x08\x41pproval\x12\x10\n\x08\x61pprover\x18\x01 \x01(\t\x12\x11\n\ton_behalf\x18\x02 \x01(\t\"0\n\tRejection\x12\x10\n\x08rejector\x18\x01 \x01(\t\x12\x11\n\ton_behalf\x18\x02 \x01(\tb\x06proto3')
)



_PROPOSAL_PROPOSALTYPE = _descriptor.EnumDescriptor(
  name='ProposalType',
  full_name='Proposal.ProposalType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='ADD_ROLE_TASK', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADD_ROLE_MEMBER', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADD_ROLE_OWNER', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADD_ROLE_ADMIN', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_ROLE_TASK', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_ROLE_MEMBER', index=5, number=5,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_ROLE_OWNER', index=6, number=6,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_ROLE_ADMIN', index=7, number=7,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADD_TASK_OWNER', index=8, number=8,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='ADD_TASK_ADMIN', index=9, number=9,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_TASK_OWNER', index=10, number=10,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REMOVE_TASK_ADMIN', index=11, number=11,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='UPDATE_USER_MANAGER', index=12, number=12,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=429,
  serialized_end=726,
)
_sym_db.RegisterEnumDescriptor(_PROPOSAL_PROPOSALTYPE)

_PROPOSAL_STATUS = _descriptor.EnumDescriptor(
  name='Status',
  full_name='Proposal.Status',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='OPEN', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REJECTED', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CONFIRMED', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=728,
  serialized_end=775,
)
_sym_db.RegisterEnumDescriptor(_PROPOSAL_STATUS)


_PROPOSALSCONTAINER = _descriptor.Descriptor(
  name='ProposalsContainer',
  full_name='ProposalsContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposals', full_name='ProposalsContainer.proposals', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=24,
  serialized_end=74,
)


_PROPOSAL = _descriptor.Descriptor(
  name='Proposal',
  full_name='Proposal',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='proposal_id', full_name='Proposal.proposal_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='proposal_type', full_name='Proposal.proposal_type', index=1,
      number=2, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object_id', full_name='Proposal.object_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='related_id', full_name='Proposal.related_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='opener', full_name='Proposal.opener', index=4,
      number=5, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='closer', full_name='Proposal.closer', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='status', full_name='Proposal.status', index=6,
      number=7, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='open_reason', full_name='Proposal.open_reason', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='close_reason', full_name='Proposal.close_reason', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='Proposal.metadata', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='approvals', full_name='Proposal.approvals', index=10,
      number=11, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='rejections', full_name='Proposal.rejections', index=11,
      number=12, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='created_date', full_name='Proposal.created_date', index=12,
      number=13, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='closed_date', full_name='Proposal.closed_date', index=13,
      number=14, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _PROPOSAL_PROPOSALTYPE,
    _PROPOSAL_STATUS,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=77,
  serialized_end=775,
)


_APPROVAL = _descriptor.Descriptor(
  name='Approval',
  full_name='Approval',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='approver', full_name='Approval.approver', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='on_behalf', full_name='Approval.on_behalf', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=777,
  serialized_end=824,
)


_REJECTION = _descriptor.Descriptor(
  name='Rejection',
  full_name='Rejection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='rejector', full_name='Rejection.rejector', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='on_behalf', full_name='Rejection.on_behalf', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=826,
  serialized_end=874,
)

_PROPOSALSCONTAINER.fields_by_name['proposals'].message_type = _PROPOSAL
_PROPOSAL.fields_by_name['proposal_type'].enum_type = _PROPOSAL_PROPOSALTYPE
_PROPOSAL.fields_by_name['status'].enum_type = _PROPOSAL_STATUS
_PROPOSAL.fields_by_name['approvals'].message_type = _APPROVAL
_PROPOSAL.fields_by_name['rejections'].message_type = _REJECTION
_PROPOSAL_PROPOSALTYPE.containing_type = _PROPOSAL
_PROPOSAL_STATUS.containing_type = _PROPOSAL
DESCRIPTOR.message_types_by_name['ProposalsContainer'] = _PROPOSALSCONTAINER
DESCRIPTOR.message_types_by_name['Proposal'] = _PROPOSAL
DESCRIPTOR.message_types_by_name['Approval'] = _APPROVAL
DESCRIPTOR.message_types_by_name['Rejection'] = _REJECTION
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ProposalsContainer = _reflection.GeneratedProtocolMessageType('ProposalsContainer', (_message.Message,), dict(
  DESCRIPTOR = _PROPOSALSCONTAINER,
  __module__ = 'proposal_state_pb2'
  # @@protoc_insertion_point(class_scope:ProposalsContainer)
  ))
_sym_db.RegisterMessage(ProposalsContainer)

Proposal = _reflection.GeneratedProtocolMessageType('Proposal', (_message.Message,), dict(
  DESCRIPTOR = _PROPOSAL,
  __module__ = 'proposal_state_pb2'
  # @@protoc_insertion_point(class_scope:Proposal)
  ))
_sym_db.RegisterMessage(Proposal)

Approval = _reflection.GeneratedProtocolMessageType('Approval', (_message.Message,), dict(
  DESCRIPTOR = _APPROVAL,
  __module__ = 'proposal_state_pb2'
  # @@protoc_insertion_point(class_scope:Approval)
  ))
_sym_db.RegisterMessage(Approval)

Rejection = _reflection.GeneratedProtocolMessageType('Rejection', (_message.Message,), dict(
  DESCRIPTOR = _REJECTION,
  __module__ = 'proposal_state_pb2'
  # @@protoc_insertion_point(class_scope:Rejection)
  ))
_sym_db.RegisterMessage(Rejection)


# @@protoc_insertion_point(module_scope)
