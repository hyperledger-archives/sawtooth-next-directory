# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: task_state.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='task_state.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=_b('\n\x10task_state.proto\"C\n\x17TaskAttributesContainer\x12(\n\x0ftask_attributes\x18\x01 \x03(\x0b\x32\x0f.TaskAttributes\"A\n\x0eTaskAttributes\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x10\n\x08metadata\x18\x03 \x01(\t\"E\n\x19TaskRelationshipContainer\x12(\n\rrelationships\x18\x01 \x03(\x0b\x32\x11.TaskRelationship\"_\n\x10TaskRelationship\x12\x0f\n\x07task_id\x18\x01 \x01(\t\x12\x13\n\x0bidentifiers\x18\x02 \x03(\t\x12\x11\n\tobject_id\x18\x03 \x01(\t\x12\x12\n\nrelated_id\x18\x04 \x01(\tb\x06proto3')
)




_TASKATTRIBUTESCONTAINER = _descriptor.Descriptor(
  name='TaskAttributesContainer',
  full_name='TaskAttributesContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_attributes', full_name='TaskAttributesContainer.task_attributes', index=0,
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
  serialized_start=20,
  serialized_end=87,
)


_TASKATTRIBUTES = _descriptor.Descriptor(
  name='TaskAttributes',
  full_name='TaskAttributes',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='TaskAttributes.task_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='name', full_name='TaskAttributes.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='metadata', full_name='TaskAttributes.metadata', index=2,
      number=3, type=9, cpp_type=9, label=1,
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
  serialized_start=89,
  serialized_end=154,
)


_TASKRELATIONSHIPCONTAINER = _descriptor.Descriptor(
  name='TaskRelationshipContainer',
  full_name='TaskRelationshipContainer',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='relationships', full_name='TaskRelationshipContainer.relationships', index=0,
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
  serialized_start=156,
  serialized_end=225,
)


_TASKRELATIONSHIP = _descriptor.Descriptor(
  name='TaskRelationship',
  full_name='TaskRelationship',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='task_id', full_name='TaskRelationship.task_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='identifiers', full_name='TaskRelationship.identifiers', index=1,
      number=2, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='object_id', full_name='TaskRelationship.object_id', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='related_id', full_name='TaskRelationship.related_id', index=3,
      number=4, type=9, cpp_type=9, label=1,
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
  serialized_start=227,
  serialized_end=322,
)

_TASKATTRIBUTESCONTAINER.fields_by_name['task_attributes'].message_type = _TASKATTRIBUTES
_TASKRELATIONSHIPCONTAINER.fields_by_name['relationships'].message_type = _TASKRELATIONSHIP
DESCRIPTOR.message_types_by_name['TaskAttributesContainer'] = _TASKATTRIBUTESCONTAINER
DESCRIPTOR.message_types_by_name['TaskAttributes'] = _TASKATTRIBUTES
DESCRIPTOR.message_types_by_name['TaskRelationshipContainer'] = _TASKRELATIONSHIPCONTAINER
DESCRIPTOR.message_types_by_name['TaskRelationship'] = _TASKRELATIONSHIP
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

TaskAttributesContainer = _reflection.GeneratedProtocolMessageType('TaskAttributesContainer', (_message.Message,), dict(
  DESCRIPTOR = _TASKATTRIBUTESCONTAINER,
  __module__ = 'task_state_pb2'
  # @@protoc_insertion_point(class_scope:TaskAttributesContainer)
  ))
_sym_db.RegisterMessage(TaskAttributesContainer)

TaskAttributes = _reflection.GeneratedProtocolMessageType('TaskAttributes', (_message.Message,), dict(
  DESCRIPTOR = _TASKATTRIBUTES,
  __module__ = 'task_state_pb2'
  # @@protoc_insertion_point(class_scope:TaskAttributes)
  ))
_sym_db.RegisterMessage(TaskAttributes)

TaskRelationshipContainer = _reflection.GeneratedProtocolMessageType('TaskRelationshipContainer', (_message.Message,), dict(
  DESCRIPTOR = _TASKRELATIONSHIPCONTAINER,
  __module__ = 'task_state_pb2'
  # @@protoc_insertion_point(class_scope:TaskRelationshipContainer)
  ))
_sym_db.RegisterMessage(TaskRelationshipContainer)

TaskRelationship = _reflection.GeneratedProtocolMessageType('TaskRelationship', (_message.Message,), dict(
  DESCRIPTOR = _TASKRELATIONSHIP,
  __module__ = 'task_state_pb2'
  # @@protoc_insertion_point(class_scope:TaskRelationship)
  ))
_sym_db.RegisterMessage(TaskRelationship)


# @@protoc_insertion_point(module_scope)
