#include "contiki.h"
#include "dev/serial-line.h"
#include "net/rime/rime.h"
#include "net/netstack.h"

#ifdef IOTLAB_M3
#include "dev/light-sensor.h"
#include "dev/pressure-sensor.h"
#endif
#include "dev/acc-mag-sensor.h"
#include "dev/gyr-sensor.h"

#include "dev/leds.h"
#include "dev/spi.h"
#include "dev/cc2420/cc2420.h"
#include "dev/cc2420/cc2420_const.h"
#include <stdio.h>

/*
 * Prints "Hello World !", and echoes whatever arrives on the serial link
 */
 #ifdef IOTLAB_M3

 /* Light sensor */
 static void config_light()
 {
   light_sensor.configure(LIGHT_SENSOR_SOURCE, ISL29020_LIGHT__AMBIENT);
   light_sensor.configure(LIGHT_SENSOR_RESOLUTION, ISL29020_RESOLUTION__16bit);
   light_sensor.configure(LIGHT_SENSOR_RANGE, ISL29020_RANGE__1000lux);
   SENSORS_ACTIVATE(light_sensor);
 }

 static float process_light()
 {
   int light_val = light_sensor.value(0);
   float light = ((float)light_val) / LIGHT_SENSOR_VALUE_SCALE;
   return light;
 }

 /* Pressure */
 static void config_pressure()
 {
   pressure_sensor.configure(PRESSURE_SENSOR_DATARATE, LPS331AP_P_12_5HZ_T_1HZ);
   SENSORS_ACTIVATE(pressure_sensor);
 }

 static float process_pressure()
 {
   int pressure;
   pressure = pressure_sensor.value(0);
   return ((float)pressure / PRESSURE_SENSOR_VALUE_SCALE);
 }
 #endif

 float light[5];
 float pressure[5];
 int i;

PROCESS(serial_echo, "Serial Echo");
AUTOSTART_PROCESSES(&serial_echo);

/*---------------------------------------------------------------------------*/
PROCESS_THREAD(serial_echo, ev, data)
{
  PROCESS_BEGIN();
  static struct etimer timer;
  static struct etimer etimerbegin;

  #ifdef IOTLAB_M3
    config_light();
    config_pressure();
  #endif


       PROCESS_YIELD();
       etimer_set(&timer, CLOCK_SECOND);
       for(i=0;i<5;i++){
         PROCESS_WAIT_EVENT_UNTIL(etimer_expired(&timer));
         light[i] = process_light();
         pressure[i] = process_pressure();
         etimer_restart(&timer);
       }
       printf("light: [%f, %f, %f, %f, %f]\n", light[0], light[1], light[2], light[3], light[4]);
       printf("pressure: [%f, %f, %f, %f, %f]\n", pressure[0], pressure[1], pressure[2], pressure[3], pressure[4]);
   PROCESS_END();
 }
