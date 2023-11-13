# Generated by Django 4.2.3 on 2023-11-13 19:22

from django.db import migrations

SQL = """
----------------------------------------------------------------------
-- Trigger procedure to notification counts on notification changes
----------------------------------------------------------------------
CREATE OR REPLACE FUNCTION temba_notification_on_change() RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' AND position('U' IN NEW.medium) > 0 AND NOT NEW.is_seen THEN -- new notification inserted
    PERFORM temba_insert_notificationcount(NEW.org_id, NEW.user_id, 1);
  ELSIF TG_OP = 'UPDATE' AND position('U' IN NEW.medium) > 0 THEN -- existing notification updated
    IF OLD.is_seen AND NOT NEW.is_seen THEN -- becoming unseen again
      PERFORM temba_insert_notificationcount(NEW.org_id, NEW.user_id, 1);
    ELSIF NOT OLD.is_seen AND NEW.is_seen THEN -- becoming seen
      PERFORM temba_insert_notificationcount(NEW.org_id, NEW.user_id, -1);
    END IF;
  ELSIF TG_OP = 'DELETE' AND position('U' IN OLD.medium) > 0 AND NOT OLD.is_seen THEN -- existing notification deleted
    PERFORM temba_insert_notificationcount(OLD.org_id, OLD.user_id, -1);
  END IF;
  RETURN NULL;
END;
$$ LANGUAGE plpgsql;
"""


class Migration(migrations.Migration):
    dependencies = [
        ("notifications", "0015_remove_notification_notificatio_org_id_f9db19_idx_and_more"),
    ]

    operations = [migrations.RunSQL(SQL)]
