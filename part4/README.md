# HBnB Front-End Implementation - Part 4

This directory contains the HTML and CSS implementation for the HBnB application, following the design specifications and requirements.

## Project Structure

```
part4/
├── index.html          # Main page - List of Places
├── login.html          # Login Form
├── place.html          # Place Details page
├── add_review.html     # Add Review Form
├── styles.css          # Main stylesheet
├── images/             # Image assets directory
│   ├── logo.png        # Application logo (placeholder)
│   └── icon.png        # Favicon (placeholder)
└── README.md          # This file
```

## Pages Implemented

### 1. Index Page (index.html)
- **Purpose**: Display a list of places as cards
- **Features**:
  - Responsive grid layout for place cards
  - Each card includes: name, price per night, "View Details" button
  - Uses semantic HTML5 structure with `<article>` for place cards
  - Required CSS classes: `place-card`, `details-button`

### 2. Login Page (login.html)
- **Purpose**: User authentication form
- **Features**:
  - Email and password input fields
  - Responsive form design
  - Form validation attributes (required, email type)
  - Uses semantic HTML5 form elements

### 3. Place Details Page (place.html)
- **Purpose**: Show detailed information about a specific place
- **Features**:
  - Place information with image, price, host, description
  - Amenities list
  - Reviews section with review cards
  - Add review functionality (shown when logged in)
  - Required CSS classes: `place-details`, `place-info`, `review-card`

### 4. Add Review Page (add_review.html)
- **Purpose**: Form for adding reviews (authenticated users only)
- **Features**:
  - Rating selection (1-5 stars)
  - Review text area
  - User name input
  - Form validation with JavaScript
  - Review guidelines section
  - Required CSS classes: `add-review`, `form`

## Design Specifications Met

### Required Structure Elements
- ✅ **Header**: Contains logo with class `logo` and login button with class `login-button`
- ✅ **Navigation Bar**: Links to index.html and login.html
- ✅ **Footer**: "All rights reserved" text
- ✅ **Main Content**: Uses semantic HTML5 `<main>` element

### Fixed Parameters Applied
- ✅ **Margin**: 20px for place and review cards
- ✅ **Padding**: 10px within place and review cards
- ✅ **Border**: 1px solid #ddd for place and review cards
- ✅ **Border Radius**: 10px for place and review cards

### CSS Classes Implemented
- ✅ `place-card` - Styling for place cards on index page
- ✅ `details-button` - Styling for "View Details" buttons
- ✅ `place-details` - Container for place detail information
- ✅ `place-info` - Place information layout
- ✅ `review-card` - Individual review styling
- ✅ `add-review` - Add review form container
- ✅ `form` - General form styling
- ✅ `login-button` - Header login/logout button
- ✅ `logo` - Application logo styling

## Features

### Responsive Design
- Mobile-first approach with breakpoints at 768px and 480px
- Grid layouts adjust for different screen sizes
- Navigation collapses on smaller screens

### Accessibility
- Semantic HTML5 elements (`<header>`, `<nav>`, `<main>`, `<article>`, `<section>`)
- Proper form labels and ARIA attributes
- Alt text for images
- Keyboard navigation support

### Image Handling
- Placeholder images with SVG fallbacks using `onerror` attribute
- Responsive image sizing with `object-fit: cover`
- Proper alt text for accessibility

### JavaScript Enhancements
- Form validation on add review page
- Authentication state handling (placeholder logic)
- User feedback with alerts and confirmations

## Color Palette
- Primary: #2c3e50 (Dark blue-gray)
- Secondary: #3498db (Blue)
- Success: #27ae60 (Green)
- Warning: #f39c12 (Orange)
- Background: #f8f9fa (Light gray)
- Cards: #ffffff (White)

## Typography
- Font Family: Arial, sans-serif
- Headings: Bold, color #2c3e50
- Body Text: Regular, color #333
- Links: Color #3498db with hover effects

## Browser Compatibility
- HTML5 and CSS3 features used
- Compatible with modern browsers (Chrome, Firefox, Safari, Edge)
- Responsive design works on mobile devices

## W3C Validation
All HTML pages are designed to pass W3C validation:
- Proper DOCTYPE declaration
- Semantic HTML5 structure
- Valid attributes and nesting
- Proper form elements and labels

## Future Enhancements
- JavaScript for dynamic content loading
- User authentication integration
- Real image upload functionality
- Search and filtering capabilities
- Interactive map integration
- Booking system integration

## Usage

1. Open `index.html` in a web browser to view the main page
2. Navigate through the pages using the navigation menu
3. All forms are ready for backend integration
4. Replace placeholder images in the `images/` directory with actual assets

## Notes
- The logo and favicon are currently placeholder files
- Authentication logic is stubbed with JavaScript placeholders
- Form submissions point to placeholder endpoints
- All CSS follows the specified fixed parameters
- Images include fallback SVG placeholders for better UX
