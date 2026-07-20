export const sampleCareData = {
  stats: [
    { label: "Patients", value: "3" },
    { label: "Open tasks", value: "8" },
    { label: "Meds due", value: "2" },
    { label: "Appointments", value: "4" },
  ],
  patients: [
    {
      name: "Avery Johnson",
      careLevel: "High touch",
      condition: "Post-op recovery",
      nextAction: "Check incision and pain level at 2:00 PM",
    },
    {
      name: "Maria Chen",
      careLevel: "Daily support",
      condition: "Diabetes management",
      nextAction: "Log glucose reading before dinner",
    },
    {
      name: "Samuel Ortiz",
      careLevel: "Wellness check",
      condition: "Hypertension",
      nextAction: "Confirm tomorrow's cardiology ride",
    },
  ],
  timeline: [
    { time: "9:00 AM", title: "Medication round", detail: "Metformin and Lisinopril due soon" },
    { time: "11:30 AM", title: "Home visit", detail: "Caregiver Elena assigned to Avery" },
    { time: "3:15 PM", title: "Vitals review", detail: "Blood pressure trend needs review" },
  ],
};
