-- Generated by collect_sql on 2024-12-10 18:48 UTC

----------------------------------------------------------------------
-- Convenience method to call contact_toggle_system_group with a row
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION
  contact_toggle_system_group(_contact contacts_contact, _group_type CHAR(1), _add BOOLEAN)
RETURNS VOID AS $$
DECLARE
  _group_id INT;
BEGIN
  PERFORM contact_toggle_system_group(_contact.id, _contact.org_id, _group_type, _add);
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Toggle a contact's membership of a system group in their org
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION
  contact_toggle_system_group(_contact_id INT, _org_id INT, _group_type CHAR(1), _add BOOLEAN)
RETURNS VOID AS $$
DECLARE
  _group_id INT;
BEGIN
  -- lookup the group id
  SELECT id INTO STRICT _group_id FROM contacts_contactgroup
  WHERE org_id = _org_id AND group_type = _group_type;
  -- don't do anything if group doesn't exist for some inexplicable reason
  IF _group_id IS NULL THEN
    RETURN;
  END IF;
  IF _add THEN
    BEGIN
      INSERT INTO contacts_contactgroup_contacts (contactgroup_id, contact_id) VALUES (_group_id, _contact_id);
    EXCEPTION WHEN unique_violation THEN
      -- do nothing
    END;
  ELSE
    DELETE FROM contacts_contactgroup_contacts WHERE contactgroup_id = _group_id AND contact_id = _contact_id;
  END IF;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Determines the item count scope for a broadcast record
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_broadcast_countscope(_broadcast msgs_broadcast) RETURNS TEXT STABLE AS $$
BEGIN
  IF _broadcast.schedule_id IS NOT NULL AND _broadcast.is_active = TRUE THEN
    RETURN 'msgs:folder:E';
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Determines the (mutually exclusive) system label for a broadcast record
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_broadcast_determine_system_label(_broadcast msgs_broadcast) RETURNS CHAR(1) STABLE AS $$
BEGIN
  IF _broadcast.schedule_id IS NOT NULL AND _broadcast.is_active = TRUE THEN
    RETURN 'E';
  END IF;

  RETURN NULL; -- does not match any label
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles DELETE statements on broadcast table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_broadcast_on_delete() RETURNS TRIGGER AS $$
BEGIN
    -- add negative system label counts for all rows that belonged to a system label
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT org_id, temba_broadcast_determine_system_label(oldtab), -count(*), FALSE FROM oldtab
    WHERE temba_broadcast_determine_system_label(oldtab) IS NOT NULL
    GROUP BY org_id, temba_broadcast_determine_system_label(oldtab);

    -- add negative item counts for all rows that belonged to a folder
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_broadcast_countscope(oldtab), -count(*), FALSE FROM oldtab
    WHERE temba_broadcast_countscope(oldtab) IS NOT NULL
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on broadcast table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_broadcast_on_insert() RETURNS TRIGGER AS $$
BEGIN
    -- add system label counts for all rows which belong to a system label
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT org_id, temba_broadcast_determine_system_label(newtab), count(*), FALSE FROM newtab
    WHERE temba_broadcast_determine_system_label(newtab) IS NOT NULL
    GROUP BY org_id, temba_broadcast_determine_system_label(newtab);

    -- add positive item counts for all rows which belong to a folder
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_broadcast_countscope(newtab), count(*), FALSE FROM newtab
    WHERE temba_broadcast_countscope(newtab) IS NOT NULL
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles UPDATE statements on broadcast table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_broadcast_on_update() RETURNS TRIGGER AS $$
BEGIN
    -- add negative counts for all old non-null system labels that don't match the new ones
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT o.org_id, temba_broadcast_determine_system_label(o), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE temba_broadcast_determine_system_label(o) IS DISTINCT FROM temba_broadcast_determine_system_label(n) AND temba_broadcast_determine_system_label(o) IS NOT NULL
    GROUP BY o.org_id, temba_broadcast_determine_system_label(o);

    -- add negative counts for all old non-null item count scopes that don't match the new ones
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT o.org_id, temba_broadcast_countscope(o), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE temba_broadcast_countscope(o) IS DISTINCT FROM temba_broadcast_countscope(n) AND temba_broadcast_countscope(o) IS NOT NULL
    GROUP BY 1, 2;

    -- add counts for all new system labels that don't match the old ones
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT n.org_id, temba_broadcast_determine_system_label(n), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE temba_broadcast_determine_system_label(o) IS DISTINCT FROM temba_broadcast_determine_system_label(n) AND temba_broadcast_determine_system_label(n) IS NOT NULL
    GROUP BY n.org_id, temba_broadcast_determine_system_label(n);

    -- add positive counts for all new non-null item counts that don't match the old ones
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT n.org_id, temba_broadcast_countscope(n), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE temba_broadcast_countscope(o) IS DISTINCT FROM temba_broadcast_countscope(n) AND temba_broadcast_countscope(n) IS NOT NULL
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles deletion of flow runs
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_flowrun_delete() RETURNS TRIGGER AS $$
DECLARE
    p INT;
    _path_json JSONB;
    _path_len INT;
