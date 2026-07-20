# Mobile App Prototype

This folder starts the Android and iOS side of the Caregiver Dashboard using Expo and React Native. It is intentionally separate from the FastAPI web app so you can experiment with mobile layout, color, typography, and navigation without disrupting the working browser dashboard.

## Structure

```text
mobile/
  App.js                      Default Expo entry point
  App.android.jsx             Android-specific entry point
  App.ios.jsx                 iOS-specific entry point
  app.json                    Expo application configuration
  babel.config.js             Expo Babel configuration
  package.json                Mobile app dependencies and scripts
  src/
    CaregiverMobileApp.jsx    Shared mobile dashboard screen
    components/               Reusable design components
    data/                     Mobile sample data while API integration is pending
    theme/                    Design tokens for color and spacing experiments
```

## Run locally

From the `mobile/` folder:

```bash
npm install
npm run android
npm run ios
```

You can also run `npm run web` to preview the React Native layout in a browser while iterating on design. The Android and iOS entry files currently share the same dashboard screen but pass a platform label, making it easy to split behavior or styling later.

## Design exploration ideas

- Update `src/theme/tokens.js` to try different colors, spacing, and brand directions.
- Edit `src/components/DashboardCard.jsx` to test different card styles across the app.
- Replace `src/data/sampleCare.js` with API data from the FastAPI `/api/summary` endpoint when you are ready to connect mobile to the backend.
