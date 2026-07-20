import { StatusBar } from "expo-status-bar";
import { FlatList, Platform, SafeAreaView, ScrollView, StyleSheet, Text, View } from "react-native";

import { DashboardCard } from "./components/DashboardCard";
import { sampleCareData } from "./data/sampleCare";
import { colors, spacing } from "./theme/tokens";

const platformCopy = {
  android: "Android prototype",
  ios: "iOS prototype",
};

export function CaregiverMobileApp({ platform = Platform.OS }) {
  const platformLabel = platformCopy[platform] ?? "Mobile prototype";

  return (
    <SafeAreaView style={styles.safeArea}>
      <StatusBar style="dark" />
      <ScrollView contentContainerStyle={styles.container}>
        <View style={styles.header}>
          <Text style={styles.kicker}>{platformLabel}</Text>
          <Text style={styles.heading}>Caregiver Dashboard</Text>
          <Text style={styles.subheading}>
            A React Native starting point for exploring mobile care coordination design patterns.
          </Text>
        </View>

        <FlatList
          data={sampleCareData.stats}
          horizontal
          keyExtractor={(item) => item.label}
          showsHorizontalScrollIndicator={false}
          contentContainerStyle={styles.statsRow}
          renderItem={({ item }) => (
            <View style={styles.statPill}>
              <Text style={styles.statValue}>{item.value}</Text>
              <Text style={styles.statLabel}>{item.label}</Text>
            </View>
          )}
        />

        <DashboardCard title="Today's focus" tone="highlight">
          <Text style={styles.highlightTitle}>2 medication windows need attention</Text>
          <Text style={styles.highlightText}>
            Prioritize due-soon medications, high-priority tasks, and appointment transportation.
          </Text>
        </DashboardCard>

        <DashboardCard title="Patients">
          {sampleCareData.patients.map((patient) => (
            <View key={patient.name} style={styles.patientRow}>
              <View style={styles.avatar}>
                <Text style={styles.avatarText}>{patient.name.charAt(0)}</Text>
              </View>
              <View style={styles.patientCopy}>
                <Text style={styles.patientName}>{patient.name}</Text>
                <Text style={styles.patientMeta}>{patient.careLevel} · {patient.condition}</Text>
                <Text style={styles.patientAction}>{patient.nextAction}</Text>
              </View>
            </View>
          ))}
        </DashboardCard>

        <DashboardCard title="Care timeline">
          {sampleCareData.timeline.map((event) => (
            <View key={`${event.time}-${event.title}`} style={styles.timelineRow}>
              <Text style={styles.timelineTime}>{event.time}</Text>
              <View style={styles.timelineCopy}>
                <Text style={styles.timelineTitle}>{event.title}</Text>
                <Text style={styles.timelineDetail}>{event.detail}</Text>
              </View>
            </View>
          ))}
        </DashboardCard>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  safeArea: {
    backgroundColor: colors.background,
    flex: 1,
  },
  container: {
    padding: spacing.lg,
    paddingBottom: spacing.xl,
  },
  header: {
    marginBottom: spacing.lg,
  },
  kicker: {
    color: colors.primaryDark,
    fontSize: 13,
    fontWeight: "800",
    letterSpacing: 0.8,
    textTransform: "uppercase",
  },
  heading: {
    color: colors.text,
    fontSize: 34,
    fontWeight: "800",
    marginTop: spacing.xs,
  },
  subheading: {
    color: colors.muted,
    fontSize: 16,
    lineHeight: 24,
    marginTop: spacing.sm,
  },
  statsRow: {
    gap: spacing.sm,
    paddingBottom: spacing.md,
  },
  statPill: {
    backgroundColor: colors.card,
    borderColor: colors.border,
    borderRadius: 18,
    borderWidth: 1,
    minWidth: 118,
    padding: spacing.md,
  },
  statValue: {
    color: colors.primaryDark,
    fontSize: 26,
    fontWeight: "800",
  },
  statLabel: {
    color: colors.muted,
    fontSize: 13,
    marginTop: 2,
  },
  highlightTitle: {
    color: colors.card,
    fontSize: 21,
    fontWeight: "800",
  },
  highlightText: {
    color: "#dbeafe",
    fontSize: 15,
    lineHeight: 22,
    marginTop: spacing.sm,
  },
  patientRow: {
    flexDirection: "row",
    gap: spacing.md,
    paddingVertical: spacing.md,
  },
  avatar: {
    alignItems: "center",
    backgroundColor: colors.border,
    borderRadius: 20,
    height: 40,
    justifyContent: "center",
    width: 40,
  },
  avatarText: {
    color: colors.primaryDark,
    fontWeight: "800",
  },
  patientCopy: {
    flex: 1,
  },
  patientName: {
    color: colors.text,
    fontSize: 16,
    fontWeight: "800",
  },
  patientMeta: {
    color: colors.muted,
    marginTop: 2,
  },
  patientAction: {
    color: colors.text,
    lineHeight: 20,
    marginTop: spacing.xs,
  },
  timelineRow: {
    borderLeftColor: colors.border,
    borderLeftWidth: 3,
    flexDirection: "row",
    gap: spacing.md,
    paddingBottom: spacing.md,
    paddingLeft: spacing.md,
  },
  timelineTime: {
    color: colors.primaryDark,
    fontSize: 13,
    fontWeight: "800",
    width: 72,
  },
  timelineCopy: {
    flex: 1,
  },
  timelineTitle: {
    color: colors.text,
    fontWeight: "800",
  },
  timelineDetail: {
    color: colors.muted,
    lineHeight: 20,
    marginTop: 2,
  },
});
