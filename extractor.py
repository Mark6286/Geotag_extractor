import os
import exifread
import csv
import tkinter as tk
from tkinter import filedialog, messagebox

def extract_geotags(folder_path):
    geotags = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".jpg") or filename.endswith(".jpeg") or filename.endswith(".png"):
            filepath = os.path.join(folder_path, filename)
            with open(filepath, 'rb') as image_file:
                tags = exifread.process_file(image_file)
                if 'GPS GPSLatitude' in tags and 'GPS GPSLongitude' in tags:
                    # Extract latitude and longitude
                    latitude = tags['GPS GPSLatitude']
                    longitude = tags['GPS GPSLongitude']
                    # Convert coordinates to decimal format
                    latitude_decimal = convert_to_decimal(latitude)
                    longitude_decimal = convert_to_decimal(longitude)
                    geotags.append({
                        'filename': filename,
                        'latitude': latitude_decimal,
                        'longitude': longitude_decimal
                    })
    return geotags

def convert_to_decimal(coord):
    degrees = float(coord.values[0].num) / float(coord.values[0].den)
    minutes = float(coord.values[1].num) / float(coord.values[1].den) / 60
    seconds = float(coord.values[2].num) / float(coord.values[2].den) / 3600
    decimal_degrees = degrees + minutes + seconds
    return decimal_degrees

def save_to_csv(geotags, csv_file):
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['filename', 'latitude', 'longitude'])
        writer.writeheader()
        for tag in geotags:
            writer.writerow(tag)

def browse_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        folder_entry.delete(0, tk.END)
        folder_entry.insert(tk.END, folder_path)

def browse_output():
    csv_file = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if csv_file:
        output_entry.delete(0, tk.END)
        output_entry.insert(tk.END, csv_file)

def process_photos():
    folder_path = folder_entry.get()
    csv_file = output_entry.get()

    if not folder_path or not csv_file:
        messagebox.showerror("Error", "Please provide both a folder path and an output CSV file path.")
        return

    geotags = extract_geotags(folder_path)
    save_to_csv(geotags, csv_file)
    messagebox.showinfo("Success", "Geotags extracted and saved to CSV file successfully.")

# Create main window
root = tk.Tk()
root.title("Extract Geotags from Photos")
root.resizable(False, False)
root.iconbitmap("icon.ico") #ico format
#root.iconphoto(True, tk.PhotoImage(file="icon.png")) png format
# try:
#     root.iconbitmap("icon.ico")  # Use ICO format for Windows
# except tk.TclError:
#     try:
#         root.iconphoto(True, tk.PhotoImage(file="icon.png"))  # Use PNG format as fallback
#     except tk.TclError:
#         try:
#             root.iconphoto(True, tk.PhotoImage(file="icon.jpg"))  # Use JPEG format as fallback
#         except tk.TclError:
#             try:
#                 root.iconphoto(True, tk.PhotoImage(file="icon.gif"))  # Use GIF format as fallback
#             except tk.TclError:
#                 print("Error: Could not set window icon.")

# Create widgets
folder_label = tk.Label(root, text="Folder Path:")
folder_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
folder_entry = tk.Entry(root, width=50)
folder_entry.grid(row=0, column=1, padx=10, pady=5)
browse_folder_button = tk.Button(root, text="Browse", command=browse_folder)
browse_folder_button.grid(row=0, column=2, padx=5, pady=5)

output_label = tk.Label(root, text="Output CSV File:")
output_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)
output_entry = tk.Entry(root, width=50)
output_entry.grid(row=1, column=1, padx=10, pady=5)
browse_output_button = tk.Button(root, text="Browse", command=browse_output)
browse_output_button.grid(row=1, column=2, padx=5, pady=5)

process_button = tk.Button(root, text="Process Photos", command=process_photos)
process_button.grid(row=2, column=1, pady=10)

# Start the GUI event loop
root.mainloop()