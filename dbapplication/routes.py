from flask import render_template,redirect,url_for,flash, request
from flask_login import login_user, logout_user, current_user, login_required
from models import User
from models import (
    User, Footwear, ActivewearTops, Bottoms, Outerwear, RecoveryAndWellness,
    FootwearSubCategory, ActivewearSubCategory, BottomsSubCategory,
    OuterwearSubCategory, RecoverySubCategory, Accessories, Swimwear,
    CompressionWear, SpecialtySportswear, ProtectiveGear,
    AccessoriesSubCategory, SwimwearSubCategory, CompressionSubCategory,
    SpecialtySportswearSubCategory, ProtectiveGearSubCategory
)

def register_routes(app, db,bcrypt):
    
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
            return redirect(url_for('index'))
            
            
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            user = User.query.filter(User.username == username).first()
            if user:
                if bcrypt.check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('index'))
            
            else:
                return "Username Or password Incorrect"
    
    
    
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
        

    # app.py

    @app.route('/men')
    def men():
        footwear_items = FootwearSubCategory.query.filter_by(for_gender='Men').all()
        activewear_items = ActivewearSubCategory.query.filter_by(for_gender='Men').all()
        bottoms_items = BottomsSubCategory.query.filter_by(for_gender='Men').all()
        outerwear_items = OuterwearSubCategory.query.filter_by(for_gender='Men').all()
        recovery_items = RecoverySubCategory.query.filter_by(for_gender='Men').all()
        accessories_items = AccessoriesSubCategory.query.filter_by(for_gender='Men').all()
        swimwear_items = SwimwearSubCategory.query.filter_by(for_gender='Men').all()
        compression_items = CompressionSubCategory.query.filter_by(for_gender='Men').all()
        specialty_items = SpecialtySportswearSubCategory.query.filter_by(for_gender='Men').all()
        protective_gear_items = ProtectiveGearSubCategory.query.filter_by(for_gender='Men').all()
        
        men_items = {
            'Footwear': footwear_items,
            'Activewear Tops': activewear_items,
            'Bottoms': bottoms_items,
            'Outerwear': outerwear_items,
            'Recovery & Wellness': recovery_items,
            'Accessories': accessories_items,
            'Swimwear': swimwear_items,
            'Compression Wear': compression_items,
            'Specialty Sportswear': specialty_items,
            'Protective Gear': protective_gear_items
        }
        
        return render_template('men.html', men_items=men_items)


    @app.route('/women')
    @login_required
    def women():
        return render_template('women.html')

    @app.route('/kids')
    @login_required
    def kids():
        return render_template('kids.html')
    
    
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