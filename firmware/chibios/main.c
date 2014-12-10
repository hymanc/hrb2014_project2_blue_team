#include "ch.h"
#include "hal.h"
#include "chprintf.h"

#include <stdlib.h>
#include <math.h>

#define INTEGRAL_MAX 65535

#define ADC_BUF_DEPTH 2 // Double buffered ADC
#define ADC_CH_NUM 1

//static ADCConfig adccfg = {};
static adcsample_t samples[ADC_BUF_DEPTH * ADC_CH_NUM];

static const ADCConversionGroup adcgrpcfg = 
{
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
   57600,
   0,
   0,
   0,
};

// PWM Configuration
static PWMConfig pwmcfg = 
{
   1E6,
   100,
   NULL,
   {
       {PWM_OUTPUT_ACTIVE_HIGH, NULL},
       {PWM_OUTPUT_ACTIVE_HIGH, NULL},
       {PWM_OUTPUT_DISABLED, NULL},
       {PWM_OUTPUT_DISABLED, NULL}
   },
   0,
   0,
   0
};

/**
 * @brief
 */
char toHexCharacter(uint8_t nibble)
{
    switch(nibble)
    {
	case 0x0:	return '0';
	case 0x1:	return '1';
	case 0x2:	return '2';
	case 0x3: 	return '3';
	case 0x4:	return '4';
	case 0x5: 	return '5';
	case 0x6:	return '6';
	case 0x7: 	return '7';
	case 0x8:	return '8';
	case 0x9: 	return '9';
	case 0xA: 	return 'A';
	case 0xB: 	return 'B';
	case 0xC:	return 'C';
	case 0xD:	return 'D';
	case 0xE:	return 'E';
	case 0xF:	return 'F'; 
	default:	return 'Q';
    }
    return '0';
}

/**
 * @brief
 */
void toHex16Str(uint16_t hexVal, char *outStr)
{
    outStr[0] = toHexCharacter((uint8_t) (hexVal >> 12));
    outStr[1] = toHexCharacter((uint8_t) (hexVal >> 8) & 0xF);
    outStr[2] = toHexCharacter((uint8_t) (hexVal >> 4) & 0xF);
    outStr[3] = toHexCharacter((uint8_t) (hexVal) & 0xF);
}

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
    
    /* PWM Setup */
    pwmStart(&PWMD1, &pwmcfg);
    pwmEnableChannel(&PWMD1, 0, PWM_PERCENTAGE_TO_WIDTH(&PWMD1, 0050));
    pwmEnableChannel(&PWMD1, 1, PWM_PERCENTAGE_TO_WIDTH(&PWMD1, 0050));
    
    uint16_t setpoint;
    uint16_t feedbackValue;
    
    int16_t err;
    int16_t err_d;
    int32_t err_i;
    int16_t last_err;
    
    int32_t command; 
    uint16_t currentDuty = 0050;
    
    // TODO Fractional PID
    int16_t KP = 1;
    int16_t KI = 1;
    int16_t KD = 1;
    
    uint32_t loopCounter;
    char out[64];
    out[0] = 'F';
    out[1] = ':';
    out[6] = '\n';
    
    while (TRUE) 
    {
	// Read serial input
	
	// ADC Read of feedback
	adcConvert(&ADCD1, &adcgrpcfg, samples, ADC_BUF_DEPTH);
	
	// TODO: Compute control
	feedbackValue = samples[0];
	/*
	last_err = err;
	err = setpoint - feedbackValue;
	err_d = err - last_err;
	err_i += err;
	if(err_i > INTEGRAL_MAX)
	{
	    err_i = INTEGRAL_MAX;
	}
	else if(err_i < -INTEGRAL_MAX)
	{
	    err_i = -INTEGRAL_MAX;
	}
	*/
	//command = KP * err + KD * err_d + KI * err_i;
	command = err/10;
	currentDuty = abs(command);
	if(currentDuty > 8000)
	{
	    currentDuty = 8000;
	}
	
	chThdSleepMilliseconds(50);
	
	if((loopCounter % 10) == 0)
	{
	    palTogglePad(GPIOA, GPIOA_LED_GREEN);
	    // Publish data to the serial port
	    toHex16Str(feedbackValue, (out + 2));
	    sdWrite(&SD2, (uint8_t *) out, 7);
	}
	
	loopCounter++;
    }
  return 0;
}
