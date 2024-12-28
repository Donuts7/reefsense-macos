"""Results display component for the GUI."""

import tkinter as tk
from tkinter import ttk

class ResultsDisplay:
    def __init__(self, parent, row=0):
        self.text = tk.Text(parent, height=15, width=60)
        self.text.grid(row=row, column=0, columnspan=4, pady=5)

    def display_results(self, class_coverage, total_coverage):#, image_coverages):
        self.text.delete(1.0, tk.END)
        
        self.text.insert(tk.END, "Class-wise Coverage:\n")
        for class_name, coverage in class_coverage.items():
            self.text.insert(tk.END, f"{class_name}: {coverage:.2f}%\n")
            
        self.text.insert(tk.END, f"\nTotal Coverage: {total_coverage:.2f}%\n")
        
        # self.text.insert(tk.END, "\nPer-Image Coverage:\n")
        # for image_name, coverage in image_coverages.items():
        #     self.text.insert(tk.END, f"\nImage {image_name}:\n")
        #     for class_name, perc in coverage.items():
        #         self.text.insert(tk.END, f"{class_name}: {perc:.2f}%\n")