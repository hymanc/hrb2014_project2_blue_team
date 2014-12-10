#include "ch.h"
#include "hal.h"
#include "chprintf.h"

#include <stdlib.h>
#include <string.h>

#define ADC_BUF_DEPTH 2 // Double buffered ADC
#define ADC_CH_NUM 1

//static ADCConfig adccfg = {};
static adcsample_t samples[ADC_BUF_DEPTH * ADC_CH_NUM];

static const ADCConversionGroup adcgrpcfg = {
    FALSE,
    ADC_CH_NUM,
    NULL,
    NULL,
    0, 0,
    ADC_SMPR1_SMP_AN10(ADC_SAMPLE_1P5),
    0,
    ADC_SQR1_NUM_CH(ADC_CH_NUM),
    0,
    ADC_SQR3_SQ1_N(ADC_CHANNEL_IN0)
};

// Serial configuration
static SerialConfig ser_cfg = 
{
   38400,
   0,
   0,
   0,
};



/*
 * Application entry point.
 */
int main(void) 
{
    halInit();    	// ChibiOS HAL initialization
    chSysInit();	// ChibiOS System Initialization

    /* Configure I/O */
    // Serial
    palSetPadMode(GPIOA, 2, PAL_MODE_STM32_ALTERNATE_PUSHPULL); // Tx
    palSetPadMode(GPIOA, 3, PAL_MODE_INPUT); // Rx
    
    // Motor Control
    palSetPadMode(GPIOA, 8, PAL_MODE_STM32_ALTERNATE_PUSHPULL);
    palSetPadMode(GPIOA, 9, PAL_MODE_STM32_ALTERNATE_PUSHPULL);
    palSetPadMode(GPIOA, 10, PAL_MODE_OUTPUT_PUSHPULL);
    palSetPadMode(GPIOA, 11, PAL_MODE_OUTPUT_PUSHPULL);
    
    palSetPadMode(GPIOA, 0, PAL_MODE_INPUT_ANALOG); // Set ADC input pin
    
    /* Serial Port Startup */
    sdStart(&SD2, &ser_cfg);	// Activate VCP USART2 driver
    
    /* ADC Startup */
    adcStart(&ADCD1, NULL);      // Activate ADC driver
    //adcStartConversion(&ADCD1, &adcgrpcfg, &samples[0], ADC_BUF_DEPTH);
    
    uint16_t setpoint;
    uint16_t feedback_value;
    
    uint16_t err;
    uint16_t err_d;
    uint32_t err_i;

    char out[64];
    while (TRUE) 
    {
	// ADC Read
	adcConvert(&ADCD1, &adcgrpcfg, samples, ADC_BUF_DEPTH);
	// Convert sample to string
	chThdSleepMilliseconds(100);
	//sdWrite(&SD2, "ABC\n", 4);
	sprintf(out, "PRINTY");
	sdWrite(&SD2, out, 7);
	// Test Blinky
	/*
	palClearPad(GPIOA, GPIOA_LED_GREEN);
	chThdSleepMilliseconds(500);
	palSetPad(GPIOA, GPIOA_LED_GREEN);
	chThdSleepMilliseconds(500);
	*/
    }
  return 0;
}
