# HBnB FrontEnd

A modern, responsive web frontend for the HBnB (Holberton BnB) vacation rental platform. This project provides a complete user interface for browsing, viewing, and reviewing vacation rental properties.

## 🌟 Features

- **Responsive Design**: Fully responsive layout that works on desktop, tablet, and mobile devices
- **Property Listings**: Browse available vacation rentals with real property images
- **Detailed Property Pages**: Individual pages for each property with comprehensive information
- **Review System**: View existing reviews and add new ones (login required)
- **User Authentication**: Login system integration
- **Modern UI**: Clean, modern interface with intuitive navigation

## 📁 Project Structure

```
FrontEnd/
├── index.html              # Home page with property listings
├── place2.html             # Modern City Apartment details
├── place3.html             # Beachfront Villa details  
├── place4.html             # Historic Downtown Loft details
├── place5.html             # Countryside Cottage details
├── place6.html             # Luxury Penthouse details
├── login.html              # User login page
├── styles.css              # Main stylesheet
├── images/                 # Property images and assets
│   ├── logo.png
│   ├── icon.png
│   ├── Cozy Mountain Cabin.png
│   ├── Modern City Apartment.png
│   ├── Beachfront Villa.png
│   ├── Historic Downtown Loft.png
│   ├── Countryside Cottage.png
│   └── Luxury Penthouse.png
└── README.md               # This file
```

## 🏠 Properties

The platform features 6 unique properties:

1. **Cozy Mountain Cabin** - $120/night
   - Mountain retreat with fireplace and hiking trails
   - Host: John Smith

2. **Modern City Apartment** - $200/night  
   - Downtown apartment with city views and modern amenities
   - Host: Jane Doe

3. **Beachfront Villa** - $350/night
   - Luxury beachfront property with private pool and ocean access
   - Host: Maria Rodriguez

4. **Historic Downtown Loft** - $180/night
   - Charming loft with exposed brick and historic character
   - Host: Alex Mercer

5. **Countryside Cottage** - $95/night
   - Peaceful rural retreat with garden and fireplace
   - Host: Emily Clark

6. **Luxury Penthouse** - $500/night
   - Ultra-modern penthouse with panoramic views and premium amenities
   - Host: James Brown

## 🎨 Design Features

### Responsive Layout
- CSS Grid and Flexbox for modern layout
- Mobile-first responsive design
- Consistent typography and spacing

### Visual Elements
- High-quality property images with SVG fallbacks
- Star rating system for reviews
- Modern card-based design
- Consistent color scheme and branding

### Interactive Features
- Hover effects on buttons and cards
- Form validation for login and reviews
- Dynamic review form (shows/hides based on login status)
- Smooth navigation between pages

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Local web server (optional, for development)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd holbertonschool-hbnb/part4/FrontEnd
   ```

2. **Open in browser**
   - Simply open `index.html` in your web browser
   - Or use a local development server:
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8000
   ```

3. **Navigate to the application**
   - Open `http://localhost:8000` (if using a server)
   - Or directly open the `index.html` file

## 📱 Usage

### Browsing Properties
1. Start at the home page (`index.html`)
2. Browse the 6 available properties
3. Click "View Details" on any property to see more information

### Viewing Property Details
- Each property has its own dedicated page
- View property images, descriptions, and amenities
- Read existing customer reviews
- See pricing and host information

### Adding Reviews
1. Navigate to any property details page
2. Scroll to the "Add Your Review" section
3. Login is required to submit reviews
4. Select a rating (1-5 stars) and write your comment

### User Authentication
- Click "Login" in the header to access the login page
- Enter credentials to authenticate
- Once logged in, you can add reviews to properties

## 🛠️ Technical Details

### Technologies Used
- **HTML5**: Semantic markup structure
- **CSS3**: Modern styling with Grid and Flexbox
- **JavaScript**: Interactive functionality and form handling
- **SVG**: Scalable fallback images
- **Base64**: Embedded fallback graphics

### Browser Support
- Chrome 60+
- Firefox 55+
- Safari 10+
- Edge 16+

### Performance Features
- Optimized images with fallbacks
- Efficient CSS with minimal dependencies
- Semantic HTML for accessibility
- Mobile-optimized responsive design

## 🎯 Features in Detail

### Property Cards
- Display property image, name, and price
- Hover effects for better user experience
- Direct links to detailed property pages

### Property Detail Pages
- Large property images with error handling
- Comprehensive property descriptions
- Amenity lists with data attributes
- Review sections with star ratings
- Add review functionality (login required)

### Review System
- Display existing reviews with user names and ratings
- Star rating display (★★★★★)
- Add review form with validation
- Login requirement for new reviews

### Responsive Design
- Mobile-first approach
- Flexible grid layouts
- Scalable images and text
- Touch-friendly interface elements

## 🔧 Customization

### Adding New Properties
1. Create a new `placeX.html` file following the existing template
2. Add property images to the `/images` directory
3. Update `index.html` to include the new property card
4. Update navigation links as needed

### Styling Changes
- Modify `styles.css` for global style changes
- CSS variables are used for consistent theming
- Responsive breakpoints can be adjusted in media queries

### Content Updates
- Property details can be modified in individual HTML files
- Review content is currently static but structured for dynamic updates
- Image paths and fallbacks can be updated as needed

## 📞 Support

For questions or issues:
- Check the existing documentation
- Review the code comments for implementation details
- Test in multiple browsers for compatibility issues

## 🤝 Contributing

When contributing to this project:
1. Follow the existing code structure and naming conventions
2. Test responsive design on multiple screen sizes
3. Ensure all images have proper fallbacks
4. Validate HTML and CSS
5. Test form functionality

## 👨‍💻 Author

**Hector**
- GitHub: [@hector](https://github.com/hector)
- Project: HBnB FrontEnd Development
- Role: Frontend Developer

## 📄 License

This project is part of the Holberton School curriculum.

---

**Last Updated**: January 2025  
**Author**: Hector
