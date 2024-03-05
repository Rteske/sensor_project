/*
 * UTILITY.C
 *
 *  Created on: Dec 26, 2023
 *      Author: sunil
 */

#include <UTILITY.h>

extern TIM_HandleTypeDef htim2;

void Set_PWM_Duty_Cycle(uint8_t PWM_Duty_Cycle) {
	TIM2->CCR1 = PWM_Duty_Cycle;
	HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1);
}
