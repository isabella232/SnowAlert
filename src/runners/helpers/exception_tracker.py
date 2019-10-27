import pybrake
import sentry_sdk
from ..config import ENV, AIRBRAKE_PROJECT_KEY, AIRBRAKE_PROJECT_ID, SENTRY_DSN


class ExceptionTracker:
    airbrake_notifier = None

    def __init__(self):
        if SENTRY_DSN:
            sentry_sdk.init(SENTRY_DSN)
            self.use_sentry = True

        if AIRBRAKE_PROJECT_KEY and AIRBRAKE_PROJECT_ID:
            self.airbrake_notifier = pybrake.Notifier(
                project_id=AIRBRAKE_PROJECT_ID,
                project_key=AIRBRAKE_PROJECT_KEY,
                environment=ENV,
            )

    def notify(self, *args):
        for a in args:
            if self.use_sentry:
                try:
                    if isinstance(a, Exception)
                        sentry_sdk.capture_exception(a)
                    else:
                        sentry_sdk.capture_message(a)
                except Exception as e:
                    print(e)
            if self.airbrake_notifier:
                try:
                    self.airbrake_notifier.notify(a)
                except Exception as e:
                    print(e)
