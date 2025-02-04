import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import joblib
import numpy as np

class NetworkAttackDetectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Attack Detector")
        self.root.geometry("800x600")
        
        # Load the saved models
        try:
            self.label_model = joblib.load('binary_classifier_rf.joblib')
            self.type_model = joblib.load('multiclass_classifier_dt.joblib')
            print("Models loaded successfully")
        except Exception as e:
            print(f"Error loading models: {e}")
            messagebox.showerror("Error", "Failed to load models. Please ensure model files are in the correct location.")
            root.destroy()
            return
        
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # File selection
        ttk.Label(main_frame, text="Select Network Data File (CSV):").grid(row=0, column=0, sticky=tk.W)
        self.file_path = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.file_path, width=50).grid(row=1, column=0, padx=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_file).grid(row=1, column=1)
        
        # Analyze button
        ttk.Button(main_frame, text="Analyze", command=self.analyze_data).grid(row=2, column=0, pady=20)
        
        # Results frame
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Results display
        self.result_text = tk.Text(results_frame, height=10, width=60)
        self.result_text.grid(row=0, column=0, pady=10)
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.result_text['yscrollcommand'] = scrollbar.set

    def browse_file(self):
        filename = filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            self.file_path.set(filename)

    def preprocess_data(self, df):
        # Convert string values to numeric
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = pd.to_numeric(df[col], errors='coerce')
                df[col] = df[col].fillna(0)
                
        # List of required columns based on your training data
        required_columns = [
            'arp.opcode', 'arp.hw.size', 'icmp.checksum', 'icmp.seq_le',
            'http.content_length', 'http.response', 'tcp.ack', 'tcp.ack_raw',
            'tcp.checksum', 'tcp.connection.fin', 'tcp.connection.rst',
            'tcp.connection.syn', 'tcp.connection.synack', 'tcp.flags',
            'tcp.flags.ack', 'tcp.len', 'tcp.seq', 'udp.stream',
            'udp.time_delta', 'dns.qry.name', 'dns.qry.qu',
            'dns.retransmission', 'dns.retransmit_request',
            'mqtt.conflag.cleansess', 'mqtt.conflags', 'mqtt.hdrflags',
            'mqtt.len', 'mqtt.msgtype', 'mqtt.proto_len', 'mqtt.topic_len',
            'mqtt.ver', 'mbtcp.len'
        ]
        
        # Ensure all required columns exist
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Select only the required columns in the correct order
        return df[required_columns]

    def analyze_data(self):
        try:
            # Load and preprocess the data
            file_path = self.file_path.get()
            if not file_path:
                messagebox.showerror("Error", "Please select a file first.")
                return
            
            df = pd.read_csv(file_path)
            processed_data = self.preprocess_data(df)
            
            # Make predictions
            attack_labels = self.label_model.predict(processed_data)
            attack_types = self.type_model.predict(processed_data)
            
            # Calculate statistics
            total_records = len(attack_labels)
            attack_count = np.sum(attack_labels == 1)
            normal_count = np.sum(attack_labels == 0)
            
            # Display results
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, f"Analysis Results:\n\n")
            self.result_text.insert(tk.END, f"Total Records Analyzed: {total_records}\n")
            self.result_text.insert(tk.END, f"Attacks Detected: {attack_count}\n")
            self.result_text.insert(tk.END, f"Normal Traffic: {normal_count}\n\n")
            
            # Display attack type distribution
            self.result_text.insert(tk.END, "Attack Type Distribution:\n")
            type_counts = pd.Series(attack_types).value_counts()
            for attack_type, count in type_counts.items():
                self.result_text.insert(tk.END, f"{attack_type}: {count}\n")
                
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred during analysis: {str(e)}")

def main():
    root = tk.Tk()
    app = NetworkAttackDetectorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
