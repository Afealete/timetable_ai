import { useState, useEffect } from "react";
import API from "../services/api";
import "./DataManagement.css";

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

interface ExamPeriod {
  id: string;
  day: string;
  time: string;
  duration: number;
}

interface Exam {
  id: number;
  course: string;
  duration: number;
  required_room_type: string | null;
}

export default function DataManagement() {
  const [lecturers, setLecturers] = useState<Lecturer[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [timeslots, setTimeslots] = useState<Timeslot[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [examPeriods, setExamPeriods] = useState<ExamPeriod[]>([]);
  const [exams, setExams] = useState<Exam[]>([]);
  const [activeTab, setActiveTab] = useState("lecturers");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [lectRes, roomRes, timeRes, courseRes, examPeriodRes, examRes] = await Promise.all([
        API.get("/data/lecturers"),
        API.get("/data/rooms"),
        API.get("/data/timeslots"),
        API.get("/data/courses"),
        API.get("/data/exam-periods"),
        API.get("/data/exams")
      ]);
      setLecturers(lectRes.data);
      setRooms(roomRes.data);
      setTimeslots(timeRes.data);
      setCourses(courseRes.data);
      setExamPeriods(examPeriodRes.data);
      setExams(examRes.data);
    } catch (error) {
      console.error("Error loading data:", error);
    }
  };

  return (
    <div className="data-management">
      <h2 className="dm-heading">Data Management</h2>

      <div className="dm-tab-wrapper">
        <nav className="dm-tab-list">
          {["lecturers", "rooms", "timeslots", "courses", "exam-periods", "exams"].map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`dm-tab-button ${activeTab === tab ? "active" : ""}`}
            >
              {tab.charAt(0).toUpperCase() + tab.slice(1).replace("-", " ")}
            </button>
          ))}
        </nav>
      </div>

      {activeTab === "lecturers" && (
        <LecturerManager lecturers={lecturers} onUpdate={loadData} error={error} setError={setError} />
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
      {activeTab === "exam-periods" && (
        <ExamPeriodManager examPeriods={examPeriods} onUpdate={loadData} />
      )}
      {activeTab === "exams" && (
        <ExamManager exams={exams} courses={courses} onUpdate={loadData} />
      )}
    </div>
  );
}