BEGIN
    -- if this is a user delete then remove from results
    IF OLD.delete_from_results THEN
        PERFORM temba_update_category_counts(OLD.flow_id, NULL, OLD.results::json);
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles changes to a flow run
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_flowrun_on_change() RETURNS TRIGGER AS $$
BEGIN
    -- restrict status changes
    IF OLD.status NOT IN ('A', 'W') AND NEW.status IN ('A', 'W') THEN RAISE EXCEPTION 'Cannot restart an exited flow run'; END IF;

    -- we don't support rewinding run paths so the new path must contain the old
    IF NOT (COALESCE(NEW.path_nodes, '{}'::uuid[]) @> COALESCE(OLD.path_nodes, '{}'::uuid[])) THEN
        RAISE EXCEPTION 'Cannot rewind a flow run path (old=%, new=%)', array_length(OLD.path_nodes, 1), array_length(NEW.path_nodes, 1);
    END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles DELETE statements on flowrun table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_flowrun_on_delete() RETURNS TRIGGER AS $$
BEGIN
    -- add negative status counts for all rows being deleted manually
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT flow_id, format('status:%s', status), -count(*), FALSE FROM oldtab
    WHERE delete_from_results = TRUE GROUP BY 1, 2;

    -- add negative node counts for any runs sitting at a node
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT flow_id, format('node:%s', current_node_uuid), -count(*), FALSE FROM oldtab
    WHERE status IN ('A', 'W') AND current_node_uuid IS NOT NULL GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on flowrun table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_flowrun_on_insert() RETURNS TRIGGER AS $$
BEGIN
    -- add status counts for all new status values
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT flow_id, format('status:%s', status), count(*), FALSE FROM newtab GROUP BY 1, 2;

    -- add start counts for all new start values
    INSERT INTO flows_flowstartcount("start_id", "count", "is_squashed")
    SELECT start_id, count(*), FALSE FROM newtab WHERE start_id IS NOT NULL GROUP BY start_id;

    -- add node counts for all new current node values
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT flow_id, format('node:%s', current_node_uuid), count(*), FALSE FROM newtab
    WHERE status IN ('A', 'W') AND current_node_uuid IS NOT NULL GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles UPDATE statements on flowrun table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_flowrun_on_update() RETURNS TRIGGER AS $$
BEGIN
    -- add negative status counts for all old status values that don't match the new ones
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT o.flow_id, format('status:%s', o.status), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE o.status != n.status
    GROUP BY 1, 2;

    -- add status counts for all new status values that don't match the old ones
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT n.flow_id, format('status:%s', n.status), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE o.status != n.status
    GROUP BY 1, 2;

    -- add negative node counts for all old current node values that don't match the new ones
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT o.flow_id, format('node:%s', o.current_node_uuid), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE o.current_node_uuid IS NOT NULL AND o.status IN ('A', 'W') AND (o.current_node_uuid != n.current_node_uuid OR n.status NOT IN ('A', 'W'))
    GROUP BY 1, 2;

    -- add node counts for all new current node values that don't match the old ones
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT n.flow_id, format('node:%s', n.current_node_uuid), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE n.current_node_uuid IS NOT NULL AND o.current_node_uuid != n.current_node_uuid AND n.status IN ('A', 'W')
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles changes to a flow session's status
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_flowsession_status_change() RETURNS TRIGGER AS $$
BEGIN
  -- restrict changes
  IF OLD.status != 'W' AND NEW.status = 'W' THEN RAISE EXCEPTION 'Cannot restart an exited flow session'; END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles DELETE statements on contacts_contactgroup_contacts table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_group_contacts_on_delete() RETURNS TRIGGER AS $$
