import numpy as np
import os
import cv2
import json

# from pathlib import Path
from PySide6.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QButtonGroup
from PySide6.QtCore import QThread, Signal, Qt, QTimer
from PySide6.QtGui import QPixmap, QImage, QDoubleValidator
from ui_generated.main_window import Ui_MainWindow
from app.sandal import AdaptiveSandalMeasurement
from datetime import datetime

class CameraThread(QThread):
    """Thread untuk handling live camera feed"""
    frame_ready = Signal(np.ndarray)
    detection_ready = Signal(np.ndarray, dict)

    
    def __init__(self):
        super().__init__()
        self.camera = None
        self.is_running = False
        self.detect_state = True  # Your sandal detector instance
        self.system = AdaptiveSandalMeasurement()
        self.detection_enabled = False  # Flag untuk mengaktifkan deteksi    
    
    def enable_detection(self, enabled: bool):
        """Enable/disable detection processing"""
        self.detection_enabled = enabled
    
    def auto_detection(self, enabled: bool):
        self.detect_state = enabled
        print(f"status auto detect: {enabled}")
        
    def start_camera(self, camera_id=0):
        self.camera = cv2.VideoCapture(camera_id)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.is_running = True
        self.start()
        
    def stop_camera(self):
        self.is_running = False
        if self.camera:
            self.camera.release()
            
    def run(self):
        while self.is_running and self.camera and self.camera.isOpened():
            ret, frame = self.camera.read()
            if ret:
                
                # Jalankan deteksi jika detector tersedia
                if self.detection_enabled and self.detect_state:
                    try:
                        # Process detection
                        measurements, result_image = self.system.process_image(frame)
                        print(f"data : {measurements}")
                        self.detection_ready.emit(result_image, measurements)
                    except Exception as e:
                        print(f"Detection error: {e}")
                elif self.detect_state is not True:
                    self.frame_ready.emit(frame)
                    # print(f"test :{self.detect_state}")   
            self.msleep(33)  # ~30 FPS

