import { useState, useEffect } from "react";
import API from "../services/api";

interface Lecturer {
  id: number;
  name: string;
  unavailable_slots: string[];
}

interface Room {
  id: string;
  capacity: number;
}

interface Timeslot {
  id: string;
  day: string;
  time: string;
}

interface Course {
  id: number;
  name: string;
  lecturer: string;
  group: string;
  students: number;
  capacity: number;
  room: string | null;
}

export default function DataManagement() {
  const [lecturers, setLecturers] = useState<Lecturer[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [timeslots, setTimeslots] = useState<Timeslot[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [activeTab, setActiveTab] = useState("lecturers");

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [lectRes, roomRes, timeRes, courseRes] = await Promise.all([
        API.get("/data/lecturers"),
        API.get("/data/rooms"),
        API.get("/data/timeslots"),
        API.get("/data/courses")
      ]);
      setLecturers(lectRes.data);
      setRooms(roomRes.data);
      setTimeslots(timeRes.data);
      setCourses(courseRes.data);
    } catch (error) {
      console.error("Error loading data:", error);
    }
  };

  return (
    <div className="p-6">
      <h2 className="text-2xl font-bold mb-6">Data Management</h2>

      <div className="mb-4">
        <nav className="flex space-x-4">
          {["lecturers", "rooms", "timeslots", "courses"].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded ${
                activeTab === tab ? "bg-blue-500 text-white" : "bg-gray-200"
              }`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1)}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === "lecturers" && (
        <LecturerManager lecturers={lecturers} onUpdate={loadData} />
      )}
      {activeTab === "rooms" && (
        <RoomManager rooms={rooms} onUpdate={loadData} />
      )}
      {activeTab === "timeslots" && (
        <TimeslotManager timeslots={timeslots} onUpdate={loadData} />
      )}
      {activeTab === "courses" && (
        <CourseManager courses={courses} lecturers={lecturers} rooms={rooms} onUpdate={loadData} />
      )}
    </div>
  );
}

function LecturerManager({ lecturers, onUpdate }: { lecturers: Lecturer[], onUpdate: () => void }) {
  const [form, setForm] = useState({ name: "", unavailable_slots: [] as string[] });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post("/data/lecturers", form);
      setForm({ name: "", unavailable_slots: [] });
      onUpdate();
    } catch (error) {
      console.error("Error adding lecturer:", error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await API.delete(`/data/lecturers/${id}`);
      onUpdate();
    } catch (error) {
      console.error("Error deleting lecturer:", error);
    }
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Lecturers</h3>
      <form onSubmit={handleSubmit} className="mb-6 p-4 border rounded">
        <div className="mb-2">
          <label className="block text-sm font-medium">Name</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({...form, name: e.target.value})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Add Lecturer
        </button>
      </form>

      <div className="space-y-2">
        {lecturers.map(lect => (
          <div key={lect.id} className="flex justify-between items-center p-2 border rounded">
            <span>{lect.name}</span>
            <button
              onClick={() => handleDelete(lect.id)}
              className="bg-red-500 text-white px-2 py-1 rounded"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function RoomManager({ rooms, onUpdate }: { rooms: Room[], onUpdate: () => void }) {
  const [form, setForm] = useState({ id: "", capacity: 0 });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post("/data/rooms", form);
      setForm({ id: "", capacity: 0 });
      onUpdate();
    } catch (error) {
      console.error("Error adding room:", error);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await API.delete(`/data/rooms/${id}`);
      onUpdate();
    } catch (error) {
      console.error("Error deleting room:", error);
    }
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Rooms</h3>
      <form onSubmit={handleSubmit} className="mb-6 p-4 border rounded">
        <div className="mb-2">
          <label className="block text-sm font-medium">Room ID</label>
          <input
            type="text"
            value={form.id}
            onChange={(e) => setForm({...form, id: e.target.value})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Capacity</label>
          <input
            type="number"
            value={form.capacity}
            onChange={(e) => setForm({...form, capacity: parseInt(e.target.value)})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Add Room
        </button>
      </form>

      <div className="space-y-2">
        {rooms.map(room => (
          <div key={room.id} className="flex justify-between items-center p-2 border rounded">
            <span>{room.id} (Capacity: {room.capacity})</span>
            <button
              onClick={() => handleDelete(room.id)}
              className="bg-red-500 text-white px-2 py-1 rounded"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function TimeslotManager({ timeslots, onUpdate }: { timeslots: Timeslot[], onUpdate: () => void }) {
  const [form, setForm] = useState({ id: "", day: "", time: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post("/data/timeslots", form);
      setForm({ id: "", day: "", time: "" });
      onUpdate();
    } catch (error) {
      console.error("Error adding timeslot:", error);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await API.delete(`/data/timeslots/${id}`);
      onUpdate();
    } catch (error) {
      console.error("Error deleting timeslot:", error);
    }
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Timeslots</h3>
      <form onSubmit={handleSubmit} className="mb-6 p-4 border rounded">
        <div className="mb-2">
          <label className="block text-sm font-medium">Timeslot ID</label>
          <input
            type="text"
            value={form.id}
            onChange={(e) => setForm({...form, id: e.target.value})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Day</label>
          <input
            type="text"
            value={form.day}
            onChange={(e) => setForm({...form, day: e.target.value})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Time</label>
          <input
            type="text"
            value={form.time}
            onChange={(e) => setForm({...form, time: e.target.value})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Add Timeslot
        </button>
      </form>

      <div className="space-y-2">
        {timeslots.map(slot => (
          <div key={slot.id} className="flex justify-between items-center p-2 border rounded">
            <span>{slot.id}: {slot.day} {slot.time}</span>
            <button
              onClick={() => handleDelete(slot.id)}
              className="bg-red-500 text-white px-2 py-1 rounded"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function CourseManager({ courses, lecturers, rooms, onUpdate }: {
  courses: Course[],
  lecturers: Lecturer[],
  rooms: Room[],
  onUpdate: () => void
}) {
  const [form, setForm] = useState({
    name: "",
    lecturer: "",
    group: "",
    students: 0,
    capacity: 0,
    room: ""
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post("/data/courses", form);
      setForm({ name: "", lecturer: "", group: "", students: 0, capacity: 0, room: "" });
      onUpdate();
    } catch (error) {
      console.error("Error adding course:", error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await API.delete(`/data/courses/${id}`);
      onUpdate();
    } catch (error) {
      console.error("Error deleting course:", error);
    }
  };

  return (
    <div>
      <h3 className="text-xl font-semibold mb-4">Courses</h3>
      <form onSubmit={handleSubmit} className="mb-6 p-4 border rounded">
        <div className="mb-2">
          <label className="block text-sm font-medium">Course Name</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({...form, name: e.target.value})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Lecturer</label>
          <select
            value={form.lecturer}
            onChange={(e) => setForm({...form, lecturer: e.target.value})}
            className="w-full p-2 border rounded"
            required
          >
            <option value="">Select Lecturer</option>
            {lecturers.map(l => <option key={l.id} value={l.name}>{l.name}</option>)}
          </select>
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Group</label>
          <input
            type="text"
            value={form.group}
            onChange={(e) => setForm({...form, group: e.target.value})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Students</label>
          <input
            type="number"
            value={form.students}
            onChange={(e) => setForm({...form, students: parseInt(e.target.value)})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Capacity</label>
          <input
            type="number"
            value={form.capacity}
            onChange={(e) => setForm({...form, capacity: parseInt(e.target.value)})}
            className="w-full p-2 border rounded"
            required
          />
        </div>
        <div className="mb-2">
          <label className="block text-sm font-medium">Room (Optional)</label>
          <select
            value={form.room}
            onChange={(e) => setForm({...form, room: e.target.value})}
            className="w-full p-2 border rounded"
          >
            <option value="">Select Room</option>
            {rooms.map(r => <option key={r.id} value={r.id}>{r.id}</option>)}
          </select>
        </div>
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Add Course
        </button>
      </form>

      <div className="space-y-2">
        {courses.map(course => (
          <div key={course.id} className="p-2 border rounded">
            <div className="flex justify-between items-center">
              <span>{course.name} - {course.lecturer} - {course.group}</span>
              <button
                onClick={() => handleDelete(course.id)}
                className="bg-red-500 text-white px-2 py-1 rounded"
              >
                Delete
              </button>
            </div>
            <div className="text-sm text-gray-600">
              Students: {course.students}, Capacity: {course.capacity}, Room: {course.room || 'Not assigned'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}