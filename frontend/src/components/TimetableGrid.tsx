const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

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
  timetableType?: "course" | "exam";
}

function parsePeriod(period: string) {
  const normalized = period.trim();
  const parts = normalized.split("-").map((p) => p.trim());
  if (parts.length !== 2) return null;

  const parseTime = (time: string) => {
    const cleaned = time.replace(/\s+/g, "").replace(/:00$/, "");
    const [hourStr, minuteStr] = cleaned.split(":");
    const hour = parseInt(hourStr, 10);
    const minute = minuteStr ? parseInt(minuteStr, 10) : 0;
    if (Number.isNaN(hour) || Number.isNaN(minute)) return null;
    return hour * 60 + minute;
  };

  const start = parseTime(parts[0]);
  const end = parseTime(parts[1]);
  if (start === null || end === null) return null;
  return { start, end };
}

function formatMinutes(minutes: number) {
  const hour = Math.floor(minutes / 60);
  const minute = minutes % 60;
  return `${hour.toString().padStart(2, "0")}:${minute.toString().padStart(2, "0")}`;
}

function normalizePeriod(period: string) {
  const parsed = parsePeriod(period);
  if (!parsed) return period.trim();
  return `${formatMinutes(parsed.start)}-${formatMinutes(parsed.end)}`;
}

function getDisplayPeriods(data: TimetableItem[], isExamTimetable: boolean) {
  const uniquePeriods = Array.from(
    new Set(
      data
        .map((item) => item.period)
        .filter(Boolean)
        .map((period) => normalizePeriod(period))
    )
  ) as string[];

  const sortedPeriods = uniquePeriods
    .map((period) => ({ period, parsed: parsePeriod(period) }))
    .filter((item) => item.parsed !== null)
    .sort((a, b) => (a.parsed!.start - b.parsed!.start))
    .map((item) => item.period);

  // For exam timetables, don't add breaks
  if (isExamTimetable) {
    return sortedPeriods;
  }

  // For course timetables, add breaks between gaps
  const displayPeriods: string[] = [];
  for (let i = 0; i < sortedPeriods.length; i++) {
    const current = sortedPeriods[i];
    displayPeriods.push(current);

    const currentParsed = parsePeriod(current);
    const nextParsed = sortedPeriods[i + 1] ? parsePeriod(sortedPeriods[i + 1]) : null;
    if (currentParsed && nextParsed && nextParsed.start > currentParsed.end) {
      displayPeriods.push(`${formatMinutes(currentParsed.end)}-${formatMinutes(nextParsed.start)}`);
    }
  }

  return displayPeriods;
}

export default function TimetableGrid({ data, timetableType = "course" }: Props) {
  if (!data || !Array.isArray(data) || data.length === 0) {
    return <div className="timetable-empty">No timetable data available</div>;
  }

  const isExamTimetable = timetableType === "exam";
  const periods = getDisplayPeriods(data, isExamTimetable);

  const getCell = (day: string, period: string) => {
    return data.filter(
      (item) => item.day === day && normalizePeriod(item.period) === normalizePeriod(period)
    );
  };

  const isBreakRow = (period: string) => {
    return data.every((item) => normalizePeriod(item.period) !== normalizePeriod(period));
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
        {periods.map((p) => {
          const breakRow = isBreakRow(p);
          return (
            <tr key={p} className={breakRow ? "break-row" : undefined}>
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
                    ) : breakRow ? (
                      <span className="break-cell">Break</span>
                    ) : (
                      <span className="empty-cell">-</span>
                    )}
                  </td>
                );
              })}
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}