class MainWindow(QMainWindow):
    range_updated = Signal(str, list)  # Changed from int to str for descriptive keys
    detect_state = Signal(bool)
    
    def __init__(self):
        super().__init__()
        print("🚀 Initializing App...")
        
        # setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # setup Detector
        self.system = AdaptiveSandalMeasurement()
        
        # Settings file path - pastikan path absolute
        self.settings_file = os.path.abspath("database/profile_settings.json")
        print(f"📂 Settings file path: {self.settings_file}")
        
        # Default ranges menggunakan descriptive keys
        self.default_ranges = {
            "size_1": [260.7, 266.7],  # Previously 39
            "size_2": [267.3, 273.3],  # Previously 40
            "size_3": [274.0, 280.0],  # Previously 41
            "size_4": [280.7, 286.7],  # Previously 42
            "size_5": [287.3, 293.3],  # Previously 43
            "size_6": [294.0, 300.0],  # Previously 44
            "size_7": [300.7, 306.7]   # Previously 45
        }
        
        # Default size labels untuk QLabel
        self.default_size_labels = {
            "size_1": "39",
            "size_2": "40", 
            "size_3": "41",
            "size_4": "42",
            "size_5": "43",
            "size_6": "44",
            "size_7": "45"
        }
        
        # Mapping radio button ke size key
        self.size_button_mapping = {
            1: "size_1",
            2: "size_2", 
            3: "size_3",
            4: "size_4",
            5: "size_5",
            6: "size_6",
            7: "size_7"
        }
        
        # Mapping QLabel objectName ke size key
        self.label_mapping = {
            "labelSize1": "size_1",
            "labelSize2": "size_2",
            "labelSize3": "size_3", 
            "labelSize4": "size_4",
            "labelSize5": "size_5",
            "labelSize6": "size_6",
            "labelSize7": "size_7"
        }
        
        # variabel
        self.state_check_box = True
        self.camera_active = False
        self.current_image = None
        self.selected_size = None
        self.camera_thread = CameraThread()
        
        # Flag untuk tracking perubahan
        self.ranges_modified = False
        self.current_profile = None
        
        # Initialize size ranges and labels from saved settings or defaults
        self.size_ranges = self.default_ranges.copy()
        self.size_labels = self.default_size_labels.copy()
        self.all_profiles = self.load_all_profiles()
        
        # Update backward compatibility variables
        self.update_backward_compatibility_vars()
        
        # Setup
        self.setup_connections()
        self.setup_size_selection()
        self.setup_range_inputs()
        self.setup_profile_management()
        self.populate_range_inputs()
        self.update_size_labels()  # Update QLabel texts
        
        print("✅ App initialization complete")
    
    def update_size_labels(self):
        """Update text pada QLabel berdasarkan size_labels"""
        try:
            for label_name, size_key in self.label_mapping.items():
                if hasattr(self.ui, label_name):
                    label_widget = getattr(self.ui, label_name)
                    if size_key in self.size_labels:
                        label_widget.setText(self.size_labels[size_key])
                        print(f"📝 Updated {label_name} text to: {self.size_labels[size_key]}")
                else:
                    print(f"⚠️ Label {label_name} not found in UI")
        except Exception as e:
            print(f"❌ Error updating size labels: {e}")
    
    def setup_profile_management(self):
        """Setup profile management untuk combobox dan save button"""
        try:
            # Populate combobox dengan profiles yang tersimpan
            self.populate_profile_combobox()
            
            # Connect signals
            if hasattr(self.ui, 'boxTipe'):
                self.ui.boxTipe.currentTextChanged.connect(self.on_profile_selected)
                self.ui.boxTipe.editTextChanged.connect(self.on_profile_text_changed)
            else:
                print("⚠️ boxTipe combobox not found")
                
        except Exception as e:
            print(f"❌ Error setting up profile management: {e}")
    
    def populate_profile_combobox(self):
        """Populate combobox dengan profiles yang tersimpan"""
        try:
            if not hasattr(self.ui, 'boxTipe'):
                return
                
            self.ui.boxTipe.blockSignals(True)
            self.ui.boxTipe.clear()
            
            # Add saved profiles
            profile_names = list(self.all_profiles.keys())
            if profile_names:
                self.ui.boxTipe.addItems(profile_names)
                print(f"📋 Loaded profiles: {profile_names}")
            
            self.ui.boxTipe.blockSignals(False)
        except Exception as e:
            print(f"❌ Error populating profile combobox: {e}")
    
    def on_profile_selected(self, profile_name):
        """Handle ketika profile dipilih dari combobox"""
        try:
            if not profile_name or profile_name == self.current_profile:
                return
            
            print(f"🔄 Loading profile: {profile_name}")
            
            if profile_name in self.all_profiles:
                self.load_profile(profile_name)
            else:
                print(f"⚠️ Profile '{profile_name}' not found in saved profiles")
        except Exception as e:
            print(f"❌ Error selecting profile: {e}")
    
    def on_profile_text_changed(self, text):
        """Handle ketika text di combobox diubah manual"""
        try:
            # Mark as modified when user types new profile name
            if text and text != self.current_profile:
                self.ranges_modified = True
        except Exception as e:
            print(f"❌ Error handling profile text change: {e}")
    
    def load_profile(self, profile_name):
        """Load profile berdasarkan nama dengan support untuk format lama dan baru"""
        if profile_name not in self.all_profiles:
            print(f"❌ Profile '{profile_name}' not found")
            return False
        
        try:
            profile_data = self.all_profiles[profile_name]
            
            # Load size ranges dengan backward compatibility
            if 'ranges' in profile_data:
                self.size_ranges = {}
                
                # Check if using old format (numeric keys) or new format (descriptive keys)
                old_format_keys = ['39', '40', '41', '42', '43', '44', '45']
                new_format_keys = ['size_1', 'size_2', 'size_3', 'size_4', 'size_5', 'size_6', 'size_7']
                
                ranges_data = profile_data['ranges']
                
                # Convert old format to new format if needed
                if any(key in ranges_data for key in old_format_keys):
                    print("📄 Converting old format ranges to new format")
                    # Mapping old numeric keys to new descriptive keys
                    old_to_new = {
                        '39': 'size_1', '40': 'size_2', '41': 'size_3', '42': 'size_4',
                        '43': 'size_5', '44': 'size_6', '45': 'size_7'
                    }
                    
                    for old_key, new_key in old_to_new.items():
                        if old_key in ranges_data:
                            values = ranges_data[old_key]
                            self.size_ranges[new_key] = [float(values[0]), float(values[1])]
                else:
                    # Use new format directly
                    for size_key, values in ranges_data.items():
                        self.size_ranges[size_key] = [float(values[0]), float(values[1])]
            
            # Load size labels dengan backward compatibility
            if 'size_labels' in profile_data:
                labels_data = profile_data['size_labels']
                self.size_labels = {}
                
                # Check format and convert if needed
                if any(key in labels_data for key in ['39', '40', '41', '42', '43', '44', '45']):
                    print("📄 Converting old format labels to new format")
                    old_to_new = {
                        '39': 'size_1', '40': 'size_2', '41': 'size_3', '42': 'size_4',
                        '43': 'size_5', '44': 'size_6', '45': 'size_7'
                    }
                    
                    for old_key, new_key in old_to_new.items():
                        if old_key in labels_data:
                            self.size_labels[new_key] = labels_data[old_key]
                else:
                    # Use new format directly
                    self.size_labels = labels_data.copy()
                
                print(f"📋 Loaded size labels: {self.size_labels}")
            else:
                # Use default labels if not found
                self.size_labels = self.default_size_labels.copy()
                print("📋 Using default size labels")
            
            # Load selected size dengan mapping
            if 'selected_size' in profile_data:
                old_selected = profile_data['selected_size']
                if old_selected:
                    # Convert old numeric selected_size to new format
                    if isinstance(old_selected, int):
                        old_to_new_selected = {
                            39: 'size_1', 40: 'size_2', 41: 'size_3', 42: 'size_4',
                            43: 'size_5', 44: 'size_6', 45: 'size_7'
                        }
                        self.selected_size = old_to_new_selected.get(old_selected, None)
                    else:
                        self.selected_size = old_selected
                    
                    self.set_selected_radio_button(self.selected_size)
            
            # Update UI
            self.populate_range_inputs()
            self.update_size_labels()  # Update QLabel texts
            self.update_backward_compatibility_vars()
            
            self.current_profile = profile_name
            self.ranges_modified = False
            
            print(f"✅ Profile '{profile_name}' loaded successfully")
            print(f"📊 Loaded ranges: {self.size_ranges}")
            print(f"📝 Loaded labels: {self.size_labels}")
            print(f"📐 Selected size: {self.selected_size}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading profile '{profile_name}': {e}")
            return False
    
    def save_current_profile(self):
        """Save profile saat ini dengan nama dari combobox"""
        try:
            if not hasattr(self.ui, 'boxTipe'):
                QMessageBox.warning(self, "Error", "Profile combobox not found!")
                return False
                
            profile_name = self.ui.boxTipe.currentText().strip()
            
            if not profile_name:
                QMessageBox.warning(self, "Warning", "Please enter a profile name!")
                return False
            
            # Check if all min/max fields are filled
            if not self.validate_all_ranges():
                QMessageBox.warning(self, "Warning", "Please fill all MIN and MAX values!")
                return False
            
            # Get current selected size from radio buttons
            current_selected_size = self.get_selected_radio_button()
            
            # Update current data
            self.update_ranges_from_ui()
            
            # Prepare profile data dengan format baru
            profile_data = {
                'ranges': {},
                'size_labels': {},
                'selected_size': current_selected_size,
                'last_modified': datetime.now().isoformat()
            }
            
            # Save ranges dengan descriptive keys
            for size_key in ['size_1', 'size_2', 'size_3', 'size_4', 'size_5', 'size_6', 'size_7']:
                if size_key in self.size_ranges:
                    profile_data['ranges'][size_key] = [
                        float(self.size_ranges[size_key][0]),
                        float(self.size_ranges[size_key][1])
                    ]
                
                # Save size labels
                if size_key in self.size_labels:
                    profile_data['size_labels'][size_key] = self.size_labels[size_key]
            
            # Save to all_profiles
            self.all_profiles[profile_name] = profile_data
            self.current_profile = profile_name
            
            # Save to file
            if self.save_all_profiles():
                # Update combobox if new profile
                if profile_name not in [self.ui.boxTipe.itemText(i) for i in range(self.ui.boxTipe.count())]:
                    self.ui.boxTipe.addItem(profile_name)
                    self.ui.boxTipe.setCurrentText(profile_name)
                
                self.ranges_modified = False
                QMessageBox.information(self, "Success", f"Profile '{profile_name}' saved successfully!")
                return True
            else:
                QMessageBox.critical(self, "Error", "Failed to save profile!")
                return False
                
        except Exception as e:
            print(f"❌ Error saving profile: {e}")
            QMessageBox.critical(self, "Error", f"Failed to save profile:\n{str(e)}")
            return False
    
    def validate_all_ranges(self):
        """Validate bahwa semua field min/max terisi"""
        try:
            range_inputs = [
                (self.ui.min1, self.ui.max1),
                (self.ui.min2, self.ui.max2),
                (self.ui.min3, self.ui.max3),
                (self.ui.min4, self.ui.max4),
                (self.ui.min5, self.ui.max5),
                (self.ui.min6, self.ui.max6),
                (self.ui.min7, self.ui.max7),
            ]
        
            for min_input, max_input in range_inputs:
                if not min_input.text().strip() or not max_input.text().strip():
                    return False
                
                try:
                    min_val = float(min_input.text())
                    max_val = float(max_input.text())
                    if min_val >= max_val:
                        return False
                except ValueError:
                    return False
            
            return True
        except Exception as e:
            print(f"❌ Error validating ranges: {e}")
            return False
    
    def update_ranges_from_ui(self):
        """Update size_ranges dari nilai UI saat ini menggunakan descriptive keys"""
        try:
            range_inputs = [
                ("size_1", self.ui.min1, self.ui.max1),  # size_1 = previously 39
                ("size_2", self.ui.min2, self.ui.max2),  # size_2 = previously 40
                ("size_3", self.ui.min3, self.ui.max3),  # size_3 = previously 41
                ("size_4", self.ui.min4, self.ui.max4),  # size_4 = previously 42
                ("size_5", self.ui.min5, self.ui.max5),  # size_5 = previously 43
                ("size_6", self.ui.min6, self.ui.max6),  # size_6 = previously 44
                ("size_7", self.ui.min7, self.ui.max7),  # size_7 = previously 45
            ]
            
            for size_key, min_input, max_input in range_inputs:
                try:
                    min_val = float(min_input.text())
                    max_val = float(max_input.text())
                    self.size_ranges[size_key] = [min_val, max_val]
                except ValueError:
                    print(f"❌ Invalid input for {size_key}")
        except Exception as e:
            print(f"❌ Error updating ranges from UI: {e}")
    
    def get_selected_radio_button(self):
        """Get ukuran yang dipilih dari radio button dengan descriptive key"""
        try:
            # Mapping button position to descriptive key
            radio_buttons = [
                ("size_1", getattr(self.ui, 'btn1', None)),  # btn1 now maps to size_1
                ("size_2", getattr(self.ui, 'btn2', None)),  # btn2 now maps to size_2
                ("size_3", getattr(self.ui, 'btn3', None)),  # btn3 now maps to size_3
                ("size_4", getattr(self.ui, 'btn4', None)),  # btn4 now maps to size_4
                ("size_5", getattr(self.ui, 'btn5', None)),  # btn5 now maps to size_5
                ("size_6", getattr(self.ui, 'btn6', None)),  # btn6 now maps to size_6
                ("size_7", getattr(self.ui, 'btn7', None)),  # btn7 now maps to size_7
            ]
            
            for size_key, radio_button in radio_buttons:
                if radio_button and radio_button.isChecked():
                    return size_key
            
            return None
        except Exception as e:
            print(f"❌ Error getting selected radio button: {e}")
            return None
    
    def set_selected_radio_button(self, size_key):
        """Set radio button berdasarkan descriptive key"""
        try:
            if not size_key:
                return
            
            # Mapping descriptive key to button
            key_to_button = {
                "size_1": getattr(self.ui, 'btn1', None),
                "size_2": getattr(self.ui, 'btn2', None),
                "size_3": getattr(self.ui, 'btn3', None),
                "size_4": getattr(self.ui, 'btn4', None),
                "size_5": getattr(self.ui, 'btn5', None),
                "size_6": getattr(self.ui, 'btn6', None),
                "size_7": getattr(self.ui, 'btn7', None),
            }
            
            # Clear all radio buttons first
            for button in key_to_button.values():
                if button:
                    button.setChecked(False)
            
            # Set selected radio button
            selected_button = key_to_button.get(size_key)
            if selected_button:
                selected_button.setChecked(True)
                print(f"📐 Selected radio button for {size_key}")
        except Exception as e:
            print(f"❌ Error setting selected radio button: {e}")
    
    def load_all_profiles(self):
        """Load semua profiles dari file JSON"""
        print(f"📖 Loading all profiles from: {self.settings_file}")
        
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                print(f"📄 Loaded {len(data)} profiles: {list(data.keys())}")
                return data
            else:
                print("📋 No saved profiles file found")
                return {}
                
        except Exception as e:
            print(f"❌ Error loading profiles: {e}")
            return {}
    
    def save_all_profiles(self):
        """Save semua profiles ke file JSON"""
        print(f"💾 Saving all profiles to: {self.settings_file}")
        print(f"📊 Profiles to save: {list(self.all_profiles.keys())}")
        
        try:
            # Ensure directory exists
            directory = os.path.dirname(self.settings_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # Save to temporary file first (atomic write)
            temp_file = self.settings_file + '.tmp'
            with open(temp_file, 'w', encoding='utf-8') as f:
                json.dump(self.all_profiles, f, indent=4, ensure_ascii=False)
            
            # Move temp file to actual file (atomic operation)
            if os.path.exists(self.settings_file):
                os.remove(self.settings_file)
            os.rename(temp_file, self.settings_file)
            
            print(f"✅ All profiles saved successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error saving profiles: {e}")
            return False
    
    def setup_range_inputs(self):
        """Setup range input fields with number validation"""
        try:
            from PySide6.QtCore import Qt
            
            # Validator untuk angka positif dengan max 1 decimal
            validator = QDoubleValidator(0.0, 999.9, 1)
            validator.setNotation(QDoubleValidator.Notation.StandardNotation)
            
            range_inputs = [
                self.ui.min1, self.ui.max1,
                self.ui.min2, self.ui.max2,
                self.ui.min3, self.ui.max3,
                self.ui.min4, self.ui.max4,
                self.ui.min5, self.ui.max5,
                self.ui.min6, self.ui.max6,
                self.ui.min7, self.ui.max7
            ]
            
            for line_edit in range_inputs:
                line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
                line_edit.setValidator(validator)
                
        except Exception as e:
            print(f"❌ Error setting up range inputs: {e}")
    
    def connect_range_inputs(self):
        """Connect range input signals"""
        try:
            range_connections = [
                ("size_1", self.ui.min1, self.ui.max1),
                ("size_2", self.ui.min2, self.ui.max2),
                ("size_3", self.ui.min3, self.ui.max3),
                ("size_4", self.ui.min4, self.ui.max4),
                ("size_5", self.ui.min5, self.ui.max5),
                ("size_6", self.ui.min6, self.ui.max6),
                ("size_7", self.ui.min7, self.ui.max7)
            ]
            
            for size_key, min_input, max_input in range_connections:
                # Connect textChanged untuk tracking perubahan
                min_input.textChanged.connect(lambda text, s=size_key: self.mark_modified())
                max_input.textChanged.connect(lambda text, s=size_key: self.mark_modified())
                
                # Connect editingFinished untuk validation dan update
                min_input.editingFinished.connect(lambda s=size_key, input=min_input: self.update_range_value(s, input, True))
                max_input.editingFinished.connect(lambda s=size_key, input=max_input: self.update_range_value(s, input, False))
        except Exception as e:
            print(f"❌ Error connecting range inputs: {e}")
    
    def mark_modified(self):
        """Mark bahwa ada perubahan yang perlu disimpan"""
        try:
            self.ranges_modified = True
            print("📝 Ranges marked as modified")
        except Exception as e:
            print(f"❌ Error marking modified: {e}")
    
    def update_range_value(self, size_key, input_widget, is_min):
        """Update nilai range saat editing selesai"""
        try:
            value = float(input_widget.text())
            
            if is_min:
                self.size_ranges[size_key][0] = value
                print(f"📊 Updated min for {size_key}: {value}")
            else:
                self.size_ranges[size_key][1] = value
                print(f"📊 Updated max for {size_key}: {value}")
            
            # Update backward compatibility variables
            self.update_backward_compatibility_vars()
            
            # Validate range
            self.validate_range(size_key)
            
            # Emit signal
            self.range_updated.emit(size_key, self.size_ranges[size_key])
            
            # Mark as modified
            self.ranges_modified = True
            
        except ValueError:
            print(f"❌ Invalid input for {size_key}: {input_widget.text()}")
            # Reset ke nilai sebelumnya
            try:
                if is_min:
                    input_widget.setText(str(self.size_ranges[size_key][0]))
                else:
                    input_widget.setText(str(self.size_ranges[size_key][1]))
            except:
                pass
        except Exception as e:
            print(f"❌ Error updating range value: {e}")
    
    def populate_range_inputs(self):
        """Fill range inputs with current values"""
        try:
            range_inputs = [
                ("size_1", self.ui.min1, self.ui.max1),
                ("size_2", self.ui.min2, self.ui.max2),
                ("size_3", self.ui.min3, self.ui.max3),
                ("size_4", self.ui.min4, self.ui.max4),
                ("size_5", self.ui.min5, self.ui.max5),
                ("size_6", self.ui.min6, self.ui.max6),
                ("size_7", self.ui.min7, self.ui.max7),
            ]
        
            # Block signals untuk avoid trigger
            for size_key, min_input, max_input in range_inputs:
                if size_key in self.size_ranges:
                    min_input.blockSignals(True)
                    max_input.blockSignals(True)
                    
                    min_input.setText(str(self.size_ranges[size_key][0]))
                    max_input.setText(str(self.size_ranges[size_key][1]))
                    
                    min_input.blockSignals(False)
                    max_input.blockSignals(False)
            
            print("📋 Range inputs populated")
        except Exception as e:
            print(f"❌ Error populating range inputs: {e}")
    
    def update_backward_compatibility_vars(self):
        """Update backward compatibility variables"""
        try:
            # Map new descriptive keys to old variable names for backward compatibility
            key_to_old_var = {
                "size_1": "range_size39",
                "size_2": "range_size40", 
                "size_3": "range_size41",
                "size_4": "range_size42",
                "size_5": "range_size43",
                "size_6": "range_size44",
                "size_7": "range_size45"
            }
            
            for size_key, var_name in key_to_old_var.items():
                if size_key in self.size_ranges:
                    setattr(self, var_name, [str(self.size_ranges[size_key][0]), str(self.size_ranges[size_key][1])])
        except Exception as e:
            print(f"❌ Error updating backward compatibility vars: {e}")
    
    def validate_range(self, size_key):
        """Validate that min < max for a size"""
        try:
            if size_key not in self.size_ranges:
                return
                
            min_val = self.size_ranges[size_key][0]
            max_val = self.size_ranges[size_key][1]
            
            if min_val >= max_val:
                print(f"❌ Invalid range for {size_key}: {min_val} >= {max_val}")
                
                # Show warning dengan label yang user-friendly
                size_label = self.size_labels.get(size_key, size_key)
                QMessageBox.warning(self, "Invalid Range", 
                                  f"Size {size_label}: Minimum ({min_val}) must be less than maximum ({max_val})!")
                
                # Reset to default
                if size_key in self.default_ranges:
                    self.size_ranges[size_key] = self.default_ranges[size_key].copy()
                    print(f"🔄 Reset {size_key} to default: {self.size_ranges[size_key]}")
                    
                    # Update backward compatibility
                    self.update_backward_compatibility_vars()
                    
                    # Update UI
                    self.populate_range_inputs()
        except Exception as e:
            print(f"❌ Error validating range: {e}")
    
    def setup_size_selection(self):
        """Setup size selection radio buttons dengan descriptive keys"""
        try:
            self.size_button_group = QButtonGroup(self)
            
            # Mapping button to descriptive keys
            self.size_mapping = {
                self.ui.btn1: "size_1",
                self.ui.btn2: "size_2",
                self.ui.btn3: "size_3",
                self.ui.btn4: "size_4",
                self.ui.btn5: "size_5",
                self.ui.btn6: "size_6",
                self.ui.btn7: "size_7",
            }
            
            # Add buttons to group with string IDs
            for i, (radio_button, size_key) in enumerate(self.size_mapping.items()):
                self.size_button_group.addButton(radio_button, i)
            
            # Connect signal menggunakan button index
            self.size_button_group.idClicked.connect(self.on_size_selected)
            print("✅ Size selection setup completed")
            
        except Exception as e:
            print(f"⚠️ Size selection setup error: {e}")
    
    def on_size_selected(self, button_id):
        """Handle size selection dengan descriptive key"""
        try:
            # Convert button_id to size_key
            size_keys = list(self.size_mapping.values())
            if 0 <= button_id < len(size_keys):
                self.selected_size = size_keys[button_id]
                print(f"📐 Selected size: {self.selected_size}")
                
                # Update status jika ada
                if hasattr(self.ui, 'statusResult'):
                    size_label = self.size_labels.get(self.selected_size, self.selected_size)
                    self.ui.statusResult.setText(size_label)
                    
        except Exception as e:
            print(f"⚠️ Size selection error: {e}")
    
    # def on_range_updated(self, size_key, range_values):
    #     """Handle range update signal"""
    #     try:
    #         size_label = self.size_labels.get(size_key, size_key)
    #         print(f"📏 Range updated - {size_label}: {range_values[0]} - {range_values[1]} mm")
    #     except Exception as e:
    #         print(f"❌ Error handling range update: {e}")
    
    # def setup_connections(self):
    #     """Setup semua connections"""
    #     try:
    #         self.connect_range_inputs()
    #     except Exception as e:
    #         print(f"❌ Error setting up connections: {e}")
    
    # ===== UTILITY METHODS FOR SIZE MANAGEMENT =====
    
    # def change_size_labels(self, new_labels_dict):
    #     """Change size labels programmatically
        
    #     Args:
    #         new_labels_dict (dict): Dictionary with size_key -> label mapping
    #         Example: {"size_1": "XS", "size_2": "S", "size_3": "M", ...}
    #     """
    #     try:
    #         # Update size labels
    #         for size_key, label in new_labels_dict.items():
    #             if size_key in self.size_labels:
    #                 self.size_labels[size_key] = label
            
    #         # Update QLabel texts
    #         self.update_size_labels()
            
    #         # Mark as modified
    #         self.ranges_modified = True
            
    #         print(f"📝 Size labels changed: {new_labels_dict}")
    #         return True
            
    #     except Exception as e:
    #         print(f"❌ Error changing size labels: {e}")
    #         return False
    
    # def create_demo_profiles_with_descriptive_keys(self):
    #     """Create demo profiles dengan descriptive keys"""
    #     try:
    #         demo_profiles = {
    #             "E8010M_Letters": {
    #                 "ranges": {
    #                     "size_1": [236.6, 243.3],
    #                     "size_2": [253.3, 260.0],
    #                     "size_3": [270.0, 276.6],
    #                     "size_4": [286.6, 293.3],
    #                     "size_5": [303.3, 310.0],
    #                     "size_6": [323.3, 330.0],
    #                     "size_7": [336.6, 343.3]
    #                 },
    #                 "size_labels": {
    #                     "size_1": "XS", "size_2": "S", "size_3": "M", "size_4": "L",
    #                     "size_5": "XL", "size_6": "XXL", "size_7": "XXXL"
    #                 },
    #                 "selected_size": "size_3",  # M
    #                 "last_modified": datetime.now().isoformat()
    #             },
    #             "E8010M_Numbers": {
    #                 "ranges": {
    #                     "size_1": [236.6, 243.3],
    #                     "size_2": [253.3, 260.0],
    #                     "size_3": [270.0, 276.6],
    #                     "size_4": [286.6, 293.3],
    #                     "size_5": [303.3, 310.0],
    #                     "size_6": [323.3, 330.0],
    #                     "size_7": [336.6, 343.3]
    #                 },
    #                 "size_labels": {
    #                     "size_1": "39", "size_2": "40", "size_3": "41", "size_4": "42",
    #                     "size_5": "43", "size_6": "44", "size_7": "45"
    #                 },
    #                 "selected_size": "size_4",  # 42
    #                 "last_modified": datetime.now().isoformat()
    #             },
    #             "E8010M_Custom": {
    #                 "ranges": {
    #                     "size_1": [236.6, 243.3],
    #                     "size_2": [253.3, 260.0],
    #                     "size_3": [270.0, 276.6],
    #                     "size_4": [286.6, 293.3],
    #                     "size_5": [303.3, 310.0],
    #                     "size_6": [323.3, 330.0],
    #                     "size_7": [336.6, 343.3]
    #                 },
    #                 "size_labels": {
    #                     "size_1": "Mini", "size_2": "Small", "size_3": "Regular", "size_4": "Large",
    #                     "size_5": "XLarge", "size_6": "XXL", "size_7": "Jumbo"
    #                 },
    #                 "selected_size": "size_2",  # Small
    #                 "last_modified": datetime.now().isoformat()
    #             }
    #         }
            
    #         # Merge dengan existing profiles
    #         self.all_profiles.update(demo_profiles)
            
    #         # Save dan update UI
    #         if self.save_all_profiles():
    #             self.populate_profile_combobox()
    #             print("✅ Demo profiles with descriptive keys created successfully!")
    #             QMessageBox.information(self, "Success", "Demo profiles created successfully!")
    #             return True
    #         else:
    #             QMessageBox.warning(self, "Warning", "Failed to save demo profiles!")
    #             return False
                
    #     except Exception as e:
    #         print(f"❌ Error creating demo profiles: {e}")
    #         QMessageBox.critical(self, "Error", f"Failed to create demo profiles:\n{str(e)}")
    #         return False
    
    # def convert_old_profile_to_new_format(self, profile_name):
    #     """Convert old format profile (numeric keys) to new format (descriptive keys)"""
    #     try:
    #         if profile_name not in self.all_profiles:
    #             print(f"❌ Profile '{profile_name}' not found")
    #             return False
            
    #         profile_data = self.all_profiles[profile_name]
    #         updated = False
            
    #         # Convert ranges
    #         if 'ranges' in profile_data:
    #             ranges_data = profile_data['ranges']
    #             old_keys = ['39', '40', '41', '42', '43', '44', '45']
                
    #             if any(key in ranges_data for key in old_keys):
    #                 print(f"🔄 Converting ranges in profile '{profile_name}'")
    #                 new_ranges = {}
    #                 old_to_new = {
    #                     '39': 'size_1', '40': 'size_2', '41': 'size_3', '42': 'size_4',
    #                     '43': 'size_5', '44': 'size_6', '45': 'size_7'
    #                 }
                    
    #                 for old_key, new_key in old_to_new.items():
    #                     if old_key in ranges_data:
    #                         new_ranges[new_key] = ranges_data[old_key]
                    
    #                 profile_data['ranges'] = new_ranges
    #                 updated = True
            
    #         # Convert size_labels
    #         if 'size_labels' in profile_data:
    #             labels_data = profile_data['size_labels']
    #             old_keys = ['39', '40', '41', '42', '43', '44', '45']
                
    #             if any(key in labels_data for key in old_keys):
    #                 print(f"🔄 Converting size_labels in profile '{profile_name}'")
    #                 new_labels = {}
    #                 old_to_new = {
    #                     '39': 'size_1', '40': 'size_2', '41': 'size_3', '42': 'size_4',
    #                     '43': 'size_5', '44': 'size_6', '45': 'size_7'
    #                 }
                    
    #                 for old_key, new_key in old_to_new.items():
    #                     if old_key in labels_data:
    #                         new_labels[new_key] = labels_data[old_key]
                    
    #                 profile_data['size_labels'] = new_labels
    #                 updated = True
            
    #         # Convert selected_size
    #         if 'selected_size' in profile_data:
    #             old_selected = profile_data['selected_size']
    #             if isinstance(old_selected, int):
    #                 old_to_new_selected = {
    #                     39: 'size_1', 40: 'size_2', 41: 'size_3', 42: 'size_4',
    #                     43: 'size_5', 44: 'size_6', 45: 'size_7'
    #                 }
    #                 new_selected = old_to_new_selected.get(old_selected)
    #                 if new_selected:
    #                     profile_data['selected_size'] = new_selected
    #                     updated = True
            
    #         if updated:
    #             # Update last_modified
    #             profile_data['last_modified'] = datetime.now().isoformat()
                
    #             # Save changes
    #             if self.save_all_profiles():
    #                 print(f"✅ Profile '{profile_name}' converted to new format")
    #                 return True
    #             else:
    #                 print(f"❌ Failed to save converted profile '{profile_name}'")
    #                 return False
    #         else:
    #             print(f"ℹ️ Profile '{profile_name}' already in new format")
    #             return True
                
    #     except Exception as e:
    #         print(f"❌ Error converting profile '{profile_name}': {e}")
    #         return False
    
    # ===== BACKWARD COMPATIBILITY METHODS =====
    
    # def load_ranges(self):
    #     """Load ranges from JSON file - backward compatibility"""
    #     return self.default_ranges.copy()
    
    # def save_ranges(self):
    #     """Save ranges to JSON file - backward compatibility"""
    #     return self.save_current_profile()
    
    def force_save_current_values(self):
        """Force save nilai saat ini dari UI - backward compatibility"""
        return self.save_current_profile()
            
    def setup_connections(self):
        try:
            #select photo
            self.ui.loadImage.clicked.connect(self.slect_image)
            self.ui.detectImage.clicked.connect(self.detect_image)
            
            #live
            self.ui.startCamera.clicked.connect(self.start_camera)
            self.ui.stopCamera.clicked.connect(self.stop_camera)
            self.ui.captureFrame.clicked.connect(self.capture_frame)
            self.ui.checkBox.stateChanged.connect(self.chack_state)
            
            #camera
            self.camera_thread.frame_ready.connect(self.stream_camera_display)
            # self.camera_thread.detection_ready.connect(self.update_detection_display)
            self.camera_thread.detection_ready.connect(self.update_camera_display)
            self.detect_state.connect(self.camera_thread.auto_detection)
            
            #save size
            self.ui.saveInputSize.clicked.connect(self.save_current_profile)
            
            self.connect_range_inputs()
            
            #export
            self.ui.saveImage.clicked.connect(self.save_image)
            
        except Exception as e:
            print(f"⚠️  Connection setup error: {e}")
    
    
    def chack_state(self, state):
        self.state_check_box = state == 2
        self.detect_state.emit(self.state_check_box)
    
    def slect_image(self):
        """Load image for photo mode"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Image", "", 
            "Image Files (*.png *.jpg *.jpeg *.bmp *.tiff)"
        )
        if file_path:
            self.current_image = cv2.imread(file_path)
            self.display_image(self.current_image)
            self.ui.loadImage.setEnabled(True)
    
    def detect_image(self):
        if self.current_image is not None:
            measurements, result_image = self.system.process_image(self.current_image)
            # measurements, result_image = self.system.process_image_with_tilt(self.current_image)
            self.display_image(result_image)
            print(measurements)
            self.display_measurements(measurements)
            self.ui.detectImage.setEnabled(True)
    
    def get_size_for_length(self, length):
        toleransi = 3.0
        kondisi = [length, length - toleransi, length + toleransi]
        for val in kondisi:
            for size, (min_val, max_val) in self.size_ranges.items():
                    if min_val <= val <= max_val:
                        return val
        return length
    
    # def check_size(self, length):
    #     self.selected_size = None
    #     label_size = ["XS", "S", "M", "L", "XL", "2XL", "3XL"]
    #     try:
    #         for size, (min_val, max_val) in self.size_ranges.items():
    #             if min_val <= length <= max_val:
    #                 # Tentukan indeks ukuran berdasarkan size (41 -> M, 42 -> L, dll.)
    #                 size_index = size - 39  # Misalnya size 39 -> indeks 0, 40 -> indeks 1, dsb.
    #                 if 0 <= size_index < len(label_size):
    #                     self.selected_size = label_size[size_index]
    #                 break
    #         if self.selected_size is not None:
    #             self.bg_color("rgb(0, 255, 0)")
    #             return self.selected_size
    #         else:
    #             self.bg_color("rgb(255, 0, 0)")
    #             return ""
    #     except (ValueError, TypeError):
    #         return None
    
    def check_size(self, length):
        self.selected_size = None
        label_size = ["XS", "S", "M", "L", "XL", "2XL", "3XL"]
        try:
            # Iterate over the size ranges and determine the correct size
            for size_key, (min_val, max_val) in self.size_ranges.items():
                if min_val <= length <= max_val:
                    # Tentukan indeks ukuran berdasarkan key size (size_1 -> indeks 0, size_2 -> indeks 1, dll.)
                    size_index = int(size_key.split('_')[1]) - 1  # Extract number from "size_1" to "size_7" and adjust index
                    if 0 <= size_index < len(label_size):
                        self.selected_size = label_size[size_index]
                    break

            if self.selected_size is not None:
                self.bg_color("rgb(0, 255, 0)")  # Green for valid size
                return self.selected_size
            else:
                self.bg_color("rgb(255, 0, 0)")  # Red for invalid size
                return ""
        except (ValueError, TypeError):
            return None
    
    def bg_color(self, color):
        BASE_LABEL_STYLE = """
        border-radius: 25px;
        font-size: 70px;
        color: rgb(0, 0, 0);
        """
        full_style = f"background-color: {color}; {BASE_LABEL_STYLE}"
        self.ui.statusResult.setStyleSheet(full_style)

    def start_camera(self):
        camera_id = self.ui.boxID.value()
        self.camera_thread.start_camera(camera_id)
        self.camera_thread.enable_detection(True)
    
    def stop_camera(self):
        self.camera_thread.stop_camera()
        self.camera_thread.enable_detection(False)
    
    def capture_frame(self):
        if self.camera_thread.current_frame is not None:
            self.camera_thread.enable_detection(True)
            QTimer.singleShot(5000, lambda: self.camera_thread.enable_detection(False))
        
    
    def save_image():
        pass
    
    def save_size(self):
        if self.force_save_current_values():
            print("✅ Settings saved successfully on close")
        else:
            print("❌ Failed to save settings on close") 
    
    def display_measurements(self, measurements):
        corrected_length = measurements.get('corrected_length_mm', measurements['raw_length_mm'])
        corrected_width = measurements.get('corrected_width_mm', measurements['raw_width_mm'])
        corrected_length = self.get_linear_length(corrected_length)
        self.ui.lengthValue.setText(f"{corrected_length:.1f} mm")
        self.ui.widthValue.setText(f"{corrected_width:.1f} mm")
        self.ui.areaValue.setText(f"{measurements['area_mm2']:.0f} mm²")
        self.ui.perimeterValue.setText(f"{measurements['perimeter_mm']:.1f} mm")
        self.ui.ratioValue.setText(f"{measurements['pixel_to_mm_ratio']:.3f} px/mm")
        self.ui.markersValue.setText(f"{measurements['markers_detected']}/8")
        rounded_value = round(corrected_length, 1)
        self.ui.statusResult.setText(str(self.check_size(rounded_value)))
    
    def get_linear_length(self, length):
        corrected_length = None
        tipe = self.ui.boxTipe.currentText()
        if tipe == "E9006M":
            corrected_length = length
        elif tipe == "E8010M":
            corrected_length = 0.9106*length + 10.526
        return self.get_size_for_length(corrected_length)
        
    
    def update_camera_display(self, frame, measurements):
        """Update display with camera frame"""
        self.current_image = frame.copy()
        self.display_image(self.current_image)
        self.display_measurements(measurements)
        
    def update_detection_display(self, processed_frame, measurements):
        """Update display with detection results"""
        self.display_image(processed_frame)
        print(f"data : {measurements}")
        self.display_measurements(measurements)
        
    def stream_camera_display(self,frame):
        if self.camera_thread.frame_ready is not None:
           self.display_image(frame)  
        
    def display_image(self, img_path):
        if img_path is not None:
            # Convert BGR to RGB
            rgb_image = cv2.cvtColor(img_path, cv2.COLOR_BGR2RGB)
            
            # Convert to QImage
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            
            # Scale to fit display
            pixmap = QPixmap.fromImage(qt_image)
            scaled_pixmap = pixmap.scaled(
                self.ui.screenImage.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            
            self.ui.screenImage.setPixmap(scaled_pixmap)