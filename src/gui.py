import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from .models import ModelManager
from .analysis import calculate_coverage

class CoralAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Coral Analysis Tool")
        self.model_manager = ModelManager()
        self.setup_gui()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Model selection
        ttk.Label(main_frame, text="Model Type:").grid(row=0, column=0, sticky=tk.W)
        self.model_var = tk.StringVar(value="hc")
        ttk.Radiobutton(main_frame, text="Hard Coral", variable=self.model_var, 
                       value="hc").grid(row=0, column=1)
        ttk.Radiobutton(main_frame, text="Groups", variable=self.model_var, 
                       value="groups").grid(row=0, column=2)
        
        # Image folder selection
        ttk.Label(main_frame, text="Image Folder:").grid(row=1, column=0, sticky=tk.W)
        self.image_path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.image_path_var, width=40).grid(
            row=1, column=1, columnspan=2)
        ttk.Button(main_frame, text="Browse", command=self.select_image_folder).grid(
            row=1, column=3)
        
        # Labels folder selection
        ttk.Label(main_frame, text="Labels Folder:").grid(row=2, column=0, sticky=tk.W)
        self.labels_path_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.labels_path_var, width=40).grid(
            row=2, column=1, columnspan=2)
        ttk.Button(main_frame, text="Browse", command=self.select_labels_folder).grid(
            row=2, column=3)
        
        # Image limit
        ttk.Label(main_frame, text="Image Limit:").grid(row=3, column=0, sticky=tk.W)
        self.limit_var = tk.StringVar(value="")
        ttk.Entry(main_frame, textvariable=self.limit_var, width=10).grid(
            row=3, column=1, sticky=tk.W)
        
        # Analysis options
        self.quantify_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Quantify Only", variable=self.quantify_var).grid(
            row=4, column=0, columnspan=2, sticky=tk.W)
        
        # Action buttons
        ttk.Button(main_frame, text="Analyze", command=self.run_analysis).grid(
            row=5, column=0, columnspan=4, pady=10)
        
        # Results display
        self.results_text = tk.Text(main_frame, height=15, width=60)
        self.results_text.grid(row=6, column=0, columnspan=4, pady=5)
        
    def select_image_folder(self):
        folder = filedialog.askdirectory(title="Select Image Folder")
        if folder:
            self.image_path_var.set(folder)
            
    def select_labels_folder(self):
        folder = filedialog.askdirectory(title="Select Labels Folder")
        if folder:
            self.labels_path_var.set(folder)
            
    def run_analysis(self):
        image_dir = self.image_path_var.get()
        label_dir = self.labels_path_var.get()
        
        if not image_dir:
            messagebox.showerror("Error", "Please select an image folder")
            return
            
        try:
            limit = int(self.limit_var.get()) if self.limit_var.get() else None
        except ValueError:
            messagebox.showerror("Error", "Invalid limit value")
            return
            
        model_type = self.model_var.get()
        model, class_names = self.model_manager.load_model(model_type)
        
        if self.quantify_var.get():
            if not label_dir:
                messagebox.showerror("Error", "Please select a labels folder for quantification")
                return
            self.run_quantification(image_dir, label_dir, class_names, limit)
        else:
            self.run_prediction(model, image_dir, label_dir, class_names, limit)
            
    def run_quantification(self, image_dir, label_dir, class_names, limit):
        try:
            class_coverage, total_coverage, image_coverages = calculate_coverage(
                image_dir, label_dir, class_names, limit)
            
            self.display_results(class_coverage, total_coverage, image_coverages)
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            
    def run_prediction(self, model, image_dir, label_dir, class_names, limit):
        try:
            # Run prediction
            results = model.predict(
                source=image_dir,
                save=True,
                save_txt=True,
                conf=0.25,
                agnostic_nms=True
            )
            
            # Get prediction results and display
            predicted_label_dir = "path/to/predicted/labels"  # Update with actual path
            class_coverage, total_coverage, image_coverages = calculate_coverage(
                image_dir, predicted_label_dir, class_names, limit)
            
            self.display_results(class_coverage, total_coverage, image_coverages)
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            
    def display_results(self, class_coverage, total_coverage, image_coverages):
        self.results_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "Class-wise Coverage:\n")
        for class_name, coverage in class_coverage.items():
            self.results_text.insert(tk.END, f"{class_name}: {coverage:.2f}%\n")
            
        self.results_text.insert(tk.END, f"\nTotal Coverage: {total_coverage:.2f}%\n")
        
        self.results_text.insert(tk.END, "\nPer-Image Coverage:\n")
        for image_name, coverage in image_coverages.items():
            self.results_text.insert(tk.END, f"\nImage {image_name}:\n")
            for class_name, perc in coverage.items():
                self.results_text.insert(tk.END, f"{class_name}: {perc:.2f}%\n")