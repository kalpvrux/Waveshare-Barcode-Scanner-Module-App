from UI import Ui_Barcode_Scanner_Module
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import Qt, QTimer
import serial
import serial.tools.list_ports

# Constants
US_h = 0x00
Czech_h = 0x01
France_h = 0x02
Germany_h = 0x03
Hungary_h = 0x04
Italy_h = 0x05
Japan_h = 0x06
Spain_h = 0x07
Turkey_F_h = 0x08
Turkey_Q_h = 0x09

LED_Indicator_En = 0x80
LED_Indicator_Dis = 0x00
Buz_Indicator_En = 0x40
Buz_Indicator_Dis = 0x00
Target_light_Dis = 0x00
Target_light_Com = 0x10
Target_light_Keep = 0x20
Light_Dis = 0x00
Light_Com = 0x04
Light_Keep = 0x08
Manual_Mode = 0x00
Command_Mode = 0x01
Continous_Mode = 0x02
Sensor_Mode = 0x03

UART_Output_Hex = 0x00
USB_Output_Hex = 0x01
USB_Virtual_Port_Hex = 0x03

On = 0x80
Off = 0x00

class MainWindow(QMainWindow, Ui_Barcode_Scanner_Module):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Barcode Scanner Module")

        items = ['1200', '4800', '9600', '14400' , '19200' , '38400' , '57600' , '115200' ]
        
        self.br_comboBox.addItems(items)
        self.br_comboBox.setCurrentText('9600')
        
        self.comport_comboBox.setPlaceholderText("Select COM_Port")
        self.refresh_ports()

        self.Barcode_Settings.clicked.connect(self.switch_to_Barcode_Settings_page)
        self.EAN8.clicked.connect(self.handle_EAN8)
        self.EAN13.clicked.connect(self.handle_EAN13)
        self.UPCA.clicked.connect(self.handle_UPCA)
        self.UPCE0.clicked.connect(self.handle_UPCE0)
        self.UPCE1.clicked.connect(self.handle_UPCE1)
        self.Code39.clicked.connect(self.handle_Code39)
        self.Code93.clicked.connect(self.handle_Code93)
        self.Code128.clicked.connect(self.handle_Code128)
        self.CodeBar.clicked.connect(self.handle_CodeBar)
        self.QR_Code.clicked.connect(self.handle_QR_code)
        self.Interleaved_2_of_5.clicked.connect(self.handle_Interleaved_2of5)
        self.Industrial_25.clicked.connect(self.handle_Industrial_25)
        self.Matrix_2_of_5.clicked.connect(self.handle_Matrix_2_of_5)
        self.Code11.clicked.connect(self.handle_Code11)
        self.MSI.clicked.connect(self.handle_MSI)
        self.RSS_14.clicked.connect(self.handle_RSS_14)
        self.Limited_RSS.clicked.connect(self.handle_Limited_RSS)
        self.Expanded_RSS.clicked.connect(self.handle_Expanded_RSS)
        self.DM.clicked.connect(self.handle_DM)
        self.PDF417.clicked.connect(self.handle_PDF417)
        self.Enable_ALL_barcode.clicked.connect(self.enable_all_barcodes)
        self.Disable_All_barcode.clicked.connect(self.disable_all_barcodes)
        
        self.KeyBoard_Set.clicked.connect(self.switch_to_keyboard_set_page)
        self.Keyboard_lang_set.clicked.connect(self.KeyBoard_settings)

        self.Enhanced_Settings.clicked.connect(self.switch_to_enhanced_settings_page)
        self.Br_delay_endis.clicked.connect(self.Br_En_Dis_setting)
        self.barcode_delay_dial.valueChanged.connect(self.update_barcode_delay)
        self.barcode_delay_dial.sliderReleased.connect(self.barcode_delay_dial_released)
        self.PreSuf_data_set.clicked.connect(self.Prefix_And_Suffix_Data_Setting)
        self.Send_all_data.clicked.connect(self.update_spinbox_state)
        self.first_M_data.clicked.connect(self.update_spinbox_state)
        self.last_n_data.clicked.connect(self.update_spinbox_state)
        self.no_MN_data.clicked.connect(self.update_spinbox_state)
        self.MN_data_set.clicked.connect(self.on_MN_data_set_clicked)
        
        self.Time_Settings.clicked.connect(self.switch_to_time_set_page)
        self.Scan_Interval_set.clicked.connect(self.handle_scan_interval_set)
        self.Scan_Interval_dial.valueChanged.connect(self.Scan_Interval_delay)
        self.Time_of_single_scan_set.clicked.connect(self.handle_Time_of_single_scan_set)
        self.Time_of_single_scan_dial.valueChanged.connect(self.Time_of_single_scan_delay)
        self.AuSleep_endis.clicked.connect(self.AuSleep_En_Dis_setting)
        self.Auto_Sleep_Function_dial.valueChanged.connect(self.handle_auto_sleep_function_value_change)
        self.Auto_Sleep_Function_set.clicked.connect(self.handle_Auto_Sleep_Function_slider_released)

        self.Board_Settings.clicked.connect(self.switch_to_Board_Settings_set_page)
        self.Board_Settings_set_all.clicked.connect(self.Board_settings_function)

        self.Set_Interface.clicked.connect(self.switch_USB_mode_set_page)
        self.USB_Virtual_Port.clicked.connect(self.USB_Interface_function)
        self.UART_Output.clicked.connect(self.USB_Interface_function)
        self.USB_Output.clicked.connect(self.USB_Interface_function)

        self.Buzzer_Settings.clicked.connect(self.switch_to_buzzer_settings_set_page)
        self.Buzzer_Settings_set_all.clicked.connect(self.buzzer_settings_function)
        self.BTD.valueChanged.connect(self.handle_BTD_value_change)
        self.BT.valueChanged.connect(self.handle_BT_value_change)

        self.BaudRate.clicked.connect(self.switch_to_baudrate_set_page)
        self.br_1200.clicked.connect(self.handle_br_1200_click)
        self.br_4800.clicked.connect(self.handle_br_4800_click)
        self.br_9600.clicked.connect(self.handle_br_9600_click)
        self.br_14400.clicked.connect(self.handle_br_14400_click)
        self.br_19200.clicked.connect(self.handle_br_19200_click)
        self.br_38400.clicked.connect(self.handle_br_38400_click)
        self.br_57600.clicked.connect(self.handle_br_57600_click)
        self.br_115200.clicked.connect(self.handle_br_115200_click)

        self.Save_Restore.clicked.connect(self.switch_to_save_restore_set_page)
        self.RESTORE_FACTORY_SETTING.clicked.connect(self.SET_RESTORE_FACTORY_SETTING)
        self.RESTORE_USER_SETTING.clicked.connect(self.SET_RESTORE_USER_SETTING)
        self.SAVE_TO_FLASH.clicked.connect(self.SET_SAVE_TO_FLASH)
        self.SAVE_USER_SETTING.clicked.connect(self.SET_SAVE_USER_SET)
        self.Light_Sleep.clicked.connect(self.SET_LIGHT_SLEEP)
        self.Deep_sleep.clicked.connect(self.SET_DEEP_SLEEP)
        self.wake_up.clicked.connect(self.SET_WAKE_UP)


        self.Serial_Terminal.clicked.connect(self.switch_to_serial_terminal_set_page)
        self.Connect_comport.clicked.connect(self.start_serial_monitor)
        self.Disconnect_comport.clicked.connect(self.disconnect_comport)
        self.Clear_Serial_monitor.clicked.connect(self.clear_serial_monitor_text)

        self.serial_connection = None

    def SET_RESTORE_FACTORY_SETTING(self):
        Restore_Factory_Setting = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0xD9, 0x50, 0xAB, 0xCD])
        self.send_command(Restore_Factory_Setting)

    def SET_RESTORE_USER_SETTING(self):
        Restore_user_Setting = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0xD9, 0x55, 0xAB, 0xCD])
        self.send_command(Restore_user_Setting)
    
    def SET_SAVE_TO_FLASH(self):
        SAVE_TO_FLASH = bytes([0x7E, 0x00, 0x09, 0x01, 0x00, 0x00, 0x00, 0xDE, 0xC8])
        self.send_command(SAVE_TO_FLASH)

    def SET_SAVE_USER_SET(self):
        Save_user_Setting = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0xD9, 0x56, 0xAB, 0xCD])
        self.send_command(Save_user_Setting)

    def SET_LIGHT_SLEEP(self):
        light_sleep = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0xD9, 0xA0, 0xAB, 0xCD])
        self.send_command(light_sleep)

    def SET_DEEP_SLEEP(self):
        Deep_sleep = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0xD9, 0xA5, 0xAB, 0xCD])
        self.send_command(Deep_sleep)

    def SET_WAKE_UP(self):
        wake_up = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0xD9, 0x00, 0xAB, 0xCD])
        self.send_command(wake_up)

    def handle_BT_value_change(self):
        dial_value = self.BT.value()
        frequency = dial_value * 20
        self.BT_counter_lbl.setText(f"{frequency} Hz")


    def handle_BTD_value_change(self):
        dial_value = self.BTD.value()
        self.Buzz_time_counter_lbl.setText(f"{dial_value} ms")

    def buzzer_settings_function(self):
        if self.BM_en.isChecked():
            Hex_Code_1 = 0x00
        elif self.BM_dis.isChecked():
            Hex_Code_1 = 0x02

        if self.BIS_en.isChecked():
            Hex_Code_2 = 0x00
        elif self.BIS_dis.isChecked():
            Hex_Code_2 = 0x01

        dial_value_1 = self.BTD.value()
        hex_value_1 = int(f"{dial_value_1:02X}", 16)  # Convert value to 2-digit hexadecimal

        dial_value_2 = self.BT.value()
        hex_value_2 = int(f"{dial_value_2:02X}", 16)  # Convert value to 2-digit hexadecimal

        Duration_of_warning_tone = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0B, hex_value_1 , 0xAB, 0xCD])
        warning_tone = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0A, hex_value_2, 0xAB, 0xCD])
        Buzzer_ON_OFF = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0C, 0x00 + Hex_Code_2, 0xAB, 0xCD])
        buzzer_settings = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0E, Hex_Code_1 + 0x04, 0xAB, 0xCD])

        self.send_command(Duration_of_warning_tone)
        self.send_command(warning_tone)
        self.send_command(Buzzer_ON_OFF)
        self.send_command(buzzer_settings)

    def handle_Auto_Sleep_Function_slider_released(self):
        """Handle the slider release, convert value, and send data to serial."""
        dial_value = self.Auto_Sleep_Function_dial.value()  # Get the dial value
        hex_value = format(dial_value, '04X')  # Convert the value to a 4-digit hex string

        # Split the hex value into two parts
        first_two_digits = int(hex_value[:2], 16)  # First 2 digits for Auto_Sleep_Function
        last_two_digits = int(hex_value[2:], 16)  # Last 2 digits for Auto_Sleep_Function_2

        # Construct Auto_Sleep_Function byte sequence
        Auto_Sleep_Function = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x07, On + first_two_digits, 0xAB, 0xCD])
        Auto_Sleep_Function_2 = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x08, last_two_digits, 0xAB, 0xCD])

        # Send the data to the serial port
        self.send_command(Auto_Sleep_Function)
        self.send_command(Auto_Sleep_Function_2)

        # Print sent values for debugging
        print(f"Auto_Sleep_Function: {Auto_Sleep_Function.hex()}")
        print(f"Auto_Sleep_Function_2: {Auto_Sleep_Function_2.hex()}")

    def handle_auto_sleep_function_value_change(self):
        """Handle the dial value change, divide by 10, and update the label."""
        dial_value = self.Auto_Sleep_Function_dial.value()  # Get the dial value
        divided_value = dial_value / 10  # Divide by 10

        if divided_value <= 60.0:
            # If value is between 0 and 60, print as seconds
            self.Auto_Sleep_Function_counter_lbl.setText(f"{divided_value:.1f} Sec")
        else:
            # Convert value to minutes and seconds
            minutes = int(divided_value // 60)
            seconds = divided_value % 60
            self.Auto_Sleep_Function_counter_lbl.setText(f"{minutes}M {seconds:.1f}S")

    def handle_Time_of_single_scan_set(self):
        dial_value = self.Time_of_single_scan_dial.value()  
        time_in_seconds = dial_value / 10.0  
        time_in_seconds = max(0, min(25.5, time_in_seconds)) 
        hex_value = round(time_in_seconds * 10)  
        Time_of_single_scan_Setting = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x06, hex_value , 0xAB, 0xCD])
        self.send_command(Time_of_single_scan_Setting)

    def handle_scan_interval_set(self):
        dial_value = self.Scan_Interval_dial.value()  
        time_in_seconds = dial_value / 10.0  
        time_in_seconds = max(0, min(25.5, time_in_seconds)) 
        hex_value = round(time_in_seconds * 10)  
        Scan_Interval_Setting = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x05, hex_value, 0xAB, 0xCD])
        self.send_command(Scan_Interval_Setting)

    def Prefix_And_Suffix_Data_Setting(self):
        Enhanced_Functionality_Integration = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x60, 0x02 + 0x08, 0xAB, 0xCD])
        self.send_command(Enhanced_Functionality_Integration)
        text1 = self.prefix_data_lineEdit.text()
        text2 = self.suffix_data_lineEdit.text()

        # Calculate lengths
        Prefix_Length = len(text1)
        Suffix_Length = len(text2)

        # Convert lengths to the required hex format
        Prefix_Length_Hex = (Prefix_Length * 0x10)  # This will be a number like 0x00, 0x10, 0x20, etc.
        Suffix_Length_Hex = Suffix_Length  # This will be a number like 0x00, 0x01, ..., 0x0F

        # Send the length data combined as a single byte
        Prefix_And_Suffix_length = bytes([
            0x7E, 0x00, 0x08, 0x01, 0x00, 0x62, 
            Prefix_Length_Hex + Suffix_Length_Hex,  # Combine the lengths into a single byte
            0xAB, 0xCD
        ])
        self.send_command(Prefix_And_Suffix_length)

        # Now send each prefix character one by one
        for index, char in enumerate(text1):
            ascii_value = ord(char)  # Convert to ASCII hex value
            address = 0x63 + index  # Dynamically adjust the address

            # Create the prefix data command
            Prefix_data = bytes([
                0x7E, 0x00, 0x08, 0x01, 0x00, address,  # Address is dynamic
                ascii_value,  # The ASCII hex value of the current character
                0xAB, 0xCD
            ])
            self.send_command(Prefix_data)


        for index, char in enumerate(text2):
            ascii_value = ord(char) 
            address = 0x72 + index 

            Suffix_data = bytes([
                0x7E, 0x00, 0x08, 0x01, 0x00, address,  # Address is dynamic
                ascii_value,  # The ASCII hex value of the current character
                0xAB, 0xCD
            ])
            self.send_command(Suffix_data) 
    
    def update_spinbox_state(self):
        # Disable/enable spin boxes based on the selected button
        if self.Send_all_data.isChecked():
            self.M_data_spinBox.setDisabled(True)
            self.N_data_spinBox.setDisabled(True)
            self.M_data_spinBox.setValue(0)
            self.N_data_spinBox.setValue(0)
        elif self.first_M_data.isChecked():
            self.M_data_spinBox.setEnabled(True)
            self.N_data_spinBox.setDisabled(True)
        elif self.last_n_data.isChecked():
            self.M_data_spinBox.setDisabled(True)
            self.N_data_spinBox.setEnabled(True)
        elif self.no_MN_data.isChecked():
            self.M_data_spinBox.setEnabled(True)
            self.N_data_spinBox.setEnabled(True)
    
    def on_MN_data_set_clicked(self):
        if self.Send_all_data.isChecked():
            data_mode = 0x00  # Send all data
        elif self.first_M_data.isChecked():
            data_mode = 0x01  # Send first M data
        elif self.last_n_data.isChecked():
            data_mode = 0x02  # Send last N data
        elif self.no_MN_data.isChecked():
            data_mode = 0x03  # Don’t send first M + last N data
        else:
            data_mode = 0x00

        M_value = self.M_data_spinBox.value()
        N_value = self.N_data_spinBox.value()

        # Create byte commands, ensuring M_value and N_value are within byte range (0-255)
        Length_of_interception_M = bytes([
            0x7E, 0x00, 0x08, 0x01, 0x00, 0xB1, M_value & 0xFF, 0xAB, 0xCD
        ])

        Length_of_interception_N = bytes([
            0x7E, 0x00, 0x08, 0x01, 0x00, 0xB2, N_value & 0xFF, 0xAB, 0xCD
        ])

        data_mode_command = bytes([
            0x7E, 0x00, 0x08, 0x01, 0x00, 0xB0, data_mode, 0xAB, 0xCD
        ])

        self.send_command(data_mode_command)
        self.send_command(Length_of_interception_M)
        self.send_command(Length_of_interception_N)
            
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()  # Exit the application
    
    def switch_to_Barcode_Settings_page(self):
        self.stackedWidget.setCurrentIndex(0)
        
    def handle_EAN8(self):
        if self.EAN8.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x2F, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x2F, 0x00, 0xAB, 0xCD])

        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)

        self.send_command(command)

    def handle_EAN13(self):
        if self.EAN13.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x2E, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x2E, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_UPCA(self):
        if self.UPCA.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x30, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x30, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_UPCE0(self):
        if self.UPCE0.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x31, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x31, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_UPCE1(self):
        if self.UPCE1.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x32, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x32, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Code128(self):
        if self.Code128.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x33, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x33, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Code39(self):
        if self.Code39.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x36, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x36, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Code93(self):
        if self.Code93.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x39, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x39, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_CodeBar(self):
        if self.CodeBar.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x5E, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x5E, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_QR_code(self):
        if self.QR_Code.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x3F, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x3F, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Interleaved_2of5(self):
        if self.Interleaved_2_of_5.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x40, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x40, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Industrial_25(self):
        if self.Industrial_25.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x43, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x43, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Matrix_2_of_5(self):
        if self.Matrix_2_of_5.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x46, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x46, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Code11(self):
        if self.Code11.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x49, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x49, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_MSI(self):
        if self.MSI.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x4C, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x4C, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_RSS_14(self):
        if self.RSS_14.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x4F, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x4F, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Limited_RSS(self):
        if self.Limited_RSS.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x52, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x52, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_Expanded_RSS(self):
        if self.Expanded_RSS.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x55, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x55, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_DM(self):
        if self.DM.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x58, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x58, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)

    def handle_PDF417(self):
        if self.PDF417.isChecked():
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x5B, 0x01, 0xAB, 0xCD])
        else:
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x5B, 0x00, 0xAB, 0xCD])
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        self.send_command(command)
    
    def enable_all_barcodes(self):
        barcodes = [
            self.EAN8, self.EAN13, self.UPCA, self.UPCE0, self.UPCE1, self.Code39,
            self.Code93, self.Code128, self.CodeBar, self.QR_Code, self.Interleaved_2_of_5,
            self.Industrial_25, self.Matrix_2_of_5, self.Code11, self.MSI, self.RSS_14,
            self.Limited_RSS, self.Expanded_RSS, self.DM, self.PDF417
        ]
        
        for barcode in barcodes:
            barcode.setChecked(True)

        if self.Disable_All_barcode.isChecked():
            self.Disable_All_barcode.setChecked(False)
        
        command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x2C, 0x02 + 0x00, 0xAB, 0xCD])
        self.send_command(command)

    def disable_all_barcodes(self):
        barcodes = [
            self.EAN8, self.EAN13, self.UPCA, self.UPCE0, self.UPCE1, self.Code39,
            self.Code93, self.Code128, self.CodeBar, self.QR_Code, self.Interleaved_2_of_5,
            self.Industrial_25, self.Matrix_2_of_5, self.Code11, self.MSI, self.RSS_14,
            self.Limited_RSS, self.Expanded_RSS, self.DM, self.PDF417
        ]
        
        for barcode in barcodes:
            barcode.setChecked(False)
        
        if self.Enable_ALL_barcode.isChecked():
            self.Enable_ALL_barcode.setChecked(False)

        command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x2C, 0x00 + 0x00, 0xAB, 0xCD])
        self.send_command(command)

    def switch_to_keyboard_set_page(self):
        self.stackedWidget.setCurrentIndex(1)
        
    def KeyBoard_settings(self):
        KeyBoard = US_h
        if self.US.isChecked():
            KeyBoard = US_h
        elif self.Czech.isChecked():
            KeyBoard = Czech_h
        elif self.France.isChecked():
            KeyBoard = France_h
        elif self.Germany.isChecked():
            KeyBoard = Germany_h
        elif self.Hungary.isChecked():
            KeyBoard = Hungary_h
        elif self.Italy.isChecked():
            KeyBoard = Italy_h
        elif self.Japan.isChecked():
            KeyBoard = Japan_h
        elif self.Spain.isChecked():
            KeyBoard = Spain_h
        elif self.Turkey_F.isChecked():
            KeyBoard = Turkey_F_h
        elif self.Turkey_Q.isChecked():
            KeyBoard = Turkey_Q_h
        
        Keyboard_Setting = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x61, KeyBoard, 0xAB, 0xCD])
        self.send_command(Keyboard_Setting)

    def switch_to_enhanced_settings_page(self):
        self.stackedWidget.setCurrentIndex(2)

    def Br_En_Dis_setting(self):
        if self.Br_delay_endis.isChecked():
            self.Br_delay_endis.setText("Enable")
            self.barcode_delay_dial.setEnabled(True)
        else:
            self.Br_delay_endis.setText("Disable")
            self.barcode_delay_dial.setEnabled(False)
            command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x13, 0x00, 0xAB, 0xCD])
            self.send_command(command)

    def AuSleep_En_Dis_setting(self):
        if self.AuSleep_endis.isChecked():
            self.AuSleep_endis.setText("Enable")
            self.Auto_Sleep_Function_dial.setEnabled(True)
        else:
            self.AuSleep_endis.setText("Disable")
            self.Auto_Sleep_Function_dial.setEnabled(False)

    def update_barcode_delay(self, value):
        if value == 0:
            self.Barcode_delay_counter_lbl.setText("infinite")
        else:
            delay_in_seconds = (value / 255) * 12.7
            formatted_delay = f"{delay_in_seconds:.1f}s"
            self.Barcode_delay_counter_lbl.setText(formatted_delay)

    def Scan_Interval_delay(self, value):
        delay_in_seconds = (value / 255) * 25.5
        formatted_delay = f"{delay_in_seconds:.1f}s"
        self.Scan_Interval_counter_lbl.setText(formatted_delay)
        
    def Time_of_single_scan_delay(self, value):
        delay_in_seconds = (value / 255) * 25.5
        formatted_delay = f"{delay_in_seconds:.1f}s"
        self.Time_of_single_scan_counter_lbl.setText(formatted_delay)
    
    def barcode_delay_dial_released(self):
        dial_value = self.barcode_delay_dial.value()
        delay_in_seconds = (dial_value / 255) * 12.7
        hex_value = max(0x00, min(0x7F, round((delay_in_seconds / 12.7) * 0x7F)))
        delay_enable_bit = 0x80  # Bit 7 is 1 (enable delay)

        command = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x13, delay_enable_bit + hex_value, 0xAB, 0xCD])
        self.send_command(command)

    def switch_to_time_set_page(self):
        self.stackedWidget.setCurrentIndex(3)

    def switch_to_Board_Settings_set_page(self):
        self.stackedWidget.setCurrentIndex(4)
    
    def Board_settings_function(self):
        mode = Command_Mode  # Default to Command_Mode
        if self.manual_mode_button.isChecked():
            mode = Manual_Mode
        elif self.continous_mode_button.isChecked():
            mode = Continous_Mode
        elif self.sensor_mode_button.isChecked():
            mode = Sensor_Mode

        # White Light settings
        White_light_setting = Light_Dis  # Default to Light_Dis
        if self.WL_on.isChecked():
            White_light_setting = Light_Keep
        elif self.WL_com.isChecked():
            White_light_setting = Light_Com
        elif self.WL_off.isChecked():
            White_light_setting = Light_Dis

        # Onboard Light (LED Indicator) settings
        led_setting = LED_Indicator_Dis  # Default to LED_Indicator_Dis
        if self.OBL_on.isChecked():
            led_setting = LED_Indicator_En
        elif self.OBL_off.isChecked():
            led_setting = LED_Indicator_Dis

        # Buzzer settings
        buzzer_setting = Buz_Indicator_Dis  # Default to Buz_Indicator_Dis
        if self.BI_en.isChecked():
            buzzer_setting = Buz_Indicator_En
        elif self.BI_dis.isChecked():
            buzzer_setting = Buz_Indicator_Dis

        # Target Light settings
        target_light_setting = Target_light_Dis  # Default to Target_light_Dis
        if self.TL_on.isChecked():
            target_light_setting = Target_light_Keep
        elif self.TL_com.isChecked():
            target_light_setting = Target_light_Com
        elif self.TL_off.isChecked():
            target_light_setting = Target_light_Dis

        # Construct the hex command based on the selected settings
        common_setting = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x00,
            led_setting + buzzer_setting + target_light_setting + White_light_setting + mode,
            0xAB, 0xCD
        ])

        self.send_command(common_setting)

    def switch_USB_mode_set_page(self):
        self.stackedWidget.setCurrentIndex(5)
    
    def USB_Interface_function(self):
        interface = USB_Virtual_Port_Hex
        if self.USB_Virtual_Port.isChecked():
            interface = USB_Virtual_Port_Hex
        elif self.UART_Output.isChecked():
            interface = UART_Output_Hex
        elif self.USB_Output.isChecked():
            interface = USB_Output_Hex

        Module_interface = bytes([0x7E, 0x00, 0x08, 0x01, 0x00, 0x0D, interface, 0xAB, 0xCD])
        self.send_command(Module_interface)

    def switch_to_buzzer_settings_set_page(self):
        self.stackedWidget.setCurrentIndex(6)

    def switch_to_baudrate_set_page(self):
        self.stackedWidget.setCurrentIndex(7)

    def handle_br_1200_click(self):
        BR_1200 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0xC4, 0x09, 0xAB, 0xCD])
        self.send_command(BR_1200)

    def handle_br_4800_click(self):
        BR_4800 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0x71, 0x02, 0xAB, 0xCD])
        self.send_command(BR_4800)

    def handle_br_9600_click(self):
        BR_9600 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0x39, 0x01, 0xAB, 0xCD])
        self.send_command(BR_9600)

    def handle_br_14400_click(self):
        BR_14400 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0xD0, 0x00, 0xAB, 0xCD])
        self.send_command(BR_14400)

    def handle_br_19200_click(self):
        BR_19200 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0x9C, 0x00, 0xAB, 0xCD])
        self.send_command(BR_19200)

    def handle_br_38400_click(self):
        BR_38400 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0x4E, 0x00, 0xAB, 0xCD])
        self.send_command(BR_38400)

    def handle_br_57600_click(self):
        BR_57600 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0x34, 0x00, 0xAB, 0xCD])
        self.send_command(BR_57600)

    def handle_br_115200_click(self):
        BR_115200 = bytes([0x7E, 0x00, 0x08, 0x02, 0x00, 0x2A, 0x1A, 0x00, 0xAB, 0xCD])
        self.send_command(BR_115200)

    def switch_to_save_restore_set_page(self):
        self.stackedWidget.setCurrentIndex(8)


    def switch_to_serial_terminal_set_page(self):
        self.stackedWidget.setCurrentIndex(9)

    def start_serial_monitor(self):
        com_port = self.comport_comboBox.currentText()
        baud_rate = self.br_comboBox.currentText()
        
        if not com_port or "No COM" in com_port:
            # Show error popup if no COM port is selected
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Critical)
            error_msg.setWindowTitle("Error")
            error_msg.setText("Please select a COM port and try again.")
            error_msg.exec()
            self.refresh_ports()
            return  # Exit the function if no valid COM port is selected
        try:
            # Open the serial port
            self.serial_connection = serial.Serial(com_port, baud_rate, timeout=1)
            # Start a timer to periodically read data from the serial port
            self.timer = QTimer()
            self.timer.timeout.connect(self.read_serial_data)
            self.timer.start(100)  # Check every 100ms                
            self.Serial_monitor_textEdit.append("Serial monitor started...")
        except serial.SerialException as e:
            self.Serial_monitor_textEdit.append(f"Error opening serial port: {e}")

    def read_serial_data(self):
        """Read data from the serial port and append it to the QTextEdit."""
        if self.serial_connection and self.serial_connection.in_waiting > 0:
            data = self.serial_connection.read(self.serial_connection.in_waiting).decode('utf-8', errors='ignore')
            self.Serial_monitor_textEdit.append(data)

    def disconnect_comport(self):
        """Disconnect the COM port if it's open."""
        if self.serial_connection and self.serial_connection.is_open:
            self.serial_connection.close()
            self.serial_connection = None
            self.Serial_monitor_textEdit.append("Serial port disconnected.")
        else:
            self.Serial_monitor_textEdit.append("No serial connection to disconnect.")

    def clear_serial_monitor_text(self):
        self.Serial_monitor_textEdit.clear()

    def send_command(self, command):
        com = self.comport_comboBox.currentText()
        baud = self.br_comboBox.currentText()

        # Check if the COM port is valid
        if not com or "No COM" in com:
            if not hasattr(self, 'com_port_error_shown') or not self.com_port_error_shown:
                self.show_error("Please select a COM port and try again.")
                self.com_port_error_shown = True  # Flag to ensure only one error is shown
            return  # Exit function if COM port is not valid
        
        # If COM port is valid, attempt to send the command
        try:
            with serial.Serial(com, baud, timeout=1) as ser:
                ser.write(command)
                print(f"Sent data: {command.hex()}")
            # Reset error flag after a successful send
            self.com_port_error_shown = False
        except serial.SerialException as e:
            self.show_error(f"Error opening serial port: {e}")
            # Reset error flag in case of serial exception
            self.com_port_error_shown = False

    def show_error(self, message):
        """Displays an error message box."""
        error_msg = QMessageBox()
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.setWindowTitle("Error")
        error_msg.setText(message)
        error_msg.exec()

    def refresh_ports(self):
        ports = serial.tools.list_ports.comports()  # Fetch the list of COM ports
        items = sorted([port.device for port in ports])  # Create and sort a list of port names
        self.comport_comboBox.clear()
        if items:
            self.comport_comboBox.addItems(items)
        else:
            self.comport_comboBox.addItem("No COM port found")

if __name__ == "__main__":
    app = QApplication([])
    windows = MainWindow()
    windows.show()
    app.exec()
