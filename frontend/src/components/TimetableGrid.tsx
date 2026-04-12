const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];
const periods = [
  "08:00-10:00",
  "10:00-12:00",
  "12:00-14:00",
  "14:00-16:00"
];

interface TimetableItem {
  day: string;
  period: string;
  course?: string;
  lecturer?: string;
  room?: string;
  [key: string]: any;
}

interface Props {
  data: TimetableItem[];
}

export default function TimetableGrid({ data }: Props) {
  console.log("TimetableGrid RENDERED with data:", data);

  if (!data || !Array.isArray(data) || data.length === 0) {
    return <div className="timetable-empty">No timetable data available</div>;
  }

  const getCell = (day: string, period: string) => {
    return data.filter(
      (item) => item.day === day && item.period === period
    );
  };

  return (
    <table>
      <thead>
        <tr>
          <th>Time</th>
          {days.map((d) => (
            <th key={d}>{d}</th>
          ))}
        </tr>
      </thead>

      <tbody>
        {periods.map((p) => (
          <tr key={p}>
            <td><b>{p}</b></td>

            {days.map((d) => {
              const classes = getCell(d, p);

              return (
                <td key={d}>
                  {classes.length > 0 ? (
                    classes.map((c, i) => (
                      <div key={i} className="class-cell">
                        <b>{c.course || "N/A"}</b><br />
                        {c.lecturer || "No lecturer"}<br />
                        {c.room || "No room"}
                      </div>
                    ))
                  ) : (
                    <span className="empty-cell">-</span>
                  )}
                </td>
              );
            })}
          </tr>
        ))}
      </tbody>
    </table>
  );
}