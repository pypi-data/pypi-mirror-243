import json
from datetime import datetime
from unittest.mock import MagicMock

from chinoscriba.rest import RESTResponse
from dateutil.tz import UTC
from django.utils import timezone


def _mock_nullable_stats():
    """Mocks a stats response that contains None items

    To check which items can be None, refer to stats.serializers.StatSerializer
    and make sure this test is updated.
    """
    def wrapper(*args, **kwargs):
        res = MagicMock(spec=RESTResponse)
        # fixme: restore when the SDK generator supports nullable fields
        # data = json.dumps({
        #     "manual_logs": None,
        #     "all_logs": None,
        #     "oldest_log": None,
        #     "total_blocks": 0,
        #     "total_log_in_blocks": 0,
        #     "oldest_block": None,
        #     "month_data": {}
        # })
        empty_date = timezone.make_aware(datetime.min, timezone=UTC)
        empty_date = empty_date.strftime("%Y-%m-%dT%H:%M:%S.%f%z")
        data = json.dumps({
            "manual_logs": 0,
            "all_logs": 0,
            "oldest_log": empty_date,
            "total_blocks": 0,
            "total_log_in_blocks": 0,
            "oldest_block": empty_date,
            "month_data": {}
        })
        res.configure_mock(data=data)
        return res

    return wrapper
