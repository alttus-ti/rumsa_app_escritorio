from PySide6.QtCore import QDate, QEvent, QObject, Qt
from PySide6.QtWidgets import QCalendarWidget, QDialog, QVBoxLayout


class DatePicker(QObject):
    """Abre un calendario al pulsar un campo de fecha de solo lectura."""

    def __init__(self, field, window, title):
        super().__init__(field)
        self.field = field
        self.window = window
        self.title = title
        field.setReadOnly(True)
        field.viewport().setCursor(Qt.CursorShape.PointingHandCursor)
        field.viewport().installEventFilter(self)

    def eventFilter(self, watched, event):
        if (event.type() == QEvent.Type.MouseButtonPress
                and event.button() == Qt.MouseButton.LeftButton):
            self.open_calendar()
            return True
        return super().eventFilter(watched, event)

    def open_calendar(self):
        dialog = QDialog(self.window)
        dialog.setWindowTitle(self.title)
        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)
        calendar = QCalendarWidget(dialog)
        layout.addWidget(calendar)
        current = QDate.fromString(self.field.toPlainText().strip(), "dd-MM-yyyy")
        if current.isValid():
            calendar.setSelectedDate(current)

        def select_date(date):
            self.field.setPlainText(date.toString("dd-MM-yyyy"))
            dialog.accept()

        calendar.clicked.connect(select_date)
        dialog.exec()
