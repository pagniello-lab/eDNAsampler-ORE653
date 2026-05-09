from datetime import datetime, timedelta
import os
import math

WITTY_PI_DIR = "/home/ore653/wittypi"
SCHEDULE_FILE = f"{WITTY_PI_DIR}/schedule.wpi"
RUN_SCRIPT = f"{WITTY_PI_DIR}/runScript.sh"

MOTOR_CYCLES = 3

# BREAKS IF YOU TRY TO SCHEDULE AN EVENT UNDER 2 MIN AWAY

def schedule_wakeup(sample_time, sample_duration, pres_duration, interval_min):

    now = datetime.now()

    # -------- WAKE TIME --------
    wake = datetime.strptime(sample_time, "%H:%M").replace(
        year=now.year,
        month=now.month,
        day=now.day
    )

    # SETS IT TO BE TOMORROW AT THE DESIRED TIME IF TODAY IS ALREADY PAST THIS TIME.
    if wake <= now:
        wake += timedelta(days=1)

    # -------- SAMPLE RUNTIME --------
    interval_sec = interval_min*60
    runtime_sec = sample_duration + interval_sec + pres_duration + 180 # Adds 3 min for transitions and startup
    runtime_min = math.ceil(runtime_sec / 60)

    wake_offset_sec = max(0, int((wake - now).total_seconds()))

    wake_offset_hrs = wake_offset_sec // 3600
    wake_offset_min = (wake_offset_sec % 3600) // 60
    wake_offset_sec_remainder = wake_offset_sec % 60

    # -------- FIXED WITTY PI SCHEDULE --------      BREAKS IF YOU TRY TO SCHEDULE AN EVENT UNDER 2 MIN AWAY
    schedule_text = f"""BEGIN {now.strftime('%Y-%m-%d %H:%M:%S')}
END   2035-12-31 23:59:59

ON M2
OFF H{wake_offset_hrs} M{wake_offset_min - 2} S{wake_offset_sec_remainder}

ON M{runtime_min}
OFF M15 WAIT
"""

    schedule_file = "/home/ore653/wittypi/schedule.wpi"

    with open(schedule_file, "w") as f:
        f.write(schedule_text)

    # ---------------- APPLY TO WITTY PI ----------------
    os.system(f"cd {WITTY_PI_DIR} && sudo ./runScript.sh")

    print("[Scheduler] Witty Pi schedule applied")
