import aipkgs_notifications.enums as enums
import aipkgs_notifications.utils as utils


class AlertPayload:
    def __init__(self, title: str, subtitle: str = None, body: str = None):
        self.localized = False

        self.title_loc_key = None
        self.title_loc_args = None
        self.subtitle_loc_key = None
        self.subtitle_loc_args = None
        self.body_loc_key = None
        self.body_loc_args = None

        self.title = title
        self.subtitle = subtitle
        self.body = body

    def to_dict(self) -> dict:
        data = {"title": self.title,
                "subtitle": self.subtitle,
                "body": self.body}

        if self.localized:
            data["title-loc-key"] = self.title_loc_key
            data["title-loc-args"] = self.title_loc_args
            data["subtitle-loc-key"] = self.subtitle_loc_key
            data["subtitle-loc-args"] = self.subtitle_loc_args
            data["body-loc-key"] = self.body_loc_key
            data["body-loc-args"] = self.body_loc_args

        data = utils.remove_nulls(data)
        return data

    def localize_payload(self, title_loc_key: str = None, title_loc_args: list = None, subtitle_loc_key: str = None, subtitle_loc_args: list = None, body_loc_key: str = None,
                         body_loc_args: list = None) -> None:
        self.localized = True

        self.title_loc_key = title_loc_key
        self.title_loc_args = title_loc_args
        self.subtitle_loc_key = subtitle_loc_key
        self.subtitle_loc_args = subtitle_loc_args
        self.body_loc_key = body_loc_key
        self.body_loc_args = body_loc_args


class SoundPayload:
    def __init__(self, name: str, critical: bool = None, volume: int = None):
        self.name = name
        self.critical = critical
        self.volume = volume

    def to_dict(self) -> dict:
        data = {"name": self.name,
                "critical": 1 if self.critical else None,
                "volume": self.volume if (self.volume and ((self.volume >= 0) and (self.volume <= 1))) else None}

        data = utils.remove_nulls(data)

        return data


class Payload:
    def __init__(self, alert: AlertPayload = None, category: str = None, sound: SoundPayload = None, badge: int = None, data: dict = None, thread_id: str = None,
                 content_available: bool = None, mutable_content: bool = None, target_content_id: str = None,
                 target_content_type: str = None, target_content_url: str = None, interruption_level: enums.InterruptionLevel = None, relevance_score: int = None,
                 filter_criteria: str = None,
                 stale_date: str = None, content_state: dict = None, timestamp: int = None, event: str = None, dismissal_date: int = None):
        self.alert = alert
        self.category = category
        self.sound = sound
        self.badge = badge
        self.data = data
        self.thread_id = thread_id
        self.content_available = content_available
        self.mutable_content = mutable_content
        self.target_content_id = target_content_id
        self.target_content_type = target_content_type
        self.target_content_url = target_content_url
        self.interruption_level = interruption_level
        self.relevance_score = relevance_score
        self.filter_criteria = filter_criteria
        self.stale_date = stale_date
        self.content_state = content_state
        self.timestamp = timestamp
        self.event = event
        self.dismissal_date = dismissal_date

    def to_dict(self) -> dict:
        data = {"aps": {"alert": self.alert.to_dict() if self.alert else None,
                        "category": self.category,
                        "sound": self.sound.to_dict() if self.sound else {"name": "default"},
                        "badge": self.badge,
                        "thread-id": self.thread_id,
                        "content-available": 1 if self.content_available else None,
                        "mutable-content": 1 if self.mutable_content else None,
                        "target-content-id": self.target_content_id,
                        "target-content-type": self.target_content_type,
                        "target-content-url": self.target_content_url,
                        "interruption-level": self.interruption_level.value if self.interruption_level else None,
                        "relevance-score": self.relevance_score if (self.relevance_score and ((self.relevance_score >= 0) and (self.relevance_score <= 1))) else None,
                        "filter-criteria": self.filter_criteria,
                        "stale-date": self.stale_date,
                        "content-state": self.content_state,
                        "timestamp": self.timestamp,
                        "event": self.event,
                        "dismissal-date": self.dismissal_date
                        },
                "data": self.data}

        # if self.push_type == apns.PushType.background:
        #     data["aps"]["content-available"] = 1

        if self.content_available:
            data["aps"]["alert"] = None
            data["aps"]["sound"] = None
            data["aps"]["badge"] = None

        data = utils.remove_nulls(data)

        return data
