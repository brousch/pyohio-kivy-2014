from jnius import autoclass, cast
from plyer.platforms.android import activity
from plyer.facades import Battery

Intent = autoclass('android.content.Intent')
BatteryManager = autoclass('android.os.BatteryManager')
IntentFilter = autoclass('android.content.IntentFilter')


class AndroidBattery(Battery):
    def _get_status(self):
        status = {"connected": None, "percentage": None}

        ifilter = IntentFilter(Intent.ACTION_BATTERY_CHANGED)

        batteryStatus = cast('android.content.Intent',
            activity.registerReceiver(None, ifilter))

        query = batteryStatus.getIntExtra(BatteryManager.EXTRA_STATUS, -1)
        isCharging = (query == BatteryManager.BATTERY_STATUS_CHARGING or
                     query == BatteryManager.BATTERY_STATUS_FULL)

        level = batteryStatus.getIntExtra(BatteryManager.EXTRA_LEVEL, -1)
        scale = batteryStatus.getIntExtra(BatteryManager.EXTRA_SCALE, -1)
        percentage = level / float(scale)

        status['connected'] = isCharging
        status['percentage'] = percentage * 100

        return status


def instance():
    return AndroidBattery()
