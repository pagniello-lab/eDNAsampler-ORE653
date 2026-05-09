import json
import datetime
from sampler import run_sampler

CONFIG_FILE = "config.json"


def load_config():
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)


def parse_sample_time(time_str):
    """Convert HH:MM string to a datetime.time object."""
    return datetime.datetime.strptime(time_str, "%H:%M").time()


def should_run_now(config):
    """Return True if the sampler is armed and it's time to run."""
    if not config.get("armed", False):
        return False

    sample_time = parse_sample_time(config.get("sample_time", "02:00"))
    current_time = datetime.datetime.now().time()

    return abs(
    datetime.datetime.combine(datetime.date.today(), current_time) -
    datetime.datetime.combine(datetime.date.today(), sample_time)
    ).seconds < 60

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def main():
    config = load_config()

    # 1. Must be armed
    if not config.get("armed", False):
        print("Not armed. Exiting.")
        return

    # 2. Check schedule
    if not should_run_now(config):
        print("Armed, but not scheduled time yet.")
        return

    # 3. Run sampler ONCE
    print("Scheduled sample time reached. Starting sampling sequence...")

    config = run_sampler(config)

    # 4. Persist updated state (armed -> False)
    save_config(config)

if __name__ == "__main__":
    main()