BEGIN
    -- add negative count for all deleted rows
    INSERT INTO contacts_contactgroupcount("group_id", "count", "is_squashed")
    SELECT o.contactgroup_id, -count(*), FALSE FROM oldtab o GROUP BY 1;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on contacts_contactgroup_contacts table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_group_contacts_on_insert() RETURNS TRIGGER AS $$
BEGIN
    -- add positive count for all new rows
    INSERT INTO contacts_contactgroupcount("group_id", "count", "is_squashed")
    SELECT n.contactgroup_id, count(*), FALSE FROM newtab n GROUP BY 1;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Inserts a new channelcount row with the given values
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_insert_channelcount(_channel_id INTEGER, _count_type VARCHAR(2), _count_day DATE, _count INT) RETURNS VOID AS $$
  BEGIN
    IF _channel_id IS NOT NULL THEN
      INSERT INTO channels_channelcount("channel_id", "count_type", "day", "count", "is_squashed")
        VALUES(_channel_id, _count_type, _count_day, _count, FALSE);
    END IF;
  END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION temba_insert_flowcategorycount(_flow_id integer, result_key text, _result json, _count integer)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
  BEGIN
    IF _result->>'category' IS NOT NULL THEN
      INSERT INTO flows_flowcategorycount("flow_id", "node_uuid", "result_key", "result_name", "category_name", "count", "is_squashed")
        VALUES(_flow_id, (_result->>'node_uuid')::uuid, result_key, _result->>'name', _result->>'category', _count, FALSE);
    END IF;
  END;
$function$;

