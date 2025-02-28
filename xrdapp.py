import sys
import os
import numpy as np
import xylib
import struct
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidget, QVBoxLayout, QWidget, QGridLayout, QMessageBox, QDialog, QCheckBox, QVBoxLayout, QDialogButtonBox, QLineEdit, QLabel, QFormLayout
from PyQt5.QtGui import QIcon
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class CustomToolbar(NavigationToolbar):
    def __init__(self, canvas, parent):
        super().__init__(canvas, parent)
        # Remove items 6 and 7 from the toolbar
        self.actions()[6].setVisible(False)
        # self.actions()[7].setVisible(False)
        # duplicate 'Rescale plot' functionality
        self.actions()[0].triggered.disconnect()
        self.actions()[0].triggered.connect(parent.rescale_plot)
        # Add custom buttons for "Import Data", "Load Temperatures", "Fit Screen", "Toggle Hover", "Clear Data", "Toggle List", "Toggle Grid", and "Set Ticks"
        self.insertAction(self.actions()[1], self.addAction(QIcon(resource_path('media/import-content.png')), 'Import Data', parent.import_data))
        self.insertAction(self.actions()[2], self.addAction(QIcon(resource_path('media/temperature-low.png')), 'Load Temperatures', parent.import_temperatures))
        self.insertAction(self.actions()[3], self.addAction(QIcon(resource_path('media/stretch-vertically.png')), 'Fit Screen', parent.fit_screen))
        self.hover_action = self.addAction(QIcon(resource_path('media/cursor.png')), 'Toggle Cursor', parent.toggle_hover)
        self.insertAction(self.actions()[4], self.hover_action)
        self.hover_action.setCheckable(True)
        self.hover_action.setChecked(False)
        
        self.insertAction(self.actions()[5],self.addAction(QIcon(resource_path('media/toggle-list-icon.png')), 'Toggle File List', parent.toggle_list))
        self.insertAction(self.actions()[6],self.addAction(QIcon(resource_path('media/toggle-grid-icon.png')), 'Toggle Grid', parent.open_grid_dialog))
        self.insertAction(self.actions()[7],self.addAction(QIcon(resource_path('media/set-ticks-icon.png')), 'Set Ticks', parent.open_ticks_dialog))
        self.insertAction(self.actions()[8],self.addAction(QIcon(resource_path('media/font-size-icon.png')), 'Set Font Size', parent.open_font_size_dialog))
       
        # Add a new button for converting files

        self.info_action = self.addAction(QIcon(resource_path('media/info-icon.png')), 'App Info', parent.show_info)
        self.addAction(self.info_action)

        self.convert_action = self.addAction(QIcon(resource_path('media/convert-icon.png')), 'Convert Data', parent.convert_file)
        self.addAction(self.convert_action)

        self.clear_action = self.addAction(QIcon(resource_path('media/clear-data-icon.png')), 'Clear Data', parent.confirm_clear_data)
        self.addAction(self.clear_action)

class GridDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Toggle Grid')
        self.layout = QVBoxLayout()

        self.vertical_grid_checkbox = QCheckBox('Vertical Grid')
        self.layout.addWidget(self.vertical_grid_checkbox)

        self.horizontal_grid_checkbox = QCheckBox('Horizontal Grid')
        self.layout.addWidget(self.horizontal_grid_checkbox)

        self.minor_vertical_grid_checkbox = QCheckBox('Minor Vertical Grid')
        self.layout.addWidget(self.minor_vertical_grid_checkbox)

        self.minor_horizontal_grid_checkbox = QCheckBox('Minor Horizontal Grid')
        self.layout.addWidget(self.minor_horizontal_grid_checkbox)

        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def set_initial_state(self, ax):
        self.vertical_grid_checkbox.setChecked(any(line.get_visible() for line in ax.get_xgridlines() if line.get_linestyle() == '-'))
        self.horizontal_grid_checkbox.setChecked(any(line.get_visible() for line in ax.get_ygridlines() if line.get_linestyle() == '-'))
        
        # Use the flags to set the state of the minor grid checkboxes
        self.minor_vertical_grid_checkbox.setChecked(self.parent().minor_vertical_grid_enabled)
        self.minor_horizontal_grid_checkbox.setChecked(self.parent().minor_horizontal_grid_enabled)

class TicksDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Ticks')
        self.layout = QFormLayout()
        
        self.xticks_input = QLineEdit()
        self.layout.addRow(QLabel('X Ticks Spacing:'), self.xticks_input)
        
        self.yticks_input = QLineEdit()
        self.layout.addRow(QLabel('Y Ticks Spacing:'), self.yticks_input)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        # Add the Reset button
        self.reset_button = self.buttons.addButton("Reset", QDialogButtonBox.ActionRole)
        self.reset_button.clicked.connect(self.reset_ticks)
        
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)
    
    def reset_ticks(self):
        self.xticks_input.clear()
        self.yticks_input.clear()
        self.parent().reset_ticks()

class FontSizeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Set Font Size')
        self.layout = QFormLayout()
        
        # Field for axis labels font size
        self.font_size_input = QLineEdit()
        self.layout.addRow(QLabel('Axis Labels Font Size:'), self.font_size_input)
        
        # Field for tick labels font size
        self.tick_font_size_input = QLineEdit()
        self.layout.addRow(QLabel('Tick Labels Font Size:'), self.tick_font_size_input)
        
        # Field for title font size
        self.title_font_size_input = QLineEdit()
        self.layout.addRow(QLabel('Title Font Size:'), self.title_font_size_input)
        
        # Field for cursor annotation text size
        self.cursor_font_size_input = QLineEdit()
        self.layout.addRow(QLabel('Cursor Annotation Font Size:'), self.cursor_font_size_input)
        
        self.buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.buttons.accepted.connect(self.accept)
        self.buttons.rejected.connect(self.reject)
        
        # Add the Reset button
        self.reset_button = self.buttons.addButton("Reset", QDialogButtonBox.ActionRole)
        self.reset_button.clicked.connect(self.reset_font_sizes)
        
        self.layout.addWidget(self.buttons)
        self.setLayout(self.layout)
    
    def set_initial_state(self, ax):
        current_font_size = ax.xaxis.label.get_size()
        current_tick_font_size = ax.xaxis.get_ticklabels()[0].get_size() if ax.xaxis.get_ticklabels() else current_font_size
        current_title_font_size = ax.title.get_size()
        current_cursor_font_size = self.parent().annot.get_fontsize() if self.parent().annot else current_font_size
        self.font_size_input.setText(str(current_font_size))
        self.tick_font_size_input.setText(str(current_tick_font_size))
        self.title_font_size_input.setText(str(current_title_font_size))
        self.cursor_font_size_input.setText(str(current_cursor_font_size))
    
    def reset_font_sizes(self):
        self.font_size_input.setText("10.0")  # Default font size for axis labels
        self.tick_font_size_input.setText("10.0")  # Default font size for tick labels
        self.title_font_size_input.setText("12.0")  # Default font size for title
        self.cursor_font_size_input.setText("10.0")  # Default font size for cursor annotation
        self.parent().reset_font_sizes()

class XRDApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = []
        self.temperatures = []  
        self.current_index = 0
        self.xlim = None
        self.ylim = None
        self.fileNames = []
        self.hover_enabled = False
        self.xlim_margin_val = 0.00
        self.ylim_margin_val = 0.05
        self.list_visible = True
        self.vertical_grid_enabled = False  # Flag for vertical grid
        self.horizontal_grid_enabled = False  # Flag for horizontal grid
        self.minor_vertical_grid_enabled = False  # Flag for minor vertical grid
        self.minor_horizontal_grid_enabled = False  # Flag for minor horizontal grid
        self.font_size = 10  # Default font size
        self.tick_font_size = 10  # Default font size for tick labels       
        self.title_font_size = 12  # Default font size for title
        self.cursor_font_size = 10  # Default font size for cursor annotation

        self.setWindowIcon(QIcon(resource_path('media/icon_main.png')))

        self.initUI()
        self.showMaximized()  # Start the application in full-screen mode
    def initUI(self):
        self.setWindowTitle('XRD Data Viewer')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.layout = QGridLayout(central_widget)
        self.layout.setColumnStretch(0, 9)  # Set the stretch factor for the plot to 9
        self.layout.setColumnStretch(1, 1)  # Set the stretch factor for the list to 1

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas, 1, 0, 2, 9)  # Adjust the span to 9 columns

        # Initialize the toolbar after the canvas is created
        self.toolbar = CustomToolbar(self.canvas, self)
        self.layout.addWidget(self.toolbar, 0, 0, 1, 10)

        self.listWidget = QListWidget()
        self.listWidget.currentRowChanged.connect(self.on_listbox_select)
        self.layout.addWidget(self.listWidget, 1, 9, 2, 1)  # Adjust the span to 1 column

        # Connect the canvas to the hover event
        self.canvas.mpl_connect("motion_notify_event", self.on_hover)

    def import_data(self):
        files, _ = QFileDialog.getOpenFileNames(self, 'Select XRD Data Files', '', 'XRD Data Files (*.xy *.raw *.txt *.csv)')
        if files:
            self.clear_data()
            self.fileNames = files
            initial_theta = None
            theta_step = None
            for i, file in enumerate(files):
                try:
                    initial_theta, theta_step, data = self.read_file(file, i, initial_theta, theta_step)
                    if data is not None:
                        self.data.append(data)
                except Exception as e:
                    print(f"Error loading {file}: {e}")
                    QMessageBox.warning(self, "Invalid File", f"Error loading {file}: {e}")
            self.listWidget.clear()
            self.listWidget.addItems(files)
            self.current_index = 0
            self.plot_data()
            self.rescale_plot()
    

    def export_metadata(self, f, meta):
        for i in range(meta.size()):
            key = meta.get_key(i)
            value = meta.get(key)
            f.write('# %s: %s\n' % (key, value.replace('\n', '\n#\t')))

    def convert_file(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "No data available to convert.")
            return

        reply = QMessageBox.question(self, 'Convert Files', 'Do you want to convert currently loaded files?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            for i, data in enumerate(self.data):
                try:
                    # Create the "XRDapp converted" folder in the same location as the original files
                    original_folder = os.path.dirname(self.fileNames[i])
                    converted_folder = os.path.join(original_folder, 'XRDapp converted')
                    os.makedirs(converted_folder, exist_ok=True)

                    # Save the converted file in the "XRDapp converted" folder
                    file_name = os.path.splitext(os.path.basename(self.fileNames[i]))[0] + '_converted.txt'
                    converted_file_path = os.path.join(converted_folder, file_name)
                    
                    with open(converted_file_path, 'w') as f:
                        for x, y in data:
                            f.write(f"{x:.6f}\t{y:.6f}\n")
                    print(f"Converted {self.fileNames[i]} to {converted_file_path}")
                except Exception as e:
                    print(f"Error converting {self.fileNames[i]}: {e}")
                    QMessageBox.warning(self, "Conversion Error", f"Error converting {self.fileNames[i]}: {e}")
        QMessageBox.information(self, "Conversion Complete", "Files have been successfully converted.")
        

    # def convert_file(self, opt):
    #     if opt.INPUT_FILE == '-':
    #         src = (sys.stdin.buffer if hasattr(sys.stdin, 'buffer') else sys.stdin)
    #         d = xylib.load_string(src.read(), opt.t)
    #     else:
    #         d = xylib.load_file(opt.INPUT_FILE, opt.t or '')
    #     f = opt.OUTPUT_FILE
    #     f.write('# exported by XRDapp from a %s file\n' % d.fi.name)
    #     if not opt.s and d.meta.size():
    #         self.export_metadata(f, d.meta)
    #         f.write('\n')
    #     nb = d.get_block_count()
    #     for i in range(nb):
    #         block = d.get_block(i)
    #         if nb > 1 or block.get_name():
    #             f.write('\n### block #%d %s\n' % (i, block.get_name()))
    #         if not opt.s:
    #             self.export_metadata(f, block.meta)
    #         ncol = block.get_column_count()
    #         col_names = [block.get_column(k).get_name() or ('column_%d' % k) for k in range(1, ncol + 1)]
    #         f.write('# ' + '\t'.join(col_names) + '\n')
    #         nrow = block.get_point_count()
    #         for j in range(nrow):
    #             values = ["%.6f" % block.get_column(k).get_value(j) for k in range(1, ncol + 1)]
    #             f.write('\t'.join(values) + '\n')

    def read_raw_file(self, fileName, fileIndex, initial_theta, theta_step):
        try:
            dataset = xylib.load_file(fileName)
            col1, col2, meta, start2th, stepsize, nstep = self.extract_file(dataset)
            if col1 == 0 and col2 == 0:
                raise ValueError("Failed to extract columns from the file.")
            data = self.save_as_np(fileName, col2, start2th, stepsize, nstep)
            initial_theta = None
            theta_step = None
            return initial_theta, theta_step, data
        except RuntimeError as e:
            with open(fileName, 'rb') as f:
                header = f.read(6)
                if header == b'RAW4.0' and fileIndex == 0:
                    initial_theta, theta_step = self.prompt_for_theta_values()
                return initial_theta, theta_step, self.handle_raw4_file(fileName, initial_theta, theta_step)
            raise e
        
    def read_file(self, fileName, file_index, initial_theta, theta_step):
        try:
            d = xylib.load_file(fileName)
            block = d.get_block(0)
            col1 = block.get_column(1)
            col2 = block.get_column(2)
            x_values = [col1.get_value(i) for i in range(col1.get_point_count())]
            y_values = [col2.get_value(i) for i in range(col2.get_point_count())]
            initial_theta = None
            theta_step = None
            return initial_theta, theta_step, np.column_stack((x_values, y_values))
        except RuntimeError as e:
            with open(fileName, 'rb') as f:
                header = f.read(6)
                if header == b'RAW4.0' and file_index == 0:
                    initial_theta, theta_step = self.prompt_for_theta_values()
                return initial_theta, theta_step, self.handle_raw4_file(fileName, initial_theta, theta_step)
            raise e
            
    def extract_file(self, file):
        print('trying to extract the file')
        block = file.get_block(0)
        col1 = block.get_column(1)
        col2 = block.get_column(2)
        meta = block.meta
        keys = []
        for i in range(0, meta.size()):
            keys.append(meta.get_key(i))
        for key in keys:
            print(key, meta.get(key))
        if meta.has_key("START_2THETA"):
            start2th = float(meta.get('START_2THETA'))
        elif meta.has_key("THETA_START"):
            start2th = 2 * float(meta.get('THETA_START'))
        else:
            return 0, 0, 0, 0, 0, 0
        if meta.has_key('STEP_SIZE'):
            stepsize = float(meta.get('STEP_SIZE'))
        else:
            stepsize = col1.get_step()
        if meta.has_key("STEPS"):
            nstep = float(meta.get('STEPS'))
        else:
            nstep = col2.get_point_count()
        return col1, col2, meta, start2th, stepsize, nstep

    def save_as_np(self, path, col2, start, step, nstep):
        filename = os.path.basename(path)
        path = os.path.dirname(path)
        print('analyzed file: ', filename)
        if not path.endswith('/'):
            path = path + '/'
        npx = np.arange(start, start + step * nstep, step)
        valy = [col2.get_value(index) for index in range(col2.get_point_count())]
        npy = np.array(valy)
        npdataset = np.array([npx, npy]).T
        return npdataset

    def parse_raw4_file(self, file_path, initial_theta=None, theta_step=None):
        x_values = []
        y_values = []
        with open(file_path, 'rb') as f:
            data = f.read()
            if initial_theta is None or theta_step is None:
                positions = [pos for pos in range(len(data)) if data.startswith(b'2Theta', pos)]
                if positions:
                    initial_theta_pos = positions[-1] + 38 + 6
                    initial_theta = struct.unpack('<d', data[initial_theta_pos:initial_theta_pos + 8])[0]
                    if initial_theta is not None:
                        pos = data.rfind(struct.pack('<d', initial_theta), 0, initial_theta_pos)
                        if pos != -1:
                            theta_step_pos = pos + 8
                            theta_step = struct.unpack('<d', data[theta_step_pos:theta_step_pos + 8])[0]
            
            pos = len(data) - 4
            while pos >= 0:
                y = struct.unpack('<f', data[pos:pos + 4])[0]
                y_values.insert(0, y)
                pos -= 4
                if pos >= 8 and data[pos:pos + 8] == b'\x00\x00\x00\x00\x00\x00\x00\x00':
                    if data[pos+8:pos + 16] != b'\x00\x00\x00\x00\x00\x00\x00\x00':
                        delimiter_flag = True
                    else:
                        delimiter_flag = False
                    break
            
            # Check if we need to skip every other value
            if delimiter_flag:
                y_values = y_values[1::2]  # Skip every other value
            
            if initial_theta is not None and theta_step is not None:
                for i in range(len(y_values)):
                    x = initial_theta + i * theta_step
                    x_values.append(x)
        
        return x_values, y_values
 
    def handle_raw4_file(self, fileName, initial_theta=None, theta_step=None):
        x_values, y_values = self.parse_raw4_file(fileName, initial_theta, theta_step)
        data = np.column_stack((x_values, y_values))
        return data

    def prompt_for_theta_values(self):
        # Ask the user if they want to provide custom theta values
        reply = QMessageBox.question(self, 'Custom Theta Values', 'Do you want to provide custom initial theta and theta step values?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            # Create a dialog to input theta values
            dialog = QDialog(self)
            dialog.setWindowTitle("Input Theta Values")
            layout = QFormLayout(dialog)
            initial_theta_input = QLineEdit(dialog)
            theta_step_input = QLineEdit(dialog)
            layout.addRow("Initial Theta:", initial_theta_input)
            layout.addRow("Theta Step:", theta_step_input)
            buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, dialog)
            layout.addWidget(buttons)
            buttons.accepted.connect(dialog.accept)
            buttons.rejected.connect(dialog.reject)
            dialog.setLayout(layout)
            
            if dialog.exec_() == QDialog.Accepted:
                initial_theta = float(initial_theta_input.text())
                theta_step = float(theta_step_input.text())
                return initial_theta, theta_step
            else:
                return None, None
        else:
            # If the user clicks "No", return None for both values
            return None, None
    
    def import_temperatures(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "Please load XRD data before loading temperature data.")
            return
        else:
            file, _ = QFileDialog.getOpenFileName(self, 'Select Temperature Data File', '', 'Temperature Data File (*.txt)')
            if file:
                try:
                    self.temperatures = np.loadtxt(file)
                    if len(self.temperatures.shape) != 1:
                        raise ValueError("Invalid temperature data format")
                    self.plot_data()
                except ValueError as e:
                    print(f"Error loading {file}: {e}")
                    QMessageBox.warning(self, "Invalid File", f"Error loading {file}: {e}")
    def rescale_plot(self):
        if self.data:
            all_x = np.concatenate([d[:, 0] for d in self.data])
            all_y = np.concatenate([d[:, 1] for d in self.data])
            x_min, x_max = all_x.min(), all_x.max()
            y_min, y_max = all_y.min(), all_y.max()
            x_margin = self.xlim_margin_val * (x_max - x_min)
            y_margin = self.ylim_margin_val * (y_max - y_min)
            self.ax.set_xlim(x_min - x_margin, x_max + x_margin)
            self.ax.set_ylim(y_min - y_margin, y_max + y_margin)
            self.canvas.draw()

    def fit_screen(self):
        if self.data:
            data = self.data[self.current_index]
            x_min, x_max = data[:, 0].min(), data[:, 0].max()
            y_min, y_max = data[:, 1].min(), data[:, 1].max()
            x_margin = self.xlim_margin_val * (x_max - x_min)
            y_margin = self.ylim_margin_val * (y_max - y_min)
            self.ax.set_xlim(x_min - x_margin, x_max + x_margin)
            self.ax.set_ylim(y_min - y_margin, y_max + y_margin)
            self.canvas.draw()

    def plot_data(self):
        if self.data and self.current_index < len(self.data):
            data = self.data[self.current_index]
            self.figure.clear()
            self.ax = self.figure.add_subplot(111) # Ensure ax is always initialized
            line, = self.ax.plot(data[:, 0], data[:, 1])
            
            # Create annotation for hovering
            self.annot = self.ax.annotate("", xy=(0,0), xytext=(20,-20),
                                        textcoords="offset points",
                                        bbox=dict(boxstyle="round", fc="w"),
                                        arrowprops=dict(arrowstyle="->"))
            self.annot.set_visible(False)
            if len(self.temperatures) > 0 and self.current_index < len(self.temperatures):
                self.ax.set_title(f"Temperature: {self.temperatures[self.current_index]}°C")
            else:
                self.ax.set_title("XRD Data")
            self.ax.set_xlabel("2θ") # Set x-axis title to "2θ"
            self.ax.set_ylabel("Intensity")
            if self.xlim and self.ylim:
                self.ax.set_xlim(self.xlim)
                self.ax.set_ylim(self.ylim)
            
            # Apply grid settings using the boolean flags
            self.ax.grid(self.vertical_grid_enabled, axis='x')
            self.ax.grid(self.horizontal_grid_enabled, axis='y')
            self.ax.minorticks_on()
            if self.minor_vertical_grid_enabled:
                self.ax.grid(True, which='minor', axis='x', linewidth=0.5)
            else:
                self.ax.grid(False, which='minor', axis='x')
            if self.minor_horizontal_grid_enabled:
                self.ax.grid(True, which='minor', axis='y', linewidth=0.5)
            else:
                self.ax.grid(False, which='minor', axis='y')
            
            # Apply font size settings
            self.ax.xaxis.label.set_size(self.font_size)
            self.ax.yaxis.label.set_size(self.font_size)
            self.ax.title.set_size(self.title_font_size)
            
            for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
                label.set_size(self.tick_font_size)
            
            self.figure.tight_layout() # Apply tight_layout
            self.canvas.draw()

    def on_hover(self, event):
        if not self.hover_enabled or not self.data:
            return
        vis = self.annot.get_visible()
        if event.inaxes == self.ax:
            cont, ind = self.ax.lines[0].contains(event)
            if cont:
                self.update_annot(ind)
                self.annot.set_visible(True)
                self.canvas.draw_idle()
            else:
                if vis:
                    self.annot.set_visible(False)
                    self.canvas.draw_idle()

    def update_annot(self, ind):
        pos = self.ax.lines[0].get_xydata()[ind["ind"][0]]
        self.annot.xy = pos
        text = f"{pos[0]:.2f}, {pos[1]:.2f}"
        self.annot.set_text(text)
        self.annot.get_bbox_patch().set_alpha(0.4)

    def toggle_hover(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "Please load XRD data before enabling cursor.")
            self.toolbar.hover_action.setChecked(False)
            return
        self.hover_enabled = self.toolbar.hover_action.isChecked()

    # def convert_file(self):
    #     if not self.data:
    #         QMessageBox.warning(self, "No Data", "No data available to convert.")
    #         return
        
    #     for i, data in enumerate(self.data):
    #         try:
    #             file_name = os.path.splitext(self.fileNames[i])[0] + '_converted.txt'
    #             with open(file_name, 'w') as f:
    #                 for x, y in data:
    #                     f.write(f"{x:.6f}\t{y:.6f}\n")
    #             print(f"Converted {self.fileNames[i]} to {file_name}")
    #         except Exception as e:
    #             print(f"Error converting {self.fileNames[i]}: {e}")
    #             QMessageBox.warning(self, "Conversion Error", f"Error converting {self.fileNames[i]}: {e}")

    def confirm_clear_data(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "No loaded data to clear.")
            return
        else:
            reply = QMessageBox.question(self, 'Clear Data', 'Are you sure you want to clear all data?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.clear_data()

    def clear_data(self):
        self.data = []
        self.temperatures = []
        self.current_index = 0
        self.fileNames = []
        self.figure.clear()
        self.canvas.draw()
        self.listWidget.clear()
        self.hover_enabled = False
        self.toolbar.hover_action.setChecked(False)
        print("Data cleared")



    def toggle_list(self):
        if self.list_visible:
            self.layout.removeWidget(self.listWidget)
            self.listWidget.setVisible(False)
            self.layout.setColumnStretch(0, 10)  # Adjust the stretch factor for the plot to occupy the full width
        else:
            self.layout.addWidget(self.listWidget, 1, 9, 2, 1)  # Add the list widget back to the layout
            self.listWidget.setVisible(True)
            self.layout.setColumnStretch(0, 9)  # Set the stretch factor for the plot to 9
            self.layout.setColumnStretch(1, 1)  # Set the stretch factor for the list to 1
        self.list_visible = not self.list_visible

    def open_grid_dialog(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "Please load XRD data before toggling grid.")
            return
        dialog = GridDialog(self)
        dialog.set_initial_state(self.ax)
        if dialog.exec_():
            self.vertical_grid_enabled = dialog.vertical_grid_checkbox.isChecked()
            self.horizontal_grid_enabled = dialog.horizontal_grid_checkbox.isChecked()
            self.minor_vertical_grid_enabled = dialog.minor_vertical_grid_checkbox.isChecked()
            self.minor_horizontal_grid_enabled = dialog.minor_horizontal_grid_checkbox.isChecked()
            
            self.ax.grid(self.vertical_grid_enabled, axis='x')
            self.ax.grid(self.horizontal_grid_enabled, axis='y')
            self.ax.minorticks_on()
            if self.minor_vertical_grid_enabled:
                self.ax.grid(True, which='minor', axis='x', linewidth=0.5)
            else:
                self.ax.grid(False, which='minor', axis='x')
            if self.minor_horizontal_grid_enabled:
                self.ax.grid(True, which='minor', axis='y', linewidth=0.5)
            else:
                self.ax.grid(False, which='minor', axis='y')
            self.canvas.draw()

    def open_ticks_dialog(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "Please load XRD data before setting ticks.")
            return
        dialog = TicksDialog(self)
        if dialog.exec_():
            xticks_spacing = dialog.xticks_input.text()
            yticks_spacing = dialog.yticks_input.text()
            if xticks_spacing:
                xticks_spacing = float(xticks_spacing)
                self.ax.set_xticks(np.arange(self.ax.get_xlim()[0], self.ax.get_xlim()[1], xticks_spacing))
            if yticks_spacing:
                yticks_spacing = float(yticks_spacing)
                self.ax.set_yticks(np.arange(self.ax.get_ylim()[0], self.ax.get_ylim()[1], yticks_spacing))
            self.canvas.draw()
    
    def reset_ticks(self):
        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()
        self.plot_data()  # Call plot_data to redraw the plot with default tick settings

    def open_font_size_dialog(self):
        if not self.data:
            QMessageBox.warning(self, "No Data", "Please load XRD data before setting font size.")
            return
        dialog = FontSizeDialog(self)
        dialog.set_initial_state(self.ax)
        if dialog.exec_():
            try:
                new_font_size = float(dialog.font_size_input.text())
                new_tick_font_size = float(dialog.tick_font_size_input.text())
                new_title_font_size = float(dialog.title_font_size_input.text())
                new_cursor_font_size = float(dialog.cursor_font_size_input.text())
                self.font_size = new_font_size
                self.tick_font_size = new_tick_font_size
                self.title_font_size = new_title_font_size
                self.cursor_font_size = new_cursor_font_size
                self.apply_font_size()
            except ValueError:
                QMessageBox.warning(self, "Invalid Input", "Please enter a valid number for font size.")
    
    def reset_font_sizes(self):
        self.font_size = 10  # Default font size for axis labels
        self.tick_font_size = 10  # Default font size for tick labels
        self.title_font_size = 12  # Default font size for title
        self.cursor_font_size = 10  # Default font size for cursor annotation
        self.apply_font_size()
    
    def apply_font_size(self):
        self.ax.xaxis.label.set_size(self.font_size)
        self.ax.yaxis.label.set_size(self.font_size)
        self.ax.title.set_size(self.title_font_size)
        
        for label in self.ax.get_xticklabels() + self.ax.get_yticklabels():
            label.set_size(self.tick_font_size)
        
        if self.annot:
            self.annot.set_fontsize(self.cursor_font_size)
        
        self.canvas.draw()

    def on_listbox_select(self, index):
        if index >= 0:
            self.xlim = self.ax.get_xlim()
            self.ylim = self.ax.get_ylim()
            self.current_index = index
            self.plot_data()

    def show_info(self):
        info_text = (
            "Developed for: the Open University, School of Engineering and Innovation.\n\n"
            "Version: 1.3.0\n\n"
            "Developed by:\nIhor Sobianin\nJames Bowen\nMatthew Kershaw\n\n"
            "Contact: ihor.sobianin@open.ac.uk"
        )
        QMessageBox.information(self, "App Information", info_text)
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = XRDApp()
    ex.show()
    sys.exit(app.exec_())