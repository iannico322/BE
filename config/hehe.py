import time
import random
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk
import os
import math
import json

class AITrainingSystem:
    def __init__(self):
        self.popup_windows = []
        self.training_active = True
        self.brain_window = None
        
    def show_popup(self, title, message, duration=3):
        """Show a popup window that auto-closes"""
        def create_popup():
            popup = tk.Tk()
            popup.title(title)
            popup.geometry("450x180")
            popup.configure(bg='#1a1a2e')
            popup.resizable(False, False)
            
            # Center the window
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - (450 // 2) + random.randint(-50, 50)
            y = (popup.winfo_screenheight() // 2) - (180 // 2) + random.randint(-50, 50)
            popup.geometry(f"450x180+{x}+{y}")
            
            # Modern border
            border_frame = tk.Frame(popup, bg='#16213e', bd=1)
            border_frame.pack(fill='both', expand=True, padx=1, pady=1)
            
            inner_frame = tk.Frame(border_frame, bg='#1a1a2e')
            inner_frame.pack(fill='both', expand=True, padx=1, pady=1)
            
            title_label = tk.Label(inner_frame, text=title, bg='#1a1a2e', fg='#4fc3f7', 
                                 font=('Segoe UI', 11, 'bold'))
            title_label.pack(pady=10)
            
            label = tk.Label(inner_frame, text=message, bg='#1a1a2e', fg='#ffffff', 
                           font=('Segoe UI', 9), wraplength=400, justify='center')
            label.pack(pady=20)
            
            self.popup_windows.append(popup)
            
            # Auto close after duration
            popup.after(duration * 1000, popup.destroy)
            popup.mainloop()
        
        thread = threading.Thread(target=create_popup, daemon=True)
        thread.start()
    
    def show_realistic_training_visualization(self):
        """Show realistic neural network training visualization"""
        train_win = tk.Tk()
        train_win.title("Neural Network Training - PyTorch GPU Accelerated")
        train_win.geometry("900x700")
        train_win.configure(bg='#2b2b2b')
        train_win.resizable(False, False)
        
        # Center window
        train_win.update_idletasks()
        x = (train_win.winfo_screenwidth() // 2) - (450)
        y = (train_win.winfo_screenheight() // 2) - (350)
        train_win.geometry(f"900x700+{x}+{y}")
        
        # Title
        title_label = tk.Label(train_win, text="🧠 Deep Neural Network Training", 
                             bg='#2b2b2b', fg='#4fc3f7', font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=10)
        
        # Main frame
        main_frame = tk.Frame(train_win, bg='#2b2b2b')
        main_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Left panel - Network visualization
        left_frame = tk.Frame(main_frame, bg='#3c3c3c', bd=1, relief='solid')
        left_frame.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        network_label = tk.Label(left_frame, text="Network Architecture", 
                               bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 12, 'bold'))
        network_label.pack(pady=5)
        
        canvas = tk.Canvas(left_frame, width=420, height=350, bg='#3c3c3c', highlightthickness=0)
        canvas.pack(pady=5)
        
        # Right panel - Training metrics
        right_frame = tk.Frame(main_frame, bg='#3c3c3c', bd=1, relief='solid')
        right_frame.pack(side='right', fill='both', expand=True)
        
        metrics_label = tk.Label(right_frame, text="Training Metrics", 
                               bg='#3c3c3c', fg='#ffffff', font=('Segoe UI', 12, 'bold'))
        metrics_label.pack(pady=5)
        
        # Training log
        log_frame = tk.Frame(right_frame, bg='#3c3c3c')
        log_frame.pack(fill='both', expand=True, padx=5, pady=5)
        
        log_text = tk.Text(log_frame, bg='#1a1a1a', fg='#00ff00', 
                         font=('Consolas', 9), height=20, width=40)
        log_text.pack(fill='both', expand=True)
        
        # Progress bars
        progress_frame = tk.Frame(train_win, bg='#2b2b2b')
        progress_frame.pack(fill='x', padx=20, pady=10)
        
        epoch_label = tk.Label(progress_frame, text="Epoch Progress:", 
                             bg='#2b2b2b', fg='#ffffff', font=('Segoe UI', 10))
        epoch_label.pack(anchor='w')
        
        epoch_progress = ttk.Progressbar(progress_frame, length=860, mode='determinate')
        epoch_progress.pack(pady=5)
        
        overall_label = tk.Label(progress_frame, text="Overall Training:", 
                               bg='#2b2b2b', fg='#ffffff', font=('Segoe UI', 10))
        overall_label.pack(anchor='w')
        
        overall_progress = ttk.Progressbar(progress_frame, length=860, mode='determinate')
        overall_progress.pack(pady=5)
        
        self.popup_windows.append(train_win)
        
        # Animation variables
        animation_step = 0
        epoch = 0
        layer_nodes = [784, 512, 256, 128, 64, 10]  # Realistic layer sizes
        connections = []
        
        # Initialize network connections
        def init_network():
            connections.clear()
            for layer_idx in range(len(layer_nodes) - 1):
                layer_connections = []
                for i in range(min(10, layer_nodes[layer_idx])):  # Limit visual connections
                    for j in range(min(10, layer_nodes[layer_idx + 1])):
                        weight = random.uniform(-1, 1)
                        layer_connections.append({
                            'from_node': i,
                            'to_node': j,
                            'weight': weight,
                            'activity': 0
                        })
                connections.append(layer_connections)
        
        init_network()
        
        # Training metrics
        training_data = {
            'losses': [],
            'accuracies': [],
            'val_losses': [],
            'val_accuracies': []
        }
        
        def animate_training():
            nonlocal animation_step, epoch
            if not self.training_active:
                return
                
            canvas.delete("all")
            
            # Draw network layers
            layer_positions = []
            for layer_idx, num_nodes in enumerate(layer_nodes):
                x = 60 + layer_idx * 60
                nodes = []
                display_nodes = min(10, num_nodes)  # Limit visual nodes
                
                for node_idx in range(display_nodes):
                    y = 50 + node_idx * 30
                    # Node activity simulation
                    activity = 0.3 + 0.7 * math.sin(animation_step * 0.1 + layer_idx + node_idx)
                    activity = max(0.1, min(1.0, activity))  # Clamp between 0.1 and 1.0
                    
                    # Color based on activity - ensure valid range
                    intensity = max(0, min(255, int(255 * activity)))
                    intensity_half = max(0, min(255, intensity // 2))
                    color = f"#{intensity:02x}{intensity_half:02x}00"
                    
                    canvas.create_oval(x-5, y-5, x+5, y+5, fill=color, outline='#ffffff')
                    
                    # Add node labels for input/output layers
                    if layer_idx == 0 and node_idx < 5:
                        canvas.create_text(x-20, y, text=f"x{node_idx}", fill='#ffffff', font=('Arial', 8))
                    elif layer_idx == len(layer_nodes)-1:
                        canvas.create_text(x+20, y, text=f"y{node_idx}", fill='#ffffff', font=('Arial', 8))
                    
                    nodes.append((x, y, activity))
                
                layer_positions.append(nodes)
                
                # Layer labels
                if layer_idx == 0:
                    canvas.create_text(x, 20, text="Input\n784", fill='#4fc3f7', font=('Arial', 10, 'bold'))
                elif layer_idx == len(layer_nodes)-1:
                    canvas.create_text(x, 20, text="Output\n10", fill='#4fc3f7', font=('Arial', 10, 'bold'))
                else:
                    canvas.create_text(x, 20, text=f"Hidden\n{num_nodes}", fill='#4fc3f7', font=('Arial', 10, 'bold'))
            
            # Draw connections with weight visualization
            for layer_idx, layer_connections in enumerate(connections):
                if layer_idx < len(layer_positions) - 1:
                    from_layer = layer_positions[layer_idx]
                    to_layer = layer_positions[layer_idx + 1]
                    
                    for conn in layer_connections[:30]:  # Limit visual connections
                        if conn['from_node'] < len(from_layer) and conn['to_node'] < len(to_layer):
                            from_x, from_y, from_activity = from_layer[conn['from_node']]
                            to_x, to_y, to_activity = to_layer[conn['to_node']]
                            
                            # Connection strength based on weight
                            weight = conn['weight']
                            weight_intensity = max(0, min(255, int(255 * abs(weight))))
                            
                            if weight > 0:
                                color = f"#00{weight_intensity:02x}00"
                            else:
                                color = f"#{weight_intensity:02x}0000"
                            
                            # Activity pulse
                            conn['activity'] = from_activity * abs(weight)
                            width = max(1, int(3 * conn['activity']))
                            
                            canvas.create_line(from_x, from_y, to_x, to_y, 
                                             fill=color, width=width, stipple='gray25')
            
            # Update training metrics
            if animation_step % 10 == 0:
                epoch += 1
                
                # Realistic loss decrease
                base_loss = 2.5 * math.exp(-epoch * 0.01) + random.uniform(0, 0.1)
                loss = max(0.001, base_loss)
                
                # Realistic accuracy increase
                base_acc = 95 * (1 - math.exp(-epoch * 0.02)) + random.uniform(-2, 2)
                accuracy = min(99.9, max(60, base_acc))
                
                val_loss = loss + random.uniform(0, 0.05)
                val_acc = accuracy - random.uniform(0, 3)
                
                training_data['losses'].append(loss)
                training_data['accuracies'].append(accuracy)
                training_data['val_losses'].append(val_loss)
                training_data['val_accuracies'].append(val_acc)
                
                # Update log
                log_entry = f"Epoch {epoch:4d} | Loss: {loss:.4f} | Acc: {accuracy:.2f}% | Val_Loss: {val_loss:.4f} | Val_Acc: {val_acc:.2f}%\n"
                log_text.insert(tk.END, log_entry)
                log_text.see(tk.END)
                
                # Keep log manageable
                if epoch > 50:
                    log_text.delete("1.0", "2.0")
            
            # Update progress bars
            epoch_progress['value'] = (animation_step % 100)
            overall_progress['value'] = min(100, animation_step / 10)
            
            animation_step += 1
            
            if animation_step < 1000:
                train_win.after(100, animate_training)
            else:
                train_win.after(2000, lambda: [train_win.destroy(), self.show_ai_human_greeting()])
        
        animate_training()
        train_win.mainloop()

    def show_ai_human_greeting(self):
        """Show AI human figure greeting after training completion"""
        greeting_win = tk.Tk()
        greeting_win.title("AI Training Complete - Meet Your AI")
        greeting_win.geometry("800x600")
        greeting_win.configure(bg='#0f1419')
        greeting_win.resizable(False, False)
        
        # Center window
        greeting_win.update_idletasks()
        x = (greeting_win.winfo_screenwidth() // 2) - (400)
        y = (greeting_win.winfo_screenheight() // 2) - (300)
        greeting_win.geometry(f"800x600+{x}+{y}")
        
        # Title
        title_label = tk.Label(greeting_win, text="✨ AI TRAINING COMPLETE ✨", 
                             bg='#0f1419', fg='#4fc3f7', font=('Segoe UI', 18, 'bold'))
        title_label.pack(pady=20)
        
        # Main canvas for AI figure
        canvas = tk.Canvas(greeting_win, width=700, height=400, bg='#0f1419', highlightthickness=0)
        canvas.pack(pady=20)
        
        # Greeting text
        greeting_frame = tk.Frame(greeting_win, bg='#0f1419')
        greeting_frame.pack(pady=10)
        
        greeting_text = tk.Label(greeting_frame, text="", bg='#0f1419', fg='#ffffff', 
                               font=('Segoe UI', 14), justify='center')
        greeting_text.pack()
        
        self.popup_windows.append(greeting_win)
        
        # Animation variables
        animation_step = 0
        greeting_phase = 0
        
        def draw_human_figure():
            nonlocal animation_step, greeting_phase
            canvas.delete("all")
            
            # Center position
            center_x, center_y = 350, 200
            
            # Holographic effect
            glow_intensity = 0.5 + 0.3 * math.sin(animation_step * 0.1)
            glow_intensity = max(0.2, min(1.0, glow_intensity))  # Clamp values
            
            # Draw holographic grid background
            for i in range(0, 700, 50):
                alpha = max(0, min(255, int(50 * glow_intensity)))
                alpha_half = max(0, min(255, alpha // 2))
                canvas.create_line(i, 0, i, 400, fill=f"#{alpha:02x}{alpha:02x}{alpha_half:02x}", width=1)
            for i in range(0, 400, 50):
                alpha = max(0, min(255, int(50 * glow_intensity)))
                alpha_half = max(0, min(255, alpha // 2))
                canvas.create_line(0, i, 700, i, fill=f"#{alpha:02x}{alpha:02x}{alpha_half:02x}", width=1)
            
            # Human figure with animation
            head_bob = 5 * math.sin(animation_step * 0.1)
            arm_wave = 20 * math.sin(animation_step * 0.2)
            
            # Color intensity based on glow
            color_intensity = max(0, min(255, int(255 * glow_intensity)))
            figure_color = f"#{color_intensity:02x}{color_intensity:02x}ff"
            
            # Head (circle)
            head_x, head_y = center_x, center_y - 80 + head_bob
            canvas.create_oval(head_x-25, head_y-25, head_x+25, head_y+25, 
                             outline=figure_color, width=3, fill='')
            
            # Eyes (animated)
            eye_blink = 1 if animation_step % 60 < 5 else 8
            canvas.create_oval(head_x-12, head_y-8, head_x-5, head_y-8+eye_blink, 
                             fill=figure_color, outline=figure_color)
            canvas.create_oval(head_x+5, head_y-8, head_x+12, head_y-8+eye_blink, 
                             fill=figure_color, outline=figure_color)
            
            # Smile
            canvas.create_arc(head_x-15, head_y-5, head_x+15, head_y+15, 
                            start=0, extent=180, outline=figure_color, width=2, style='arc')
            
            # Body (rectangle)
            body_x, body_y = center_x, center_y + 20
            canvas.create_rectangle(body_x-20, body_y-30, body_x+20, body_y+50, 
                                  outline=figure_color, width=3, fill='')
            
            # Arms (with waving animation)
            # Left arm (static)
            canvas.create_line(body_x-20, body_y-10, body_x-40, body_y+10, 
                             fill=figure_color, width=3)
            canvas.create_line(body_x-40, body_y+10, body_x-35, body_y+30, 
                             fill=figure_color, width=3)
            
            # Right arm (waving)
            arm_end_x = body_x + 40 + arm_wave
            arm_end_y = body_y - 20 + abs(arm_wave) * 0.5
            canvas.create_line(body_x+20, body_y-10, arm_end_x, arm_end_y, 
                             fill=figure_color, width=3)
            canvas.create_line(arm_end_x, arm_end_y, arm_end_x+10, arm_end_y+15, 
                             fill=figure_color, width=3)
            
            # Legs
            canvas.create_line(body_x-10, body_y+50, body_x-15, body_y+90, 
                             fill=figure_color, width=3)
            canvas.create_line(body_x+10, body_y+50, body_x+15, body_y+90, 
                             fill=figure_color, width=3)
            
            # Feet
            canvas.create_line(body_x-15, body_y+90, body_x-25, body_y+90, 
                             fill=figure_color, width=3)
            canvas.create_line(body_x+15, body_y+90, body_x+25, body_y+90, 
                             fill=figure_color, width=3)
            
            # Digital aura effect
            for i in range(12):
                angle = (animation_step * 0.05 + i * 0.52) % (2 * math.pi)
                radius = 100 + 20 * math.sin(animation_step * 0.03 + i)
                
                aura_x = center_x + radius * math.cos(angle)
                aura_y = center_y + radius * math.sin(angle) * 0.7
                
                r = max(100, min(255, random.randint(100, 255)))
                g = max(100, min(255, random.randint(100, 255)))
                particle_color = f"#{r:02x}{g:02x}ff"
                canvas.create_oval(aura_x-2, aura_y-2, aura_x+2, aura_y+2, 
                                 fill=particle_color, outline=particle_color)
            
            # Greeting text animation
            if greeting_phase == 0 and animation_step > 50:
                greeting_text.config(text="Hello there! 👋")
                greeting_phase = 1
            elif greeting_phase == 1 and animation_step > 100:
                greeting_text.config(text="Hi Master Nico! 👋\nI'm your personally made AI")
                greeting_phase = 2
            elif greeting_phase == 2 and animation_step > 150:
                greeting_text.config(text="Hi Master Nico! 👋\nI'm your personally made AI\n\nI've learned from 2.8 billion neural samples")
                greeting_phase = 3
            elif greeting_phase == 3 and animation_step > 200:
                greeting_text.config(text="Hi Master Nico! 👋\nI'm your personally made AI\n\nI've learned from 2.8 billion neural samples\nReady to assist you with anything! ✨")
                greeting_phase = 4
            
            animation_step += 1
            
            if animation_step < 400:
                greeting_win.after(50, draw_human_figure)
            else:
                # Keep window open for viewing
                close_button = tk.Button(greeting_win, text="Thank you, AI! 🤖", 
                                       command=greeting_win.destroy,
                                       bg='#4fc3f7', fg='#ffffff', 
                                       font=('Segoe UI', 12, 'bold'),
                                       padx=20, pady=10)
                close_button.pack(pady=20)
        
        draw_human_figure()
        greeting_win.mainloop()

    def print_with_delay(self, text, delay=0.03):
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def realistic_loading_animation(self, text, duration=3):
        """Realistic loading animation"""
        chars = ["[    ]", "[=   ]", "[==  ]", "[=== ]", "[====]", 
                "[=== ]", "[==  ]", "[=   ]"]
        
        end_time = time.time() + duration
        i = 0
        while time.time() < end_time:
            percentage = min(100, int((time.time() - (end_time - duration)) / duration * 100))
            sys.stdout.write(f'\r{chars[i % len(chars)]} {percentage:3d}% {text}')
            sys.stdout.flush()
            time.sleep(0.2)
            i += 1
        sys.stdout.write(f'\r[====] 100% {text} - Complete\n')

    def simulate_training(self):
        # Professional header
        print("=" * 70)
        print("🤖 ADVANCED NEURAL NETWORK TRAINING SYSTEM".center(70))
        print("=" * 70)
        print("📊 Deep Learning Model: Transformer Architecture")
        print("🎯 Objective: Personal AI Assistant for Master Nico")
        print("⚡ Hardware: RTX 4090 | CUDA 12.0 | 32GB RAM")
        print("=" * 70)
        print()
        
        # Show realistic training visualization
        self.show_realistic_training_visualization()

    def close_all_popups(self):
        """Close all popup windows"""
        for window in self.popup_windows:
            try:
                window.destroy()
            except:
                pass
        self.popup_windows.clear()

    def run(self):
        try:
            self.simulate_training()
        except KeyboardInterrupt:
            self.training_active = False
            self.close_all_popups()
            print("\n\n" + "=" * 50)
            print("⚠️  TRAINING INTERRUPTED".center(50))
            print("=" * 50)
            print("💾 Saving current model state...")
            print("🔒 Training session ended safely")
            time.sleep(1)
            print("✅ Model partially trained and saved")

if __name__ == "__main__":
    # Set console title
    os.system("title 🤖 Neural Network Training - Personal AI for Master Nico")
    
    trainer = AITrainingSystem()
    trainer.run()