----------------------------------------------------------------------
-- Handles DELETE statements on ivr_call table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_ivrcall_on_delete() RETURNS TRIGGER AS $$
BEGIN
    -- add negative count for all rows being deleted manually
    INSERT INTO msgs_systemlabelcount(org_id, label_type, count, is_squashed)
    SELECT org_id, 'C', -count(*), FALSE
    FROM oldtab GROUP BY org_id;

    -- add negative count for all rows being deleted manually
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, 'msgs:folder:C', -count(*), FALSE FROM oldtab GROUP BY 1;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on ivr_call table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_ivrcall_on_insert() RETURNS TRIGGER AS $$
BEGIN
    -- add call count for all new rows
    INSERT INTO msgs_systemlabelcount(org_id, label_type, count, is_squashed)
    SELECT org_id, 'C', count(*), FALSE FROM newtab GROUP BY org_id;

    -- add call count for all new rows
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, 'msgs:folder:C', count(*), FALSE FROM newtab GROUP BY 1;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Determines the item count scope for a msg record
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_countscope(_msg msgs_msg) RETURNS TEXT STABLE AS $$
BEGIN
  IF _msg.direction = 'I' THEN
    -- incoming IVR messages aren't part of any system labels
    IF _msg.msg_type = 'V' THEN
      RETURN NULL;
    END IF;

    IF _msg.visibility = 'V' AND _msg.status = 'H' AND _msg.flow_id IS NULL THEN
      RETURN 'msgs:folder:I';
    ELSIF _msg.visibility = 'V' AND _msg.status = 'H' AND _msg.flow_id IS NOT NULL THEN
      RETURN 'msgs:folder:W';
    ELSIF _msg.visibility = 'A'  AND _msg.status = 'H' THEN
      RETURN 'msgs:folder:A';
    END IF;
  ELSE
    IF _msg.VISIBILITY = 'V' THEN
      IF _msg.status = 'I' OR _msg.status = 'Q' OR _msg.status = 'E' THEN
        RETURN 'msgs:folder:O';
      ELSIF _msg.status = 'W' OR _msg.status = 'S' OR _msg.status = 'D' OR _msg.status = 'R' THEN
        RETURN 'msgs:folder:S';
      ELSIF _msg.status = 'F' THEN
        RETURN 'msgs:folder:X';
      END IF;
    END IF;
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Determines the channel count code for a message
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_determine_channel_count_code(_msg msgs_msg) RETURNS CHAR(2) STABLE AS $$
BEGIN
  IF _msg.direction = 'I' THEN
    IF _msg.msg_type = 'V' THEN RETURN 'IV'; ELSE RETURN 'IM'; END IF;
  ELSE
    IF _msg.msg_type = 'V' THEN RETURN 'OV'; ELSE RETURN 'OM'; END IF;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Determines the (mutually exclusive) system label for a msg record
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_determine_system_label(_msg msgs_msg) RETURNS CHAR(1) STABLE AS $$
BEGIN
  IF _msg.direction = 'I' THEN
    -- incoming IVR messages aren't part of any system labels
    IF _msg.msg_type = 'V' THEN
      RETURN NULL;
    END IF;

    IF _msg.visibility = 'V' AND _msg.status = 'H' AND _msg.flow_id IS NULL THEN
      RETURN 'I';
    ELSIF _msg.visibility = 'V' AND _msg.status = 'H' AND _msg.flow_id IS NOT NULL THEN
      RETURN 'W';
    ELSIF _msg.visibility = 'A'  AND _msg.status = 'H' THEN
      RETURN 'A';
    END IF;
  ELSE
    IF _msg.VISIBILITY = 'V' THEN
      IF _msg.status = 'I' OR _msg.status = 'Q' OR _msg.status = 'E' THEN
        RETURN 'O';
      ELSIF _msg.status = 'W' OR _msg.status = 'S' OR _msg.status = 'D' OR _msg.status = 'R' THEN
        RETURN 'S';
      ELSIF _msg.status = 'F' THEN
        RETURN 'X';
      END IF;
    END IF;
  END IF;

  RETURN NULL; -- might not match any label
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles DELETE statements on msgs_msg_labels table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_labels_on_delete() RETURNS TRIGGER AS $$
BEGIN
    -- add negative label count for all deleted rows
    INSERT INTO msgs_labelcount("label_id", "is_archived", "count", "is_squashed")
    SELECT o.label_id, m.visibility != 'V', -count(*), FALSE FROM oldtab o
    INNER JOIN msgs_msg m ON m.id = o.msg_id
    GROUP BY o.label_id, m.visibility != 'V';

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on msgs_msg_labels table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_labels_on_insert() RETURNS TRIGGER AS $$
BEGIN
    -- add label count for all new rows
    INSERT INTO msgs_labelcount("label_id", "is_archived", "count", "is_squashed")
    SELECT n.label_id, m.visibility != 'V', count(*), FALSE FROM newtab n
    INNER JOIN msgs_msg m ON m.id = n.msg_id
    GROUP BY n.label_id, m.visibility != 'V';

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Trigger procedure to update user and system labels on column changes
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_on_change() RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP IN ('INSERT', 'UPDATE') THEN
    -- prevent illegal message states
    IF NEW.direction = 'I' AND NEW.status NOT IN ('P', 'H') THEN
      RAISE EXCEPTION 'Incoming messages can only be PENDING or HANDLED';
    END IF;
    IF NEW.direction = 'O' AND NEW.visibility = 'A' THEN
      RAISE EXCEPTION 'Outgoing messages cannot be archived';
    END IF;
  END IF;

  -- existing message updated
  IF TG_OP = 'UPDATE' THEN
    -- restrict changes
    IF NEW.direction <> OLD.direction THEN RAISE EXCEPTION 'Cannot change direction on messages'; END IF;
    IF NEW.created_on <> OLD.created_on THEN RAISE EXCEPTION 'Cannot change created_on on messages'; END IF;
    IF NEW.msg_type <> OLD.msg_type THEN RAISE EXCEPTION 'Cannot change msg_type on messages'; END IF;
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles DELETE statements on msg table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_on_delete() RETURNS TRIGGER AS $$
BEGIN
    -- add negative system label counts for all messages that belonged to a system label
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT org_id, temba_msg_determine_system_label(oldtab), -count(*), FALSE FROM oldtab
    WHERE temba_msg_determine_system_label(oldtab) IS NOT NULL
    GROUP BY org_id, temba_msg_determine_system_label(oldtab);

    -- add negative item counts for all rows that belonged to a folder
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_msg_countscope(oldtab), -count(*), FALSE FROM oldtab
    WHERE temba_msg_countscope(oldtab) IS NOT NULL
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on msg table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_on_insert() RETURNS TRIGGER AS $$
BEGIN
    -- add broadcast counts for all new broadcast values
    INSERT INTO msgs_broadcastmsgcount("broadcast_id", "count", "is_squashed")
    SELECT broadcast_id, count(*), FALSE FROM newtab WHERE broadcast_id IS NOT NULL GROUP BY broadcast_id;

    -- add system label counts for all messages which belong to a system label
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT org_id, temba_msg_determine_system_label(newtab), count(*), FALSE FROM newtab
    WHERE temba_msg_determine_system_label(newtab) IS NOT NULL
    GROUP BY org_id, temba_msg_determine_system_label(newtab);

    -- add positive item counts for all rows which belong to a folder
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_msg_countscope(newtab), count(*), FALSE FROM newtab
    WHERE temba_msg_countscope(newtab) IS NOT NULL
    GROUP BY 1, 2;

    -- add channel counts for all messages with a channel
    INSERT INTO channels_channelcount("channel_id", "count_type", "day", "count", "is_squashed")
    SELECT channel_id, temba_msg_determine_channel_count_code(newtab), created_on::date, count(*), FALSE FROM newtab
    WHERE channel_id IS NOT NULL GROUP BY channel_id, temba_msg_determine_channel_count_code(newtab), created_on::date;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles UPDATE statements on msg table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_msg_on_update() RETURNS TRIGGER AS $$
