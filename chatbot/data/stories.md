## story_update_member
* update{"member_status": "MEMBER", "resource_name": "abc"}
  - utter_noop

## story_update_not_member
* update{"member_status": "NOT_MEMBER", "resource_name": "abc"}
  - utter_noop

## story_update_pending
* update{"member_status": "PENDING", "resource_name": "abc"}
  - utter_noop

## story_update_owner
* update{"owner_status": "OWNER", "resource_name": "abc"}
  - utter_noop

## story_offer
* offer{"member_status": "NOT_MEMBER", "resource_id": "123", "resource_name": "abc"}
  - utter_offer

## story_expired{"member_status": "NOT_MEMBER", "resource_id": "123", "resource_name": "abc", "resource_type": "ROLE"}
* expired
  - utter_expired

## story_member
* member{"member_status": "MEMBER", "resource_id": "123", "resource_name": "abc"}
  - utter_member

## story_owner
* owner{"owner_status": "OWNER", "resource_id": "123", "resource_name": "abc"}
  - utter_owner

## story_owner_not_member
* owner{"owner_status": "OWNER", "member_status": "NOT_MEMBER", "resource_id": "123", "resource_name": "abc"}
  - utter_owner_not_member

## story_pending_role
* pending{"member_status": "PENDING", "resource_type": "ROLE", "resource_id": "123", "resource_name": "abc"}
  - utter_pending_role

## story_pending_pack
* pending{"member_status": "PENDING", "resource_type": "PACK", "resource_id": "123", "resource_name": "abc"}
  - utter_pending_pack

## story_recommend
* recommend{"member_status": "NOT_MEMBER", "resource_id": "123", "resource_name": "abc"}
  - utter_recommendation
  - utter_ask_request_access

## story_access_member
* access
  - slot{"member_status": "MEMBER"}
  - utter_access_member

## story_access_not_member_pack
* access
  - slot{"member_status": "NOT_MEMBER", "resource_type": "PACK"}
  - utter_current_draft_pack

## story_access_not_member_role
* access
  - slot{"member_status": "NOT_MEMBER", "resource_type": "ROLE"}
  - utter_current_draft_role

## story_access_pending
* access
  - slot{"member_status": "PENDING"}
  - utter_access_pending

## story_affirm_member
* affirm
  - slot{"member_status": "MEMBER"}
  - utter_generic

## story_affirm_pending
* affirm
  - slot{"member_status": "PENDING"}
  - utter_generic

## story_affirm_not_member_pack
* affirm
  - slot{"member_status": "NOT_MEMBER", "resource_type": "PACK"}
  - utter_recommended_draft_pack

## story_affirm_not_member_role
* affirm
  - slot{"member_status": "NOT_MEMBER", "resource_type": "ROLE"}
  - utter_recommended_draft_role

## story_deny
* deny
  - utter_standby

## story_request_access_pack
* request_access{"reason": "I need access.", "resource_id": "1234", "resource_type": "PACK"}
  - action_request_access
  - utter_fanfare_sent

## story_request_access_role
* request_access{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - utter_fanfare_sent

## story_request_access_role_1
* request_access{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "1"}
  - utter_fanfare_sent

## story_request_access_role_2
* request_access{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "2"}
  - utter_send_failure_invalid

## story_request_access_role_3
* request_access{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "3"}
  - utter_send_failure_pending

## story_request_access_role_4
* request_access{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "4"}
  - utter_send_failure_unknown

## story_no_owner
* no_owner
  - utter_no_owner

## story_cancel
* cancel
  - utter_passive
  - utter_standby

## story_thank
* thank
  - utter_thank

## story_greet
* greet
  - utter_greet

## story_feeling
* feeling
  - utter_feeling

## story_bye
* bye
  - utter_bye

## story_laugh
* laugh
  - utter_laugh

## story_awe
* awe
  - utter_awe

## story_insult
* insult
  - utter_insult

## story_help
* help
  - utter_help

## story_name
* name
  - utter_name

## story_whoami
* whoami
  - utter_whoami
