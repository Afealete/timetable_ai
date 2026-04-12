interface Columns {
  course?: string;
  lecturer?: string;
  room?: string;
  capacity?: string;
  students?: string;
  group?: string;
}

interface Props {
  columns?: Columns;
  setColumns: React.Dispatch<React.SetStateAction<Columns>>;
}

export default function ColumnMapper({ columns = {}, setColumns }: Props) {
  return (
    <div className="column-mapper">
      <input
        className="column-input"
        placeholder="Course Column"
        value={columns.course || ""}
        onChange={e => setColumns(prev => ({ ...prev, course: e.target.value }))}
      />

      <input
        className="column-input"
        placeholder="Lecturer Column"
        value={columns.lecturer || ""}
        onChange={e => setColumns(prev => ({ ...prev, lecturer: e.target.value }))}
      />

      <input
        className="column-input"
        placeholder="Room Column"
        value={columns.room || ""}
        onChange={e => setColumns(prev => ({ ...prev, room: e.target.value }))}
      />

      <input
        className="column-input"
        placeholder="Capacity Column"
        value={columns.capacity || ""}
        onChange={e => setColumns(prev => ({ ...prev, capacity: e.target.value }))}
      />

      <input
        className="column-input"
        placeholder="Students Column"
        value={columns.students || ""}
        onChange={e => setColumns(prev => ({ ...prev, students: e.target.value }))}
      />

      <input
        placeholder="Group Column"
        value={columns.group || ""}
        onChange={e => setColumns(prev => ({ ...prev, group: e.target.value }))}
      />
    </div>
  );
}