BEGIN
    -- add negative counts for all old non-null system labels that don't match the new ones
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT o.org_id, temba_msg_determine_system_label(o), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE temba_msg_determine_system_label(o) IS DISTINCT FROM temba_msg_determine_system_label(n) AND temba_msg_determine_system_label(o) IS NOT NULL
    GROUP BY 1, 2;

    -- add counts for all new system labels that don't match the old ones
    INSERT INTO msgs_systemlabelcount("org_id", "label_type", "count", "is_squashed")
    SELECT n.org_id, temba_msg_determine_system_label(n), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE temba_msg_determine_system_label(o) IS DISTINCT FROM temba_msg_determine_system_label(n) AND temba_msg_determine_system_label(n) IS NOT NULL
    GROUP BY 1, 2;

    -- add negative item counts for all rows that belonged to a folder they no longer belong to
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT o.org_id, temba_msg_countscope(o), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE temba_msg_countscope(o) IS DISTINCT FROM temba_msg_countscope(n) AND temba_msg_countscope(o) IS NOT NULL
    GROUP BY 1, 2;

    -- add positive item counts for all rows that now belong to a folder they didn't belong to
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT n.org_id, temba_msg_countscope(n), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE temba_msg_countscope(o) IS DISTINCT FROM temba_msg_countscope(n) AND temba_msg_countscope(n) IS NOT NULL
    GROUP BY 1, 2;

    -- add negative old-state label counts for all messages being archived/restored
    INSERT INTO msgs_labelcount("label_id", "is_archived", "count", "is_squashed")
    SELECT ml.label_id, o.visibility != 'V', -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    INNER JOIN msgs_msg_labels ml ON ml.msg_id = o.id
    WHERE (o.visibility = 'V' AND n.visibility != 'V') or (o.visibility != 'V' AND n.visibility = 'V')
    GROUP BY 1, 2;

    -- add new-state label counts for all messages being archived/restored
    INSERT INTO msgs_labelcount("label_id", "is_archived", "count", "is_squashed")
    SELECT ml.label_id, n.visibility != 'V', count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    INNER JOIN msgs_msg_labels ml ON ml.msg_id = n.id
    WHERE (o.visibility = 'V' AND n.visibility != 'V') or (o.visibility != 'V' AND n.visibility = 'V')
    GROUP BY 1, 2;

    -- add new flow activity counts for incoming messages now marked as handled by a flow
    INSERT INTO flows_flowactivitycount("flow_id", "scope", "count", "is_squashed")
    SELECT s.flow_id, unnest(ARRAY[
            format('msgsin:hour:%s', extract(hour FROM NOW())),
            format('msgsin:dow:%s', extract(isodow FROM NOW())),
            format('msgsin:date:%s', NOW()::date)
        ]), s.msgs, FALSE
    FROM (
        SELECT n.flow_id, count(*) AS msgs FROM newtab n INNER JOIN oldtab o ON o.id = n.id
        WHERE n.direction = 'I' AND o.flow_id IS NULL AND n.flow_id IS NOT NULL
        GROUP BY 1
    ) s;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Determines the item count scope for a notification
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_notification_countscope(_notification notifications_notification) RETURNS TEXT STABLE AS $$
BEGIN
    RETURN format('notifications:%s:%s', _notification.user_id, CASE WHEN _notification.is_seen THEN 'S' ELSE 'U' END);
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles DELETE statements on notification table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_notification_on_delete() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_notification_countscope(oldtab), -count(*), FALSE FROM oldtab
    WHERE position('U' IN medium) > 0 GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on notification table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_notification_on_insert() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_notification_countscope(newtab), count(*), FALSE FROM newtab
    WHERE position('U' IN medium) > 0 GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles UPDATE statements on notification table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_notification_on_update() RETURNS TRIGGER AS $$
