from flask import render_template,redirect,url_for,flash, request, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from models import User
from models import (
    User, Footwear, ActivewearTops, Bottoms, Outerwear, RecoveryAndWellness,
    FootwearSubCategory, ActivewearSubCategory, BottomsSubCategory,
    OuterwearSubCategory, RecoverySubCategory, Accessories, Swimwear,
    CompressionWear, SpecialtySportswear, ProtectiveGear,
    AccessoriesSubCategory, SwimwearSubCategory, CompressionSubCategory,
    SpecialtySportswearSubCategory, ProtectiveGearSubCategory, Cart
)


import jwt
import datetime
from sqlalchemy import func


def create_token(user_id,app):
    payload = {
        'sub': user_id,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15) 
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
                    'image': f"{category.lower().replace(' & ', '_').replace(' ', '_')}/{item.type.replace(' ', '_').lower()}.jpg"
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
    @app.route('/messi/admin')
    @login_required
    def admin():
        id = current_user.uid
        if id == 1:
            users = User.query.all()
            footwear = Footwear.query.all()
            footwear_subcategories = FootwearSubCategory.query.all()
            activewear_tops = ActivewearTops.query.all()
            activewear_subcategories = ActivewearSubCategory.query.all()
            bottoms = Bottoms.query.all()
            bottoms_subcategories = BottomsSubCategory.query.all()
            outerwear = Outerwear.query.all()
            outerwear_subcategories = OuterwearSubCategory.query.all()
            recovery_and_wellness = RecoveryAndWellness.query.all()
            recovery_subcategories = RecoverySubCategory.query.all()
            accessories = Accessories.query.all()
            accessories_subcategories = AccessoriesSubCategory.query.all()
            swimwear = Swimwear.query.all()
            swimwear_subcategories = SwimwearSubCategory.query.all()
            compression_wear = CompressionWear.query.all()
            compression_subcategories = CompressionSubCategory.query.all()
            specialty_sportswear = SpecialtySportswear.query.all()
            specialty_sportswear_subcategories = SpecialtySportswearSubCategory.query.all()
            protective_gear = ProtectiveGear.query.all()
            protective_gear_subcategories = ProtectiveGearSubCategory.query.all()
            return render_template('admin.html', users=users,
        footwear=footwear,
        footwear_subcategories=footwear_subcategories,
        activewear_tops=activewear_tops,
        activewear_subcategories=activewear_subcategories,
        bottoms=bottoms,
        bottoms_subcategories=bottoms_subcategories,
        outerwear=outerwear,
        outerwear_subcategories=outerwear_subcategories,
        recovery_and_wellness=recovery_and_wellness,
        recovery_subcategories=recovery_subcategories,
        accessories=accessories,
        accessories_subcategories=accessories_subcategories,
        swimwear=swimwear,
        swimwear_subcategories=swimwear_subcategories,
        compression_wear=compression_wear,
        compression_subcategories=compression_subcategories,
        specialty_sportswear=specialty_sportswear,
        specialty_sportswear_subcategories=specialty_sportswear_subcategories,
        protective_gear=protective_gear,
        protective_gear_subcategories=protective_gear_subcategories)
        else:
            flash("must be admin")
            return redirect(url_for('index'))



    @app.route('/messi/admin/generate_report', methods=['GET', 'POST'])
    @login_required
    def generate_report():
        if current_user.role != 'admin':
            flash('Unauthorized access.', 'danger')
            return redirect(url_for('index'))

        if request.method == 'POST':
            # 1. Calculate Most Popular Product
            popular_product = db.session.query(
                Invoice.product_id,
                Invoice.product_type,
                func.sum(Invoice.quantity).label('total_quantity')
            ).group_by(Invoice.product_id, Invoice.product_type).order_by(func.sum(Invoice.quantity).desc()).first()

            if popular_product:
                most_popular_product_id = popular_product.product_id
                most_popular_product_type = popular_product.product_type
                total_quantity = popular_product.total_quantity
            else:
                most_popular_product_id = None
                most_popular_product_type = None
                total_quantity = 0

            # 2. Generate Future Demand (Placeholder Logic)
            future_demand = "Stable demand expected based on current sales trends."

            # 3. Create a Report Entry
            report = Report(
                most_popular_product_id=most_popular_product_id,
                most_popular_product_type=most_popular_product_type,
                future_demand=future_demand
            )
            db.session.add(report)
            db.session.commit()

            flash('Inventory report generated successfully.', 'success')
            return redirect(url_for('view_report', report_id=report.id))

        return render_template('generate_report.html')

    @app.route('/messi/admin/view_report/<int:report_id>')
    @login_required
    def view_report(report_id):
        if current_user.role != 'admin':
            flash('Unauthorized access.', 'danger')
            return redirect(url_for('index'))

        report = Report.query.get_or_404(report_id)

        # Fetch the most popular product details
        popular_product = None
        if report.most_popular_product_type and report.most_popular_product_id:
            try:
                # Dynamically get the model class based on product_type
                product_model = globals()[report.most_popular_product_type]
                popular_product = product_model.query.get(report.most_popular_product_id)
            except KeyError:
                popular_product = None

        return render_template('view_report.html', report=report, popular_product=popular_product, total_quantity=report.most_popular_product_id and report.total_quantity or 0)


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
            # Handle checkout logic (payment processing, stock deduction, invoice creation)
            try:
                for item in cart_items:
                    product = item.get_product()
                    if not product:
                        continue  # Skip if product not found

                    # Check stock again
                    if item.quantity > product.quantity:
                        flash(f'Not enough stock for {product.type}.', 'danger')
                        return redirect(url_for('view_cart'))

                    # Deduct stock
                    product.quantity -= item.quantity

                    # Create Invoice
                    invoice = Invoice(
                        user_id=current_user.uid,
                        product_id=item.product_id,
                        product_type=item.product_type,
                        quantity=item.quantity,
                        price=product.price,
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