import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from MyQR import myqr
import os
import base64
import cv2
import pyzbar.pyzbar as pyzbar
import time
from tkinter import PhotoImage

class QRAttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Attendance App")

        # Load the image
        self.image = PhotoImage(file="logoofqr.png")

        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Display the image
        ttk.Label(self.main_frame, image=self.image).grid(row=0, column=0, columnspan=3, pady=10)

        ttk.Label(self.main_frame, text="QR Attendance App", font=("Helvetica", 16, "bold")).grid(row=1, column=0,
                                                                                                  columnspan=3, pady=10)

        self.option_var = tk.IntVar()
        ttk.Radiobutton(self.main_frame, text="Generate QR Codes", variable=self.option_var, value=1).grid(row=2,
                                                                                                           column=1,
                                                                                                           padx=5,
                                                                                                           pady=5)
        ttk.Radiobutton(self.main_frame, text="Record Attendance", variable=self.option_var, value=2).grid(row=3,
                                                                                                           column=1,
                                                                                                           padx=5,
                                                                                                           pady=5)

        self.upload_button = ttk.Button(self.main_frame, text="Upload Students File like (.txt)",
                                        command=self.upload_students_file)
        self.upload_button.grid(row=4, column=1, pady=10)

        self.action_button = ttk.Button(self.main_frame, text="Start", command=self.perform_action)
        self.action_button.grid(row=5, column=1, pady=10)

        self.filename = ""

        # Create a menu bar
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Create a "Help" menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="About", command=self.show_about_page)

    def upload_students_file(self):
        self.filename = filedialog.askopenfilename(initialdir="/", title="Select Students File",
                                                   filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if self.filename:
            messagebox.showinfo("Success", f"Students file '{os.path.basename(self.filename)}' uploaded successfully.")

    def perform_action(self):
        option = self.option_var.get()

        if not self.filename:
            messagebox.showerror("Error", "Please upload the students file.")
            return

        if option == 1:
            self.generate_qr_codes()
        elif option == 2:
            self.record_attendance()
        else:
            messagebox.showerror("Error", "Please select an option.")

    def generate_qr_codes(self):
        with open(self.filename, 'r') as f:
            lines = f.read().split("\n")

        save_dir = os.path.join(os.getcwd(), '../Student_qr_codes_list')
        os.makedirs(save_dir, exist_ok=True)

        for student in lines:
            encoded_name = base64.b64encode(student.encode())

            myqr.run(
                str(encoded_name),
                level='H',
                version=1,
                colorized=True,
                contrast=1.0,
                brightness=1.0,
                save_name=f"{student}.bmp",
                save_dir=save_dir
            )

        messagebox.showinfo("Success", "QR codes generated successfully in the 'Student_qr_codes_list' folder.")

    def record_attendance(self):
        cap = cv2.VideoCapture(0)

        fob = open('../attendance.txt', 'w+')

        names = []

        def enter_data(z):
            if z in names:
                pass
            else:
                names.append(z)
                z = ''.join(str(z))
                fob.write(z + '\n')
            return names

        def check_data(data):
            data = str(data)
            if data in names:
                print('Already Present')
            else:
                print('\n' + str(len(names) + 1) + '\n' + data)
                enter_data(data)

        while True:
            _, frame = cap.read()
            decoded_objects = pyzbar.decode(frame)
            for obj in decoded_objects:
                check_data(obj.data)
                time.sleep(1)

            cv2.imshow("Frame", frame)

            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.destroyAllWindows()
                break

        fob.close()

    def show_about_page(self):
        about_text = """
        QR Attendance App

        This application allows you to generate QR codes for student attendance and record attendance using QR codes.

        Developed by sam@cm
        """

        messagebox.showinfo("About QR Attendance App", about_text)


def main():
    root = tk.Tk()
    app = QRAttendanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
