#include "ch.h"
#include "hal.h"
#include "chprintf.h"

#include <stdlib.h>
#include <math.h>

#define MDIR_A 11
#define MDIR_B 12

#define INTEGRAL_MAX 65535

#define ADC_BUF_DEPTH 2 // Double buffered ADC
#define ADC_CH_NUM 1

#define KP 1
#define KI 0
#define KD 0

//static ADCConfig adccfg = {};
static adcsample_t samples[ADC_BUF_DEPTH * ADC_CH_NUM];

typedef struct
{
    int16_t errorP;
    int32_t errorI;
    int16_t errorD;
    int16_t errorLast;
}error_t;

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
   1000,
   NULL,
   {
       {PWM_OUTPUT_ACTIVE_HIGH, NULL},
       {PWM_OUTPUT_DISABLED, NULL},
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

/**
 * 
 */
void disableMotor(void)
{
    // TODO: Set duty cycles to 0
    return;
}

/**
 * 
 */
void setMotorDirection(int8_t direction)
{
    if(direction == 0) // Braking
    {
	palClearPad(GPIOB, 11);
	palClearPad(GPIOB, 12);
	return;
    }
    else if(direction > 0) // Direction forward
    {
	palSetPad(GPIOB, 11);
	palClearPad(GPIOB, 12);
	return;
    }
    else if(direction < 0) // Direction rearward
    {
	palClearPad(GPIOB, 11);
	palSetPad(GPIOB, 12);
	return;
    }
}

/**
 * 
 */
int16_t computeControl(uint16_t setpoint, uint16_t feedback, error_t *err)
{
    // Compute new error terms
    err->errorLast = err->errorP;
    err->errorP = ((int16_t) setpoint) - feedback;
    err->errorI += err->errorP;
    if(err->errorI > INTEGRAL_MAX)
	err->errorI = INTEGRAL_MAX;
    else if(err->errorI < -1*INTEGRAL_MAX)
	err->errorI = -1*INTEGRAL_MAX;
    err->errorD = err->errorP - err->errorLast;
    
    return (KP * err->errorP + KD*err->errorD + KI*err->errorI);// Compute control command
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
    palSetPadMode(GPIOA, 2, PAL_MODE_STM32_ALTERNATE_PUSHPULL); // VCP Tx
    palSetPadMode(GPIOA, 3, PAL_MODE_INPUT);			// VCP Rx
    
    // Motor Control
    palSetPadMode(GPIOB, 6, PAL_MODE_STM32_ALTERNATE_PUSHPULL); // PWM-EN	PB6
    palSetPadMode(GPIOA, 11, PAL_MODE_OUTPUT_PUSHPULL);		// Other EN	PA11
    palSetPadMode(GPIOB, MDIR_A, PAL_MODE_OUTPUT_PUSHPULL); // DIR A Channel	PB11
    palSetPadMode(GPIOB, MDIR_B, PAL_MODE_OUTPUT_PUSHPULL); // DIR B Channel	PB12
    palSetPad(GPIOA, 11); // Turn on secondary enable
    
    // Feedback ADC
    palSetPadMode(GPIOA, 0, PAL_MODE_INPUT_ANALOG); // Slider pot PA0
    
    /* Serial Port Startup */
    sdStart(&SD2, &ser_cfg);	// Activate VCP USART2 driver
    
    /* ADC Startup */
    adcStart(&ADCD1, NULL);      // Activate ADC driver
    //adcStartConversion(&ADCD1, &adcgrpcfg, &samples[0], ADC_BUF_DEPTH);
    
    /* PWM Setup */
    pwmStart(&PWMD4, &pwmcfg);
    pwmEnableChannel(&PWMD4, 0, PWM_PERCENTAGE_TO_WIDTH(&PWMD4, 4000));	// Default duty on EN channel
    setMotorDirection(1);
    
    uint16_t setpoint = 0;
    uint16_t feedbackValue = 0;
    
    
    int32_t command = 0; 
    uint16_t currentDuty = 0050;
    
    uint32_t loopCounter = 0; // Loop counter
    
    char out[64];
    out[0] = 'F';
    out[1] = ':';
    out[6] = '\n';
    
    uint8_t serialIn;
    uint16_t serialLen;
    
    error_t errors;
    
    while (TRUE) 
    {
	// Read serial input
	serialLen = sdAsynchronousRead(&SD2, &serialIn, 1);
	if(serialLen > 0)
	{
	    palTogglePad(GPIOA, GPIOA_LED_GREEN);
	    switch(serialIn)
	    {
		case 'U':
		    setpoint = 0;
		    break;
		case 'D':
		    setpoint = 300;
		    break;
		case 'H':
		    setpoint = 500;
		    break;
		case 'S':
		    setpoint = 100;
		    break;
	    }
	}
	// ADC Read of feedback pot
	adcConvert(&ADCD1, &adcgrpcfg, samples, ADC_BUF_DEPTH);
	
	// Compute control
	feedbackValue = samples[0];
	command = computeControl(setpoint, feedbackValue, &errors);
	if(command < 0)
	    setMotorDirection(-1);
	else
	    setMotorDirection(1);
	currentDuty = abs(command);
	if(currentDuty > 7000)
	{
	    currentDuty = 7000;
	}
	pwmEnableChannel(&PWMD4, 0, PWM_PERCENTAGE_TO_WIDTH(&PWMD4, currentDuty));//TODO: Set PWM duty for control
	
	chThdSleepMilliseconds(50);
	
	if((loopCounter % 10) == 0)
	{
	    //palTogglePad(GPIOA, GPIOA_LED_GREEN);
	    
	    // Format Publish data to the serial port
	    toHex16Str(feedbackValue, (out + 2));
	    sdWrite(&SD2, (uint8_t *) out, 7);
	}
	
	loopCounter++;
    }
  return 0;
}
