"""
StoryCodeWizard UI Styles
アプリケーション全体で使用するスタイル定義
"""
import customtkinter as ctk


class AppStyles:
    """アプリケーション共通スタイル定義クラス"""
    
    # カラーパレット
    COLORS = {
        'primary': '#1f538d',
        'primary_dark': '#14375e',
        'secondary': '#2fa572',
        'secondary_dark': '#1d694a',
        'accent': '#4a9eff',
        'background': '#212121',
        'surface': '#2b2b2b',
        'surface_light': '#383838',
        'sidebar': '#2d2d2d',  # VS Code風サイドバー
        'sidebar_hover': '#404040',  # サイドバーホバー状態
        'sidebar_active': '#1f538d',  # サイドバーアクティブ状態
        'text': '#ffffff',
        'text_secondary': '#b0b0b0',
        'text_sidebar': '#cccccc',  # サイドバーテキスト
        'border': '#404040',
        'error': '#f44336',
        'warning': '#ff9800',
        'success': '#4caf50',
    }
    
    # フォント設定
    FONTS = {
        'default': ('Helvetica', 13),
        'heading': ('Helvetica', 16, 'bold'),
        'subheading': ('Helvetica', 14, 'bold'),
        'small': ('Helvetica', 11),
        'code': ('Courier New', 12),
        'sidebar_icon': ('Arial', 20),  # サイドバーアイコン用
    }
    
    # 共通サイズ（レイアウト間隔を改善）
    SIZES = {
        'padding_small': 8,
        'padding_medium': 16,
        'padding_large': 24,
        'padding_extra_large': 32,
        'button_height': 36,
        'input_height': 40,
        'corner_radius': 8,
        'border_width': 1,
        'label_spacing': 4,  # ラベルと入力フィールド間の間隔
        'section_spacing': 20,  # セクション間の間隔
        'sidebar_width': 70,  # サイドバー幅
        'sidebar_button_size': 50,  # サイドバーボタンサイズ
    }
    
    @classmethod
    def initialize(cls):
        """CustomTkinterのデフォルト設定を適用"""
        # カスタムカラーテーマを設定
        ctk.set_default_color_theme("blue")
        
    @classmethod
    def get_button_style(cls, variant='primary'):
        """ボタンスタイルを取得"""
        styles = {
            'primary': {
                'fg_color': cls.COLORS['primary'],
                'hover_color': cls.COLORS['primary_dark'],
                'text_color': cls.COLORS['text'],
                'corner_radius': cls.SIZES['corner_radius'],
                'font': cls.FONTS['default']
            },
            'secondary': {
                'fg_color': cls.COLORS['secondary'],
                'hover_color': cls.COLORS['secondary_dark'],
                'text_color': cls.COLORS['text'],
                'corner_radius': cls.SIZES['corner_radius'],
                'font': cls.FONTS['default']
            },
            'outline': {
                'fg_color': 'transparent',
                'border_color': cls.COLORS['border'],
                'text_color': cls.COLORS['text'],
                'hover_color': cls.COLORS['surface_light'],
                'corner_radius': cls.SIZES['corner_radius'],
                'border_width': cls.SIZES['border_width'],
                'font': cls.FONTS['default']
            },
            'sidebar': {
                'fg_color': 'transparent',
                'hover_color': cls.COLORS['sidebar_hover'],
                'text_color': cls.COLORS['text_sidebar'],
                'corner_radius': cls.SIZES['corner_radius'],
                'font': cls.FONTS['sidebar_icon'],
                'width': cls.SIZES['sidebar_button_size'],
                'height': cls.SIZES['sidebar_button_size']
            }
        }
        return styles.get(variant, styles['primary'])
    
    @classmethod
    def get_entry_style(cls):
        """入力フィールドスタイルを取得"""
        return {
            'corner_radius': cls.SIZES['corner_radius'],
            'height': cls.SIZES['input_height'],
            'font': cls.FONTS['default'],
            'border_width': cls.SIZES['border_width']
        }
    
    @classmethod
    def get_frame_style(cls, variant='default'):
        """フレームスタイルを取得"""
        styles = {
            'default': {
                'corner_radius': cls.SIZES['corner_radius'],
                'fg_color': cls.COLORS['surface']
            },
            'card': {
                'corner_radius': cls.SIZES['corner_radius'],
                'fg_color': cls.COLORS['surface_light'],
                'border_width': 1,
                'border_color': cls.COLORS['border']
            },
            'sidebar': {
                'corner_radius': 0,
                'fg_color': cls.COLORS['sidebar'],
                'border_width': 0
            }
        }
        return styles.get(variant, styles['default'])
    
    @classmethod
    def get_scrollable_frame_style(cls):
        """スクロール可能フレームスタイルを取得"""
        return {
            'corner_radius': cls.SIZES['corner_radius'],
            'fg_color': cls.COLORS['surface']
        }
    
    @classmethod
    def get_sidebar_style(cls):
        """サイドバー専用スタイルを取得"""
        return {
            'frame': cls.get_frame_style('sidebar'),
            'button': cls.get_button_style('sidebar'),
            'colors': {
                'background': cls.COLORS['sidebar'],
                'hover': cls.COLORS['sidebar_hover'],
                'active': cls.COLORS['sidebar_active'],
                'text': cls.COLORS['text_sidebar']
            }
        }
    
    @classmethod
    def get_label_spacing(cls):
        """ラベルと入力フィールド間の適切な間隔を取得"""
        return cls.SIZES['label_spacing']
    
    @classmethod
    def get_section_spacing(cls):
        """セクション間の適切な間隔を取得"""
        return cls.SIZES['section_spacing']