/**
 * @file avr_firmware.c
 * EECS 498 End Effector Force Control Firmware
 */

#include <stdlib.h>
#include <string.h>
#include <avr/io.h>
#include <avr/interrupt.h>
#include <util/delay.h>

#include "force_feedback.h"

#define F_CPU 16000000UL // CPU Frequency

#define TX_LENGTH	64
#define RX_LENGTH	64

// Servo PWM Defines
#define SERVO_PWM_PERIOD 	5000
#define SERVO_PWM_MAX 		525
#define SERVO_PWM_CENTER 	375
#define SERVO_PWM_MIN 		225

// Primitive FIFO (no deep copies or anything)

volatile cfifo_t *rxFifo;
volatile cfifo_t *txFifo;

/**
 * @brief Checks if a FIFO is empty
 */
int8_t fifoEmpty(cfifo_t *fifo)
{
    if(fifo->head == fifo->tail)
	return 1;
    return 0;
}

/**
 * @brief Checks if a FIFO is full
 */
int8_t fifoFull(cfifo_t *fifo)
{
    if( ( (fifo->tail + 1) % fifo->length ) == fifo->head )
	return 1;
    return 0;
}

/**
 * @brief Reads a value from a FIFO via absolute position, no validity checks
 */
int8_t fifoReadAbsolute(cfifo_t *fifo, uint16_t position, void *back)
{
    if(position < fifo->length)
    {
	back = fifo->data + position;
	return 0;
    }
    return -1;
}

/**
 * @brief Read an element from a FIFO relative to the head
 */
int8_t fifoRead(cfifo_t *fifo, uint16_t hposition, void *back)
{
    if(hposition < fifo->length)
    {
	uint16_t index = ( fifo->head + hposition ) % fifo->length;
	back = fifo->data + index;
	return 0;
    }
    return -1;
}

/**
 * @brief FIFO dequeue
 */
int8_t fifoPopLeft(cfifo_t *fifo, void *back)
{
    if(!fifoEmpty(fifo))
    {
	int8_t rval = fifoRead(fifo, 0, back);
	if(rval == 0)
	    fifo->head++;
	return rval;
    }
    return -1;
}

/**
 * @brief Pushes new data onto the circular FIFO
 */
int8_t fifoPushRight(cfifo_t *fifo, void *data)
{
    // Check if FIFO is full
    if(fifoFull(fifo))
	return -1;
    // Memcpy data into FIFO
    fifo->tail = (fifo->tail + 1) % fifo->length;
    memcpy(fifo->data + fifo->tail, data, fifo->dsize);
    return 0;
}

/**
 * @brief Read Force Feedback ADC
 */
void readFeedback(uint16_t data)
{

}

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
    }
    return 0;
}

/**
 * 
 */
void toHex8(uint8_t value, char *back)
{
    back[0] = toHexCharacter(value >> 4);
    back[1] = toHexCharacter(value & 0xF);
    back[2] = '\0';
}

/**
 * 
 */
void toHex16(uint16_t value, char *back)
{
    back[0] = toHexCharacter((uint8_t) value >> 12);
    back[1] = toHexCharacter((uint8_t) (value >> 8) & 0xF);
    back[2] = toHexCharacter((uint8_t) (value >> 4) & 0xF);
    back[3] = toHexCharacter((uint8_t) value & 0xF);
    back[4] = '\0';
}

/**
 * 
 */
void sendFeedback(uint16_t data)
{
    uint8_t low = (uint8_t) data;
    uint8_t high = (uint8_t) (data >> 8);
    // Convert to hex string
    
    sendByteBlocking(high);
    sendByteBlocking(low);
}
/**
 * @brief Sets the motor duty cycle
 * @param duty duty>0: forward torque, duty<0: backward torque, duty=0: Stopped
 */
void setMotorDuty(int16_t duty)
{
    if(duty < 0)
    {
	// Set PWM duty cycle and direction to reverse
    } 
    else
    {
	// Set PWM duty cycle and direction to forward
    }
}

