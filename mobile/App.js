import { Platform } from "react-native";

import { CaregiverMobileApp } from "./src/CaregiverMobileApp";

export default function App() {
  return <CaregiverMobileApp platform={Platform.OS} />;
}
