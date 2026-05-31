# Studio Web Dashboard

In addition to the powerful desktop application, VisionStudioAI includes a modern web-based dashboard and landing page.

## Tech Stack

The web frontend is built using the latest industry standards:

- **React 19**: For a declarative and component-based UI.
- **TypeScript**: Ensuring type safety and maintainability.
- **Tailwind CSS 4**: For a utility-first, highly responsive design.
- **Framer Motion**: Powering smooth animations and transitions.
- **Vite**: The next-generation frontend tool for fast builds and HMR.

## Key Features

### Interactive Landing Page
A high-conversion landing page that introduces users to the VisionStudioAI ecosystem, featuring:
- Hero sections with smooth entry animations.
- Feature breakdowns using modern card layouts.
- Responsive navigation.

### Design Dashboard
A central hub for managing your design projects. It mirrors the aesthetic of the desktop app, providing a consistent experience across platforms.

## Development & Deployment

To run the web project locally:

```bash
cd studio-frontend
npm install
npm run dev
```

To build for production:

```bash
npm run build
```

The output will be in the `dist/` directory, ready to be hosted on any static site provider like Vercel, Netlify, or GitHub Pages.
