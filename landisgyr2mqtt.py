import ultraheat_api as hm
import os
import paho.mqtt.client as mqtt
import simplejson as json

broker_address="BROKER_IP"
client = mqtt.Client("meterreader")
client.username_pw_set("BROKER_USER", "BROKER_PASSWORD")
client.connect(broker_address)

# Check available ports
ports = hm.find_ports()
for p in ports:
    print(p.device)
print(len(ports), 'ports found')

# Read the Ultraheat device
heat_meter_service = hm.HeatMeterService(hm.UltraheatReader("/dev/ttyUSB0")) # Replace /dev/ttyUSB0 with "by-id" address...
response_data = heat_meter_service.read()

heaterStats = {
    "heat_usage_mwh"                            : response_data.heat_usage_mwh,
    "heat_usage_gj"                             : response_data.heat_usage_gj,
    "volume_usage_m3"                           : response_data.volume_usage_m3,
    "ownership_number"                          : response_data.ownership_number,
    "volume_previous_year_m3"                   : response_data.volume_previous_year_m3,
    "heat_previous_year_mwh"                    : response_data.heat_previous_year_mwh,
    "heat_previous_year_gj"                     : response_data.heat_previous_year_gj,
    "error_number"                              : response_data.error_number,
    "device_number"                             : response_data.device_number,
    "measurement_period_minutes"                : response_data.measurement_period_minutes,
    "power_max_kw"                              : response_data.power_max_kw,
    "power_max_previous_year_kw"                : response_data.power_max_previous_year_kw,
    "flowrate_max_m3ph"                         : response_data.flowrate_max_m3ph,
    "flowrate_max_previous_year_m3ph"           : response_data.flowrate_max_previous_year_m3ph,
    "flow_temperature_max_c"                    : response_data.flow_temperature_max_c,
    "return_temperature_max_c"                  : response_data.return_temperature_max_c,
    "flow_temperature_max_previous_year_c"      : response_data.flow_temperature_max_previous_year_c,
    "return_temperature_max_previous_year_c"    : response_data.return_temperature_max_previous_year_c,
    "operating_hours"                           : response_data.operating_hours,
    "fault_hours"                               : response_data.fault_hours,
    "fault_hours_previous_year"                 : response_data.fault_hours_previous_year,
    "yearly_set_day"                            : response_data.yearly_set_day,
    "monthly_set_day"                           : response_data.monthly_set_day,
    "meter_date_time"                           : response_data.meter_date_time,
    "measuring_range_m3ph"                      : response_data.measuring_range_m3ph,
    "settings_and_firmware"                     : response_data.settings_and_firmware,
    "flow_hours"                                : response_data.flow_hours
}
for reading in heaterStats:
    client.publish("keller/heatreader/" + reading, str(heaterStats[reading]))