BEGIN
    -- add negative counts for all old count scopes that don't match the new ones
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT o.org_id, temba_notification_countscope(o), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE position('U' IN o.medium) > 0 AND temba_notification_countscope(o) != temba_notification_countscope(n)
    GROUP BY 1, 2;

    -- add positive counts for all new count scopes that don't match the old ones
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT n.org_id, temba_notification_countscope(n), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE position('U' IN n.medium) > 0 AND temba_notification_countscope(o) != temba_notification_countscope(n)
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Determines the item count scope for a ticket
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_ticket_countscope(_ticket tickets_ticket) RETURNS TEXT STABLE AS $$
BEGIN
    RETURN format('tickets:%s:%s:%s', _ticket.status, _ticket.topic_id, COALESCE(_ticket.assignee_id, 0));
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Trigger procedure to update contact ticket counts
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_ticket_on_change() RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN -- new ticket inserted
    IF NEW.status = 'O' THEN
      UPDATE contacts_contact SET ticket_count = ticket_count + 1, modified_on = NOW() WHERE id = NEW.contact_id;
    END IF;
  ELSIF TG_OP = 'UPDATE' THEN -- existing ticket updated
    IF OLD.status = 'O' AND NEW.status = 'C' THEN -- ticket closed
      UPDATE contacts_contact SET ticket_count = ticket_count - 1, modified_on = NOW() WHERE id = OLD.contact_id;
    ELSIF OLD.status = 'C' AND NEW.status = 'O' THEN -- ticket reopened
      UPDATE contacts_contact SET ticket_count = ticket_count + 1, modified_on = NOW() WHERE id = OLD.contact_id;
    END IF;
  ELSIF TG_OP = 'DELETE' THEN -- existing ticket deleted
    IF OLD.status = 'O' THEN -- open ticket deleted
      UPDATE contacts_contact SET ticket_count = ticket_count - 1, modified_on = NOW() WHERE id = OLD.contact_id;
    END IF;
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles DELETE statements on ticket table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_ticket_on_delete() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_ticket_countscope(oldtab), -count(*), FALSE FROM oldtab
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles INSERT statements on ticket table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_ticket_on_insert() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT org_id, temba_ticket_countscope(newtab), count(*), FALSE FROM newtab
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles UPDATE statements on ticket table
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_ticket_on_update() RETURNS TRIGGER AS $$
BEGIN
    -- add negative counts for all old count scopes that don't match the new ones
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT o.org_id, temba_ticket_countscope(o), -count(*), FALSE FROM oldtab o
    INNER JOIN newtab n ON n.id = o.id
    WHERE temba_ticket_countscope(o) != temba_ticket_countscope(n)
    GROUP BY 1, 2;

    -- add positive counts for all new count scopes that don't match the old ones
    INSERT INTO orgs_itemcount("org_id", "scope", "count", "is_squashed")
    SELECT n.org_id, temba_ticket_countscope(n), count(*), FALSE FROM newtab n
    INNER JOIN oldtab o ON o.id = n.id
    WHERE temba_ticket_countscope(o) != temba_ticket_countscope(n)
    GROUP BY 1, 2;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION temba_update_category_counts(_flow_id integer, new json, old json)
 RETURNS void
 LANGUAGE plpgsql
AS $function$
DECLARE
  DECLARE node_uuid text;
  DECLARE result_key text;
  DECLARE result_value text;
  DECLARE value_key text;
  DECLARE value_value text;
  DECLARE _new json;
  DECLARE _old json;
