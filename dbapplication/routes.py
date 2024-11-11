from flask import render_template,redirect,url_for,flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import User
from models import (
    User, Footwear, ActivewearTops, Bottoms, Outerwear, RecoveryAndWellness,
    FootwearSubCategory, ActivewearSubCategory, BottomsSubCategory,
    OuterwearSubCategory, RecoverySubCategory, Accessories, Swimwear,
    CompressionWear, SpecialtySportswear, ProtectiveGear,
    AccessoriesSubCategory, SwimwearSubCategory, CompressionSubCategory,
    SpecialtySportswearSubCategory, ProtectiveGearSubCategory, Cart, Invoice, Report
)

import csv
import requests
from io import StringIO
import jwt
from datetime import datetime, timedelta
from sqlalchemy import func
from werkzeug.utils import secure_filename
import uuid
from PIL import Image
import os


def create_token(user_id,app):
    payload = {
        'sub': user_id,
        'iat': datetime.utcnow(),
        'exp': datetime.utcnow() + timedelta(minutes=15) 
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def extract_auth_token(authenticated_request):
    auth_header = authenticated_request.headers.get('Authorization')
    if auth_header:
        return auth_header.split(" ")[1]
    else:
        return None


def decode_token(token,app):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None



def register_routes(app, db,bcrypt):

    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'csv'}


    def validate_image(stream):
        try:
            img = Image.open(stream)
            img.verify()
            return True
        except Exception:
            return False

    def optimize_image(image_path, quality=85):
        try:
            img = Image.open(image_path)
            img.save(image_path, optimize=True, quality=quality)
        except Exception as e:
            print(f"Error optimizing image: {e}")

    def allowed_file(filename):
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


    def get_items_for_gender(gender):
        """
        Fetches all items for the specified gender across all subcategories.
        Returns a list of dictionaries containing item details.
        """
        items = []
        
        # Define a list of tuples with subcategory models and their category names
        subcategories = [
            (FootwearSubCategory, 'Footwear'),
            (ActivewearSubCategory, 'Activewear Tops'),
            (BottomsSubCategory, 'Bottoms'),
            (OuterwearSubCategory, 'Outerwear'),
            (RecoverySubCategory, 'Recovery & Wellness'),
            (AccessoriesSubCategory, 'Accessories'),
            (SwimwearSubCategory, 'Swimwear'),
            (CompressionSubCategory, 'Compression Wear'),
            (SpecialtySportswearSubCategory, 'Specialty Sportswear'),
            (ProtectiveGearSubCategory, 'Protective Gear')
        ]
        
        for model, category in subcategories:
            queried_items = model.query.filter_by(for_gender=gender).all()
            for item in queried_items:
                items.append({
                    'category': category,
                    'type': item.type,
                    'price': item.price,
                    'size': item.size,
                    'quantity': item.quantity,
                    'product_id': item.id,               # Ensure 'id' is correct
                    'product_type': model.__name__,      # e.g., 'FootwearSubCategory'
                    'image': item.image if item.image else 'default.jpg'  # Use image field
                })
        
        return items

    
    @app.route('/', methods = ['GET', 'POST'])
    def index():
        return render_template('index.html')
    
    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            hashed_password = bcrypt.generate_password_hash(password)
            user = User(username=username, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))



    @app.route('/messi/admin/bulk_upload', methods=['POST'])
    @login_required
    def bulk_upload():
        if current_user.uid != 1:
            flash("Access denied. Admins only.", 'danger')
            return redirect(url_for('index'))

        if 'bulk_csv' not in request.files:
            flash("No file part in the request.", 'danger')
            return redirect(url_for('admin'))

        file = request.files['bulk_csv']

        if file.filename == '':
            flash("No file selected.", 'danger')
            return redirect(url_for('admin'))

        if not allowed_file(file.filename):
            flash("Invalid file type. Please upload a CSV file.", 'danger')
            return redirect(url_for('admin'))

        try:
            # Read CSV content
            stream = StringIO(file.stream.read().decode("UTF8"), newline=None)
            csv_input = csv.DictReader(stream)

            required_fields = ['main_category', 'type', 'price', 'size', 'quantity', 'for_gender', 'image_url']
            for field in required_fields:
                if field not in csv_input.fieldnames:
                    flash(f"Missing required field: {field}", 'danger')
                    return redirect(url_for('admin'))

            success_count = 0
            failure_count = 0
            failure_messages = []

            # Mapping main categories to their models and main category tables
            main_category_models = {
                'footwear': FootwearSubCategory,
                'activewear_tops': ActivewearSubCategory,
                'bottoms': BottomsSubCategory,
                'outerwear': OuterwearSubCategory,
                'recovery_and_wellness': RecoverySubCategory,
                'accessories': AccessoriesSubCategory,
                'swimwear': SwimwearSubCategory,
                'compression_wear': CompressionSubCategory,
                'specialty_sportswear': SpecialtySportswearSubCategory,
                'protective_gear': ProtectiveGearSubCategory
            }

            main_category_table = {
                'footwear': Footwear,
                'activewear_tops': ActivewearTops,
                'bottoms': Bottoms,
                'outerwear': Outerwear,
                'recovery_and_wellness': RecoveryAndWellness,
                'accessories': Accessories,
                'swimwear': Swimwear,
                'compression_wear': CompressionWear,
                'specialty_sportswear': SpecialtySportswear,
                'protective_gear': ProtectiveGear
            }

            # Mapping main categories to their foreign key field names
            foreign_key_mapping = {
                'footwear': 'footwear_id',
                'activewear_tops': 'activewear_id',
                'bottoms': 'bottoms_id',
                'outerwear': 'outerwear_id',
                'recovery_and_wellness': 'recovery_id',
                'accessories': 'accessories_id',
                'swimwear': 'swimwear_id',
                'compression_wear': 'compression_wear_id',
                'specialty_sportswear': 'specialty_sportswear_id',
                'protective_gear': 'protective_gear_id'
            }

            for idx, row in enumerate(csv_input, start=1):
                main_category = row['main_category'].strip().lower()
                product_type = row['type'].strip()
                price = row['price'].strip()
                size = row['size'].strip()
                quantity = row['quantity'].strip()
                for_gender = row['for_gender'].strip()
                image_url = row.get('image_url', '').strip()  # image_url is optional

                # Validate main_category
                SubCategoryModel = main_category_models.get(main_category)
                MainCategoryModel = main_category_table.get(main_category)
                foreign_key_field = foreign_key_mapping.get(main_category)

                if not SubCategoryModel or not MainCategoryModel or not foreign_key_field:
                    failure_count += 1
                    failure_messages.append(f"Row {idx}: Invalid main category '{main_category}'.")
                    continue

                # Fetch the corresponding main category entry
                main_category_entry = MainCategoryModel.query.filter_by(type=product_type).first()
                if not main_category_entry:
                    # Create the main category entry
                    main_category_entry = MainCategoryModel(type=product_type, quantity=0)
                    db.session.add(main_category_entry)
                    db.session.commit()

                # Validate and convert price
                try:
                    price = float(price)
                    if price < 0:
                        raise ValueError
                except ValueError:
                    failure_count += 1
                    failure_messages.append(f"Row {idx}: Invalid price '{row['price']}'.")
                    continue

                # Validate and convert quantity
                try:
                    quantity = int(quantity)
                    if quantity < 0:
                        raise ValueError
                except ValueError:
                    failure_count += 1
                    failure_messages.append(f"Row {idx}: Invalid quantity '{row['quantity']}'.")
                    continue

                # Validate for_gender
                if for_gender not in ['Men', 'Women', 'Kids']:
                    failure_count += 1
                    failure_messages.append(f"Row {idx}: Invalid for_gender '{for_gender}'.")
                    continue

                # Handle image
                if image_url:
                    # Download image from image_url
                    try:
                        response = requests.get(image_url)
                        if response.status_code == 200:
                            image_filename = secure_filename(os.path.basename(image_url))
                            unique_filename = f"{uuid.uuid4().hex}_{image_filename}"
                            category_folder = os.path.join(app.root_path, 'static', 'images', main_category.lower())
                            os.makedirs(category_folder, exist_ok=True)
                            image_path = os.path.join(category_folder, unique_filename)

                            with open(image_path, 'wb') as img_file:
                                img_file.write(response.content)

                            # Optionally, optimize the image
                            optimize_image(image_path)

                            image_relative_path = f"{main_category.lower()}/{unique_filename}"
                        else:
                            raise Exception("Image URL could not be accessed.")
                    except Exception as e:
                        failure_count += 1
                        failure_messages.append(f"Row {idx}: Failed to download image from URL '{image_url}'. Error: {str(e)}")
                        continue
                else:
                    # Assign a default image
                    image_relative_path = "default.jpg"  # Ensure this default image exists in your static/images folder

                try:
                    # Create a new subcategory product with foreign key
                    # Dynamically set the foreign key based on main_category
                    product_data = {
                        "type": product_type,
                        "price": price,
                        "size": size,
                        "quantity": quantity,
                        "for_gender": for_gender,
                        "image": image_relative_path
                    }
                    product_data[foreign_key_field] = main_category_entry.id

                    new_product = SubCategoryModel(**product_data)

                    db.session.add(new_product)
                    # Optionally update main category quantity
                    main_category_entry.quantity += quantity
                    db.session.commit()
                    success_count += 1

                except Exception as e:
                    db.session.rollback()
                    failure_count += 1
                    failure_messages.append(f"Row {idx}: Database error: {str(e)}")
                    continue

            # Summary of Bulk Upload
            summary_message = f"Bulk Upload Completed: {success_count} succeeded, {failure_count} failed."
            flash(summary_message, 'info')

            if failure_messages:
                for message in failure_messages:
                    flash(message, 'warning')

            return redirect(url_for('admin'))

        except Exception as e:
            print(f"Bulk upload error: {e}")
            flash("An error occurred while processing the CSV file.", 'danger')
            return redirect(url_for('admin'))

            
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            try:
                user_data = request.get_json()
                
                if not user_data or 'username' not in user_data or 'password' not in user_data:
                    return jsonify({'error': 'Missing username or password'}), 400
                    
                username = user_data["username"]
                password = user_data["password"]

                existing_user = User.query.filter_by(username=username).first()
                if existing_user is None:
                    return jsonify({'error': 'Invalid credentials'}), 403
                    
                if not bcrypt.check_password_hash(existing_user.password, password):
                    return jsonify({'error': 'Invalid credentials'}), 403
                
                # Create JWT token
                token = create_token(existing_user.uid,app)
                
                # If you want to also maintain a session
                login_user(existing_user)
                
                return jsonify({
                    "token": token,
                    "username": existing_user.username
                }), 200
                
            except Exception as e:
                print(f"Login error: {e}")
                return jsonify({'error': 'Internal server error'}), 500

    
    
    
    @app.route('/logout')
    def logout():
        logout_user()
        return redirect(url_for('index'))
    


    ######admin page
   # routes.py

    # routes.py

    @app.route('/messi/admin')
    @login_required
    def admin():
        if current_user.uid != 1:
            flash("Access denied. Admins only.", 'danger')
            return redirect(url_for('index'))

        # Fetch all users and product categories
        users = User.query.all()
        footwear = Footwear.query.all()
        activewear_tops = ActivewearTops.query.all()
        bottoms = Bottoms.query.all()
        outerwear = Outerwear.query.all()
        recovery_and_wellness = RecoveryAndWellness.query.all()
        accessories = Accessories.query.all()
        swimwear = Swimwear.query.all()
        compression_wear = CompressionWear.query.all()
        specialty_sportswear = SpecialtySportswear.query.all()
        protective_gear = ProtectiveGear.query.all()
        invoices = Invoice.query.order_by(Invoice.date.desc()).all()

        # Subcategories
        footwear_subcategories = FootwearSubCategory.query.all()
        activewear_subcategories = ActivewearSubCategory.query.all()
        bottoms_subcategories = BottomsSubCategory.query.all()
        outerwear_subcategories = OuterwearSubCategory.query.all()
        recovery_subcategories = RecoverySubCategory.query.all()
        accessories_subcategories = AccessoriesSubCategory.query.all()
        swimwear_subcategories = SwimwearSubCategory.query.all()
        compression_subcategories = CompressionSubCategory.query.all()
        specialty_sportswear_subcategories = SpecialtySportswearSubCategory.query.all()
        protective_gear_subcategories = ProtectiveGearSubCategory.query.all()

        # Prepare subcategories data
        subcategories_data = {
            # ... (existing code)
        }

        return render_template('admin.html',
            users=users,
            footwear=footwear,
            activewear_tops=activewear_tops,
            bottoms=bottoms,
            outerwear=outerwear,
            recovery_and_wellness=recovery_and_wellness,
            accessories=accessories,
            swimwear=swimwear,
            compression_wear=compression_wear,
            specialty_sportswear=specialty_sportswear,
            protective_gear=protective_gear,
            footwear_subcategories=footwear_subcategories,
            activewear_subcategories=activewear_subcategories,
            bottoms_subcategories=bottoms_subcategories,
            outerwear_subcategories=outerwear_subcategories,
            recovery_subcategories=recovery_subcategories,
            accessories_subcategories=accessories_subcategories,
            swimwear_subcategories=swimwear_subcategories,
            compression_subcategories=compression_subcategories,
            specialty_sportswear_subcategories=specialty_sportswear_subcategories,
            protective_gear_subcategories=protective_gear_subcategories,
            invoices=invoices,
            subcategories_data=subcategories_data
        )



    # Route to Edit Item Price
    @app.route('/admin/edit_item', methods=['POST'])
    @login_required
    def edit_item():
        if current_user.uid != 1:
            flash("Access denied. Admins only.", 'danger')
            return redirect(url_for('index'))
        
        product_type = request.form.get('product_type')
        item_id = request.form.get('item_id')
        new_price = request.form.get('new_price')
        new_image = request.files.get('new_image')  # Get the uploaded image file

        if not all([product_type, item_id, new_price]):
            flash("Product type, item ID, and new price are required.", 'danger')
            return redirect(url_for('admin'))

        try:
            new_price = float(new_price)
            if new_price < 0:
                flash("Price cannot be negative.", 'danger')
                return redirect(url_for('admin'))
        except ValueError:
            flash("Invalid price format.", 'danger')
            return redirect(url_for('admin'))
        
        # Map product_type to the corresponding model
        model_mapping = {
            'footwear': Footwear,
            'footwear_subcategory': FootwearSubCategory,
            'activewear_tops': ActivewearTops,
            'activewear_subcategory': ActivewearSubCategory,
            'bottoms': Bottoms,
            'bottoms_subcategory': BottomsSubCategory,
            'outerwear': Outerwear,
            'outerwear_subcategory': OuterwearSubCategory,
            'recovery_and_wellness': RecoveryAndWellness,
            'recovery_subcategory': RecoverySubCategory,
            'accessories': Accessories,
            'accessories_subcategory': AccessoriesSubCategory,
            'swimwear': Swimwear,
            'swimwear_subcategory': SwimwearSubCategory,
            'compression_wear': CompressionWear,
            'compression_subcategory': CompressionSubCategory,
            'specialty_sportswear': SpecialtySportswear,
            'specialty_sportswear_subcategory': SpecialtySportswearSubCategory,
            'protective_gear': ProtectiveGear,
            'protective_gear_subcategory': ProtectiveGearSubCategory
        }

        model = model_mapping.get(product_type)
        if not model:
            flash("Invalid product type.", 'danger')
            return redirect(url_for('admin'))
        
        # Query the item
        item = model.query.get(int(item_id))
        if not item:
            flash("Item not found.", 'danger')
            return redirect(url_for('admin'))
        
        # Update the price
        item.price = new_price

        # Handle image upload if a new image is provided
        if new_image and allowed_file(new_image.filename):
            if not validate_image(new_image.stream):
                flash("Uploaded file is not a valid image.", 'danger')
                return redirect(url_for('admin'))
            
            # Reset stream position after validation
            new_image.stream.seek(0)
            
            filename = secure_filename(new_image.filename)
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            
            # Determine the main category based on product_type
            # Extract main category from product_type (e.g., 'footwear_subcategory' -> 'footwear')
            main_category_key = product_type.replace('_subcategory', '')
            category_folder = os.path.join(app.root_path, 'static', 'images', main_category_key.lower())
            os.makedirs(category_folder, exist_ok=True)
            
            image_path = os.path.join(category_folder, unique_filename)
            new_image.save(image_path)
            
            # Optimize the image
            optimize_image(image_path)
            
            # Optionally, delete the old image file if it exists and is not default
            if item.image and item.image != 'default.jpg':
                old_image_path = os.path.join(app.root_path, 'static', 'images', item.image)
                if os.path.exists(old_image_path):
                    try:
                        os.remove(old_image_path)
                    except Exception as e:
                        print(f"Error deleting old image: {e}")
            
            # Update the image path in the database
            item.image = f"{main_category_key.lower()}/{unique_filename}"
        
        elif new_image:
            # If an image was uploaded but it's invalid
            flash("Invalid image file.", 'danger')
            return redirect(url_for('admin'))
        
        try:
            db.session.commit()
            flash("Item updated successfully.", 'success')
            return redirect(url_for('admin'))
        except Exception as e:
            print(f"Error updating item: {e}")
            db.session.rollback()
            flash("An error occurred while updating the item.", 'danger')
            return redirect(url_for('admin'))


    # Route to Remove Item
    @app.route('/admin/remove_item', methods=['POST'])
    @login_required
    def remove_item():
        if current_user.uid != 1:
            flash("Access denied. Admins only.", 'danger')
            return redirect(url_for('index'))
        
        product_type = request.form.get('product_type')
        item_id = request.form.get('item_id')

        if not all([product_type, item_id]):
            flash("Invalid data provided for removal.", 'danger')
            return redirect(url_for('admin'))
        
        try:
            # Map product_type to the corresponding model
            model_mapping = {
                'footwear': Footwear,
                'footwear_subcategory': FootwearSubCategory,
                'activewear_tops': ActivewearTops,
                'activewear_subcategory': ActivewearSubCategory,
                'bottoms': Bottoms,
                'bottoms_subcategory': BottomsSubCategory,
                'outerwear': Outerwear,
                'outerwear_subcategory': OuterwearSubCategory,
                'recovery_and_wellness': RecoveryAndWellness,
                'recovery_subcategory': RecoverySubCategory,
                'accessories': Accessories,
                'accessories_subcategory': AccessoriesSubCategory,
                'swimwear': Swimwear,
                'swimwear_subcategory': SwimwearSubCategory,
                'compression_wear': CompressionWear,
                'compression_subcategory': CompressionSubCategory,
                'specialty_sportswear': SpecialtySportswear,
                'specialty_sportswear_subcategory': SpecialtySportswearSubCategory,
                'protective_gear': ProtectiveGear,
                'protective_gear_subcategory': ProtectiveGearSubCategory
            }

            model = model_mapping.get(product_type)
            if not model:
                flash("Invalid product type.", 'danger')
                return redirect(url_for('admin'))
            
            # Query the item
            item = model.query.get(int(item_id))
            if not item:
                flash("Item not found.", 'danger')
                return redirect(url_for('admin'))
            
            # Remove the item
            db.session.delete(item)
            db.session.commit()
            flash(f"{item.type} has been removed successfully.", 'success')
            return redirect(url_for('admin'))
        
        except Exception as e:
            print(f"Error removing item: {e}")
            db.session.rollback()
            flash("An error occurred while removing the item.", 'danger')
            return redirect(url_for('admin'))


    @app.route('/messi/admin/add_product', methods=['POST'])
    @login_required
    def add_product():
        if current_user.uid != 1:
            flash("Access denied. Admins only.", 'danger')
            return redirect(url_for('index'))


        main_category = request.form.get('main_category')
        product_type = request.form.get('type')
        price = request.form.get('price')
        size = request.form.get('size')
        quantity = request.form.get('quantity')
        for_gender = request.form.get('for_gender')
        image_file = request.files.get('image')


        if not all([main_category, product_type, price, size, quantity, for_gender, image_file]):
            flash("All fields are required.", 'danger')
            return redirect(url_for('admin'))


        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)

            category_folder = os.path.join(app.root_path, 'static', 'images', main_category.lower())
            os.makedirs(category_folder, exist_ok=True)

            image_path = os.path.join(category_folder, filename)
            image_file.save(image_path)
        else:
            flash("Invalid image file.", 'danger')
            return redirect(url_for('admin'))

        try:

            price = float(price)
            quantity = int(quantity)

            if price < 0 or quantity < 0:
                flash("Price and Quantity must be non-negative.", 'danger')
                return redirect(url_for('admin'))

            main_category_models = {
                'footwear': Footwear,
                'activewear_tops': ActivewearTops,
                'bottoms': Bottoms,
                'outerwear': Outerwear,
                'recovery_and_wellness': RecoveryAndWellness,
                'accessories': Accessories,
                'swimwear': Swimwear,
                'compression_wear': CompressionWear,
                'specialty_sportswear': SpecialtySportswear,
                'protective_gear': ProtectiveGear
            }

            subcategory_models = {
                'footwear': FootwearSubCategory,
                'activewear_tops': ActivewearSubCategory,
                'bottoms': BottomsSubCategory,
                'outerwear': OuterwearSubCategory,
                'recovery_and_wellness': RecoverySubCategory,
                'accessories': AccessoriesSubCategory,
                'swimwear': SwimwearSubCategory,
                'compression_wear': CompressionSubCategory,
                'specialty_sportswear': SpecialtySportswearSubCategory,
                'protective_gear': ProtectiveGearSubCategory
            }

            foreign_key_fields = {
                'footwear': 'footwear_id',
                'activewear_tops': 'activewear_id',
                'bottoms': 'bottoms_id',
                'outerwear': 'outerwear_id',
                'recovery_and_wellness': 'recovery_id',
                'accessories': 'accessories_id',
                'swimwear': 'swimwear_id',
                'compression_wear': 'compression_wear_id',
                'specialty_sportswear': 'specialty_sportswear_id',
                'protective_gear': 'protective_gear_id'
            }

            MainCategoryModel = main_category_models.get(main_category)
            SubCategoryModel = subcategory_models.get(main_category)
            foreign_key_field = foreign_key_fields.get(main_category)

            if not MainCategoryModel or not SubCategoryModel or not foreign_key_field:
                flash("Invalid main category selected.", 'danger')
                return redirect(url_for('admin'))

            # Get or create the main category item
            main_category_type = main_category.replace('_', ' ').title()
            main_category_item = MainCategoryModel.query.filter_by(type=main_category_type).first()
            if not main_category_item:
                main_category_item = MainCategoryModel(type=main_category_type, quantity=0)
                db.session.add(main_category_item)
                db.session.commit()

            # Create a new product in the selected subcategory
            new_product_data = {
                foreign_key_field: main_category_item.id,
                'type': product_type,
                'price': price,
                'size': size,
                'quantity': quantity,
                'for_gender': for_gender,
                'image': f"{main_category.lower()}/{filename}"  # Store relative path
            }
            new_product = SubCategoryModel(**new_product_data)

            db.session.add(new_product)
            db.session.commit()
            flash(f"Product '{product_type}' added successfully.", 'success')
            return redirect(url_for('admin'))

        except ValueError:
            flash("Invalid input for price or quantity.", 'danger')
            return redirect(url_for('admin'))
        except Exception as e:
            print(f"Error adding product: {e}")
            db.session.rollback()
            flash("An error occurred while adding the product.", 'danger')
            return redirect(url_for('admin'))



    @app.route('/messi/admin/generate_report', methods=['GET', 'POST'])
    @login_required
    def generate_report():
        if current_user.uid != 1:
            flash('Unauthorized access.', 'danger')
            return redirect(url_for('index'))

        if request.method == 'POST':
            try:
                # 1. Calculate Most Popular Product
                popular_product = db.session.query(
                    Invoice.product_id,
                    Invoice.product_type,
                    func.sum(Invoice.quantity).label('total_quantity')
                ).group_by(
                    Invoice.product_id, 
                    Invoice.product_type
                ).order_by(
                    func.sum(Invoice.quantity).desc()
                ).first()

                if not popular_product:
                    flash('No sales data available to generate report.', 'warning')
                    return redirect(url_for('admin'))

                # 2. Calculate Inventory Turnover
                # Get total sales value
                total_sales = db.session.query(
                    func.sum(Invoice.total_price)
                ).scalar() or 0

                # Get current inventory value (sum of price * quantity for all products)
                total_inventory_value = 0
                for model in [FootwearSubCategory, ActivewearSubCategory, BottomsSubCategory,
                            OuterwearSubCategory, RecoverySubCategory, AccessoriesSubCategory,
                            SwimwearSubCategory, CompressionSubCategory,
                            SpecialtySportswearSubCategory, ProtectiveGearSubCategory]:
                    inventory_value = db.session.query(
                        func.sum(model.price * model.quantity)
                    ).scalar() or 0
                    total_inventory_value += inventory_value

                inventory_turnover = total_sales / total_inventory_value if total_inventory_value > 0 else 0

                # 3. Generate Future Demand Prediction
                # Simple prediction based on sales trends
                thirty_days_ago = datetime.utcnow() - timedelta(days=30)
                recent_sales = db.session.query(
                    func.count(Invoice.invoice_id)
                ).filter(
                    Invoice.date >= thirty_days_ago
                ).scalar() or 0

                if recent_sales > 100:
                    future_demand = "High demand expected. Consider increasing inventory."
                elif recent_sales > 50:
                    future_demand = "Moderate demand expected. Current inventory levels should be sufficient."
                else:
                    future_demand = "Lower demand expected. Consider promotional activities."

                # 4. Create Report
                report = Report(
                    most_popular_product_id=popular_product.product_id,
                    most_popular_product_type=popular_product.product_type,
                    total_quantity=popular_product.total_quantity,
                    inventory_turnover=round(inventory_turnover, 2),
                    future_demand=future_demand
                )

                db.session.add(report)
                db.session.commit()

                flash('Inventory report generated successfully.', 'success')
                return redirect(url_for('view_report', report_id=report.id))

            except Exception as e:
                print(f"Error generating report: {e}")
                flash('An error occurred while generating the report.', 'danger')
                return redirect(url_for('admin'))

        # GET request - show form to generate report
        return render_template('generate_report.html')
    
    @app.route('/messi/admin/view_report/<int:report_id>')
    @login_required
    def view_report(report_id):
        if current_user.uid != 1:  # Ensure only admin can access
            flash('Unauthorized access.', 'danger')
            return redirect(url_for('index'))

        report = Report.query.get_or_404(report_id)
        
        # Get details of the most popular product
        popular_product = None
        if report.most_popular_product_type and report.most_popular_product_id:
            try:
                model = globals()[report.most_popular_product_type]
                popular_product = model.query.get(report.most_popular_product_id)
            except (KeyError, AttributeError):
                pass

        return render_template('view_report.html', 
                            report=report, 
                            popular_product=popular_product)

    @app.route('/men')
    def men():
        from models import Cart  # Local import to avoid circular dependency

        men_items = get_items_for_gender('Men')  # Utilize the existing function
        main_categories = [
            'All',
            'Footwear',
            'Activewear Tops',
            'Bottoms',
            'Outerwear',
            'Recovery & Wellness',
            'Accessories',
            'Swimwear',
            'Compression Wear',
            'Specialty Sportswear',
            'Protective Gear'
        ]
        cart_count = Cart.query.filter_by(user_id=current_user.uid).count() if current_user.is_authenticated else 0
        return render_template('men.html', men_items=men_items, main_categories=main_categories, cart_count=cart_count)




    @app.route('/women')
    def women():
        women_items = get_items_for_gender('Women')
        
        # Define main categories for filtering, including 'All'
        main_categories = [
            'All',
            'Footwear',
            'Activewear Tops',
            'Bottoms',
            'Outerwear',
            'Recovery & Wellness',
            'Accessories',
            'Swimwear',
            'Compression Wear',
            'Specialty Sportswear',
            'Protective Gear'
        ]
        
        return render_template('women.html', items=women_items, categories=main_categories)


    @app.route('/kids')
    def kids():
        kids_items = get_items_for_gender('Kids')
        
        # Define main categories for filtering, including 'All'
        main_categories = [
            'All',
            'Footwear',
            'Activewear Tops',
            'Bottoms',
            'Outerwear',
            'Recovery & Wellness',
            'Accessories',
            'Swimwear',
            'Compression Wear',
            'Specialty Sportswear',
            'Protective Gear'
        ]
        
        return render_template('kids.html', items=kids_items, categories=main_categories)



    @app.route("/add_to_cart", methods=["POST"])
    def add_to_cart():
        try:
            data = request.get_json()
            print("Received data in /add_to_cart:", data)  # Debugging line

            product_id = data.get('product_id')
            product_type = data.get('product_type')
            quantity = data.get('quantity', 1)

            if not product_id or not product_type:
                return jsonify({'error': 'Product ID and type are required.'}), 400

            # Local import to avoid circular dependency
            from models import Cart

            # Validate product_type corresponds to a valid model
            product_model = globals().get(product_type)
            if not product_model:
                return jsonify({'error': 'Invalid product type.'}), 400

            # Check if the product exists
            product = product_model.query.get(product_id)
            if not product:
                return jsonify({'error': 'Product not found.'}), 404

            if product.quantity < quantity:
                return jsonify({'error': 'Requested quantity exceeds available stock.'}), 400

            # Check if item is already in cart
            cart_item = Cart.query.filter_by(user_id=current_user.uid, product_type=product_type, product_id=product_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                new_cart_item = Cart(
                    user_id=current_user.uid,
                    product_type=product_type,
                    product_id=product_id,
                    quantity=quantity
                )
                db.session.add(new_cart_item)

            # Optionally, reduce the available stock immediately or upon checkout
            # product.quantity -= quantity

            db.session.commit()

            return jsonify({'message': f'Added {quantity} x {product.type} to cart.'}), 200

        except Exception as e:
            print(f"Error adding to cart: {e}")
            return jsonify({'error': 'An error occurred while adding the item to the cart.'}), 500



    @app.route("/cart", methods=["GET"])
    def view_cart():
        from models import Cart  # Local import

        cart_items = Cart.query.filter_by(user_id=current_user.uid).all()
        cart_details = []
        subtotal = 0

        for item in cart_items:
            product = item.get_product()
            if product:
                total_price = product.price * item.quantity
                subtotal += total_price
                cart_details.append({
                    'cart_id': item.id,
                    'product_id': item.product_id,
                    'product_type': item.product_type,
                    'name': product.type,
                    'price': product.price,
                    'size': product.size if hasattr(product, 'size') else 'N/A',
                    'quantity': item.quantity,
                    'total_price': total_price,
                    'image': f"images/{item.product_type.lower()}/{product.type.replace(' ', '_').lower()}.jpg"
                })

        return render_template('cart.html', cart=cart_details, subtotal=subtotal)


    @app.route("/cart/update", methods=["POST"])
    def update_cart():
        from models import Cart  # Local import

        try:
            data = request.get_json()
            cart_id = data.get('cart_id')
            new_quantity = data.get('quantity')

            if not cart_id or not new_quantity:
                return jsonify({'error': 'Cart ID and new quantity are required.'}), 400

            try:
                new_quantity = int(new_quantity)
                if new_quantity < 1:
                    return jsonify({'error': 'Quantity must be at least 1.'}), 400
            except ValueError:
                return jsonify({'error': 'Invalid quantity value.'}), 400

            cart_item = Cart.query.filter_by(id=cart_id, user_id=current_user.uid).first()
            if not cart_item:
                return jsonify({'error': 'Cart item not found.'}), 404

            product = cart_item.get_product()
            if not product:
                return jsonify({'error': 'Associated product not found.'}), 404

            if new_quantity > product.quantity:
                return jsonify({'error': 'Requested quantity exceeds available stock.'}), 400

            cart_item.quantity = new_quantity
            db.session.commit()

            total_price = product.price * cart_item.quantity

            # Calculate new subtotal
            subtotal = db.session.query(func.sum(product_model.price * Cart.quantity)).\
                join(product_model, (product_model.id == Cart.product_id)).\
                filter(Cart.user_id == current_user.uid).scalar() or 0

            return jsonify({
                'message': 'Cart updated successfully.',
                'total_price': total_price,
                'subtotal': subtotal
            }), 200

        except Exception as e:
            print(f"Error updating cart: {e}")
            return jsonify({'error': 'An error occurred while updating the cart.'}), 500


    @app.route("/cart/remove", methods=["POST"])
    def remove_from_cart():

        try:
            data = request.get_json()
            cart_id = data.get('cart_id')

            if not cart_id:
                return jsonify({'error': 'Cart ID is required.'}), 400

            cart_item = Cart.query.filter_by(id=cart_id, user_id=current_user.uid).first()
            if not cart_item:
                return jsonify({'error': 'Cart item not found.'}), 404

            db.session.delete(cart_item)
            db.session.commit()

            cart_items = Cart.query.filter_by(user_id=current_user.uid).all()
            subtotal = sum(
                [item.get_product().price * item.quantity for item in cart_items if item.get_product()]
            )

            return jsonify({'message': 'Item removed from cart.', 'subtotal': subtotal}), 200

        except Exception as e:
            print(f"Error removing from cart: {e}")
            return jsonify({'error': 'An error occurred while removing the item from the cart.'}), 500

    # Checkout Routes


    @app.route("/checkout", methods=["GET", "POST"])
    def checkout():
        cart_items = Cart.query.filter_by(user_id=current_user.uid).all()
        if not cart_items:
            flash('Your cart is empty.', 'info')
            return redirect(url_for('men'))

        cart_details = []
        subtotal = 0

        for item in cart_items:
            product = item.get_product()
            if product:
                total_price = product.price * item.quantity
                subtotal += total_price
                cart_details.append({
                    'cart_id': item.id,
                    'product_id': item.product_id,
                    'product_type': item.product_type,
                    'name': product.type,
                    'price': product.price,
                    'size': product.size if hasattr(product, 'size') else 'N/A',
                    'quantity': item.quantity,
                    'total_price': total_price,
                    'image': f"images/{item.product_type.lower()}/{product.type.replace(' ', '_').lower()}.jpg"
                })

        if request.method == 'POST':
            try:
                # Retrieve payment details from form
                card_number = request.form.get('card_number')
                expiration_date = request.form.get('expiration_date')
                cvv = request.form.get('cvv')
                cardholder_name = request.form.get('cardholder_name')

                # Simulate payment processing
                if not all([card_number, expiration_date, cvv, cardholder_name]):
                    flash('All payment fields are required.', 'danger')
                    return render_template('checkout.html', cart=cart_details, subtotal=subtotal)

                # Assume payment is successful

                # Create Invoice records and update stock
                for item in cart_items:
                    product = item.get_product()
                    if not product:
                        continue  # Skip if product not found

                    # Check stock
                    if item.quantity > product.quantity:
                        flash(f'Not enough stock for {product.type}.', 'danger')
                        return redirect(url_for('view_cart'))

                    # Deduct stock
                    product.quantity -= item.quantity

                    # Calculate total price
                    total_price = product.price * item.quantity

                    # Create Invoice
                    invoice = Invoice(
                        user_id=current_user.uid,
                        product_id=item.product_id,
                        product_type=item.product_type,
                        quantity=item.quantity,
                        price=product.price,
                        total_price=total_price,  # Populate total_price
                        status='Paid'  # Assuming payment is done
                    )
                    db.session.add(invoice)

                    # Remove item from cart
                    db.session.delete(item)

                db.session.commit()
                flash('Checkout successful! Your order has been placed.', 'success')
                return redirect(url_for('index'))

            except Exception as e:
                print(f"Error during checkout: {e}")
                db.session.rollback()
                flash('An error occurred during checkout. Please try again.', 'danger')
                return redirect(url_for('view_cart'))

        return render_template('checkout.html', cart=cart_details, subtotal=subtotal)



        
        
        # @app.route('/', methods =['GET', 'POST'])
        # def index():
        #     if request.method == 'GET':
        #         people = Person.query.all()
        #         return render_template('index.html', people=people)
        #     elif request.method =='POST':
        #         name = request.form.get('name')
        #         age = int(request.form.get('age'))
        #         job = request.form.get('job')
        #         person = Person(name=name, age=age, job=job) # here we are creating the new person that we want to add to our database
        #         db.session.add(person)
        #         db.session.commit()
        #         people = Person.query.all()
        #         return render_template('index.html', people=people)
        
        # @app.route('/delete/<pid>', methods=['DELETE'])
        # def delete(pid):
        #     Person.query.filter(Person.pid==pid).delete()
        #     db.session.commit()
        #     people = Person.query.all()
        #     return render_template('index.html', people=people)
        
        # @app.route('/details/<int:pid>')
        # def details(pid):
        #     person = Person.query.filter(Person.pid==pid).first()
        #     return render_template('detail.html', person= person)