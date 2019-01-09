## story_recommend
* recommend
  - utter_recommendation
  - utter_ask_request_access

## story_access
* access
  - utter_current_draft

## story_affirm
* affirm
  - utter_recommended_draft

## story_deny
* deny
  - utter_standby

## story_send_recommended
* send_recommended{"reason": "I need access."}
  - action_request_access
  - utter_exclame
  - utter_fanfare_sent
  - utter_request_bye

## story_send_current_pack
* send_current{"reason": "I need access.", "resource_id": "1234", "resource_type": "PACK"}
  - action_request_access
  - utter_exclame
  - utter_fanfare_sent
  - utter_request_bye

## story_send_current_role
* send_current{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - utter_exclame
  - utter_fanfare_sent
  - utter_request_bye

## story_send_current_role_1
* send_current{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "1"}
  - utter_exclame
  - utter_fanfare_sent
  - utter_request_bye

## story_send_current_role_2
* send_current{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "2"}
  - utter_send_failure_invalid

## story_send_current_role_3
* send_current{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "3"}
  - utter_send_failure_pending

## story_send_current_role_4
* send_current{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": "4"}
  - utter_send_failure_unknown

## story_send_current_role_error
* send_current{"reason": "I need access.", "resource_id": "1234", "resource_type": "ROLE"}
  - action_request_access
  - slot{"batch_status": null}
  - utter_send_failure_unknown

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