BEGIN
    -- look over the keys in our new results
    FOR result_key, result_value IN SELECT key, value from json_each(new)
    LOOP
        -- if its a new key, create a new count
        IF (old->result_key) IS NULL THEN
            execute temba_insert_flowcategorycount(_flow_id, result_key, new->result_key, 1);
        ELSE
            _new := new->result_key;
            _old := old->result_key;

            IF (_old->>'node_uuid') = (_new->>'node_uuid') THEN
                -- we already have this key, check if the value is newer
                IF timestamptz(_new->>'created_on') > timestamptz(_old->>'created_on') THEN
                    -- found an update to an existing key, create a negative and positive count accordingly
                    execute temba_insert_flowcategorycount(_flow_id, result_key, _old, -1);
                    execute temba_insert_flowcategorycount(_flow_id, result_key, _new, 1);
                END IF;
            ELSE
                -- the parent has changed, out with the old in with the new
                execute temba_insert_flowcategorycount(_flow_id, result_key, _old, -1);
                execute temba_insert_flowcategorycount(_flow_id, result_key, _new, 1);
            END IF;
        END IF;
    END LOOP;

    -- look over keys in our old results that might now be gone
    FOR result_key, result_value IN SELECT key, value from json_each(old)
    LOOP
        IF (new->result_key) IS NULL THEN
            -- found a key that's since been deleted, add a negation
            execute temba_insert_flowcategorycount(_flow_id, result_key, old->result_key, -1);
        END IF;
    END LOOP;
END;
$function$;

----------------------------------------------------------------------
-- Manages keeping track of the # of messages in our channel log
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_update_channellog_count() RETURNS TRIGGER AS $$
BEGIN
  -- ChannelLog being added
  IF TG_OP = 'INSERT' THEN
    -- Error, increment our error count
    IF NEW.is_error THEN
      PERFORM temba_insert_channelcount(NEW.channel_id, 'LE', NULL::date, 1);
    -- Success, increment that count instead
    ELSE
      PERFORM temba_insert_channelcount(NEW.channel_id, 'LS', NULL::date, 1);
    END IF;

  -- Updating is_error is forbidden
  ELSIF TG_OP = 'UPDATE' THEN
    RAISE EXCEPTION 'Cannot update is_error or channel_id on ChannelLog events';

  -- Deleting, decrement our count
  ELSIF TG_OP = 'DELETE' THEN
    -- Error, decrement our error count
    IF OLD.is_error THEN
      PERFORM temba_insert_channelcount(OLD.channel_id, 'LE', NULL::date, -1);
    -- Success, decrement that count instead
    ELSE
      PERFORM temba_insert_channelcount(OLD.channel_id, 'LS', NULL::date, -1);
    END IF;

  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Handles changes to a run's results
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_update_flowcategorycount() RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        EXECUTE temba_update_category_counts(NEW.flow_id, NEW.results::json, NULL);
    ELSIF TG_OP = 'UPDATE' THEN
        -- use string comparison to check for no-change case
        IF NEW.results = OLD.results THEN RETURN NULL; END IF;

        EXECUTE temba_update_category_counts(NEW.flow_id, NEW.results::json, OLD.results::json);
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

----------------------------------------------------------------------
-- Trigger procedure to update contact system groups on column changes
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_contact_system_groups() RETURNS TRIGGER AS $$
BEGIN
  -- new contact added
  IF TG_OP = 'INSERT' AND NEW.is_active THEN
    IF NEW.status = 'A' THEN
      PERFORM contact_toggle_system_group(NEW, 'A', true);
    ELSIF NEW.status = 'B' THEN
      PERFORM contact_toggle_system_group(NEW, 'B', true);
    ELSIF NEW.status = 'S' THEN
      PERFORM contact_toggle_system_group(NEW, 'S', true);
    ELSIF NEW.status = 'V' THEN
      PERFORM contact_toggle_system_group(NEW, 'V', true);
    END IF;
  END IF;

  -- existing contact updated
  IF TG_OP = 'UPDATE' THEN
    -- do nothing for inactive contacts
    IF NOT OLD.is_active AND NOT NEW.is_active THEN
      RETURN NULL;
    END IF;

    IF OLD.status != NEW.status THEN
      PERFORM contact_toggle_system_group(NEW, OLD.status, false);
      PERFORM contact_toggle_system_group(NEW, NEW.status, true);
    END IF;

    -- is being released
    IF OLD.is_active AND NOT NEW.is_active THEN
      PERFORM contact_toggle_system_group(NEW, 'A', false);
      PERFORM contact_toggle_system_group(NEW, 'B', false);
      PERFORM contact_toggle_system_group(NEW, 'S', false);
      PERFORM contact_toggle_system_group(NEW, 'V', false);
    END IF;

    -- is being unreleased
    IF NOT OLD.is_active AND NEW.is_active THEN
      PERFORM contact_toggle_system_group(NEW, NEW.status, true);
    END IF;
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

