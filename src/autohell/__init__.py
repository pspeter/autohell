import sys
from collections.abc import Sequence
from datetime import UTC, datetime, time, timedelta
from time import sleep
from typing import NamedTuple

import screen_brightness_control as sbc

from autohell.__about__ import __version__


class Period(NamedTuple):
    start: datetime
    end: datetime


def now_tz_aware() -> datetime:
    return datetime.now(tz=UTC).astimezone()


TODAY = now_tz_aware().date()
YESTERDAY = TODAY - timedelta(days=1)
DAY_START = datetime.combine(TODAY, time(8, 30, tzinfo=UTC))
FADE_PERIOD = Period(
    datetime.combine(TODAY, time(19, 00, tzinfo=UTC)),
    datetime.combine(TODAY, time(21, 00, tzinfo=UTC)),
)
FADE_DELTA = FADE_PERIOD.end - FADE_PERIOD.start
MIN_BRIGHTNESS = 5
MAX_BRIGHTNESS = 60
BRIGHTNESS_DELTA = MAX_BRIGHTNESS - MIN_BRIGHTNESS
CHANGE_EVERY = timedelta(minutes=1)
GRACE_PERIOD_AFTER_MANUAL_CHANGE = timedelta(hours=3)


def sleep_until(until: datetime, max_dur: timedelta = timedelta(minutes=5)) -> None:
    current_time = now_tz_aware()
    sleep_secs = min(max_dur.total_seconds(), (until - current_time).total_seconds())
    if sleep_secs > 0:
        sleep(sleep_secs)


def sleep_as_long_as_needed() -> None:
    current_time = now_tz_aware()
    if current_time < DAY_START:
        sleep_until(DAY_START)
    elif current_time < FADE_PERIOD.start:
        sleep_until(FADE_PERIOD.start)
    elif current_time < FADE_PERIOD.end:
        sleep(CHANGE_EVERY.total_seconds())
    else:
        sleep_until(DAY_START)


def adapt_brightness(current_time):
    if current_time < DAY_START or current_time > FADE_PERIOD.end:
        target = MIN_BRIGHTNESS
    elif FADE_PERIOD.start < current_time <= FADE_PERIOD.end:
        diff_time = current_time - FADE_PERIOD.start
        frac = diff_time / FADE_DELTA
        target = round(MAX_BRIGHTNESS - (BRIGHTNESS_DELTA * frac))
    else:
        target = MAX_BRIGHTNESS

    print(f"Setting brightness to: {target}")
    sbc.set_brightness(target)


def main(args: Sequence[str] | None = None) -> None:  # noqa: ARG001
    args = args if args else sys.argv[1:]
    if args and ("-V" in args or "--version" in args):
        print(f"autohell {__version__}")
    elif args:
        print(f"autohell currently does not take any arguments")
        exit(1)

    current_brightness = sbc.get_brightness()
    print("Current brightness:", current_brightness)
    prev_brightness = current_brightness
    last_manual_change = None

    adapt_brightness(now_tz_aware())
    while True:
        sleep_as_long_as_needed()

        current_time = now_tz_aware()
        current_brightness = sbc.get_brightness()

        if prev_brightness != current_brightness:
            print(f"Manual change detected, disabling autohell for {GRACE_PERIOD_AFTER_MANUAL_CHANGE}")
            last_manual_change = now_tz_aware()

        if last_manual_change and current_time - last_manual_change < GRACE_PERIOD_AFTER_MANUAL_CHANGE:
            prev_brightness = current_brightness
            continue

        adapt_brightness(current_time)

        prev_brightness = sbc.get_brightness()
