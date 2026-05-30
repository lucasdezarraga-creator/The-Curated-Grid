# 🎨 The Curated Grid: Interactive Museum Gallery

A highly polished, responsive web application designed to simulate a high-end modern art exhibition. This interactive platform features a physical wood-frame canvas simulation alongside a minimalist museum-style label placard that provides context for dynamically fetched AI-curated artworks.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![React](https://img.shields.io/badge/frontend-React-61dafb?logo=react)
![CSS3](https://img.shields.io/badge/styling-CSS3-1572b6?logo=css3)

---

## 🚀 Key Features

* **Dual-Layout Optimization (PC & Mobile):** * **Desktop:** Exhibits a high-end horizontal side-by-side arrangement. The text placard aligns neatly to the left of the physically matted and framed canvas.
  * **Mobile:** Dynamically adapts into a space-efficient vertical stack, prioritizing artwork visibility by shrinking frame margins and safely scaling the canvas bounds.
* **Collapsible Metadata Drawer:** Implements an interactive info drawer on mobile viewports. Extensive prompt logs are cleanly hidden by default behind a toggle button to prevent clutter, supporting internal text-scrolling properties for deep accessibility.
* **Native Touch-Gesture Event Handlers:** Smoothly tracks swipe velocities (`onTouchStart`, `onTouchMove`, `onTouchEnd`) for mobile clients to provide intuitive gesture navigation alongside classic paginated navigation arrows and tracking dots.
* **Asynchronous Data Safety Gates:** Prevents application runtime crashes by shielding multi-field text generation logic behind explicit conditional evaluation rendering barriers while JSON payloads finish fetching.

---

## 🛠️ Architecture & Technologies Used

* **Frontend Framework:** React (Functional components, Hooks ecosystem)
* **State Management:** `useState` (Slide indexes, touch-tracking coordinates, asynchronous dataset storage, mobile drawer toggles)
* **Lifecycle Management:** `useEffect` (Asynchronous JSON API data fetching, automatic cross-slide component state resets)
* **Layout Mechanics:** Flexbox Grid Architecture, CSS Media Queries, Viewport Units (`vh`/`vw`), Attribute Prioritization Layering

---

## Special Thanks
Thank you Google, Google Gemini, Diffuser, and Aesthetics Wiki for the help!

---

## 📁 Repository Directory Structure

```text
├── public/
│   ├── data/
│   │   └── The_Curated_Grid_painting_data.json  # Cur
