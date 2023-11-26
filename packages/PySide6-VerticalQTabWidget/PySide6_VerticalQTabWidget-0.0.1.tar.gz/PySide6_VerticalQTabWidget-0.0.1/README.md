# pySide6-vertical-tab-widget
PySide6 vertical tab widget

## Requirements
PySide6 >= 6.4

## Setup
`python -m pip install PySide6_VerticalQTabWidget`

## Usage
```python
from PySide6.QtWidgets import QWidget
from PySide6_VerticalQTabWidget import VerticalQTabWidget

vertical_tab_widget = VerticalQTabWidget()
widget1 = QWidget()
widget2 = QWidget()
vertical_tab_widget.addTab(widget1, "First Tab")
vertical_tab_widget.addTab(widget2, "Second Tab")
```


