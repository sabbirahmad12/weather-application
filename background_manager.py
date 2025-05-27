import tkinter as tk
from tkinter import ttk
import time

class BackgroundManager:
    def __init__(self, main_frame):
        self.main_frame = main_frame
        self.style = ttk.Style()
        self.animation_running = False
        self.current_frame = 0
        self.animation_frames = 10
        
        # Configure grid weights for main frame
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Define colors for different weather conditions
        self.colors = {
            'Clear': {
                'main': '#87CEEB',    # Sky blue
                'frame': '#B0E0E6',   # Powder blue
                'title_frame': '#87CEEB',  # Same as main (Sky blue)
                'text': '#000000',    # Black
                'button_text': '#104C54',  # Blue
                'gradient_start': '#87CEEB',  # Sky blue
                'gradient_end': '#B0E0E6',   # Powder blue     
            },
            'Clouds': {
                'main': '#B0C4DE',    # Light steel blue
                'frame': '#E6E6FA',   # Lavender
                'title_frame': '#B0C4DE',  # Same as main (Light steel blue)
                'text': '#000000',    # Black
                'button_text': '#4B0082',  # Indigo
                'gradient_start': '#B0C4DE',  # Light steel blue
                'gradient_end': '#E6E6FA',   # Lavender   
            },
            'Rain': {
                'main': '#4682B4',    # Steel blue
                'frame': '#87CEEB',   # Sky blue
                'title_frame': '#4682B4',  # Same as main (Steel blue)
                'text': '#FFFFFF',    # White
                'button_text': '#13556F',  # Medium blue
                'gradient_start': '#4682B4',  # Steel blue
                'gradient_end': '#87CEEB',   # Sky blue 
            },
            'Snow': {
                'main': '#F0F8FF',    # Alice blue
                'frame': '#E0FFFF',   # Light cyan
                'title_frame': '#F0F8FF',  # Same as main (Alice blue)
                'text': '#000000',    # Black
                'button_text': '#1E90FF',  # Dodger blue
                'gradient_start': '#F0F8FF',  # Alice blue
                'gradient_end': '#E0FFFF',   # Light cyan        
            },
            'Thunderstorm': {
                'main': '#483D8B',    # Dark slate blue
                'frame': '#6A5ACD',   # Slate blue
                'title_frame': '#483D8B',  # Same as main (Dark slate blue)
                'text': '#FFFFFF',    # White
                'button_text': '#000080',  # Navy
                'gradient_start': '#483D8B',  # Dark slate blue
                'gradient_end': '#6A5ACD',   # Slate blue
            },
            'Drizzle': {
                'main': '#6495ED',    # Cornflower blue
                'frame': '#87CEFA',   # Light sky blue
                'title_frame': '#6495ED',  # Same as main (Cornflower blue)
                'text': '#000000',    # Black
                'button_text': '#4169E1',  # Royal blue
                'gradient_start': '#6495ED',  # Cornflower blue
                'gradient_end': '#87CEFA',   # Light sky blue
            },
            'Mist': {
                'main': '#E6E6FA',    # Lavender
                'frame': '#F0F8FF',   # Alice blue
                'title_frame': '#E6E6FA',  # Same as main (Lavender)
                'text': '#000000',    # Black
                'button_text': '#708090',  # Slate gray
                'gradient_start': '#E6E6FA',  # Lavender
                'gradient_end': '#F0F8FF',   # Alice blue
            },
            'Haze': {
                'main': '#D4E4EA',    # Light gray
                'frame': '#A6D9F1',   # Lighter gray
                'title_frame': '#D4E4EA',  # Same as main (Light gray)
                'text': '#000000',    # Black
                'button_text': '#696969',  # Dim gray
                'gradient_start': '#D4E4EA',  # Light gray
                'gradient_end': '#A6D9F1',   # Lighter gray
            }
        }
    
    def interpolate_color(self, color1, color2, factor):
        # Convert hex to RGB
        r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
        r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
        
        # Interpolate
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        # Convert back to hex
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def animate_transition(self, old_condition, new_condition):
        if self.animation_running:
            return
            
        self.animation_running = True
        old_colors = self.colors.get(old_condition, self.colors['Clear'])
        new_colors = self.colors.get(new_condition, self.colors['Clear'])
        
        def update_frame(frame):
            if frame >= self.animation_frames:
                self.animation_running = False
                return
                
            factor = frame / self.animation_frames
            current_main = self.interpolate_color(old_colors['main'], new_colors['main'], factor)
            current_frame = self.interpolate_color(old_colors['frame'], new_colors['frame'], factor)
            
            self.main_frame.configure(background=current_main)
            self.style.configure('TFrame', background=current_frame)
            
            self.main_frame.after(50, lambda: update_frame(frame + 1))
        
        update_frame(0)
    
    def update_background(self, condition):
        # Get colors for current condition or use default
        colors = self.colors.get(condition, {
            'main': '#FFFFFF',
            'frame': '#F5F5F5',
            'title_frame': '#FFFFFF',
            'text': '#000000',
            'button_text': '#000000',
            'gradient_start': '#FFFFFF',
            'gradient_end': '#F5F5F5',
        })
        
        # Update main frame background
        self.main_frame.configure(style='Main.TFrame')
        self.style.configure('Main.TFrame', background=colors['main'])
        
        # Update all LabelFrame styles
        self.style.configure('TLabelframe', background=colors['frame'])
        self.style.configure('TLabelframe.Label', background=colors['frame'], foreground=colors['text'])
        
        # Update all Label styles
        self.style.configure('TLabel', background=colors['frame'], foreground=colors['text'])
        
        # Update all Frame styles
        self.style.configure('TFrame', background=colors['frame'])
        
        # Update only Title Frame style
        self.style.configure('Title.TFrame', background=colors['title_frame'])
        
        # Update Button styles with default background and custom text color
        self.style.configure('TButton',
                           background='#E0E0E0',  # Light gray default
                           foreground=colors['button_text'])
        
        # Map button states
        self.style.map('TButton',
                      background=[('active', '#D0D0D0'),  # Slightly darker when active
                                ('pressed', '#C0C0C0')],  # Even darker when pressed
                      foreground=[('active', colors['button_text']),
                                ('pressed', colors['button_text'])])
        
        # Update Radio button styles
        self.style.configure('TRadiobutton',
                           background=colors['frame'],
                           foreground=colors['text'])
        
        # Update Combobox styles
        self.style.configure('TCombobox',
                           fieldbackground=colors['frame'],
                           background='#E0E0E0',  # Light gray default
                           foreground=colors['text'])
        
        # Update Combobox popup styles
        self.style.map('TCombobox',
                      fieldbackground=[('readonly', colors['frame'])],
                      selectbackground=[('readonly', '#D0D0D0')],
                      selectforeground=[('readonly', colors['button_text'])])
    
    def get_colors(self, condition):
        return self.colors.get(condition, {
            'main': '#FFFFFF',
            'frame': '#F5F5F5',
            'text': '#000000',
            'button_text': '#000000',
            'gradient_start': '#FFFFFF',
            'gradient_end': '#F5F5F5',
        }) 