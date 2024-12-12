import tkinter as tk
from tkinter import filedialog, messagebox
from trafficanalysis import load_data, perform_analysis
from leadanalysis import process_files, extract_product_id
from seoqueriesanalysis import upload_file
from data_correlation import launch_advanced_data_analysis
from seodashboard import SEOAnalysisDashboard

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("UI")
        self.root.geometry("600x400") 
        self.create_ui()

    def create_ui(self):
        # Header Label
        header_label = tk.Label(
            self.root, 
            text="UI", 
            font=("Helvetica", 24), 
            bg="#006F8E", 
            fg="white", 
            padx=20, 
            pady=10
        )
        header_label.pack(fill="x")

        # Button Frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # Buttons for Lead, SEO Analysis, Traffic Analysis, SEO Dashboard
        button_lead = tk.Button(
            button_frame, 
            text="Lead", 
            font=("Helvetica", 14), 
            bg="gray", 
            fg="black", 
            relief="solid", 
            width=15, 
            command=self.open_lead_analysis
        )
        button_seo = tk.Button(
            button_frame, 
            text="SEO Analysis", 
            font=("Helvetica", 14), 
            bg="gray", 
            fg="black", 
            relief="solid", 
            width=15, 
            command=self.open_seo_analysis
        )
        button_traffic = tk.Button(
            button_frame, 
            text="Traffic Analysis", 
            font=("Helvetica", 14), 
            bg="gray", 
            fg="black", 
            relief="solid", 
            width=15, 
            command=self.open_traffic_analysis
        )
        button_seo_dashboard = tk.Button(
            button_frame, 
            text="SEO Dashboard", 
            font=("Helvetica", 14), 
            bg="gray", 
            fg="black", 
            relief="solid", 
            width=15, 
            command=self.open_seo_dashboard
        )

        # Group Buttons in Grid
        button_lead.grid(row=0, column=0, padx=10)
        button_seo.grid(row=0, column=1, padx=10)
        button_traffic.grid(row=0, column=2, padx=10)
        button_seo_dashboard.grid(row=1, column=0, columnspan=3, pady=10)

        # Bottom Label
        bottom_label = tk.Label(
            self.root, 
            text="Data Analytics - Correlation/Trends/Groups", 
            font=("Helvetica", 14), 
            bg="gray", 
            fg="black", 
            relief="solid", 
            pady=10
        )
        bottom_label.pack(fill="x", padx=20, pady=20)

    def open_lead_analysis(self):
        """Handle Lead Analysis Button."""
        process_files()

    def open_seo_analysis(self):
        """Handle SEO Analysis Button."""
        upload_file()

    def open_traffic_analysis(self):
        """Handle Traffic Analysis Button."""
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if not file_path:
            messagebox.showwarning("No File Selected", "Please select a traffic data file.")
            return
        self.data = load_data(file_path)
        if self.data is not None:
            messagebox.showinfo("File Uploaded", "Traffic data uploaded successfully!")
            self.run_traffic_analysis()

    def run_traffic_analysis(self):
        """Run the Traffic Analysis."""
        if self.data is None:
            messagebox.showerror("No Data", "Please upload traffic data first.")
            return
        perform_analysis(self.data)

    def open_seo_dashboard(self):
        """Open SEO Dashboard in a new window."""
        seo_root = tk.Toplevel(self.root)
        app = SEOAnalysisDashboard(seo_root)

    def open_data_correlation(self):
        """Handle Data Correlation Button."""
        launch_advanced_data_analysis()

def main():
    """Main function to run the app."""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()