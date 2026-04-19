from PySide6.QtWidgets import QHBoxLayout, QWidget, QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt
from src.consts import assets as assets_const
from src.consts.enums import Sizes
from src.gui.components.image import ImageWidget
from src.models.messages.satanic_zone import SzInfo
from src.utils import assets

display_width = {
    Sizes.Small: 200,
    Sizes.Medium: 240,
    Sizes.Large: 280
}

class SatanicZoneGroupBox(QFrame):
    def __init__(self, size: Sizes = Sizes.Large, show_positive: bool = True):
        super().__init__()
        
        self.show_positive = show_positive
        self.buff_items = []
        
        if show_positive:
            border_color = "rgb(100, 200, 100)"
            title_color = "rgb(100, 255, 100)"
            title_text = "✨ Satanic Buffs ✨"
        else:
            border_color = "rgb(200, 100, 100)"
            title_color = "rgb(255, 100, 100)"
            title_text = "⚠️ Satanic Debuffs ⚠️"
        
        self.setStyleSheet(f"""
            QFrame#GroupBox {{
                background-color: rgba(0, 0, 0, 0.85);
                border: 2px solid {border_color};
                border-radius: 6px;
            }}
            QToolTip {{
                background-color: black;
                color: white;
                border: 1px solid {border_color};
                padding: 6px;
                font-size: 10px;
                border-radius: 4px;
            }}
        """)
        
        self.setObjectName("GroupBox")
        self.setMinimumWidth(display_width[size])
        self.setMinimumHeight(180)
        
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(3)
        main_layout.setContentsMargins(6, 6, 6, 6)
        
        title_label = QLabel(title_text)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {title_color}; font-weight: bold; font-size: 11px; padding: 2px;")
        main_layout.addWidget(title_label)
        
        self.items_container = QWidget()
        self.items_layout = QVBoxLayout(self.items_container)
        self.items_layout.setSpacing(4)
        self.items_layout.setContentsMargins(0, 2, 0, 2)
        
        icon_size = 20
        
        for i in range(3):
            buff_container = QWidget()
            buff_layout = QHBoxLayout(buff_container)
            buff_layout.setSpacing(6)
            buff_layout.setContentsMargins(4, 3, 4, 3)
            
            icon = ImageWidget(assets.icon(assets_const.IcBuffDefault))
            icon.setFixedSize(icon_size, icon_size)
            icon.setStyleSheet("background-color: rgba(0, 0, 0, 0.3); border-radius: 3px;")
            
            text_label = QLabel("No effect")
            text_label.setWordWrap(True)
            text_label.setStyleSheet("color: #cccccc; font-size: 10px; font-weight: bold; line-height: 1.3;")
            
            buff_layout.addWidget(icon, alignment=Qt.AlignVCenter)
            buff_layout.addWidget(text_label, 1)
            
            self.items_layout.addWidget(buff_container)
            self.buff_items.append({
                'container': buff_container,
                'icon': icon,
                'text': text_label
            })
        
        main_layout.addWidget(self.items_container)
        
        self.empty_label = QLabel("No active effects" if show_positive else "No active curses")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet("color: gray; font-style: italic; padding: 10px; font-size: 9px;")
        self.empty_label.setVisible(False)
        main_layout.addWidget(self.empty_label)

    def set_buffs(self, buffs_list):
        for item in self.buff_items:
            item['icon'].setIcon(assets.icon(assets_const.IcBuffDefault))
            item['text'].setText("No effect")
            item['container'].setStyleSheet("background-color: transparent;")
        
        if not buffs_list:
            self.empty_label.setVisible(True)
            self.items_container.setVisible(False)
            return
        
        self.empty_label.setVisible(False)
        self.items_container.setVisible(True)
        
        for i, buff in enumerate(buffs_list[:3]):
            if i < len(self.buff_items):
                item = self.buff_items[i]
                item['icon'].setIcon(buff.buff_icon)
                
                color = "#64ff64" if self.show_positive else "#ff6464"
                prefix = "✨" if self.show_positive else "⚠️"
                bg_alpha = "rgba(100, 255, 100, 0.1)" if self.show_positive else "rgba(255, 100, 100, 0.1)"
                
                desc = buff.buff_description if buff.buff_description else "No description"
                # Aumentar limite de caracteres para mostrar mais descrição
                if len(desc) > 80: 
                    desc = desc[:77] + "..."
                
                # Aumentar fonte da descrição
                text = f"<b style='color:{color}; font-size:10px;'>{prefix} {buff.buff_name}</b><br><span style='color:#aaaaaa; font-size:9px; line-height:1.3;'>{desc}</span>"
                item['text'].setText(text)
                
                item['container'].setStyleSheet(f"""
                    QWidget {{
                        background-color: {bg_alpha};
                        border-radius: 4px;
                        border: 1px solid {color.replace('#', 'rgba(').replace('64', '100')}, 0.2);
                    }}
                """)
                
                tooltip = f"<div style='min-width: 200px;'><b style='color:{color}; font-size:11px;'>{buff.buff_name}</b><br><span style='font-size:10px;'>{buff.buff_description}</span></div>"
                item['icon'].setToolTip(tooltip)
                item['text'].setToolTip(tooltip)


class SatanicZoneDisplay(QWidget):
    def __init__(self, size: Sizes = Sizes.Large):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setSpacing(6)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.zone_name_frame = QFrame()
        self.zone_name_frame.setStyleSheet("background-color: rgba(150, 37, 56, 0.3); border-radius: 4px;")
        zone_name_layout = QHBoxLayout(self.zone_name_frame)
        zone_name_layout.setContentsMargins(4, 2, 4, 2)
        self.zone_name_label = QLabel("No Satanic Zone Active")
        self.zone_name_label.setStyleSheet("color: rgb(255, 200, 100); font-weight: bold; font-size: 11px;")
        zone_name_layout.addWidget(self.zone_name_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.zone_name_frame)
        
        effects_layout = QHBoxLayout()
        effects_layout.setSpacing(8)
        effects_layout.setContentsMargins(0, 0, 0, 0)
        self.buffs_box = SatanicZoneGroupBox(size=size, show_positive=True)
        self.debuffs_box = SatanicZoneGroupBox(size=size, show_positive=False)
        effects_layout.addWidget(self.buffs_box)
        effects_layout.addWidget(self.debuffs_box)
        layout.addLayout(effects_layout)

    def set_satanic_zone_info(self, sz_info: SzInfo):
        if not sz_info:
            self.zone_name_label.setText("No Satanic Zone Active")
            self.buffs_box.set_buffs([])
            self.debuffs_box.set_buffs([])
            return
        
        self.zone_name_label.setText(f"🌙 {sz_info.satanic_zone} 🌙" if sz_info.satanic_zone else "Unknown Zone")
        self.buffs_box.set_buffs(sz_info.positive_buffs if hasattr(sz_info, 'positive_buffs') else [])
        self.debuffs_box.set_buffs(sz_info.negative_buffs if hasattr(sz_info, 'negative_buffs') else [])