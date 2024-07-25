import tkinter as tk
from tkinter import ttk, messagebox
import calendar
from datetime import datetime
from calendar import month_name
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Login.persistence.model import Base, Event  # Importa tu módulo donde defines las clases del modelo

DATABASE_URL = "sqlite:///Login/db/login.sqlite"  # Cambia esto a la URL de tu base de datos
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)  # Crea todas las tablas

class Calendar:
    def __init__(self, root, organizer_id):
        self.root = root
        self.organizer_id = organizer_id
        self.root.title("Calendar")
        self.year = datetime.now().year
        self.month = datetime.now().month
        self.selected_day = None

        # Configurar estilo de botones
        self.style = ttk.Style()
        self.style.configure("Red.TButton", background="red", foreground="white")

        self.calendar_frame = ttk.Frame(self.root)
        self.calendar_frame.pack(fill="both", expand=True)
        self.details_frame = ttk.Frame(self.root)
        self.details_frame.pack(fill="both", expand=True)
        
        self.build_calendar()

    def build_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        header = ttk.Label(self.calendar_frame, text=f"{month_name[self.month]} {self.year}", font=("Arial", 20))
        header.grid(row=0, column=0, columnspan=7)

        days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
        for idx, day in enumerate(days):
            label = ttk.Label(self.calendar_frame, text=day, font=("Arial", 12))
            label.grid(row=1, column=idx)

        cal = calendar.monthcalendar(self.year, self.month)
        for r, week in enumerate(cal, 2):
            for c, day in enumerate(week):
                if day != 0:
                    # Aplicar estilo "Red.TButton" si el día tiene un evento
                    btn_style = "Red.TButton" if self.day_has_event(day) else "TButton"
                    btn = ttk.Button(self.calendar_frame, text=str(day), command=lambda d=day: self.select_day(d), style=btn_style)
                    btn.grid(row=r, column=c, padx=5, pady=5)

        prev_btn = ttk.Button(self.calendar_frame, text="<<", command=self.prev_month)
        prev_btn.grid(row=0, column=0, sticky="w")
        next_btn = ttk.Button(self.calendar_frame, text=">>", command=self.next_month)
        next_btn.grid(row=0, column=6, sticky="e")

    def prev_month(self):
        if self.month == 1:
            self.month = 12
            self.year -= 1
        else:
            self.month -= 1
        self.build_calendar()

    def next_month(self):
        if self.month == 12:
            self.month = 1
            self.year += 1
        else:
            self.month += 1
        self.build_calendar()

    def select_day(self, day):
        self.selected_day = day
        self.show_event_details()

    def day_has_event(self, day):
        # Aquí puedes verificar en la base de datos si el día tiene un evento
        start_date = datetime(self.year, self.month, day, 0, 0, 0)
        end_date = datetime(self.year, self.month, day, 23, 59, 59)
        events = session.query(Event).filter(
            Event.date.between(start_date, end_date)
        ).all()
        return len(events) > 0

    def show_event_details(self):
        for widget in self.details_frame.winfo_children():
            widget.destroy()

        selected_date = datetime(self.year, self.month, self.selected_day)

        header = ttk.Label(self.details_frame, text=f"Events for {selected_date.strftime('%B %d, %Y')}", font=("Arial", 15))
        header.pack(pady=10)

        events = session.query(Event).filter(
            Event.date.between(f"{self.year}-{self.month:02d}-{self.selected_day:02d} 00:00:00",
                               f"{self.year}-{self.month:02d}-{self.selected_day:02d} 23:59:59")
        ).all()
        if events:
            for event in events:
                event_label = ttk.Label(self.details_frame, text=f"{event.title} at {event.date.strftime('%H:%M')} - {event.location} ({'Online' if event.is_online else 'Offline'})")
                event_label.pack(pady=5)
        else:
            no_event_label = ttk.Label(self.details_frame, text="No events scheduled.")
            no_event_label.pack(pady=5)

        self.event_label = ttk.Label(self.details_frame, text="Event Name:")
        self.event_label.pack(pady=5)
        self.event_entry = ttk.Entry(self.details_frame)
        self.event_entry.pack(pady=5)

        self.time_label = ttk.Label(self.details_frame, text="Event Time (HH:MM):")
        self.time_label.pack(pady=5)
        self.time_entry = ttk.Entry(self.details_frame)
        self.time_entry.pack(pady=5)

        self.location_label = ttk.Label(self.details_frame, text="Location:")
        self.location_label.pack(pady=5)
        self.location_entry = ttk.Entry(self.details_frame)
        self.location_entry.pack(pady=5)

        self.is_online_var = tk.BooleanVar()
        self.is_online_check = ttk.Checkbutton(self.details_frame, text="Online", variable=self.is_online_var)
        self.is_online_check.pack(pady=5)

        self.save_button = ttk.Button(self.details_frame, text="Save Event", command=self.save_event)
        self.save_button.pack(pady=10)

    def save_event(self):
        event_name = self.event_entry.get()
        event_time = self.time_entry.get()
        location = self.location_entry.get()
        is_online = self.is_online_var.get()
        if event_name and event_time:
            try:
                event_datetime = datetime.strptime(f"{self.year}-{self.month}-{self.selected_day} {event_time}", "%Y-%m-%d %H:%M")
                new_event = Event(
                    title=event_name,
                    description="",
                    date=event_datetime,
                    location=location,
                    is_online=is_online,
                    organizer_id=self.organizer_id
                )
                session.add(new_event)
                session.commit()
                messagebox.showinfo("Success", f"Event '{event_name}' at {event_time} saved for {month_name[self.month]} {self.selected_day}, {self.year}")
                self.show_event_details()
                self.build_calendar()  # Redibujar el calendario para reflejar los cambios
            except ValueError:
                messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
        else:
            messagebox.showerror("Error", "Please enter both event name and time.")


if __name__ == "__main__":
    root = tk.Tk()
    app = Calendar(root, organizer_id=1)  # Asigna el organizer_id adecuado
    root.mainloop()
