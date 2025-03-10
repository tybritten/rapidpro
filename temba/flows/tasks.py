import itertools
import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone as tzone

from django_redis import get_redis_connection

from django.conf import settings
from django.utils import timezone
from django.utils.timesince import timesince

from temba import mailroom
from temba.utils.crons import cron_task
from temba.utils.models import delete_in_batches

from .models import FlowActivityCount, FlowResultCount, FlowRevision, FlowRun, FlowSession, FlowStartCount

logger = logging.getLogger(__name__)


@cron_task(lock_timeout=7200)
def squash_flow_counts():
    FlowActivityCount.squash()
    FlowResultCount.squash()
    FlowStartCount.squash()


@cron_task()
def trim_flow_revisions():
    start = timezone.now()

    # get when the last time we trimmed was
    r = get_redis_connection()
    last_trim = r.get(FlowRevision.LAST_TRIM_KEY)
    if not last_trim:
        last_trim = 0

    last_trim = datetime.utcfromtimestamp(int(last_trim)).astimezone(tzone.utc)
    count = FlowRevision.trim(last_trim)

    r.set(FlowRevision.LAST_TRIM_KEY, int(timezone.now().timestamp()))

    elapsed = timesince(start)
    logger.info(f"Trimmed {count} flow revisions since {last_trim} in {elapsed}")


@cron_task()
def interrupt_flow_sessions():
    """
    Interrupt old flow sessions which have exceeded the absolute time limit
    """

    before = timezone.now() - timedelta(days=89)
    num_interrupted = 0

    # get old sessions and organize into lists by org
    by_org = defaultdict(list)
    sessions = (
        FlowSession.objects.filter(created_on__lte=before, status=FlowSession.STATUS_WAITING)
        .only("id", "contact")
        .select_related("contact__org")
        .order_by("id")
    )
    for session in sessions:
        by_org[session.contact.org].append(session)

    for org, sessions in by_org.items():
        for batch in itertools.batched(sessions, 100):
            mailroom.queue_interrupt(org, sessions=batch)
            num_interrupted += len(sessions)

    return {"interrupted": num_interrupted}


@cron_task()
def trim_flow_sessions():
    """
    Cleanup ended flow sessions
    """

    trim_before = timezone.now() - settings.RETENTION_PERIODS["flowsession"]

    def pre_delete(session_ids):
        # detach any flows runs that belong to these sessions
        FlowRun.objects.filter(session_id__in=session_ids).update(session_id=None)

    num_deleted = delete_in_batches(FlowSession.objects.filter(ended_on__lte=trim_before), pre_delete=pre_delete)

    return {"deleted": num_deleted}
