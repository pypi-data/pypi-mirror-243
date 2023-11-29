from nap_plot_tools.cmap import make_cat10_mod_cmap, get_custom_cat10based_cmap_list
from qtpy.QtCore import Qt, QSize, QRect
from qtpy.QtGui import QColor, QPainter, QPixmap
from qtpy.QtWidgets import QSpinBox, QToolButton, QToolBar, QVBoxLayout, QWidget, QHBoxLayout, QSizePolicy

import numpy as np

class QtColorBox(QWidget):
    """A widget that shows a square with the current signal class color.
    """
    

    def __init__(self, first_color_transparent=True) -> None:
        super().__init__()
        # TODO: Check why this may be necessary
        # self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self._height = 24
        self.setFixedWidth(self._height)
        self.setFixedHeight(self._height)
        self.cmap = make_cat10_mod_cmap(first_color_transparent=first_color_transparent)
        self._value = 0
        self.color = np.round(
                255 * np.asarray(self.cmap(0))).astype(int)

    def paintEvent(self, event):
        """Paint the colorbox.  If no color, display a checkerboard pattern.

        Parameters
        ----------
        event : qtpy.QtCore.QEvent
            Event from the Qt context.
        """
        painter = QPainter(self)
        if self._value <= 0:
            self.color = np.round(
                255 * np.asarray(self.cmap(0))).astype(int)
            for i in range(self._height // 4):
                for j in range(self._height // 4):
                    if (i % 2 == 0 and j % 2 == 0) or (
                        i % 2 == 1 and j % 2 == 1
                    ):
                        painter.setPen(QColor(230, 230, 230))
                        painter.setBrush(QColor(230, 230, 230))
                    else:
                        painter.setPen(QColor(25, 25, 25))
                        painter.setBrush(QColor(25, 25, 25))
                    painter.drawRect(i * 4, j * 4, 5, 5)
        else:
            color = np.round(
                255 * np.asarray(self.cmap(self._value))).astype(int)
            painter.setPen(QColor(*list(color)))
            painter.setBrush(QColor(*list(color)))
            painter.drawRect(0, 0, self._height, self._height)
            self.color = tuple(color)

    def setToolTip(self, tooltip):
        super().setToolTip(tooltip)
    
    def setValue(self, value):
        self._value = value
        # Update colorbox
        self.update()

class QtColorSpinBox(QWidget):
    """QtColorSpinBox class.

    Custom widget to select a color and a value.
    """    
    def __init__(self, parent=None, first_color_transparent=True):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        # Colorbox
        self.colorBox = QtColorBox(first_color_transparent=first_color_transparent)
        # Spinbox
        self.spinBox = QSpinBox()
        self.spinBox.setMinimum(0)
        self.spinBox.setSingleStep(1)
        self.spinBox.setMaximumWidth(50)

        self.layout.addWidget(self.colorBox)
        self.layout.addWidget(self.spinBox)

        # Connect spinbox to color
        self.spinBox.valueChanged.connect(self.colorBox.setValue)

    @property
    def value(self):
        return self.spinBox.value()
    
    @value.setter
    def value(self, value):
        """Set the value of the spinbox and colorbox.

        Alternative syntax to setValue.

        Parameters
        ----------
        value : int
            New value.
        """        
        self.setValue(value)

    def setValue(self, value):
        """Set the value of the spinbox and colorbox.

        Syntax consistent with QSpinBox.

        Parameters
        ----------
        value : int
            New value.
        """        
        self.spinBox.setValue(value)
        # updates color in colorbox
        self.colorBox.setValue(value)
    
    def get_color(self, norm=True):
        """Get the color of the colorbox.

        Parameters
        ----------
        norm : bool, optional
            If True, color is normalized to [0, 1], by default True.

        Returns
        -------
        tuple
            Color tuple.
        """
        if norm:
            return tuple([c / 255 for c in self.colorBox.color])     
        return self.colorBox.color

    def connect(self, callback):
        self.spinBox.valueChanged.connect(callback)

    def setToolTip(self, tooltip):
        self.spinBox.setToolTip(tooltip)
        self.colorBox.setToolTip(tooltip)

    def setMinimum(self, value):
        self.spinBox.setMinimum(value)

    def setMaximum(self, value):
        self.spinBox.setMaximum(value)

    def setSingleStep(self, value):
        self.spinBox.setSingleStep(value)

class CustomToolButton(QToolButton):
    """CustomToolButton class.

    Custom tool button to add custom icons.

    If buttons are checkable, they will display a different icon when checked.

    Parameters
    ----------
    default_icon_path: str
        Path to the default icon.
    checked_icon_path: str, optional
        Path to the icon when the button is checked. If None, the default icon is used.
    """    
    _default_icon_size = 100 # px
    _additional_icon_size = 4 # px
    def __init__(self, default_icon_path, checked_icon_path=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default_icon_path = default_icon_path
        self._checked_icon_path = checked_icon_path or default_icon_path
        self.setCheckable(checked_icon_path is not None)
        self.is_connected = False
        # Set margins and padding to 0 to avoid extra space around the icon
        self.setStyleSheet("QToolButton { margin: 0px; padding: 0px; }")
        # Set fixed size based on icon size
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def setChecked(self, state):
        """Override setChecked to update the button's appearance when its state changes.

        Parameters
        ----------
        state : bool
            Button state.
        """        
        super().setChecked(state)
        self.update()  # Update the button's appearance when its state changes

    def setIconSize(self, size):
        """Override setIconSize to update the button's size when its icon size changes.

        It should called after adding the button to the toolbar.

        Parameters
        ----------
        size : int or QSize
            Icon size.
        """        
        if isinstance(size, QSize):
            self._icon_size = size
        else:
            self._icon_size = QSize(size, size)
        self.setFixedSize(self._icon_size.width() + self._additional_icon_size, self._icon_size.height() + self._additional_icon_size)
        self.update()

    def paintEvent(self, event):
        """Override paintEvent to draw the button's icon with the desired size.

        Parameters
        ----------
        event : qtpy.QtCore.QEvent
            Event from the Qt context.
        """        
        painter = QPainter(self)
        # Choose the correct pixmap based on the button's checked state
        pixmap = QPixmap(self._checked_icon_path if self.isChecked() else self._default_icon_path)
        scaled_pixmap = pixmap.scaled(self._icon_size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        rect = QRect(0, 0, self._icon_size.width(), self._icon_size.height())
        rect.moveCenter(self.rect().center())
        painter.drawPixmap(rect.topLeft(), scaled_pixmap)
        painter.end()

    def toggle(self):
        """Override toggle to update the button display.
        """        
        super().toggle()
        self.update()

class CustomToolbarWidget(QWidget):
    """CustomToolbarWidget class.

    Custom toolbar widget to add custom buttons.

    Parameters
    ----------
    parent : QWidget, optional
        Parent widget, by default None.
    """     
    _icon_size = 32
    _button_margin = 2
    _additional_toolbar_height = 8
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        # Set layout with minimum margins and spacing
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        # Add QToolBar to layout
        self.toolbar = QToolBar()
        self.layout.addWidget(self.toolbar)
        # Set toolbar with minimum margins and spacing
        self.toolbar.layout().setContentsMargins(0, 0, 0, 0)
        self.toolbar.layout().setSpacing(0)
        self.update_toolbar_height()
        # Dictionary to store buttons
        self.buttons = {}

    def add_custom_button(self, name, default_icon_path, tooltip='', callback=None, checkable=False, checked_icon_path=None):
        """Add custom button to toolbar.

        Parameters
        ----------
        name : str
            Button name.
        tooltip : str
            Button tooltip.
        default_icon_path : str
            Path to the default icon.
        callback : function or method
            Callback function or method.
        checkable : bool, optional
            If True, button is checkable, by default False
        checked_icon_path : str, optional
            Path to the icon when the button is checked. If None, the default icon is used, by default None.
        """
        # Convert paths to strings
        if not isinstance(default_icon_path, str):
            default_icon_path = str(default_icon_path)
        if checked_icon_path is not None and not isinstance(checked_icon_path, str):
            checked_icon_path = str(checked_icon_path)
        # Creates custom toolbutton
        button = CustomToolButton(default_icon_path, checked_icon_path)
        button.setIconSize(self._icon_size)
        button.setText(name)
        button.setToolTip(tooltip)
        # Add button to toolbar
        self.toolbar.addWidget(button)
        # Store button in dictionary
        self.buttons[name] = button
        # Connect button callback
        self.connect_button_callback(name, callback)
        # Adjust toolbar dimensions after adding the button
        self.update_toolbar_minimum_width()
        self.update_toolbar_height()

    def connect_button_callback(self, name, callback):
        """Sets or updates the callback for a specific button.

        Parameters:
        name: str
            The name of the button.
        callback: function
            The new callback function to set.
        """
        if name in self.buttons:
            button = self.buttons[name]
            checkable = button.isCheckable()

            # Safely disconnect existing connections
            try:
                if checkable:
                    button.toggled.disconnect()
                else:
                    button.clicked.disconnect()
            except TypeError:
                # No connections to disconnect
                pass

            # Connect the new callback
            if callback:
                if checkable:
                    button.toggled.connect(callback)
                else:
                    button.clicked.connect(lambda: callback())

    
    def update_toolbar_minimum_width(self):
        total_width = 0
        for name, button in self.buttons.items():
            total_width += button.width() + self._button_margin
        # Set the minimum width of the toolbar
        self.toolbar.setMinimumWidth(total_width)

    def update_toolbar_height(self):
        # Calculate and set the height of the toolbar based on the icon size
        calculated_height = self._icon_size + self._additional_toolbar_height
        self.toolbar.setFixedHeight(calculated_height)

    def get_button_state(self, name):
        """Get the checked state of the button.

        Parameters
        ----------
        name : str
            Button name.

        Returns
        -------
        bool or None
            Button checked state.
        """        
        # Return the checked state of the button
        return self.buttons[name].isChecked() if name in self.buttons else None

    def set_button_state(self, name, state):
        """Set the checked state of the button.

        Parameters
        ----------
        name : str
            Button name.
        state : bool
            Button checked state.
        """        
        # Set the checked state of the button
        if name in self.buttons and self.buttons[name].isCheckable():
            self.buttons[name].setChecked(state)