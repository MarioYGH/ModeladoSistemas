/*
Autor: Mario García
Programa ESP32 para adquisición de datos de la carga de un capacitor en circuito RC
date created: 05/06/24
last modified: 06/10/24
*/

#include <stdio.h>
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_adc/adc_oneshot.h" // Para hacer lecturas Oneshot o continuas
#include "esp_log.h"
#include "driver/uart.h" // Librería UART
#include "string.h"
#include "esp_timer.h"  // Incluir para esp_timer_get_time()


// UART
#define UART_PORT_NUM UART_NUM_1
#define TX_BUF_SIZE 1024
#define TXD_PIN GPIO_NUM_1
#define RXD_PIN GPIO_NUM_3

// ADC
#define ADC1_CHAN0 ADC_CHANNEL_4 // Pin 32
#define ADC_ATTEN ADC_ATTEN_DB_11

// Control del transistor
#define TRANSISTOR_PIN 5  // Pin conectado al transistor
#define EXPERIMENTS 51 // Número de experimentos
#define CHARGE_TIME 16000  // Tiempo de carga en milisegundos (15 segundos)
#define DELAY_BETWEEN_EXPERIMENTS 1000  // Pausa entre experimentos (1 segundo)
#define DISCHARGE_PIN 13  // Pin para el segundo transistor de descarga

static void control_discharge(bool state) {
    gpio_set_level(DISCHARGE_PIN, state ? 1 : 0);  // Activa (1) o desactiva (0) el pin
    printf("Descarga: %s\n", state ? "Activada" : "Desactivada");  // Debug
}

adc_oneshot_unit_handle_t adc1_handle;
static int adc_raw;
static float voltage;

esp_err_t config_ADC();
esp_err_t get_ADC_value();
esp_err_t uart_initialize();
static void tx_task(void *arg);
static void control_transistor(bool state);

void app_main() {
    config_ADC(); 
    uart_initialize();
    
    // Configura el pin del transistor
    gpio_set_direction(TRANSISTOR_PIN, GPIO_MODE_OUTPUT);
    gpio_set_level(TRANSISTOR_PIN, 0);  // Inicialmente apagado

    // Crear tarea para la transmisión de datos
    xTaskCreate(tx_task, "uart_tx_task", TX_BUF_SIZE * 2, NULL, configMAX_PRIORITIES - 1, NULL);
}

static void tx_task(void *arg) {
    char str[80];
    unsigned long elapsedTime = 0;

    for (int i = 0; i < EXPERIMENTS; i++) {
        // Inicia la carga del capacitor encendiendo el transistor 
        control_discharge(false);  // Asegúrate de que el transistor de descarga esté apagado
        control_transistor(true);

        unsigned long startTime = esp_timer_get_time() / 1000;  // Tiempo de inicio en ms

        while ((esp_timer_get_time() / 1000) - startTime < CHARGE_TIME) {  
            get_ADC_value();
            elapsedTime = (esp_timer_get_time() / 1000) - startTime;
            sprintf(str, "/* %d,%lu, %2.2f*/", i, elapsedTime, voltage);
            uart_write_bytes(UART_PORT_NUM, str, strlen(str) + 1);
            vTaskDelay(pdMS_TO_TICKS(200));  // Muestreo cada 100 ms
        }

        // Apaga el transistor de carga
        control_transistor(false);

        // Activa la descarga del capacitor
        control_discharge(true);
        vTaskDelay(pdMS_TO_TICKS(4000));  // Aumenta el tiempo de descarga (2 segundos)

        // Apaga el transistor de descarga
        control_discharge(false);

        // Pausa entre experimentos
        vTaskDelay(pdMS_TO_TICKS(DELAY_BETWEEN_EXPERIMENTS));
    }
}

// Función para controlar el transistor
static void control_transistor(bool state) {
    gpio_set_level(TRANSISTOR_PIN, state ? 1 : 0);
}

esp_err_t config_ADC() {
    // Configuración del ADC
    adc_oneshot_unit_init_cfg_t init_config1 = {
        .unit_id = ADC_UNIT_1,
    };

    adc_oneshot_new_unit(&init_config1, &adc1_handle);

    // Configuración del canal ADC
    adc_oneshot_chan_cfg_t config = {
        .bitwidth = ADC_BITWIDTH_DEFAULT,
        .atten = ADC_ATTEN,
    };

    adc_oneshot_config_channel(adc1_handle, ADC1_CHAN0, &config);

    return ESP_OK;
}

esp_err_t get_ADC_value() {
    // Leer el valor del ADC
    adc_oneshot_read(adc1_handle, ADC1_CHAN0, &adc_raw);
    voltage = (adc_raw * 5 / 4095.0);  // Conversión a voltaje (ajustado para 0-5V)

    return ESP_OK;
}

esp_err_t uart_initialize() {
    const uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE
    };

    // Instalar el controlador UART
    ESP_ERROR_CHECK(uart_driver_install(UART_PORT_NUM, TX_BUF_SIZE * 2, 0, 0, NULL, 0));
    ESP_ERROR_CHECK(uart_param_config(UART_PORT_NUM, &uart_config));
    ESP_ERROR_CHECK(uart_set_pin(UART_PORT_NUM, TXD_PIN, RXD_PIN, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));

    return ESP_OK;
}
