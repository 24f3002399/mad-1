# mad-1

# **Flask Parking Management System**
This is a Flask-based web application for managing parking lots and users. The system allows admins to manage parking lots, view parking spot availability, and interact with users' reservations. Users can register, log in, reserve parking spots, and view their reservation details.

### Requirements
Python 3.x

##### Flask

SQLAlchemy

Matplotlib

Other dependencies are listed in the requirements.txt file.

### Features
User Registration & Login: Users can register and log in to their accounts.

Admin Features: Admin users can manage parking lots, including adding, editing, and deleting lots.

Parking Spot Reservation: Users can reserve available parking spots, view their reservation status, and release parking spots.

Parking Lot Overview: Admin users can see an overview of all parking spots, including their status (available/occupied).

Summary Reports: Visual reports (pie and bar charts) for both users and admins to see parking status.

### Routes
#### User Routes
/login: User login page. (POST/GET)

/register: User registration page. (POST/GET)

/Home_user/<int:id>: User home page, displaying current reservations.

/U_summary/<int:id>: User summary page, including reservation statistics with graphical reports.

/us_prof_edit/<int:id>: Edit user profile page. (POST/GET)

/book/<int:user_id>/<int:lot_id>: User reservation page for booking a parking spot.

/release/<int:user_id>/<int:spot_id>/<int:lot_id>: User page to release a reserved spot and calculate the parking cost.

#### Admin Routes
/admin: Admin home page with overview of parking lots and spots.

/admin_search: Admin search page to find users or parking lots.

/prof_edit/<int:id>: Admin page to edit user profiles. (POST/GET)

/add_lot/<int:id>: Admin page to add a new parking lot.

/edit_lot/<int:id>: Admin page to edit parking lot details.

/delete_lot/<int:id>: Admin page to delete a parking lot.

/ad_summary: Admin summary page with graphical representation of parking spot status.

#### Shared Routes
/view_spot/<int:lot_id>/<int:spot_id>: View details of a specific parking spot.

/us_search/<int:id>: User search for parking lots by location or pin code.

/ad_search: Admin search for users or parking lots by ID or address.