/**
 * @brief Set servo pulsewidth
 */
void setServoPulsewidth(int16_t pw)
{
    pw = pw/4; // Convert pulsewidth to regvalue
    if(pw < SERVO_PWM_MIN)
	pw = SERVO_PWM_MIN;
    else if(pw > SERVO_PWM_MAX)
	pw = SERVO_PWM_MAX;
    OC1A = pw;
}

/**
 * @brief Waits for a transmit complete and sends a byte
 */
void sendByteBlocking(uint8_t byte)
{
    while(!(UCSR0A & (1<<TXC0)))
    {
	__asm__("NOP");
    }
    UDR0 = byte;
}

/**
 * 
 */
void sendByte(uint8_t byte)
{
    // If buffer empty, send 
    if(fifoEmpty(txFifo) && (UCSR0A & (1<<TXC0)))
    {
	UDR0 = byte;
    }
    else // Add to buffer
    {
	fifoPushRight(txFifo, &byte);
    }
}

/**
 * @brief Adds multiple bytes to the output buffer
 */
void sendBytes(uint8_t *bytes, uint8_t length)
{
    uint8_t i;
    for(i = 0; i < length; i++)
    {
	sendByte(bytes[i]);
    }
}

/**
 * 
 */
void readByte(uint8_t byte)
{
    // Put byte onto Rx Buffer
    fifoPushRight(rxFifo, &byte);
    // TODO: Parse command
}

/**
 * @brief Peripheral Initialization Routine
 */
void initialize(void)
{
    cli();
    // Initialize ADC
    ADMUX = (1<<REFS0); // External AVcc ref
    ADCSRA = (1<<ADEN) | (1<<ADPS2) | (1<<ADPS1); // DIV32
    
    // Initialize Serial (38400)
    UBRR0L = 25; // 38.4kbps @ F_CPU = 16MHz
    UCSR0A = 0;
    UCSR0C = (1<<UCSZ00) | (1<<UCSZ01); // Size: 8-bit
    UCSR0B = (1<<RXCIE0) | (1<<TXCIE0) | (1<<RXEN0) | (1<<TXEN0);
    
    // Initialize Motor PWM TODO
    
    // Initialize Servo PWM (OC1A)
    TCCR1A = (1<<COM1A0) | (1<<WGM11);
    TCCR1B = (1<<WGM13) | (1<<WGM12) | (1<<CS11) | (1<<CS10); //DIV64
    
    sei(); // Enable global interrupts
}

/**
 * @brief ADC Conversion Complete Interrupt Handler
 */
ISR(ADC_vect)
{
    uint16_t data = ( ADCH << 8 ) | ADCL;
    readFeedback(data);
}

/**
 * @brief USART0 Tx Interrupt Handler
 */
ISR(USART0_TX_vect)
{
    // TODO: Send next byte 
    if(!fifoEmpty(txFifo))
    {
	uint8_t data;
	fifoPopLeft(txFifo, &data);
	UDR0 = data;
    }
}

/**
 * @brief USART0 Rx Interrupt Handler
 */
ISR(USART0_RX_vect)
{
    uint8_t byte = UDR0;
    readByte(byte);
}

/**
 * @brief Application entry point
 */
void main(void)
{
    initialize();
    cfifo_t tx;
    cfifo_t rx;
    uint8_t txBuf[32];
    uint8_t rxBuf[32];
    tx.data = txBuf;
    rx.data = rxBuf;
    tx.head = 0;
    rx.head = 0;
    tx.tail = 0;
    rx.tail = 0;
    tx.dsize = 1;
    rx.dsize = 1;
    tx.length = TX_LENGTH;
    rx.length = RX_LENGTH;
    txFifo = &tx;
    rxFifo = &rx;
    
    while(1)
    {
	// Check for new serial commands
	// Read ADC
	// Set Feedback appropriately
	// Send feedback over serial
    }
}