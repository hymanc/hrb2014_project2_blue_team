#ifndef FORCE_FEEDBACK_H
#define FORCE_FEEDBACK_H

#define F_CPU 16000000UL // CPU Frequency

#define TX_LENGTH	32
#define RX_LENGTH	64

// Servo PWM Defines
#define SERVO_PWM_PERIOD 	5000
#define SERVO_PWM_MAX 		525
#define SERVO_PWM_CENTER 	375
#define SERVO_PWM_MIN 		225

// Primitive FIFO (no deep copies or anything)
typedef struct
{
    void *data;
    uint16_t length;
    uint16_t head;
    uint16_t tail;
    uint8_t dsize;
}cfifo_t;

/**
 * @brief Checks if a FIFO is empty
 */
int8_t fifoEmpty(cfifo_t *fifo);

/**
 * @brief Checks if a FIFO is full
 */
int8_t fifoFull(cfifo_t *fifo);

/**
 * @brief Reads a value from a FIFO via absolute position, no validity checks
 */
int8_t fifoReadAbsolute(cfifo_t *fifo, uint16_t position, void *back);

/**
 * @brief Read an element from a FIFO relative to the head
 */
int8_t fifoRead(cfifo_t *fifo, uint16_t hposition, void *back);

/**
 * @brief FIFO dequeue
 */
int8_t fifoPopLeft(cfifo_t *fifo, void *back);

/**
 * @brief Pushes new data onto the circular FIFO
 */
int8_t fifoPushRight(cfifo_t *fifo, void *data);

/**
 * @brief Read Force Feedback ADC
 */
void readFeedback(uint16_t data);

/**
 * @brief
 */
char toHexCharacter(uint8_t nibble);

/**
 * 
 */
void toHex8(uint8_t value, char *back);

/**
 * 
 */
void toHex16(uint16_t value, char *back);

/**
 * 
 */
void sendFeedback(uint16_t data);

/**
 * @brief Sets the motor duty cycle
 * @param duty duty>0: forward torque, duty<0: backward torque, duty=0: Stopped
 */
void setMotorDuty(int16_t duty);

/**
 * @brief Set servo pulsewidth
 */
void setServoPulsewidth(int16_t pw);

/**
 * @brief Waits for a transmit complete and sends a byte
 */
void sendByteBlocking(uint8_t byte);

/**
 * 
 */
void sendByte(uint8_t byte);

/**
 * @brief Adds multiple bytes to the output buffer
 */
void sendBytes(uint8_t *bytes, uint8_t length);

/**
 * 
 */
void readByte(uint8_t byte);

/**
 * @brief Peripheral Initialization Routine
 */
void initialize(void);

#endif