function LecturerManager({ lecturers, onUpdate, error, setError }: { lecturers: Lecturer[], onUpdate: () => void, error: string | null, setError: (error: string | null) => void }) {
  const [form, setForm] = useState({ name: "", unavailable_slots: [] as string[] });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Adding lecturer", form);
    try {
      await API.post("/data/lecturers", form);
      setForm({ name: "", unavailable_slots: [] });
      onUpdate();
    } catch (error) {
      console.error("Error adding lecturer:", error);
    }
  };

  const handleDelete = async (id: number) => {
    console.log("Deleting lecturer", id);
    try {
      await API.delete(`/data/lecturers/${id}`);
      onUpdate();
      setError(null);
    } catch (error: any) {
      console.error("Error deleting lecturer:", error);
      if (error.response && error.response.data && error.response.data.error) {
        setError(error.response.data.error);
      } else {
        setError("Failed to delete lecturer");
      }
    }
  };

  return (
    <div className="dm-card">
      <div className="dm-card-header">
        <h3 className="dm-card-title">Lecturers</h3>
      </div>
      <form onSubmit={handleSubmit} className="dm-form">
        <div className="dm-form-row">
          <label className="dm-label">Name</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({...form, name: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <button type="submit" className="dm-button dm-submit-button">
          Add Lecturer
        </button>
      </form>

      {error && <div className="dm-error">{error}</div>}

      <div className="dm-list">
        {lecturers.map(lect => (
          <div key={lect.id} className="dm-list-item">
            <span>{lect.name}</span>
            <button
              onClick={() => handleDelete(lect.id)}
              className="dm-button dm-delete-button"
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
    <div className="dm-card">
      <div className="dm-card-header">
        <h3 className="dm-card-title">Rooms</h3>
      </div>
      <form onSubmit={handleSubmit} className="dm-form">
        <div className="dm-form-row">
          <label className="dm-label">Room ID</label>
          <input
            type="text"
            value={form.id}
            onChange={(e) => setForm({...form, id: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Capacity</label>
          <input
            type="number"
            value={form.capacity}
            onChange={(e) => setForm({...form, capacity: parseInt(e.target.value)})}
            className="dm-input"
            required
          />
        </div>
        <button type="submit" className="dm-button dm-submit-button">
          Add Room
        </button>
      </form>

      <div className="dm-list">
        {rooms.map(room => (
          <div key={room.id} className="dm-list-item">
            <span>{room.id} (Capacity: {room.capacity})</span>
            <button
              onClick={() => handleDelete(room.id)}
              className="dm-button dm-delete-button"
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
    <div className="dm-card">
      <div className="dm-card-header">
        <h3 className="dm-card-title">Timeslots</h3>
      </div>
      <form onSubmit={handleSubmit} className="dm-form">
        <div className="dm-form-row">
          <label className="dm-label">Timeslot ID</label>
          <input
            type="text"
            value={form.id}
            onChange={(e) => setForm({...form, id: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Day</label>
          <input
            type="text"
            value={form.day}
            onChange={(e) => setForm({...form, day: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Time</label>
          <input
            type="text"
            value={form.time}
            onChange={(e) => setForm({...form, time: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <button type="submit" className="dm-button dm-submit-button">
          Add Timeslot
        </button>
      </form>

      <div className="dm-list">
        {timeslots.map(slot => (
          <div key={slot.id} className="dm-list-item">
            <span>{slot.id}: {slot.day} {slot.time}</span>
            <button
              onClick={() => handleDelete(slot.id)}
              className="dm-button dm-delete-button"
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
    <div className="dm-card">
      <div className="dm-card-header">
        <h3 className="dm-card-title">Courses</h3>
      </div>
      <form onSubmit={handleSubmit} className="dm-form">
        <div className="dm-form-row">
          <label className="dm-label">Course Name</label>
          <input
            type="text"
            value={form.name}
            onChange={(e) => setForm({...form, name: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Lecturer</label>
          <select
            value={form.lecturer}
            onChange={(e) => setForm({...form, lecturer: e.target.value})}
            className="dm-input"
            required
          >
            <option value="">Select Lecturer</option>
            {lecturers.map(l => <option key={l.id} value={l.name}>{l.name}</option>)}
          </select>
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Group</label>
          <input
            type="text"
            value={form.group}
            onChange={(e) => setForm({...form, group: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Students</label>
          <input
            type="number"
            value={form.students}
            onChange={(e) => setForm({...form, students: parseInt(e.target.value)})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Capacity</label>
          <input
            type="number"
            value={form.capacity}
            onChange={(e) => setForm({...form, capacity: parseInt(e.target.value)})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Room (Optional)</label>
          <select
            value={form.room}
            onChange={(e) => setForm({...form, room: e.target.value})}
            className="dm-input"
          >
            <option value="">Select Room</option>
            {rooms.map(r => <option key={r.id} value={r.id}>{r.id}</option>)}
          </select>
        </div>
        <button type="submit" className="dm-button dm-submit-button">
          Add Course
        </button>
      </form>

      <div className="dm-list">
        {courses.map(course => (
          <div key={course.id} className="dm-list-item dm-course-item">
            <div className="dm-row-between">
              <span>{course.name} - {course.lecturer} - {course.group}</span>
              <button
                onClick={() => handleDelete(course.id)}
                className="dm-button dm-delete-button"
              >
                Delete
              </button>
            </div>
            <div className="dm-course-details">
              Students: {course.students}, Capacity: {course.capacity}, Room: {course.room || 'Not assigned'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function ExamPeriodManager({ examPeriods, onUpdate }: { examPeriods: ExamPeriod[], onUpdate: () => void }) {
  const [form, setForm] = useState({ id: "", day: "", time: "", duration: 0 });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post("/data/exam-periods", form);
      setForm({ id: "", day: "", time: "", duration: 0 });
      onUpdate();
    } catch (error) {
      console.error("Error adding exam period:", error);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await API.delete(`/data/exam-periods/${id}`);
      onUpdate();
    } catch (error) {
      console.error("Error deleting exam period:", error);
    }
  };

  return (
    <div className="dm-card">
      <div className="dm-card-header">
        <h3 className="dm-card-title">Exam Periods</h3>
      </div>
      <form onSubmit={handleSubmit} className="dm-form">
        <div className="dm-form-row">
          <label className="dm-label">Period ID</label>
          <input
            type="text"
            value={form.id}
            onChange={(e) => setForm({...form, id: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Day</label>
          <input
            type="text"
            value={form.day}
            onChange={(e) => setForm({...form, day: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Time</label>
          <input
            type="text"
            value={form.time}
            onChange={(e) => setForm({...form, time: e.target.value})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Duration (minutes)</label>
          <input
            type="number"
            value={form.duration}
            onChange={(e) => setForm({...form, duration: parseInt(e.target.value)})}
            className="dm-input"
            required
          />
        </div>
        <button type="submit" className="dm-button dm-submit-button">
          Add Exam Period
        </button>
      </form>

      <div className="dm-list">
        {examPeriods.map(period => (
          <div key={period.id} className="dm-list-item">
            <span>{period.id}: {period.day} {period.time} ({period.duration}min)</span>
            <button
              onClick={() => handleDelete(period.id)}
              className="dm-button dm-delete-button"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}

function ExamManager({ exams, courses, onUpdate }: { exams: Exam[], courses: Course[], onUpdate: () => void }) {
  const [form, setForm] = useState({ course: "", duration: 0, required_room_type: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await API.post("/data/exams", form);
      setForm({ course: "", duration: 0, required_room_type: "" });
      onUpdate();
    } catch (error) {
      console.error("Error adding exam:", error);
    }
  };

  const handleDelete = async (id: number) => {
    try {
      await API.delete(`/data/exams/${id}`);
      onUpdate();
    } catch (error) {
      console.error("Error deleting exam:", error);
    }
  };

  return (
    <div className="dm-card">
      <div className="dm-card-header">
        <h3 className="dm-card-title">Exams</h3>
      </div>
      <form onSubmit={handleSubmit} className="dm-form">
        <div className="dm-form-row">
          <label className="dm-label">Course</label>
          <select
            value={form.course}
            onChange={(e) => setForm({...form, course: e.target.value})}
            className="dm-input"
            required
          >
            <option value="">Select Course</option>
            {courses.map(c => <option key={c.id} value={c.name}>{c.name}</option>)}
          </select>
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Duration (minutes)</label>
          <input
            type="number"
            value={form.duration}
            onChange={(e) => setForm({...form, duration: parseInt(e.target.value)})}
            className="dm-input"
            required
          />
        </div>
        <div className="dm-form-row">
          <label className="dm-label">Required Room Type (Optional)</label>
          <input
            type="text"
            value={form.required_room_type}
            onChange={(e) => setForm({...form, required_room_type: e.target.value})}
            className="dm-input"
          />
        </div>
        <button type="submit" className="dm-button dm-submit-button">
          Add Exam
        </button>
      </form>

      <div className="dm-list">
        {exams.map(exam => (
          <div key={exam.id} className="dm-list-item">
            <span>{exam.course} - {exam.duration}min {exam.required_room_type && `(${exam.required_room_type})`}</span>
            <button
              onClick={() => handleDelete(exam.id)}
              className="dm-button dm-delete-button"
            >
              Delete
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}