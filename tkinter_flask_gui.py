import tkinter as tk
from tkinter import ttk, messagebox, font
from tkcalendar import DateEntry
from datetime import date, datetime
import requests
import json
import threading
import time
import math

class HospitalFlaskGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏥 MedFlow Pro - Advanced Hospital Management System")
        self.root.geometry("1600x1000")
        self.root.state('zoomed')  # Maximize window on Windows
        self.root.configure(bg='#0a0e27')  # Deep space blue
        
        # Perfect color scheme - Medical Professional Theme
        self.colors = {
            'primary': '#1e3a8a',      # Medical blue
            'secondary': '#1e40af',    # Bright blue  
            'accent': '#dc2626',       # Medical red
            'success': '#059669',      # Medical green
            'warning': '#d97706',      # Amber warning
            'info': '#0284c7',        # Sky blue
            'light': '#f8fafc',       # Pure light
            'dark': '#0a0e27',        # Deep space
            'card_bg': '#ffffff',     # Pure white
            'card_hover': '#f1f5f9',  # Light hover
            'text_primary': '#1e293b', # Slate dark
            'text_secondary': '#64748b', # Slate medium
            'text_light': '#ffffff',   # Pure white
            'border': '#e2e8f0',      # Light border
            'shadow': '#00000010',     # Subtle shadow
            'gradient_start': '#1e3a8a',
            'gradient_end': '#3b82f6'
        }
        
        # Perfect typography
        self.fonts = {
            'title': ('Segoe UI', 28, 'bold'),
            'subtitle': ('Segoe UI', 14),
            'heading': ('Segoe UI', 18, 'bold'),
            'subheading': ('Segoe UI', 14, 'bold'),
            'body': ('Segoe UI', 11),
            'button': ('Segoe UI', 12, 'bold'),
            'small': ('Segoe UI', 9),
            'metric': ('Segoe UI', 32, 'bold'),
            'icon': ('Segoe UI Emoji', 24)
        }
        
        # Animation variables
        self.animation_speed = 10
        self.hover_effects = {}
        
        # API base URL
        self.api_base = "http://localhost:5000/api"
        
        # Configure perfect styling
        self.configure_perfect_styles()
        
        # Test API connection
        self.test_api_connection()
        
        # Create perfect GUI
        self.create_perfect_widgets()
        
    def test_api_connection(self):
        """Test Flask API connection"""
        try:
            response = requests.get(f"{self.api_base}/test", timeout=5)
            if response.status_code == 200:
                print("✅ Flask API connection successful!")
                messagebox.showinfo("Success", "✅ Connected to Flask API successfully!")
            else:
                raise Exception("API not responding")
        except Exception as e:
            print(f"❌ Flask API connection failed: {e}")
            messagebox.showerror("API Error", 
                               f"❌ Cannot connect to Flask API!\n\n"
                               f"Please ensure Flask server is running:\n"
                               f"python flask_app.py\n\n"
                               f"Error: {e}")
            return False
        return True
    
    def configure_perfect_styles(self):
        """Configure perfect professional TTK styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Perfect notebook styling
        style.configure('Perfect.TNotebook', 
                       background=self.colors['dark'],
                       borderwidth=0,
                       tabmargins=[0, 0, 0, 0])
        
        style.configure('Perfect.TNotebook.Tab', 
                       background=self.colors['secondary'],
                       foreground=self.colors['text_light'],
                       padding=[25, 15],
                       font=self.fonts['button'],
                       borderwidth=0,
                       focuscolor='none')
        
        style.map('Perfect.TNotebook.Tab',
                 background=[('selected', self.colors['primary']),
                           ('active', self.colors['info']),
                           ('!active', self.colors['secondary'])],
                 foreground=[('selected', self.colors['text_light']),
                           ('active', self.colors['text_light'])])
        
        # Perfect treeview styling
        style.configure('Perfect.Treeview',
                       background=self.colors['card_bg'],
                       foreground=self.colors['text_primary'],
                       fieldbackground=self.colors['card_bg'],
                       font=self.fonts['body'],
                       borderwidth=0,
                       relief='flat',
                       rowheight=35)
        
        style.configure('Perfect.Treeview.Heading',
                       background=self.colors['primary'],
                       foreground=self.colors['text_light'],
                       font=self.fonts['subheading'],
                       borderwidth=0,
                       relief='flat')
        
        style.map('Perfect.Treeview',
                 background=[('selected', self.colors['info']),
                           ('focus', self.colors['card_hover'])])
        
        # Perfect combobox styling
        style.configure('Perfect.TCombobox',
                       fieldbackground=self.colors['card_bg'],
                       background=self.colors['card_bg'],
                       borderwidth=2,
                       relief='solid',
                       bordercolor=self.colors['border'],
                       font=self.fonts['body'])
        
        style.map('Perfect.TCombobox',
                 bordercolor=[('focus', self.colors['primary']),
                            ('active', self.colors['info'])])
    
    def create_hover_effect(self, widget, enter_color, leave_color):
        """Create smooth hover effects for widgets"""
        def on_enter(event):
            widget.configure(bg=enter_color)
        
        def on_leave(event):
            widget.configure(bg=leave_color)
        
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)
    
    def create_perfect_button(self, parent, text, command, bg_color, hover_color=None, **kwargs):
        """Create a perfect modern button with hover effects"""
        if hover_color is None:
            # Darken the color for hover effect
            hover_color = self.darken_color(bg_color, 0.1)
        
        button = tk.Button(parent, 
                          text=text,
                          command=command,
                          bg=bg_color,
                          fg=self.colors['text_light'],
                          font=self.fonts['button'],
                          relief='flat',
                          bd=0,
                          cursor='hand2',
                          padx=25,
                          pady=12,
                          **kwargs)
        
        self.create_hover_effect(button, hover_color, bg_color)
        return button
    
    def darken_color(self, color, factor):
        """Darken a hex color by a factor"""
        if color.startswith('#'):
            color = color[1:]
        
        rgb = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(int(c * (1 - factor)) for c in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def create_gradient_frame(self, parent, width, height, color1, color2):
        """Create a gradient background frame"""
        canvas = tk.Canvas(parent, width=width, height=height, highlightthickness=0)
        
        # Create gradient effect
        for i in range(height):
            ratio = i / height
            r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
            r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
            
            r = int(r1 + (r2 - r1) * ratio)
            g = int(g1 + (g2 - g1) * ratio)
            b = int(b1 + (b2 - b1) * ratio)
            
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color)
        
        return canvas
    
    def create_perfect_metric_card(self, parent, icon, title, value, color, row, col):
        """Create a perfect metric card with advanced styling"""
        # Main card container with shadow effect
        card_container = tk.Frame(parent, bg=self.colors['light'])
        card_container.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        
        # Card with rounded corners effect (simulated with borders)
        card = tk.Frame(card_container, bg=color, relief='flat', bd=0)
        card.pack(fill='both', expand=True, padx=3, pady=3)
        
        # Card content with perfect spacing
        content = tk.Frame(card, bg=color)
        content.pack(fill='both', expand=True, padx=30, pady=25)
        
        # Icon with perfect positioning
        icon_label = tk.Label(content, text=icon, 
                             font=self.fonts['icon'], 
                             bg=color, fg='white')
        icon_label.pack(pady=(0, 10))
        
        # Metric value with perfect typography
        metric_label = tk.Label(content, text=value, 
                               font=self.fonts['metric'], 
                               bg=color, fg='white')
        metric_label.pack()
        
        # Title with perfect spacing
        title_label = tk.Label(content, text=title, 
                              font=self.fonts['subheading'], 
                              bg=color, fg='white')
        title_label.pack(pady=(8, 0))
        
        # Add subtle hover effect
        hover_color = self.darken_color(color, 0.1)
        self.create_hover_effect(card, hover_color, color)
        
        return {
            'card': card,
            'metric_label': metric_label,
            'title_label': title_label,
            'icon_label': icon_label
        }
    
    def create_perfect_form_field(self, parent, label_text, row, col):
        """Create a perfect form field label"""
        label = tk.Label(parent, text=label_text, 
                        font=self.fonts['subheading'], 
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_primary'])
        label.grid(row=row, column=col, sticky='w', pady=15, padx=15)
        return label
    
    def create_perfect_entry(self, parent, row, col, width=25):
        """Create a perfect entry widget with enhanced styling"""
        entry = tk.Entry(parent, width=width, 
                        font=self.fonts['body'],
                        relief='solid', 
                        bd=2,
                        highlightthickness=0,
                        borderwidth=2,
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_primary'])
        entry.grid(row=row, column=col, padx=15, pady=15, sticky='ew')
        
        # Add focus effects
        def on_focus_in(event):
            entry.configure(relief='solid', bd=2)
        
        def on_focus_out(event):
            entry.configure(relief='solid', bd=1)
        
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)
        
        return entry
    
    def create_perfect_sort_category(self, parent, title, options, column):
        """Create a perfect sorting category with options"""
        category_frame = tk.Frame(parent, bg=self.colors['light'], relief='flat', bd=0)
        category_frame.grid(row=0, column=column, padx=15, pady=15, sticky='nsew')
        
        # Category header
        header_frame = tk.Frame(category_frame, bg=self.colors['primary'], relief='flat', bd=0)
        header_frame.pack(fill='x')
        
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill='x', padx=20, pady=15)
        
        tk.Label(header_content, text=title, 
                font=self.fonts['subheading'], 
                bg=self.colors['primary'], 
                fg=self.colors['text_light']).pack()
        
        # Options container
        options_frame = tk.Frame(category_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        options_frame.pack(fill='both', expand=True)
        
        options_content = tk.Frame(options_frame, bg=self.colors['card_bg'])
        options_content.pack(fill='x', padx=20, pady=20)
        
        # Create option buttons
        for option in options:
            btn = self.create_perfect_button(
                options_content, option['text'], 
                option['command'], option['color']
            )
            btn.configure(font=self.fonts['body'], padx=20, pady=8)
            btn.pack(fill='x', pady=5)
    
    def get_date_sort_options(self):
        """Get date sorting options"""
        return [
            {
                'text': '📅 Medical Records - Latest First',
                'command': lambda: self.quick_sort_by_criteria('records', 'visit_date', 'desc'),
                'color': self.colors['success']
            },
            {
                'text': '📅 Medical Records - Oldest First',
                'command': lambda: self.quick_sort_by_criteria('records', 'visit_date', 'asc'),
                'color': self.colors['info']
            },
            {
                'text': '📅 Appointments - Upcoming',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_date', 'desc'),
                'color': self.colors['accent']
            },
            {
                'text': '📅 Appointments - Past',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_date', 'asc'),
                'color': self.colors['warning']
            },
            {
                'text': '📅 Patients - Youngest',
                'command': lambda: self.quick_sort_by_criteria('patients', 'date_of_birth', 'desc'),
                'color': self.colors['primary']
            },
            {
                'text': '📅 Patients - Oldest',
                'command': lambda: self.quick_sort_by_criteria('patients', 'date_of_birth', 'asc'),
                'color': self.colors['secondary']
            }
        ]
    
    def get_name_sort_options(self):
        """Get name sorting options"""
        return [
            {
                'text': '👤 Patients - First Name A→Z',
                'command': lambda: self.quick_sort_by_criteria('patients', 'first_name', 'asc'),
                'color': self.colors['success']
            },
            {
                'text': '👤 Patients - First Name Z→A',
                'command': lambda: self.quick_sort_by_criteria('patients', 'first_name', 'desc'),
                'color': self.colors['info']
            },
            {
                'text': '👤 Patients - Last Name A→Z',
                'command': lambda: self.quick_sort_by_criteria('patients', 'last_name', 'asc'),
                'color': self.colors['accent']
            },
            {
                'text': '👤 Patients - Last Name Z→A',
                'command': lambda: self.quick_sort_by_criteria('patients', 'last_name', 'desc'),
                'color': self.colors['warning']
            },
            {
                'text': '🏥 Records - Diagnosis A→Z',
                'command': lambda: self.quick_sort_by_criteria('records', 'diagnosis', 'asc'),
                'color': self.colors['primary']
            },
            {
                'text': '🩺 Records - Specialization A→Z',
                'command': lambda: self.quick_sort_by_criteria('records', 'specialization', 'asc'),
                'color': self.colors['secondary']
            }
        ]
    
    def get_id_sort_options(self):
        """Get ID sorting options"""
        return [
            {
                'text': '🔢 Patients - ID Ascending',
                'command': lambda: self.quick_sort_by_criteria('patients', 'patient_id', 'asc'),
                'color': self.colors['success']
            },
            {
                'text': '🔢 Patients - ID Descending',
                'command': lambda: self.quick_sort_by_criteria('patients', 'patient_id', 'desc'),
                'color': self.colors['info']
            },
            {
                'text': '📋 Records - ID Ascending',
                'command': lambda: self.quick_sort_by_criteria('records', 'record_id', 'asc'),
                'color': self.colors['accent']
            },
            {
                'text': '📋 Records - ID Descending',
                'command': lambda: self.quick_sort_by_criteria('records', 'record_id', 'desc'),
                'color': self.colors['warning']
            },
            {
                'text': '📅 Appointments - ID Ascending',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_id', 'asc'),
                'color': self.colors['primary']
            },
            {
                'text': '📅 Appointments - ID Descending',
                'command': lambda: self.quick_sort_by_criteria('appointments', 'appointment_id', 'desc'),
                'color': self.colors['secondary']
            }
        ]

    def api_request(self, endpoint, method='GET', data=None):
        """Make API request"""
        try:
            url = f"{self.api_base}/{endpoint}"
            
            if method == 'GET':
                response = requests.get(url, timeout=10)
            elif method == 'POST':
                response = requests.post(url, json=data, timeout=10)
            elif method == 'PUT':
                response = requests.put(url, json=data, timeout=10)
            else:
                raise Exception(f"Unsupported method: {method}")
            
            if response.status_code == 200:
                return response.json()
            else:
                error_data = response.json() if response.content else {'message': 'Unknown error'}
                raise Exception(error_data.get('message', 'API request failed'))
                
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {e}")
        except Exception as e:
            raise Exception(str(e))
    
    def create_perfect_widgets(self):
        """Create perfect professional GUI with advanced styling"""
        # Perfect gradient title bar
        title_frame = tk.Frame(self.root, height=120, bg=self.colors['primary'])
        title_frame.pack(fill='x')
        title_frame.pack_propagate(False)
        
        # Simplified perfect background (removing gradient for now)
        # gradient_canvas = self.create_gradient_frame(title_frame, 1600, 120, 
        #                                            self.colors['gradient_start'], 
        #                                            self.colors['gradient_end'])
        # gradient_canvas.pack(fill='both', expand=True)
        
        # Perfect title overlay
        title_overlay = tk.Frame(title_frame, bg=self.colors['primary'])
        title_overlay.place(relx=0.5, rely=0.5, anchor='center')
        
        # Main title with perfect typography
        main_title = tk.Label(title_overlay, 
                             text="🏥 MedFlow Pro", 
                             font=self.fonts['title'], 
                             fg=self.colors['text_light'], 
                             bg=self.colors['primary'])
        main_title.pack()
        
        # Subtitle with perfect spacing
        subtitle = tk.Label(title_overlay, 
                           text="Advanced Hospital Management System • Real-time Analytics • Professional Healthcare", 
                           font=self.fonts['subtitle'], 
                           fg='#e0e7ff', 
                           bg=self.colors['primary'])
        subtitle.pack(pady=(5, 0))
        
        # Perfect main container
        main_container = tk.Frame(self.root, bg=self.colors['light'])
        main_container.pack(fill='both', expand=True)
        
        # Perfect navigation bar
        nav_frame = tk.Frame(main_container, bg=self.colors['dark'], height=60)
        nav_frame.pack(fill='x')
        nav_frame.pack_propagate(False)
        
        # Perfect notebook with custom styling
        notebook_container = tk.Frame(main_container, bg=self.colors['light'])
        notebook_container.pack(fill='both', expand=True, padx=0, pady=0)
        
        self.notebook = ttk.Notebook(notebook_container, style='Perfect.TNotebook')
        self.notebook.pack(fill='both', expand=True)
        
        # Create perfect tabs
        self.create_perfect_dashboard_tab()
        self.create_perfect_patients_tab()
        # Simplified tabs for now
        self.create_appointments_tab()
        self.create_medical_records_tab()
        self.create_data_sorting_tab()
        
        # Perfect status bar with indicators
        status_frame = tk.Frame(self.root, bg=self.colors['primary'], height=40)
        status_frame.pack(side='bottom', fill='x')
        status_frame.pack_propagate(False)
        
        # Status content
        status_content = tk.Frame(status_frame, bg=self.colors['primary'])
        status_content.pack(fill='both', expand=True, padx=20, pady=8)
        
        # Connection indicator
        connection_frame = tk.Frame(status_content, bg=self.colors['primary'])
        connection_frame.pack(side='left')
        
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 System Online")
        
        status_indicator = tk.Label(connection_frame, 
                                   textvariable=self.status_var,
                                   font=self.fonts['subheading'],
                                   fg=self.colors['text_light'], 
                                   bg=self.colors['primary'])
        status_indicator.pack(side='left')
        
        # System info
        system_info = tk.Label(status_content, 
                              text="Flask API Connected • Database Active • Real-time Sync",
                              font=self.fonts['small'],
                              fg='#bfdbfe', 
                              bg=self.colors['primary'])
        system_info.pack(side='right')
    
    def create_perfect_dashboard_tab(self):
        """Create perfect dashboard with advanced analytics"""
        dashboard_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(dashboard_frame, text="📊 Analytics Dashboard")
        
        # Perfect scrollable container
        canvas = tk.Canvas(dashboard_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(dashboard_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect header section
        header_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        header_section.pack(fill='x', padx=25, pady=25)
        
        # Perfect header with gradient accent
        header_content = tk.Frame(header_section, bg=self.colors['card_bg'])
        header_content.pack(fill='x', padx=40, pady=30)
        
        # Main dashboard title
        title_frame = tk.Frame(header_content, bg=self.colors['card_bg'])
        title_frame.pack(fill='x')
        
        tk.Label(title_frame, text="📊 Real-Time Analytics Dashboard", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(title_frame, text="Comprehensive hospital metrics • Live data visualization • Performance insights", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect metrics grid
        metrics_container = tk.Frame(scrollable_frame, bg=self.colors['light'])
        metrics_container.pack(fill='x', padx=25, pady=(0,25))
        
        # Perfect metric cards with advanced design
        cards_grid = tk.Frame(metrics_container, bg=self.colors['light'])
        cards_grid.pack(fill='x', padx=20, pady=20)
        
        # Configure grid weights for perfect responsive layout
        for i in range(4):
            cards_grid.grid_columnconfigure(i, weight=1)
        
        # Create stats_frame for compatibility
        stats_frame = cards_grid
        
        # Perfect Patient Card with hover effects
        patient_card = self.create_perfect_metric_card(
            cards_grid, "👥", "Total Patients", "0", 
            self.colors['info'], 0, 0
        )
        self.patient_count_label = patient_card['metric_label']
        
        # Perfect Doctor Card
        doctor_card = self.create_perfect_metric_card(
            cards_grid, "👨‍⚕️", "Active Doctors", "0", 
            self.colors['success'], 0, 1
        )
        self.doctor_count_label = doctor_card['metric_label']
        
        # Perfect Appointment Card
        apt_card = self.create_perfect_metric_card(
            cards_grid, "📅", "Today's Appointments", "0", 
            self.colors['accent'], 0, 2
        )
        self.apt_count_label = apt_card['metric_label']
        
        # Perfect Room Card
        room_card = self.create_perfect_metric_card(
            cards_grid, "🏨", "Available Rooms", "0", 
            self.colors['warning'], 0, 3
        )
        self.room_count_label = room_card['metric_label']
        
        # Configure grid weights
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Perfect action buttons
        actions_frame = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        actions_frame.pack(fill='x', padx=25, pady=(0,25))
        
        actions_content = tk.Frame(actions_frame, bg=self.colors['card_bg'])
        actions_content.pack(fill='x', padx=40, pady=25)
        
        # Button container
        button_container = tk.Frame(actions_content, bg=self.colors['card_bg'])
        button_container.pack()
        
        # Perfect refresh button with icon
        refresh_btn = self.create_perfect_button(
            button_container, "🔄 Refresh Analytics", 
            self.refresh_dashboard, self.colors['primary']
        )
        refresh_btn.pack(side='left', padx=10)
        
        # Perfect export button
        export_btn = self.create_perfect_button(
            button_container, "📊 Export Report", 
            lambda: messagebox.showinfo("Export", "Report export feature coming soon!"), 
            self.colors['success']
        )
        export_btn.pack(side='left', padx=10)
        
        # Perfect settings button
        settings_btn = self.create_perfect_button(
            button_container, "⚙️ Settings", 
            lambda: messagebox.showinfo("Settings", "Dashboard settings coming soon!"), 
            self.colors['warning']
        )
        settings_btn.pack(side='left', padx=10)
        
        # Perfect info panel
        info_panel = tk.Frame(actions_content, bg='#f0f9ff', relief='flat', bd=0)
        info_panel.pack(fill='x', pady=(20,0))
        
        info_content = tk.Frame(info_panel, bg='#f0f9ff')
        info_content.pack(fill='x', padx=20, pady=15)
        
        tk.Label(info_content, text="💡 Real-time Updates", 
                font=self.fonts['subheading'], 
                bg='#f0f9ff', fg=self.colors['primary']).pack(anchor='w')
        
        tk.Label(info_content, text="Dashboard automatically refreshes when you add patients, book appointments, or update records", 
                font=self.fonts['body'], 
                bg='#f0f9ff', fg=self.colors['text_secondary']).pack(anchor='w', pady=(5,0))
        
        # Perfect appointments section
        apt_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        apt_section.pack(fill='both', expand=True, padx=25, pady=(0,25))
        
        # Perfect section header
        apt_header = tk.Frame(apt_section, bg=self.colors['card_bg'])
        apt_header.pack(fill='x', padx=40, pady=25)
        
        tk.Label(apt_header, text="📅 Today's Appointments Overview", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(apt_header, text="Real-time appointment tracking • Patient management • Schedule optimization", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect appointments table container
        table_container = tk.Frame(apt_section, bg=self.colors['card_bg'])
        table_container.pack(fill='both', expand=True, padx=40, pady=(0,25))
        
        # Perfect treeview with enhanced styling
        tree_frame = tk.Frame(table_container, bg=self.colors['card_bg'])
        tree_frame.pack(fill='both', expand=True)
        
        self.apt_tree = ttk.Treeview(tree_frame, 
                                    columns=('Time', 'Patient', 'Doctor', 'Status', 'Reason'), 
                                    show='headings', 
                                    height=15,
                                    style='Perfect.Treeview')
        
        # Perfect column configuration
        columns_config = {
            'Time': {'width': 100, 'text': '🕐 Time'},
            'Patient': {'width': 200, 'text': '👤 Patient'},
            'Doctor': {'width': 200, 'text': '👨‍⚕️ Doctor'},
            'Status': {'width': 120, 'text': '📊 Status'},
            'Reason': {'width': 250, 'text': '📝 Reason'}
        }
        
        for col, config in columns_config.items():
            self.apt_tree.heading(col, text=config['text'])
            self.apt_tree.column(col, width=config['width'], minwidth=80)
        
        # Perfect scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=self.apt_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient='horizontal', command=self.apt_tree.xview)
        
        self.apt_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with perfect layout
        self.apt_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Pack scrollable canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Load initial data
        self.refresh_dashboard()
    
    def create_perfect_patients_tab(self):
        """Create perfect patients management with advanced features"""
        patients_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(patients_frame, text="👥 Patient Management")
        
        # Perfect patient notebook with custom styling
        patient_notebook = ttk.Notebook(patients_frame, style='Perfect.TNotebook')
        patient_notebook.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Perfect add patient tab
        add_frame = tk.Frame(patient_notebook, bg=self.colors['light'])
        patient_notebook.add(add_frame, text="➕ Register Patient")
        
        # Perfect scrollable form
        canvas = tk.Canvas(add_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(add_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect form container
        form_frame = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        form_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Perfect form header
        header_frame = tk.Frame(form_frame, bg=self.colors['card_bg'])
        header_frame.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header_frame, text="👥 Patient Registration", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Complete patient information • Medical history • Contact details", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect form fields with advanced styling
        fields_container = tk.Frame(form_frame, bg=self.colors['card_bg'])
        fields_container.pack(fill='x', padx=40, pady=20)
        
        # Create perfect form grid
        fields_frame = tk.Frame(fields_container, bg=self.colors['card_bg'])
        fields_frame.pack(fill='x')
        
        # Configure grid weights
        fields_frame.grid_columnconfigure(1, weight=1)
        fields_frame.grid_columnconfigure(3, weight=1)
        
        # Perfect form fields with enhanced styling
        row = 0
        
        # First Name
        self.create_perfect_form_field(fields_frame, "First Name*", row, 0)
        self.first_name_entry = self.create_perfect_entry(fields_frame, row, 1)
        
        # Last Name
        self.create_perfect_form_field(fields_frame, "Last Name*", row, 2)
        self.last_name_entry = self.create_perfect_entry(fields_frame, row, 3)
        
        row += 1
        
        # Date of Birth
        self.create_perfect_form_field(fields_frame, "Date of Birth*", row, 0)
        self.dob_entry = DateEntry(fields_frame, width=25, 
                                  background=self.colors['card_bg'],
                                  foreground=self.colors['text_primary'], 
                                  borderwidth=2,
                                  relief='solid',
                                  maxdate=date.today(),
                                  font=self.fonts['body'],
                                  date_pattern='dd/mm/yyyy')
        self.dob_entry.grid(row=row, column=1, padx=15, pady=15, sticky='ew')
        
        # Gender
        self.create_perfect_form_field(fields_frame, "Gender*", row, 2)
        self.gender_combo = ttk.Combobox(fields_frame, 
                                        values=["Male", "Female", "Other"], 
                                        width=25, 
                                        font=self.fonts['body'],
                                        style='Perfect.TCombobox')
        self.gender_combo.grid(row=row, column=3, padx=15, pady=15, sticky='ew')
        
        row += 1
        
        # Phone
        self.create_perfect_form_field(fields_frame, "Phone Number", row, 0)
        self.phone_entry = self.create_perfect_entry(fields_frame, row, 1)
        
        # Email
        self.create_perfect_form_field(fields_frame, "Email Address", row, 2)
        self.email_entry = self.create_perfect_entry(fields_frame, row, 3)
        
        row += 1
        
        # Blood Type
        self.create_perfect_form_field(fields_frame, "Blood Type", row, 0)
        self.blood_combo = ttk.Combobox(fields_frame, 
                                       values=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"], 
                                       width=25, 
                                       font=self.fonts['body'],
                                       style='Perfect.TCombobox')
        self.blood_combo.grid(row=row, column=1, padx=15, pady=15, sticky='ew')
        

        
        # Perfect action buttons
        button_section = tk.Frame(form_frame, bg=self.colors['card_bg'])
        button_section.pack(fill='x', padx=40, pady=30)
        
        # Button container with perfect spacing
        btn_container = tk.Frame(button_section, bg=self.colors['card_bg'])
        btn_container.pack()
        
        # Perfect register button
        register_btn = self.create_perfect_button(
            btn_container, "🚀 Register Patient", 
            self.register_patient, self.colors['success']
        )
        register_btn.configure(padx=40, pady=15, font=self.fonts['button'])
        register_btn.pack(side='left', padx=15)
        
        # Perfect clear button
        clear_btn = self.create_perfect_button(
            btn_container, "🔄 Clear Form", 
            self.clear_patient_form, self.colors['warning']
        )
        clear_btn.configure(padx=40, pady=15, font=self.fonts['button'])
        clear_btn.pack(side='left', padx=15)
        
        # Perfect preview button
        preview_btn = self.create_perfect_button(
            btn_container, "👁️ Preview", 
            lambda: messagebox.showinfo("Preview", "Form preview feature coming soon!"), 
            self.colors['info']
        )
        preview_btn.configure(padx=40, pady=15, font=self.fonts['button'])
        preview_btn.pack(side='left', padx=15)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Create search patients tab (simplified for now)
        # self.create_perfect_search_tab(patient_notebook)
    
    def create_perfect_search_tab(self, parent):
        """Create perfect search patients tab"""
        search_frame = tk.Frame(parent, bg=self.colors['light'])
        parent.add(search_frame, text="🔍 Search Patients")
        
        # Perfect search interface
        search_container = tk.Frame(search_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        search_container.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Search header
        header = tk.Frame(search_container, bg=self.colors['card_bg'])
        header.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header, text="🔍 Patient Search & Management", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header, text="Advanced search • Patient records • Quick access", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Search controls
        search_controls = tk.Frame(search_container, bg=self.colors['card_bg'])
        search_controls.pack(fill='x', padx=40, pady=20)
        
        tk.Label(search_controls, text="Search:", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary']).pack(side='left', padx=(0,15))
        
        self.search_entry = self.create_perfect_entry_inline(search_controls, width=40)
        self.search_entry.pack(side='left', padx=10)
        self.search_entry.bind('<Return>', lambda e: self.search_patients())
        
        # Perfect search buttons
        search_btn = self.create_perfect_button(
            search_controls, "🔍 Search", 
            self.search_patients, self.colors['primary']
        )
        search_btn.pack(side='left', padx=10)
        
        load_all_btn = self.create_perfect_button(
            search_controls, "📋 Load All", 
            self.load_all_patients, self.colors['info']
        )
        load_all_btn.pack(side='left', padx=10)
        
        # Results table
        results_frame = tk.Frame(search_container, bg=self.colors['card_bg'])
        results_frame.pack(fill='both', expand=True, padx=40, pady=(0,30))
        
        self.patients_tree = ttk.Treeview(results_frame, 
                                         columns=('ID', 'Name', 'Phone', 'Email', 'DOB', 'Gender'), 
                                         show='headings', 
                                         height=20,
                                         style='Perfect.Treeview')
        
        # Configure columns
        columns_config = {
            'ID': {'width': 80, 'text': '🆔 ID'},
            'Name': {'width': 200, 'text': '👤 Full Name'},
            'Phone': {'width': 150, 'text': '📞 Phone'},
            'Email': {'width': 200, 'text': '📧 Email'},
            'DOB': {'width': 120, 'text': '📅 Birth Date'},
            'Gender': {'width': 100, 'text': '⚧ Gender'}
        }
        
        for col, config in columns_config.items():
            self.patients_tree.heading(col, text=config['text'])
            self.patients_tree.column(col, width=config['width'], minwidth=80)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.patients_tree.yview)
        h_scrollbar = ttk.Scrollbar(results_frame, orient='horizontal', command=self.patients_tree.xview)
        
        self.patients_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
    
    def create_perfect_entry_inline(self, parent, width=25):
        """Create a perfect inline entry widget"""
        entry = tk.Entry(parent, width=width, 
                        font=self.fonts['body'],
                        relief='solid', 
                        bd=2,
                        highlightthickness=0,
                        bg=self.colors['card_bg'],
                        fg=self.colors['text_primary'])
        return entry
    
    def create_perfect_appointments_tab(self):
        """Create perfect appointments tab (simplified)"""
        apt_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(apt_frame, text="📅 Appointments")
        
        # Placeholder content
        placeholder = tk.Label(apt_frame, 
                              text="📅 Perfect Appointments Interface\nComing Soon with Enhanced Features!", 
                              font=self.fonts['heading'],
                              bg=self.colors['light'],
                              fg=self.colors['text_primary'])
        placeholder.pack(expand=True)
    
    def create_perfect_medical_records_tab(self):
        """Create perfect medical records tab (simplified)"""
        records_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(records_frame, text="📋 Medical Records")
        
        # Placeholder content
        placeholder = tk.Label(records_frame, 
                              text="📋 Perfect Medical Records Interface\nAdvanced Patient History & Analytics!", 
                              font=self.fonts['heading'],
                              bg=self.colors['light'],
                              fg=self.colors['text_primary'])
        placeholder.pack(expand=True)
    
    def create_perfect_data_sorting_tab(self):
        """Create perfect data sorting tab (simplified)"""
        sorting_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(sorting_frame, text="🔄 Analytics")
        
        # Placeholder content
        placeholder = tk.Label(sorting_frame, 
                              text="🔄 Perfect Data Analytics Interface\nAdvanced Sorting & Visualization Tools!", 
                              font=self.fonts['heading'],
                              bg=self.colors['light'],
                              fg=self.colors['text_primary'])
        placeholder.pack(expand=True)
        
        # Search patients tab
        search_frame = ttk.Frame(patient_notebook)
        patient_notebook.add(search_frame, text="🔍 Search Patients")
        
        # Search section
        search_section = tk.Frame(search_frame, bg='white', relief='raised', bd=2)
        search_section.pack(fill='x', padx=10, pady=10)
        
        tk.Label(search_section, text="🔍 Search Patients", 
                font=('Arial', 14, 'bold'), bg='white', fg='#2c3e50').pack(pady=10)
        
        search_controls = tk.Frame(search_section, bg='white')
        search_controls.pack(pady=10)
        
        tk.Label(search_controls, text="Search:", font=('Arial', 11, 'bold'), 
                bg='white').pack(side='left', padx=5)
        self.search_entry = tk.Entry(search_controls, width=30, font=('Arial', 11))
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<Return>', lambda e: self.search_patients())
        
        search_btn = tk.Button(search_controls, text="🔍 Search", 
                             command=self.search_patients, bg='#2ecc71', fg='white',
                             font=('Arial', 11, 'bold'), padx=15)
        search_btn.pack(side='left', padx=5)
        
        load_all_btn = tk.Button(search_controls, text="📋 Load All", 
                               command=self.load_all_patients, bg='#f39c12', fg='white',
                               font=('Arial', 11, 'bold'), padx=15)
        load_all_btn.pack(side='left', padx=5)
        
        refresh_btn = tk.Button(search_controls, text="🔄 Refresh", 
                              command=self.refresh_patient_search, bg='#3498db', fg='white',
                              font=('Arial', 11, 'bold'), padx=15)
        refresh_btn.pack(side='left', padx=5)
        
        # Results
        results_frame = tk.Frame(search_frame, bg='white', relief='raised', bd=2)
        results_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        tk.Label(results_frame, text="Search Results", 
                font=('Arial', 12, 'bold'), bg='white', fg='#2c3e50').pack(pady=5)
        
        self.patients_tree = ttk.Treeview(results_frame, 
                                         columns=('ID', 'Name', 'Phone', 'Email', 'DOB', 'Gender'), 
                                         show='headings', height=15)
        
        self.patients_tree.heading('ID', text='ID')
        self.patients_tree.heading('Name', text='Full Name')
        self.patients_tree.heading('Phone', text='Phone')
        self.patients_tree.heading('Email', text='Email')
        self.patients_tree.heading('DOB', text='Date of Birth')
        self.patients_tree.heading('Gender', text='Gender')
        
        self.patients_tree.column('ID', width=50)
        self.patients_tree.column('Name', width=180)
        self.patients_tree.column('Phone', width=120)
        self.patients_tree.column('Email', width=180)
        self.patients_tree.column('DOB', width=100)
        self.patients_tree.column('Gender', width=80)
        
        # Scrollbar for patients
        patients_scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.patients_tree.yview)
        self.patients_tree.configure(yscrollcommand=patients_scrollbar.set)
        
        self.patients_tree.pack(side='left', fill='both', expand=True, padx=10, pady=10)
        patients_scrollbar.pack(side='right', fill='y', pady=10)
    
    def create_appointments_tab(self):
        """Create enhanced appointments tab"""
        apt_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(apt_frame, text="📅 Appointments")
        
        # Enhanced book appointment section
        book_section = tk.Frame(apt_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        book_section.pack(fill='x', padx=20, pady=20)
        
        # Modern header
        header_frame = tk.Frame(book_section, bg=self.colors['card_bg'])
        header_frame.pack(fill='x', padx=30, pady=20)
        
        tk.Label(header_frame, text="📝 Book New Appointment", 
                font=('Segoe UI', 20, 'bold'), 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_frame, text="Schedule appointments with available doctors", 
                font=('Segoe UI', 11), 
                bg=self.colors['card_bg'], 
                fg='#6c757d').pack(anchor='w', pady=(5,0))
        
        # Form
        apt_form = tk.Frame(book_section, bg='white')
        apt_form.pack(padx=30, pady=20)
        
        # Patient ID
        tk.Label(apt_form, text="Patient ID*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=0, column=0, sticky='w', pady=8, padx=5)
        
        patient_id_frame = tk.Frame(apt_form, bg='white')
        patient_id_frame.grid(row=0, column=1, padx=15, pady=8, sticky='w')
        
        self.apt_patient_id = tk.Entry(patient_id_frame, width=20, font=('Arial', 11))
        self.apt_patient_id.pack(side='left')
        
        validate_patient_btn = tk.Button(patient_id_frame, text="✓ Validate", 
                                       command=self.validate_patient_id, bg='#f39c12', fg='white',
                                       font=('Arial', 9, 'bold'), padx=8)
        validate_patient_btn.pack(side='left', padx=5)
        
        # Doctor
        tk.Label(apt_form, text="Doctor*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=1, column=0, sticky='w', pady=8, padx=5)
        self.apt_doctor_combo = ttk.Combobox(apt_form, width=27, state='readonly')
        self.apt_doctor_combo.grid(row=1, column=1, padx=15, pady=8)
        
        # Date
        tk.Label(apt_form, text="Date*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=2, column=0, sticky='w', pady=8, padx=5)
        self.apt_date = DateEntry(apt_form, width=12, background='darkblue',
                                 foreground='white', borderwidth=2, mindate=date.today())
        self.apt_date.grid(row=2, column=1, padx=15, pady=8, sticky='w')
        
        # Time
        tk.Label(apt_form, text="Time*:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=3, column=0, sticky='w', pady=8, padx=5)
        time_frame = tk.Frame(apt_form, bg='white')
        time_frame.grid(row=3, column=1, padx=15, pady=8, sticky='w')
        
        self.apt_hour = ttk.Combobox(time_frame, values=[f"{i:02d}" for i in range(8, 18)], width=5)
        self.apt_hour.pack(side='left')
        tk.Label(time_frame, text=":", bg='white', font=('Arial', 11)).pack(side='left')
        self.apt_minute = ttk.Combobox(time_frame, values=["00", "15", "30", "45"], width=5)
        self.apt_minute.pack(side='left')
        
        # Reason
        tk.Label(apt_form, text="Reason:", font=('Arial', 11, 'bold'), 
                bg='white').grid(row=4, column=0, sticky='w', pady=8, padx=5)
        self.apt_reason = tk.Text(apt_form, width=30, height=3, font=('Arial', 11))
        self.apt_reason.grid(row=4, column=1, padx=15, pady=8)
        
        # Enhanced book button
        button_frame = tk.Frame(book_section, bg=self.colors['card_bg'])
        button_frame.pack(pady=25)
        
        book_btn = tk.Button(button_frame, text="✅ Book Appointment", 
                           command=self.book_appointment, 
                           bg=self.colors['success'], fg='white',
                           font=('Segoe UI', 14, 'bold'), 
                           padx=40, pady=15,
                           relief='flat', bd=0,
                           cursor='hand2')
        book_btn.pack()
        
        # Load doctors
        self.load_doctors()
    
    def create_medical_records_tab(self):
        """Create perfect medical records tab with enhanced functionality"""
        records_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(records_frame, text="📋 Medical Records")
        
        # Perfect scrollable container
        canvas = tk.Canvas(records_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(records_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect header section
        header_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        header_section.pack(fill='x', padx=25, pady=25)
        
        header_content = tk.Frame(header_section, bg=self.colors['card_bg'])
        header_content.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header_content, text="📋 Patient Medical Records", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_content, text="Comprehensive medical history • Treatment records • Patient health analytics", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect search section
        search_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        search_section.pack(fill='x', padx=25, pady=(0,25))
        
        search_content = tk.Frame(search_section, bg=self.colors['card_bg'])
        search_content.pack(fill='x', padx=40, pady=25)
        
        # Search header
        search_header = tk.Frame(search_content, bg=self.colors['card_bg'])
        search_header.pack(fill='x', pady=(0,20))
        
        tk.Label(search_header, text="🔍 Patient Search", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        # Search controls with perfect styling
        search_controls = tk.Frame(search_content, bg=self.colors['card_bg'])
        search_controls.pack(fill='x', pady=10)
        
        # Patient ID input
        id_frame = tk.Frame(search_controls, bg=self.colors['card_bg'])
        id_frame.pack(side='left', padx=(0,20))
        
        tk.Label(id_frame, text="Patient ID:", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'],
                fg=self.colors['text_primary']).pack(anchor='w')
        
        self.records_patient_id = tk.Entry(id_frame, width=15, 
                                          font=self.fonts['body'],
                                          relief='solid', bd=2,
                                          bg=self.colors['card_bg'],
                                          fg=self.colors['text_primary'])
        self.records_patient_id.pack(pady=(5,0))
        self.records_patient_id.bind('<Return>', lambda e: self.load_medical_records())
        
        # Action buttons
        buttons_frame = tk.Frame(search_controls, bg=self.colors['card_bg'])
        buttons_frame.pack(side='left', padx=20)
        
        # Validate Patient button
        validate_btn = self.create_perfect_button(
            buttons_frame, "✓ Validate Patient", 
            self.validate_patient_for_records, self.colors['info']
        )
        validate_btn.pack(pady=2)
        
        # Load Records button
        load_btn = self.create_perfect_button(
            buttons_frame, "📋 Load Records", 
            self.load_medical_records, self.colors['success']
        )
        load_btn.pack(pady=2)
        
        # Clear button
        clear_btn = self.create_perfect_button(
            buttons_frame, "🗑️ Clear", 
            self.clear_medical_records, self.colors['warning']
        )
        clear_btn.pack(pady=2)
        
        # Patient info display
        self.patient_info_frame = tk.Frame(search_content, bg='#f0f9ff', relief='flat', bd=0)
        self.patient_info_frame.pack(fill='x', pady=(20,0))
        
        self.patient_info_label = tk.Label(self.patient_info_frame, 
                                          text="💡 Enter a Patient ID and click 'Validate Patient' to verify", 
                                          font=self.fonts['body'], 
                                          bg='#f0f9ff', 
                                          fg=self.colors['primary'])
        self.patient_info_label.pack(pady=15)
        
        # Perfect results section
        results_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        results_section.pack(fill='both', expand=True, padx=25, pady=(0,25))
        
        results_content = tk.Frame(results_section, bg=self.colors['card_bg'])
        results_content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Results header
        results_header = tk.Frame(results_content, bg=self.colors['card_bg'])
        results_header.pack(fill='x', pady=(0,20))
        
        tk.Label(results_header, text="📊 Medical Records", 
                font=self.fonts['subheading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(side='left')
        
        # Records count label
        self.records_count_label = tk.Label(results_header, 
                                           text="", 
                                           font=self.fonts['body'], 
                                           bg=self.colors['card_bg'], 
                                           fg=self.colors['text_secondary'])
        self.records_count_label.pack(side='right')
        
        # Perfect records table
        table_frame = tk.Frame(results_content, bg=self.colors['card_bg'])
        table_frame.pack(fill='both', expand=True)
        
        self.records_tree = ttk.Treeview(table_frame, 
                                        columns=('Date', 'Doctor', 'Specialization', 'Diagnosis', 'Treatment', 'Prescription'), 
                                        show='headings', 
                                        height=18,
                                        style='Perfect.Treeview')
        
        # Perfect column configuration
        columns_config = {
            'Date': {'width': 120, 'text': '📅 Visit Date'},
            'Doctor': {'width': 180, 'text': '👨‍⚕️ Doctor'},
            'Specialization': {'width': 150, 'text': '🏥 Specialization'},
            'Diagnosis': {'width': 250, 'text': '🔍 Diagnosis'},
            'Treatment': {'width': 250, 'text': '💊 Treatment'},
            'Prescription': {'width': 200, 'text': '📝 Prescription'}
        }
        
        for col, config in columns_config.items():
            self.records_tree.heading(col, text=config['text'])
            self.records_tree.column(col, width=config['width'], minwidth=100)
        
        # Perfect scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.records_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.records_tree.xview)
        
        self.records_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Bind double-click to show detailed record
        self.records_tree.bind('<Double-1>', self.show_detailed_record)
        
        # Pack with perfect layout
        self.records_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        def refresh_thread():
            try:
                # Update status on main thread
                self.root.after(0, lambda: self.status_var.set("Refreshing dashboard..."))
                
                response = self.api_request('dashboard')
                
                if response['status'] == 'success':
                    data = response['data']
                    
                    # Update GUI elements on main thread
                    def update_gui():
                        # Update metrics
                        self.patient_count_label.config(text=str(data['patient_count']))
                        self.doctor_count_label.config(text=str(data['doctor_count']))
                        self.apt_count_label.config(text=str(data['appointment_count']))
                        self.room_count_label.config(text=str(data['available_rooms']))
                        
                        # Update appointments tree
                        self.apt_tree.delete(*self.apt_tree.get_children())
                        for apt in data['today_appointments']:
                            time_str = str(apt['appointment_time']) if apt['appointment_time'] else 'N/A'
                            self.apt_tree.insert('', 'end', values=(
                                time_str,
                                f"{apt['first_name']} {apt['last_name']}",
                                f"Dr. {apt['doctor_first_name']} {apt['doctor_last_name']}",
                                apt['status'],
                                apt.get('reason', 'N/A')[:50] + '...' if apt.get('reason', '') and len(apt.get('reason', '')) > 50 else apt.get('reason', 'N/A')
                            ))
                        
                        self.status_var.set("Dashboard refreshed successfully")
                    
                    self.root.after(0, update_gui)
                else:
                    raise Exception(response.get('message', 'Unknown error'))
                    
            except Exception as e:
                def show_error():
                    messagebox.showerror("Error", f"Failed to refresh dashboard: {e}")
                    self.status_var.set("Dashboard refresh failed")
                
                self.root.after(0, show_error)
        
        # Run in thread to prevent GUI freezing
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def register_patient(self):
        """Register new patient"""
        def register_thread():
            try:
                # Validate required fields (get values on main thread)
                first_name = self.first_name_entry.get()
                last_name = self.last_name_entry.get()
                gender = self.gender_combo.get()
                
                if not all([first_name, last_name, gender]):
                    self.root.after(0, lambda: messagebox.showerror("Error", "Please fill in all required fields (*)"))
                    return
                
                self.root.after(0, lambda: self.status_var.set("Registering patient..."))
                
                # Prepare patient data
                patient_data = {
                    'first_name': first_name,
                    'last_name': last_name,
                    'date_of_birth': self.dob_entry.get_date().isoformat(),
                    'gender': gender,
                    'phone': self.phone_entry.get() or None,
                    'email': self.email_entry.get() or None,
                    'blood_type': self.blood_combo.get() or None
                }
                
                # Register patient
                response = self.api_request('patients', method='POST', data=patient_data)
                
                if response['status'] == 'success':
                    def success_callback():
                        messagebox.showinfo("Success", f"✅ Patient registered successfully!\nPatient ID: {response['patient_id']}")
                        self.clear_patient_form()
                        self.refresh_dashboard()
                        self.status_var.set("Patient registered successfully")
                    
                    self.root.after(0, success_callback)
                else:
                    raise Exception(response.get('message', 'Registration failed'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Registration failed: {e}")
                    self.status_var.set("Patient registration failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=register_thread, daemon=True).start()
    
    def clear_patient_form(self):
        """Clear patient form"""
        self.first_name_entry.delete(0, 'end')
        self.last_name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.email_entry.delete(0, 'end')
        self.gender_combo.set('')
        self.blood_combo.set('')
        self.dob_entry.set_date(date.today())
    
    def search_patients(self):
        """Search patients"""
        def search_thread():
            try:
                search_term = self.search_entry.get()
                if not search_term:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a search term"))
                    return
                
                self.root.after(0, lambda: self.status_var.set("Searching patients..."))
                
                response = self.api_request('patients/search', method='POST', data={'search_term': search_term})
                
                if response['status'] == 'success':
                    def update_results():
                        self.patients_tree.delete(*self.patients_tree.get_children())
                        
                        for patient in response['data']:
                            self.patients_tree.insert('', 'end', values=(
                                patient['patient_id'],
                                f"{patient['first_name']} {patient['last_name']}",
                                patient['phone'] or 'N/A',
                                patient['email'] or 'N/A',
                                patient['date_of_birth'],
                                patient.get('gender', 'N/A')
                            ))
                        
                        self.status_var.set(f"Found {len(response['data'])} patients")
                    
                    self.root.after(0, update_results)
                else:
                    raise Exception(response.get('message', 'Search failed'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Search failed: {e}")
                    self.status_var.set("Patient search failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def load_all_patients(self):
        """Load all patients"""
        def load_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Loading all patients..."))
                
                response = self.api_request('patients')
                
                if response['status'] == 'success':
                    def update_patients():
                        self.patients_tree.delete(*self.patients_tree.get_children())
                        
                        for patient in response['data']:
                            self.patients_tree.insert('', 'end', values=(
                                patient['patient_id'],
                                f"{patient['first_name']} {patient['last_name']}",
                                patient['phone'] or 'N/A',
                                patient['email'] or 'N/A',
                                patient['date_of_birth'],
                                patient.get('gender', 'N/A')
                            ))
                        
                        self.status_var.set(f"Loaded {len(response['data'])} patients")
                    
                    self.root.after(0, update_patients)
                else:
                    raise Exception(response.get('message', 'Failed to load patients'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Failed to load patients: {e}")
                    self.status_var.set("Failed to load patients")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def refresh_patient_search(self):
        """Refresh patient search results"""
        def refresh_thread():
            try:
                self.root.after(0, lambda: self.status_var.set("Refreshing patient data..."))
                
                # Clear current search
                search_term = self.search_entry.get()
                
                if search_term:
                    # Re-run the current search
                    response = self.api_request('patients/search', method='POST', data={'search_term': search_term})
                    
                    if response['status'] == 'success':
                        def update_search_results():
                            self.patients_tree.delete(*self.patients_tree.get_children())
                            
                            for patient in response['data']:
                                self.patients_tree.insert('', 'end', values=(
                                    patient['patient_id'],
                                    f"{patient['first_name']} {patient['last_name']}",
                                    patient['phone'] or 'N/A',
                                    patient['email'] or 'N/A',
                                    patient['date_of_birth'],
                                    patient.get('gender', 'N/A')
                                ))
                            
                            self.status_var.set(f"Refreshed: Found {len(response['data'])} patients")
                        
                        self.root.after(0, update_search_results)
                    else:
                        raise Exception(response.get('message', 'Refresh failed'))
                else:
                    # Load all patients if no search term
                    response = self.api_request('patients')
                    
                    if response['status'] == 'success':
                        def update_all_results():
                            self.patients_tree.delete(*self.patients_tree.get_children())
                            
                            for patient in response['data']:
                                self.patients_tree.insert('', 'end', values=(
                                    patient['patient_id'],
                                    f"{patient['first_name']} {patient['last_name']}",
                                    patient['phone'] or 'N/A',
                                    patient['email'] or 'N/A',
                                    patient['date_of_birth'],
                                    patient.get('gender', 'N/A')
                                ))
                            
                            self.status_var.set(f"Refreshed: Loaded {len(response['data'])} patients")
                        
                        self.root.after(0, update_all_results)
                    else:
                        raise Exception(response.get('message', 'Refresh failed'))
                        
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Refresh failed: {e}")
                    self.status_var.set("Patient refresh failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=refresh_thread, daemon=True).start()
    
    def load_doctors(self):
        """Load doctors for appointment booking"""
        def load_thread():
            try:
                response = self.api_request('doctors')
                
                if response['status'] == 'success':
                    doctor_options = [f"Dr. {doctor['first_name']} {doctor['last_name']} ({doctor['specialization']}) - ID: {doctor['doctor_id']}" 
                                    for doctor in response['data']]
                    self.apt_doctor_combo['values'] = doctor_options
                    
            except Exception as e:
                print(f"Failed to load doctors: {e}")
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def book_appointment(self):
        """Book appointment"""
        def book_thread():
            try:
                # Get values on main thread
                patient_id = self.apt_patient_id.get()
                doctor_combo = self.apt_doctor_combo.get()
                hour = self.apt_hour.get()
                minute = self.apt_minute.get()
                
                # Validate required fields
                if not all([patient_id, doctor_combo, hour, minute]):
                    self.root.after(0, lambda: messagebox.showerror("Error", "Please fill in all required fields"))
                    return
                
                self.root.after(0, lambda: self.status_var.set("Booking appointment..."))
                
                # Extract doctor ID
                doctor_id = int(doctor_combo.split("ID: ")[1])
                
                # Prepare appointment data
                appointment_time = f"{hour}:{minute}:00"
                appointment_data = {
                    'patient_id': int(patient_id),
                    'doctor_id': doctor_id,
                    'appointment_date': self.apt_date.get_date().isoformat(),
                    'appointment_time': appointment_time,
                    'reason': self.apt_reason.get('1.0', 'end-1c')
                }
                
                # Book appointment
                response = self.api_request('appointments', method='POST', data=appointment_data)
                
                if response['status'] == 'success':
                    def success_callback():
                        messagebox.showinfo("Success", "✅ Appointment booked successfully!")
                        self.refresh_dashboard()
                        # Clear form
                        self.apt_patient_id.delete(0, 'end')
                        self.apt_doctor_combo.set('')
                        self.apt_hour.set('')
                        self.apt_minute.set('')
                        self.apt_reason.delete('1.0', 'end')
                        self.status_var.set("Appointment booked successfully")
                    
                    self.root.after(0, success_callback)
                else:
                    raise Exception(response.get('message', 'Booking failed'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid Patient ID"))
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Booking failed: {e}")
                    self.status_var.set("Appointment booking failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=book_thread, daemon=True).start()
    
    def validate_patient_for_records(self):
        """Validate patient ID before loading records"""
        def validate_thread():
            try:
                patient_id = self.records_patient_id.get().strip()
                if not patient_id:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a Patient ID"))
                    return
                
                self.root.after(0, lambda: self.status_var.set(f"Validating Patient ID {patient_id}..."))
                
                # Validate patient exists
                response = self.api_request(f'validate/patient/{patient_id}')
                
                if response['status'] == 'success':
                    if response['exists']:
                        patient = response['patient']
                        def show_patient_info():
                            info_text = f"✅ Patient Found: {patient['first_name']} {patient['last_name']} (ID: {patient['patient_id']})"
                            self.patient_info_label.config(text=info_text, fg=self.colors['success'])
                            self.status_var.set("✅ Patient validated successfully")
                        
                        self.root.after(0, show_patient_info)
                    else:
                        def show_not_found():
                            self.patient_info_label.config(text=f"❌ Patient ID {patient_id} not found in database", 
                                                          fg=self.colors['accent'])
                            self.status_var.set("❌ Patient not found")
                        
                        self.root.after(0, show_not_found)
                else:
                    raise Exception(response.get('message', 'Validation failed'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid numeric Patient ID"))
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Validation failed: {e}")
                    self.status_var.set("❌ Validation failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=validate_thread, daemon=True).start()
    
    def load_medical_records(self):
        """Load medical records for a patient with enhanced display"""
        def load_thread():
            try:
                patient_id = self.records_patient_id.get().strip()
                if not patient_id:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a Patient ID"))
                    return
                
                self.root.after(0, lambda: self.status_var.set(f"Loading medical records for Patient ID {patient_id}..."))
                
                # First validate patient
                validate_response = self.api_request(f'validate/patient/{patient_id}')
                
                if validate_response['status'] == 'success' and not validate_response['exists']:
                    def show_not_found():
                        messagebox.showerror("Patient Not Found", 
                                           f"❌ Patient ID {patient_id} does not exist in the database.\n\n"
                                           f"Please check the Patient ID and try again.")
                        self.patient_info_label.config(text=f"❌ Patient ID {patient_id} not found", 
                                                      fg=self.colors['accent'])
                        self.status_var.set("❌ Patient not found")
                    
                    self.root.after(0, show_not_found)
                    return
                
                # Load medical records
                response = self.api_request(f'patients/{patient_id}/medical-records')
                
                if response['status'] == 'success':
                    patient = validate_response['patient']
                    records = response['data']
                    
                    def update_records():
                        # Clear existing records
                        self.records_tree.delete(*self.records_tree.get_children())
                        
                        # Update patient info
                        info_text = f"📋 Records for: {patient['first_name']} {patient['last_name']} (ID: {patient['patient_id']})"
                        self.patient_info_label.config(text=info_text, fg=self.colors['success'])
                        
                        # Update records count
                        self.records_count_label.config(text=f"Total Records: {len(records)}")
                        
                        if records:
                            # Populate records
                            for record in records:
                                # Format date
                                visit_date = str(record.get('visit_date', 'N/A'))
                                if visit_date != 'N/A':
                                    try:
                                        from datetime import datetime
                                        date_obj = datetime.strptime(visit_date.split()[0], '%Y-%m-%d')
                                        visit_date = date_obj.strftime('%d/%m/%Y')
                                    except:
                                        pass
                                
                                # Truncate long text for display
                                diagnosis = record.get('diagnosis', 'N/A') or 'N/A'
                                treatment = record.get('treatment', 'N/A') or 'N/A'
                                prescription = record.get('prescription', 'N/A') or 'N/A'
                                
                                diagnosis_display = diagnosis[:40] + '...' if len(diagnosis) > 40 else diagnosis
                                treatment_display = treatment[:40] + '...' if len(treatment) > 40 else treatment
                                prescription_display = prescription[:30] + '...' if len(prescription) > 30 else prescription
                                
                                self.records_tree.insert('', 'end', values=(
                                    visit_date,
                                    f"Dr. {record['doctor_first_name']} {record['doctor_last_name']}",
                                    record['specialization'],
                                    diagnosis_display,
                                    treatment_display,
                                    prescription_display
                                ))
                            
                            self.status_var.set(f"✅ Loaded {len(records)} medical records for {patient['first_name']} {patient['last_name']}")
                            
                            # Show success message
                            messagebox.showinfo("Records Loaded", 
                                              f"✅ Successfully loaded {len(records)} medical records for:\n\n"
                                              f"Patient: {patient['first_name']} {patient['last_name']}\n"
                                              f"Patient ID: {patient['patient_id']}\n\n"
                                              f"Double-click any record for detailed view.")
                        else:
                            self.status_var.set(f"No medical records found for {patient['first_name']} {patient['last_name']}")
                            messagebox.showinfo("No Records", 
                                              f"No medical records found for:\n\n"
                                              f"Patient: {patient['first_name']} {patient['last_name']}\n"
                                              f"Patient ID: {patient['patient_id']}")
                    
                    self.root.after(0, update_records)
                else:
                    raise Exception(response.get('message', 'Failed to load records'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid numeric Patient ID"))
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Failed to load medical records: {e}")
                    self.status_var.set("❌ Failed to load medical records")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def clear_medical_records(self):
        """Clear medical records display"""
        self.records_tree.delete(*self.records_tree.get_children())
        self.records_patient_id.delete(0, 'end')
        self.patient_info_label.config(text="💡 Enter a Patient ID and click 'Validate Patient' to verify", 
                                      fg=self.colors['primary'])
        self.records_count_label.config(text="")
        self.status_var.set("🗑️ Medical records cleared")
    
    def show_detailed_record(self, event):
        """Show detailed medical record in a popup"""
        selection = self.records_tree.selection()
        if not selection:
            return
        
        item = self.records_tree.item(selection[0])
        values = item['values']
        
        if not values:
            return
        
        # Get the full record data
        patient_id = self.records_patient_id.get().strip()
        if not patient_id:
            return
        
        def get_full_record():
            try:
                response = self.api_request(f'patients/{patient_id}/medical-records')
                if response['status'] == 'success':
                    records = response['data']
                    # Find the matching record by date and doctor
                    visit_date = values[0]  # Date from display
                    doctor_name = values[1]  # Doctor from display
                    
                    for record in records:
                        record_date = str(record.get('visit_date', ''))
                        if record_date:
                            try:
                                from datetime import datetime
                                date_obj = datetime.strptime(record_date.split()[0], '%Y-%m-%d')
                                formatted_date = date_obj.strftime('%d/%m/%Y')
                                if formatted_date == visit_date:
                                    self.root.after(0, lambda: self.display_detailed_record(record))
                                    return
                            except:
                                pass
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load detailed record: {e}"))
        
        threading.Thread(target=get_full_record, daemon=True).start()
    
    def display_detailed_record(self, record):
        """Display detailed medical record in a popup window"""
        detail_window = tk.Toplevel(self.root)
        detail_window.title("📋 Detailed Medical Record")
        detail_window.geometry("800x600")
        detail_window.configure(bg=self.colors['card_bg'])
        detail_window.transient(self.root)
        detail_window.grab_set()
        
        # Header
        header_frame = tk.Frame(detail_window, bg=self.colors['primary'])
        header_frame.pack(fill='x')
        
        header_content = tk.Frame(header_frame, bg=self.colors['primary'])
        header_content.pack(fill='x', padx=30, pady=20)
        
        tk.Label(header_content, text="📋 Medical Record Details", 
                font=self.fonts['heading'], 
                bg=self.colors['primary'], 
                fg=self.colors['text_light']).pack(anchor='w')
        
        # Content
        content_frame = tk.Frame(detail_window, bg=self.colors['card_bg'])
        content_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # Record details
        details = [
            ("📅 Visit Date", record.get('visit_date', 'N/A')),
            ("👨‍⚕️ Doctor", f"Dr. {record['doctor_first_name']} {record['doctor_last_name']}"),
            ("🏥 Specialization", record.get('specialization', 'N/A')),
            ("🔍 Diagnosis", record.get('diagnosis', 'N/A')),
            ("💊 Treatment", record.get('treatment', 'N/A')),
            ("📝 Prescription", record.get('prescription', 'N/A')),
            ("📋 Notes", record.get('notes', 'N/A'))
        ]
        
        for label, value in details:
            detail_frame = tk.Frame(content_frame, bg=self.colors['card_bg'])
            detail_frame.pack(fill='x', pady=10)
            
            tk.Label(detail_frame, text=label, 
                    font=self.fonts['subheading'], 
                    bg=self.colors['card_bg'], 
                    fg=self.colors['text_primary']).pack(anchor='w')
            
            # Use Text widget for long content
            if label in ["🔍 Diagnosis", "💊 Treatment", "📝 Prescription", "📋 Notes"]:
                text_widget = tk.Text(detail_frame, height=3, width=70, 
                                     font=self.fonts['body'],
                                     bg='#f8f9fa', 
                                     fg=self.colors['text_primary'],
                                     relief='solid', bd=1,
                                     wrap='word')
                text_widget.pack(fill='x', pady=(5,0))
                text_widget.insert('1.0', value or 'N/A')
                text_widget.config(state='disabled')
            else:
                tk.Label(detail_frame, text=value or 'N/A', 
                        font=self.fonts['body'], 
                        bg=self.colors['card_bg'], 
                        fg=self.colors['text_secondary']).pack(anchor='w', padx=20, pady=(5,0))
        
        # Close button
        close_btn = self.create_perfect_button(
            content_frame, "✖️ Close", 
            detail_window.destroy, self.colors['accent']
        )
        close_btn.pack(pady=20)
    

    
    def validate_patient_id(self):
        """Validate patient ID"""
        def validate_thread():
            try:
                patient_id = self.apt_patient_id.get()
                if not patient_id:
                    self.root.after(0, lambda: messagebox.showwarning("Warning", "Please enter a Patient ID"))
                    return
                
                response = self.api_request(f'validate/patient/{patient_id}')
                
                if response['status'] == 'success':
                    if response['exists']:
                        patient = response['patient']
                        self.root.after(0, lambda: messagebox.showinfo("Valid Patient", 
                                      f"✅ Patient found!\n\nID: {patient['patient_id']}\nName: {patient['first_name']} {patient['last_name']}"))
                    else:
                        self.root.after(0, lambda: messagebox.showerror("Invalid Patient", 
                                      f"❌ {response['message']}\n\nPlease check the Patient ID or register a new patient first."))
                else:
                    raise Exception(response.get('message', 'Validation failed'))
                    
            except ValueError:
                self.root.after(0, lambda: messagebox.showerror("Error", "Please enter a valid numeric Patient ID"))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Validation failed: {e}"))
        
        threading.Thread(target=validate_thread, daemon=True).start()
    
    def create_data_sorting_tab(self):
        """Create perfect Quick Sort tab with advanced functionality"""
        sorting_frame = tk.Frame(self.notebook, bg=self.colors['light'])
        self.notebook.add(sorting_frame, text="🔄 Quick Sort Analytics")
        
        # Perfect scrollable container
        canvas = tk.Canvas(sorting_frame, bg=self.colors['light'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(sorting_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.colors['light'])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Perfect header section
        header_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        header_section.pack(fill='x', padx=25, pady=25)
        
        header_content = tk.Frame(header_section, bg=self.colors['card_bg'])
        header_content.pack(fill='x', padx=40, pady=30)
        
        tk.Label(header_content, text="🔄 Advanced Quick Sort Analytics", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(anchor='w')
        
        tk.Label(header_content, text="High-performance O(n log n) sorting • Real-time data analysis • Multiple criteria", 
                font=self.fonts['body'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_secondary']).pack(anchor='w', pady=(8,0))
        
        # Perfect sorting controls section
        controls_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        controls_section.pack(fill='x', padx=25, pady=(0,25))
        
        controls_content = tk.Frame(controls_section, bg=self.colors['card_bg'])
        controls_content.pack(fill='x', padx=40, pady=30)
        
        # Quick sort categories
        categories_frame = tk.Frame(controls_content, bg=self.colors['card_bg'])
        categories_frame.pack(fill='x')
        
        # Configure grid for three columns
        for i in range(3):
            categories_frame.grid_columnconfigure(i, weight=1)
        
        # Create perfect sorting categories
        self.create_perfect_sort_category(categories_frame, "📅 Date Sorting", 
                                        self.get_date_sort_options(), 0)
        self.create_perfect_sort_category(categories_frame, "👤 Name Sorting", 
                                        self.get_name_sort_options(), 1)
        self.create_perfect_sort_category(categories_frame, "🔢 ID Sorting", 
                                        self.get_id_sort_options(), 2)
        
        # Perfect results section
        results_section = tk.Frame(scrollable_frame, bg=self.colors['card_bg'], relief='flat', bd=0)
        results_section.pack(fill='both', expand=True, padx=25, pady=(0,25))
        
        results_content = tk.Frame(results_section, bg=self.colors['card_bg'])
        results_content.pack(fill='both', expand=True, padx=40, pady=30)
        
        # Results header
        results_header = tk.Frame(results_content, bg=self.colors['card_bg'])
        results_header.pack(fill='x', pady=(0,20))
        
        tk.Label(results_header, text="📊 Sort Results", 
                font=self.fonts['heading'], 
                bg=self.colors['card_bg'], 
                fg=self.colors['text_primary']).pack(side='left')
        
        # Clear button
        clear_btn = self.create_perfect_button(
            results_header, "🗑️ Clear Results", 
            self.clear_sort_results, self.colors['warning']
        )
        clear_btn.pack(side='right')
        
        # Results info
        self.sort_info_label = tk.Label(results_content, 
                                       text="🔄 Select a sorting option above to see results", 
                                       font=self.fonts['body'], 
                                       bg=self.colors['card_bg'], 
                                       fg=self.colors['text_secondary'])
        self.sort_info_label.pack(pady=(0,15))
        
        # Perfect results table
        table_frame = tk.Frame(results_content, bg=self.colors['card_bg'])
        table_frame.pack(fill='both', expand=True)
        
        self.sort_results_tree = ttk.Treeview(table_frame, 
                                             show='headings', 
                                             height=20,
                                             style='Perfect.Treeview')
        
        # Perfect scrollbars
        v_scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.sort_results_tree.yview)
        h_scrollbar = ttk.Scrollbar(table_frame, orient='horizontal', command=self.sort_results_tree.xview)
        
        self.sort_results_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack with perfect layout
        self.sort_results_tree.pack(side='left', fill='both', expand=True)
        v_scrollbar.pack(side='right', fill='y')
        h_scrollbar.pack(side='bottom', fill='x')
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    

    

    

    

    
    def quick_sort_by_criteria(self, data_type, sort_field, order):
        """Perform quick sort with specific criteria"""
        def sort_thread():
            try:
                self.root.after(0, lambda: self.status_var.set(f"Quick sorting {data_type} by {sort_field}..."))
                
                # Determine endpoint and data structure
                if data_type == 'records':
                    endpoint = 'records/sorted'
                    data_type_display = 'Medical Records'
                elif data_type == 'patients':
                    endpoint = 'patients/sorted'
                    data_type_display = 'Patients'
                elif data_type == 'appointments':
                    endpoint = 'appointments/sorted'
                    data_type_display = 'Appointments'
                
                # Make API request
                request_data = {
                    'sort_by': sort_field,
                    'order': order
                }
                
                response = self.api_request(endpoint, method='POST', data=request_data)
                
                if response['status'] == 'success':
                    def update_results():
                        self.display_sort_results(response['data'], response['sort_info'], data_type_display)
                        self.status_var.set(f"✅ Quick Sort completed: {response['sort_info']['record_count']} records")
                    
                    self.root.after(0, update_results)
                else:
                    raise Exception(response.get('message', 'Sort failed'))
                    
            except Exception as e:
                def error_callback():
                    messagebox.showerror("Error", f"Quick Sort failed: {e}")
                    self.status_var.set("❌ Quick Sort failed")
                
                self.root.after(0, error_callback)
        
        threading.Thread(target=sort_thread, daemon=True).start()
    
    
    def display_sort_results(self, data, sort_info, data_type):
        """Display sorted results in treeview"""
        # Clear existing results
        self.sort_results_tree.delete(*self.sort_results_tree.get_children())
        
        if not data:
            self.sort_info_label.config(text="No data found to sort", fg='#e74c3c')
            return
        
        # Configure columns based on data type
        if data_type == "Medical Records":
            columns = ('Record ID', 'Patient', 'Doctor', 'Visit Date', 'Diagnosis', 'Specialization')
            self.sort_results_tree['columns'] = columns
            
            for col in columns:
                self.sort_results_tree.heading(col, text=col)
                self.sort_results_tree.column(col, width=120)
            
            # Populate data
            for record in data:
                visit_date = str(record.get('visit_date', 'N/A')).split()[0] if record.get('visit_date') else 'N/A'
                self.sort_results_tree.insert('', 'end', values=(
                    record.get('record_id', 'N/A'),
                    f"{record.get('patient_first_name', '')} {record.get('patient_last_name', '')}",
                    f"Dr. {record.get('doctor_first_name', '')} {record.get('doctor_last_name', '')}",
                    visit_date,
                    record.get('diagnosis', 'N/A')[:30] + '...' if len(str(record.get('diagnosis', ''))) > 30 else record.get('diagnosis', 'N/A'),
                    record.get('specialization', 'N/A')
                ))
        
        elif data_type == "Patients":
            columns = ('Patient ID', 'Name', 'Date of Birth', 'Gender', 'Phone', 'Email')
            self.sort_results_tree['columns'] = columns
            
            for col in columns:
                self.sort_results_tree.heading(col, text=col)
                self.sort_results_tree.column(col, width=120)
            
            # Populate data
            for patient in data:
                dob = str(patient.get('date_of_birth', 'N/A')).split()[0] if patient.get('date_of_birth') else 'N/A'
                self.sort_results_tree.insert('', 'end', values=(
                    patient.get('patient_id', 'N/A'),
                    f"{patient.get('first_name', '')} {patient.get('last_name', '')}",
                    dob,
                    patient.get('gender', 'N/A'),
                    patient.get('phone', 'N/A'),
                    patient.get('email', 'N/A')
                ))
        
        elif data_type == "Appointments":
            columns = ('Appointment ID', 'Patient', 'Doctor', 'Date', 'Time', 'Status')
            self.sort_results_tree['columns'] = columns
            
            for col in columns:
                self.sort_results_tree.heading(col, text=col)
                self.sort_results_tree.column(col, width=120)
            
            # Populate data
            for appointment in data:
                apt_date = str(appointment.get('appointment_date', 'N/A')).split()[0] if appointment.get('appointment_date') else 'N/A'
                self.sort_results_tree.insert('', 'end', values=(
                    appointment.get('appointment_id', 'N/A'),
                    f"{appointment.get('patient_first_name', '')} {appointment.get('patient_last_name', '')}",
                    f"Dr. {appointment.get('doctor_first_name', '')} {appointment.get('doctor_last_name', '')}",
                    apt_date,
                    appointment.get('appointment_time', 'N/A'),
                    appointment.get('status', 'N/A')
                ))
        
        # Update info label with perfect styling
        info_text = (f"✅ {sort_info['message']}\n"
                    f"📊 Algorithm: {sort_info['algorithm']} | "
                    f"Records: {sort_info['record_count']} | "
                    f"Field: {sort_info['sort_by']} | "
                    f"Order: {sort_info['order'].title()}ending")
        
        self.sort_info_label.config(text=info_text, fg=self.colors['success'], font=self.fonts['body'])
    
    def clear_sort_results(self):
        """Clear sort results with perfect styling"""
        self.sort_results_tree.delete(*self.sort_results_tree.get_children())
        self.sort_info_label.config(text="🔄 Select a sorting option above to see results", 
                                   fg=self.colors['text_secondary'], 
                                   font=self.fonts['body'])
        self.status_var.set("🗑️ Sort results cleared")

def main():
    root = tk.Tk()
    app = HospitalFlaskGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()