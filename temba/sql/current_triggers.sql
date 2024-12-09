-- Generated by collect_sql on 2024-12-05 16:51 UTC

CREATE TRIGGER temba_broadcast_on_delete
AFTER DELETE ON msgs_broadcast REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_broadcast_on_delete();

CREATE TRIGGER temba_broadcast_on_insert
AFTER INSERT ON msgs_broadcast REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_broadcast_on_insert();

CREATE TRIGGER temba_broadcast_on_update
AFTER UPDATE ON msgs_broadcast REFERENCING OLD TABLE AS oldtab NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_broadcast_on_update();

CREATE TRIGGER temba_channellog_update_channelcount
   AFTER INSERT OR DELETE OR UPDATE OF is_error, channel_id
   ON channels_channellog
   FOR EACH ROW
   EXECUTE PROCEDURE temba_update_channellog_count();

CREATE TRIGGER temba_flowrun_delete
    AFTER DELETE ON flows_flowrun
    FOR EACH ROW EXECUTE PROCEDURE temba_flowrun_delete();

CREATE TRIGGER temba_flowrun_on_change
    AFTER UPDATE ON flows_flowrun
    FOR EACH ROW EXECUTE PROCEDURE temba_flowrun_on_change();

CREATE TRIGGER temba_flowrun_on_delete
AFTER DELETE ON flows_flowrun REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_flowrun_on_delete();

CREATE TRIGGER temba_flowrun_on_insert
AFTER INSERT ON flows_flowrun REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_flowrun_on_insert();

CREATE TRIGGER temba_flowrun_on_update
AFTER UPDATE ON flows_flowrun REFERENCING OLD TABLE AS oldtab NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_flowrun_on_update();

CREATE TRIGGER temba_flowrun_update_flowcategorycount
    AFTER INSERT OR UPDATE OF results ON flows_flowrun
    FOR EACH ROW EXECUTE PROCEDURE temba_update_flowcategorycount();

CREATE TRIGGER temba_flowsession_status_change
    AFTER UPDATE OF status ON flows_flowsession
    FOR EACH ROW EXECUTE PROCEDURE temba_flowsession_status_change();

CREATE TRIGGER temba_group_contacts_on_delete
AFTER DELETE ON contacts_contactgroup_contacts REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_group_contacts_on_delete();

CREATE TRIGGER temba_group_contacts_on_insert
AFTER INSERT ON contacts_contactgroup_contacts REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_group_contacts_on_insert();

CREATE TRIGGER temba_ivrcall_on_delete
AFTER DELETE ON ivr_call REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_ivrcall_on_delete();

CREATE TRIGGER temba_ivrcall_on_insert
AFTER INSERT ON ivr_call REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_ivrcall_on_insert();

CREATE TRIGGER temba_msg_labels_on_delete
AFTER DELETE ON msgs_msg_labels REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_msg_labels_on_delete();

CREATE TRIGGER temba_msg_labels_on_insert
AFTER INSERT ON msgs_msg_labels REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_msg_labels_on_insert();

CREATE TRIGGER temba_msg_on_change
AFTER INSERT OR UPDATE ON msgs_msg
FOR EACH ROW EXECUTE PROCEDURE temba_msg_on_change();

CREATE TRIGGER temba_msg_on_delete
AFTER DELETE ON msgs_msg REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_msg_on_delete();

CREATE TRIGGER temba_msg_on_insert
AFTER INSERT ON msgs_msg REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_msg_on_insert();

CREATE TRIGGER temba_msg_on_update
AFTER UPDATE ON msgs_msg REFERENCING OLD TABLE AS oldtab NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_msg_on_update();

CREATE TRIGGER temba_notification_on_delete
AFTER DELETE ON notifications_notification REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_notification_on_delete();

CREATE TRIGGER temba_notification_on_insert
AFTER INSERT ON notifications_notification REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_notification_on_insert();

CREATE TRIGGER temba_notification_on_update
AFTER UPDATE ON notifications_notification REFERENCING OLD TABLE AS oldtab NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_notification_on_update();

CREATE TRIGGER temba_ticket_on_change_trg
  AFTER INSERT OR UPDATE OR DELETE ON tickets_ticket
  FOR EACH ROW EXECUTE PROCEDURE temba_ticket_on_change();

CREATE TRIGGER temba_ticket_on_delete
AFTER DELETE ON tickets_ticket REFERENCING OLD TABLE AS oldtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_ticket_on_delete();

CREATE TRIGGER temba_ticket_on_insert
AFTER INSERT ON tickets_ticket REFERENCING NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_ticket_on_insert();

CREATE TRIGGER temba_ticket_on_update
AFTER UPDATE ON tickets_ticket REFERENCING OLD TABLE AS oldtab NEW TABLE AS newtab
FOR EACH STATEMENT EXECUTE PROCEDURE temba_ticket_on_update();

CREATE TRIGGER when_contacts_changed_then_update_groups_trg
   AFTER INSERT OR UPDATE ON contacts_contact
   FOR EACH ROW EXECUTE PROCEDURE update_contact_system_groups();

