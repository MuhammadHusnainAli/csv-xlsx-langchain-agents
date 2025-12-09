import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

np.random.seed(42)
random.seed(42)

FIRST_NAMES = ['James', 'Mary', 'Robert', 'Patricia', 'John', 'Jennifer', 'Michael', 'Linda', 'David', 'Elizabeth',
               'William', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica', 'Thomas', 'Sarah', 'Christopher', 'Karen',
               'Charles', 'Lisa', 'Daniel', 'Nancy', 'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra',
               'Donald', 'Ashley', 'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
               'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa', 'Timothy', 'Deborah',
               'Ronald', 'Stephanie', 'Edward', 'Rebecca', 'Jason', 'Sharon', 'Jeffrey', 'Laura', 'Ryan', 'Cynthia',
               'Jacob', 'Kathleen', 'Gary', 'Amy', 'Nicholas', 'Angela', 'Eric', 'Shirley', 'Jonathan', 'Anna',
               'Stephen', 'Brenda', 'Larry', 'Pamela', 'Justin', 'Emma', 'Scott', 'Nicole', 'Brandon', 'Helen',
               'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Raymond', 'Christine', 'Gregory', 'Debra', 'Frank', 'Rachel',
               'Alexander', 'Carolyn', 'Patrick', 'Janet', 'Jack', 'Catherine', 'Dennis', 'Maria', 'Jerry', 'Heather']

LAST_NAMES = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez',
              'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin',
              'Lee', 'Perez', 'Thompson', 'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson',
              'Walker', 'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
              'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts',
              'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker', 'Cruz', 'Edwards', 'Collins', 'Reyes',
              'Stewart', 'Morris', 'Morales', 'Murphy', 'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper',
              'Peterson', 'Bailey', 'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson',
              'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza', 'Ruiz', 'Hughes',
              'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers', 'Long', 'Ross', 'Foster', 'Jimenez']

COMPANY_NAMES = ['Acme Corporation', 'GlobalTech Solutions', 'Pinnacle Industries', 'Vertex Dynamics', 'Quantum Enterprises',
                 'Atlas Manufacturing', 'Horizon Digital', 'Nexus Systems', 'Apex Innovations', 'Sterling Partners',
                 'Vanguard Holdings', 'Meridian Group', 'Catalyst Ventures', 'Summit Technologies', 'Eclipse Industries',
                 'Titan Corporation', 'Phoenix Global', 'Orion Networks', 'Silverline Solutions', 'Cobalt Systems',
                 'Fusion Dynamics', 'Prism Technologies', 'Zenith Corp', 'Nova Industries', 'Omega Enterprises',
                 'Delta Solutions', 'Alpha Tech', 'Beta Systems', 'Gamma Industries', 'Sigma Corporation']

CITIES = {
    'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 'San Antonio', 'San Diego',
            'Dallas', 'San Jose', 'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte', 'Seattle',
            'Denver', 'Boston', 'Nashville', 'Portland', 'Las Vegas', 'Atlanta', 'Miami', 'San Francisco'],
    'UK': ['London', 'Birmingham', 'Manchester', 'Glasgow', 'Liverpool', 'Bristol', 'Sheffield', 'Leeds', 'Edinburgh', 'Leicester'],
    'Germany': ['Berlin', 'Hamburg', 'Munich', 'Cologne', 'Frankfurt', 'Stuttgart', 'Dusseldorf', 'Leipzig', 'Dortmund', 'Essen'],
    'Canada': ['Toronto', 'Montreal', 'Vancouver', 'Calgary', 'Edmonton', 'Ottawa', 'Winnipeg', 'Quebec City', 'Hamilton', 'Victoria'],
    'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Canberra', 'Newcastle', 'Hobart', 'Darwin'],
    'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice', 'Nantes', 'Strasbourg', 'Montpellier', 'Bordeaux', 'Lille'],
    'Japan': ['Tokyo', 'Osaka', 'Nagoya', 'Sapporo', 'Fukuoka', 'Kobe', 'Kyoto', 'Kawasaki', 'Yokohama', 'Hiroshima'],
    'India': ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune', 'Ahmedabad', 'Jaipur', 'Lucknow']
}

UNIVERSITIES = ['Harvard University', 'Stanford University', 'MIT', 'Yale University', 'Princeton University',
                'Columbia University', 'University of Chicago', 'Duke University', 'Northwestern University',
                'Caltech', 'Johns Hopkins University', 'Cornell University', 'UCLA', 'UC Berkeley', 'NYU',
                'University of Michigan', 'Carnegie Mellon', 'Georgia Tech', 'University of Texas Austin',
                'University of Washington', 'Boston University', 'USC', 'Penn State', 'Ohio State University',
                'University of Florida', 'University of Illinois', 'Purdue University', 'Arizona State University']

TECH_PRODUCTS = {
    'Laptops': ['MacBook Pro 16"', 'MacBook Air M2', 'Dell XPS 15', 'Dell XPS 13', 'HP Spectre x360', 'Lenovo ThinkPad X1 Carbon',
                'ASUS ROG Zephyrus', 'Microsoft Surface Laptop 5', 'Razer Blade 15', 'Acer Swift 5'],
    'Monitors': ['Dell UltraSharp U2723QE', 'LG 27UK850-W', 'Samsung Odyssey G7', 'ASUS ProArt PA329CV', 'BenQ PD3220U',
                 'Apple Studio Display', 'ViewSonic VP2785-4K', 'HP Z27k G3', 'Acer Predator X27', 'MSI Optix MAG274QRF'],
    'Keyboards': ['Logitech MX Keys', 'Apple Magic Keyboard', 'Keychron K2', 'Das Keyboard 4', 'Corsair K95 RGB',
                  'Razer BlackWidow V3', 'SteelSeries Apex Pro', 'Ducky One 2', 'HHKB Professional Hybrid', 'Leopold FC660M'],
    'Mice': ['Logitech MX Master 3', 'Apple Magic Mouse', 'Razer DeathAdder V3', 'Logitech G Pro X Superlight',
             'SteelSeries Prime', 'Corsair Dark Core RGB', 'Zowie EC2', 'Pulsar X2', 'Finalmouse Starlight-12', 'Glorious Model O'],
    'Headphones': ['Sony WH-1000XM5', 'Apple AirPods Max', 'Bose QuietComfort 45', 'Sennheiser Momentum 4',
                   'Audio-Technica ATH-M50x', 'Beyerdynamic DT 770 Pro', 'AKG K371', 'Shure AONIC 50', 'Jabra Elite 85h', 'Bang & Olufsen H9'],
    'Webcams': ['Logitech C920', 'Logitech Brio 4K', 'Razer Kiyo Pro', 'Elgato Facecam', 'Dell UltraSharp Webcam',
                'Obsbot Tiny 4K', 'AVerMedia PW513', 'Microsoft LifeCam HD-3000', 'Anker PowerConf C300', 'Poly Studio P5'],
    'Servers': ['Dell PowerEdge R750', 'HP ProLiant DL380', 'Lenovo ThinkSystem SR650', 'Cisco UCS C220 M6',
                'Supermicro SuperServer', 'IBM Power System S922', 'Oracle Server X9-2', 'Fujitsu Primergy RX2540'],
    'Networking': ['Cisco Catalyst 9300', 'Juniper EX4300', 'Aruba 6300M', 'Meraki MS390', 'Ubiquiti UniFi Dream Machine',
                   'Netgear ProSAFE', 'TP-Link Omada', 'Fortinet FortiSwitch', 'HPE Aruba 2930F', 'Dell PowerSwitch']
}

BRANDS = {
    'Computing': ['Apple', 'Dell', 'HP', 'Lenovo', 'ASUS', 'Acer', 'Microsoft', 'Razer', 'MSI', 'Samsung'],
    'Peripherals': ['Logitech', 'Razer', 'Corsair', 'SteelSeries', 'HyperX', 'Keychron', 'Ducky', 'Zowie', 'Glorious', 'Pulsar'],
    'Audio': ['Sony', 'Bose', 'Sennheiser', 'Audio-Technica', 'Beyerdynamic', 'AKG', 'Shure', 'Jabra', 'Bang & Olufsen', 'JBL'],
    'Networking': ['Cisco', 'Juniper', 'Aruba', 'Meraki', 'Ubiquiti', 'Netgear', 'TP-Link', 'Fortinet', 'Palo Alto', 'F5']
}

SUPPLIERS = ['TechDistributors Inc', 'Global Supply Chain Co', 'Premier Electronics', 'Wholesale Tech Partners',
             'Digital Distribution Network', 'Enterprise Supply Solutions', 'Tech Logistics Group', 'Allied Electronics',
             'Component Source International', 'Direct Tech Supply', 'Ingram Micro', 'Tech Data Corporation',
             'Arrow Electronics', 'Avnet Inc', 'Synnex Corporation', 'D&H Distributing', 'ScanSource Inc']

MARKETING_CAMPAIGNS = ['Summer Sale 2024', 'Black Friday Deals', 'Cyber Monday Special', 'Back to School', 'Holiday Gift Guide',
                       'New Year Clearance', 'Spring Collection Launch', 'Tech Week Promotion', 'Flash Sale Friday',
                       'VIP Member Exclusive', 'Loyalty Rewards Event', 'Anniversary Sale', 'End of Season Clearance',
                       'Bundle & Save', 'Free Shipping Weekend', 'Early Bird Special', 'Limited Time Offer',
                       'Customer Appreciation Day', 'Refer a Friend Bonus', 'First Purchase Discount']

JOB_TITLES = {
    'Engineering': ['Software Engineer', 'Senior Software Engineer', 'Staff Engineer', 'Principal Engineer', 'Engineering Manager',
                    'DevOps Engineer', 'Site Reliability Engineer', 'Data Engineer', 'ML Engineer', 'Frontend Developer',
                    'Backend Developer', 'Full Stack Developer', 'QA Engineer', 'Security Engineer', 'Platform Engineer'],
    'Sales': ['Sales Representative', 'Account Executive', 'Sales Manager', 'Regional Sales Director', 'VP of Sales',
              'Business Development Rep', 'Enterprise Account Manager', 'Inside Sales Rep', 'Sales Operations Analyst'],
    'Marketing': ['Marketing Coordinator', 'Marketing Manager', 'Digital Marketing Specialist', 'Content Strategist',
                  'SEO Specialist', 'Social Media Manager', 'Brand Manager', 'Product Marketing Manager', 'CMO'],
    'Finance': ['Financial Analyst', 'Senior Accountant', 'Controller', 'FP&A Manager', 'CFO', 'Accounts Payable Specialist',
                'Tax Analyst', 'Treasury Analyst', 'Internal Auditor', 'Revenue Analyst'],
    'HR': ['HR Coordinator', 'HR Manager', 'Recruiter', 'Talent Acquisition Specialist', 'HR Business Partner',
           'Compensation Analyst', 'Learning & Development Manager', 'CHRO', 'Benefits Administrator'],
    'Operations': ['Operations Analyst', 'Operations Manager', 'Supply Chain Manager', 'Logistics Coordinator',
                   'Warehouse Manager', 'Procurement Specialist', 'COO', 'Process Improvement Manager']
}

def get_random_name():
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"

def get_random_email(name):
    first, last = name.lower().split()
    domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com', 'icloud.com', 'protonmail.com']
    formats = [f"{first}.{last}", f"{first}{last}", f"{first}_{last}", f"{first[0]}{last}", f"{first}{last[0]}"]
    return f"{random.choice(formats)}{random.randint(1, 99)}@{random.choice(domains)}"

def get_company_email(name, company):
    first, last = name.lower().split()
    domain = company.lower().replace(' ', '').replace(',', '')[:15] + '.com'
    return f"{first}.{last}@{domain}"

def generate_sales_data(num_rows=500):
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East', 'Africa']
    countries = {
        'North America': ['USA', 'Canada', 'Mexico'],
        'Europe': ['UK', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands'],
        'Asia Pacific': ['China', 'Japan', 'India', 'Australia', 'South Korea', 'Singapore'],
        'Latin America': ['Brazil', 'Argentina', 'Chile', 'Colombia'],
        'Middle East': ['UAE', 'Saudi Arabia', 'Qatar', 'Israel'],
        'Africa': ['South Africa', 'Nigeria', 'Egypt', 'Kenya']
    }
    
    all_products = []
    for category, products in TECH_PRODUCTS.items():
        for product in products:
            all_products.append((product, category))
    
    sales_channels = ['Direct Sales', 'Authorized Reseller', 'Online Store', 'Retail Partner', 'Government Contract']
    payment_methods = ['Visa', 'Mastercard', 'American Express', 'Wire Transfer', 'PayPal', 'Net 30', 'Net 60']
    
    data = []
    start_date = datetime(2022, 1, 1)
    
    for i in range(num_rows):
        region = random.choice(regions)
        country = random.choice(countries[region])
        city = random.choice(CITIES.get(country, CITIES['USA']))
        product, category = random.choice(all_products)
        brand = random.choice(BRANDS.get(category, BRANDS['Computing']))
        customer_name = get_random_name()
        sales_rep = get_random_name()
        
        base_price = random.uniform(50, 5000)
        quantity = random.randint(1, 100)
        discount = random.choice([0, 5, 10, 15, 20, 25])
        unit_price = round(base_price, 2)
        total_before_discount = unit_price * quantity
        discount_amount = round(total_before_discount * (discount / 100), 2)
        total_revenue = round(total_before_discount - discount_amount, 2)
        cost_ratio = random.uniform(0.4, 0.7)
        cost = round(total_revenue * cost_ratio, 2)
        profit = round(total_revenue - cost, 2)
        profit_margin = round((profit / total_revenue) * 100, 2) if total_revenue > 0 else 0
        
        order_date = start_date + timedelta(days=random.randint(0, 1000))
        ship_date = order_date + timedelta(days=random.randint(1, 14))
        
        data.append({
            'Order_ID': f'ORD-{100000 + i}',
            'Order_Date': order_date.strftime('%Y-%m-%d'),
            'Ship_Date': ship_date.strftime('%Y-%m-%d'),
            'Region': region,
            'Country': country,
            'City': city,
            'Postal_Code': f'{random.randint(10000, 99999)}',
            'Customer_ID': f'CUST-{random.randint(1000, 9999)}',
            'Customer_Name': customer_name,
            'Customer_Segment': random.choice(['Enterprise', 'SMB', 'Consumer', 'Government']),
            'Product_ID': f'PROD-{random.randint(1000, 9999)}',
            'Product_Name': product,
            'Category': category,
            'Sub_Category': category,
            'Brand': brand,
            'Supplier': random.choice(SUPPLIERS),
            'Sales_Channel': random.choice(sales_channels),
            'Sales_Rep_ID': f'REP-{random.randint(100, 500)}',
            'Sales_Rep_Name': sales_rep,
            'Quantity': quantity,
            'Unit_Price': unit_price,
            'Discount_Percent': discount,
            'Discount_Amount': discount_amount,
            'Total_Before_Discount': round(total_before_discount, 2),
            'Total_Revenue': total_revenue,
            'Cost_of_Goods': cost,
            'Gross_Profit': profit,
            'Profit_Margin_Percent': profit_margin,
            'Tax_Rate': random.choice([5, 7, 10, 12, 15, 18, 20]),
            'Tax_Amount': round(total_revenue * random.uniform(0.05, 0.2), 2),
            'Shipping_Cost': round(random.uniform(5, 200), 2),
            'Payment_Method': random.choice(payment_methods),
            'Payment_Status': random.choice(['Paid', 'Pending', 'Overdue', 'Partial']),
            'Order_Priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'Shipping_Mode': random.choice(['Standard Ground', 'Express', 'Same Day', 'Economy', 'Freight']),
            'Carrier': random.choice(['FedEx', 'UPS', 'DHL', 'USPS', 'Amazon Logistics']),
            'Return_Status': random.choice(['No Return', 'Returned', 'Partial Return']),
            'Customer_Rating': random.randint(1, 5),
            'NPS_Score': random.randint(-100, 100),
            'Lead_Time_Days': random.randint(1, 30),
            'Warehouse_Location': random.choice(['East Coast DC', 'West Coast DC', 'Central DC', 'European DC', 'Asian DC']),
            'Inventory_Level': random.randint(0, 1000),
            'Reorder_Point': random.randint(10, 100),
            'Quarter': f'Q{((order_date.month - 1) // 3) + 1}',
            'Fiscal_Year': order_date.year,
            'Week_Number': order_date.isocalendar()[1],
            'Is_Promotion': random.choice([True, False]),
            'Campaign_Name': random.choice(MARKETING_CAMPAIGNS) if random.random() > 0.5 else None,
            'Currency': random.choice(['USD', 'EUR', 'GBP', 'JPY', 'AUD']),
            'Exchange_Rate': round(random.uniform(0.8, 1.5), 4)
        })
    
    return pd.DataFrame(data)

def generate_hr_data(num_rows=400):
    education = ['High School', 'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'PhD', 'MBA']
    departments = list(JOB_TITLES.keys())
    
    data = []
    for i in range(num_rows):
        dept = random.choice(departments)
        job_title = random.choice(JOB_TITLES[dept])
        employee_name = get_random_name()
        manager_name = get_random_name()
        hire_date = datetime(2015, 1, 1) + timedelta(days=random.randint(0, 3000))
        birth_year = random.randint(1960, 2000)
        birth_date = datetime(birth_year, random.randint(1, 12), random.randint(1, 28))
        
        level_salaries = {
            'Coordinator': (45000, 65000), 'Specialist': (55000, 80000), 'Analyst': (60000, 90000),
            'Representative': (50000, 75000), 'Engineer': (80000, 140000), 'Developer': (75000, 130000),
            'Manager': (90000, 150000), 'Director': (130000, 200000), 'VP': (180000, 300000),
            'Senior': (90000, 150000), 'Staff': (120000, 180000), 'Principal': (150000, 220000),
            'Chief': (250000, 500000), 'C': (250000, 500000)
        }
        
        salary_range = (60000, 100000)
        for key, range_val in level_salaries.items():
            if key in job_title:
                salary_range = range_val
                break
        
        salary = random.randint(salary_range[0], salary_range[1])
        
        data.append({
            'Employee_ID': f'EMP-{10000 + i}',
            'First_Name': employee_name.split()[0],
            'Last_Name': employee_name.split()[1],
            'Full_Name': employee_name,
            'Email': get_company_email(employee_name, 'TechCorp'),
            'Phone': f'+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'Birth_Date': birth_date.strftime('%Y-%m-%d'),
            'Age': datetime.now().year - birth_year,
            'Hire_Date': hire_date.strftime('%Y-%m-%d'),
            'Department': dept,
            'Job_Title': job_title,
            'Manager_Name': manager_name,
            'Team_Size': random.randint(0, 15) if 'Manager' in job_title or 'Director' in job_title or 'VP' in job_title else 0,
            'Work_Location': random.choice(['New York Office', 'San Francisco HQ', 'Chicago Office', 'Austin Office', 'Seattle Office', 'Boston Office', 'Remote']),
            'Country': random.choice(['USA', 'Canada', 'UK', 'Germany', 'India']),
            'Employment_Type': random.choice(['Full-Time', 'Part-Time', 'Contract', 'Intern']),
            'Employment_Status': random.choice(['Active', 'On Leave', 'Terminated', 'Retired']),
            'Base_Salary': salary,
            'Bonus_Percent': random.choice([0, 5, 10, 15, 20, 25, 30]),
            'Stock_Options': random.randint(0, 10000),
            'Total_Compensation': round(salary * (1 + random.uniform(0, 0.3)), 2),
            'Education_Level': random.choice(education),
            'University': random.choice(UNIVERSITIES),
            'Major': random.choice(['Computer Science', 'Business Administration', 'Engineering', 'Finance', 'Marketing', 'Psychology', 'Economics', 'Data Science']),
            'Years_Experience': random.randint(0, 35),
            'Years_At_Company': (datetime.now() - hire_date).days // 365,
            'Performance_Rating': round(random.uniform(2.5, 5), 1),
            'Last_Review_Date': (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            'Training_Hours_YTD': random.randint(0, 200),
            'Certifications': random.choice(['AWS Certified', 'PMP', 'CPA', 'SHRM-CP', 'Google Analytics', 'Salesforce Admin', 'None']),
            'Skills': random.choice(['Python, SQL, AWS', 'Excel, PowerBI, SAP', 'Java, Kubernetes, Docker', 'Salesforce, HubSpot', 'Figma, Adobe CC']),
            'Projects_Completed': random.randint(0, 50),
            'Sick_Days_Used': random.randint(0, 15),
            'Vacation_Days_Used': random.randint(0, 25),
            'Vacation_Days_Remaining': random.randint(0, 20),
            'Overtime_Hours_YTD': random.randint(0, 200),
            'Remote_Work_Percent': random.choice([0, 20, 40, 60, 80, 100]),
            'Satisfaction_Score': random.randint(1, 10),
            'Engagement_Score': random.randint(1, 10),
            'Flight_Risk': random.choice(['Low', 'Medium', 'High']),
            'Promotion_Eligible': random.choice([True, False]),
            'Last_Promotion_Date': (datetime.now() - timedelta(days=random.randint(0, 1500))).strftime('%Y-%m-%d') if random.random() > 0.3 else None,
            'Health_Plan': random.choice(['Basic PPO', 'Standard PPO', 'Premium PPO', 'Family HMO', 'HSA Compatible']),
            'Retirement_Contribution_Percent': random.choice([0, 3, 5, 6, 8, 10, 15]),
            'Gender': random.choice(['Male', 'Female', 'Non-Binary', 'Prefer Not to Say']),
            'Emergency_Contact': get_random_name(),
            'Emergency_Phone': f'+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}'
        })
    
    return pd.DataFrame(data)

def generate_customer_data(num_rows=400):
    data = []
    for i in range(num_rows):
        customer_name = get_random_name()
        signup_date = datetime(2018, 1, 1) + timedelta(days=random.randint(0, 2000))
        last_purchase = signup_date + timedelta(days=random.randint(0, (datetime.now() - signup_date).days))
        country = random.choice(list(CITIES.keys()))
        city = random.choice(CITIES[country])
        
        data.append({
            'Customer_ID': f'CUST-{10000 + i}',
            'First_Name': customer_name.split()[0],
            'Last_Name': customer_name.split()[1],
            'Full_Name': customer_name,
            'Email': get_random_email(customer_name),
            'Phone': f'+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'Date_Of_Birth': (datetime(1950, 1, 1) + timedelta(days=random.randint(0, 20000))).strftime('%Y-%m-%d'),
            'Gender': random.choice(['Male', 'Female', 'Other', 'Prefer Not to Say']),
            'Address': f'{random.randint(1, 9999)} {random.choice(["Main St", "Oak Ave", "Park Blvd", "Elm Dr", "Cedar Ln", "Maple Way"])}',
            'City': city,
            'State': random.choice(['CA', 'NY', 'TX', 'FL', 'IL', 'PA', 'OH', 'GA', 'NC', 'MI']),
            'Postal_Code': f'{random.randint(10000, 99999)}',
            'Country': country,
            'Signup_Date': signup_date.strftime('%Y-%m-%d'),
            'Signup_Source': random.choice(['Website', 'Mobile App', 'Referral', 'Social Media', 'Trade Show', 'Partner']),
            'Customer_Segment': random.choice(['Premium', 'Standard', 'Basic', 'VIP', 'Enterprise']),
            'Customer_Status': random.choice(['Active', 'Inactive', 'Churned', 'At Risk']),
            'Account_Manager': get_random_name(),
            'Total_Orders': random.randint(0, 200),
            'Total_Revenue': round(random.uniform(0, 100000), 2),
            'Avg_Order_Value': round(random.uniform(20, 500), 2),
            'Last_Purchase_Date': last_purchase.strftime('%Y-%m-%d'),
            'Days_Since_Last_Purchase': (datetime.now() - last_purchase).days,
            'Purchase_Frequency': round(random.uniform(0.1, 5), 2),
            'Customer_Lifetime_Value': round(random.uniform(100, 50000), 2),
            'Acquisition_Cost': round(random.uniform(10, 500), 2),
            'Acquisition_Channel': random.choice(['Google Ads', 'Facebook Ads', 'Organic Search', 'Email Campaign', 'Referral Program', 'Direct']),
            'Preferred_Payment': random.choice(['Visa', 'Mastercard', 'PayPal', 'Apple Pay', 'American Express']),
            'Preferred_Channel': random.choice(['Email', 'SMS', 'Push Notification', 'Direct Mail']),
            'Email_Opt_In': random.choice([True, False]),
            'SMS_Opt_In': random.choice([True, False]),
            'Email_Open_Rate': round(random.uniform(0, 60), 2),
            'Email_Click_Rate': round(random.uniform(0, 20), 2),
            'Website_Visits_Monthly': random.randint(0, 50),
            'App_Sessions_Monthly': random.randint(0, 30),
            'Support_Tickets_Total': random.randint(0, 50),
            'Avg_Resolution_Time_Hours': round(random.uniform(1, 72), 2),
            'NPS_Score': random.randint(-100, 100),
            'Satisfaction_Score': round(random.uniform(1, 5), 1),
            'Reviews_Written': random.randint(0, 20),
            'Avg_Review_Rating': round(random.uniform(1, 5), 1),
            'Referrals_Made': random.randint(0, 20),
            'Loyalty_Points': random.randint(0, 50000),
            'Loyalty_Tier': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum', 'Diamond']),
            'Churn_Probability': round(random.uniform(0, 1), 4),
            'RFM_Segment': random.choice(['Champions', 'Loyal Customers', 'Potential Loyalists', 'New Customers', 'At Risk', 'Hibernating', 'Lost']),
            'Credit_Limit': round(random.uniform(500, 50000), 2),
            'Outstanding_Balance': round(random.uniform(0, 10000), 2),
            'Payment_History': random.choice(['Excellent', 'Good', 'Fair', 'Poor'])
        })
    
    return pd.DataFrame(data)

def generate_marketing_data(num_rows=250):
    channels = ['Google Ads', 'Facebook Ads', 'Instagram Ads', 'LinkedIn Ads', 'Twitter Ads', 'YouTube Ads', 'TikTok Ads', 'Email Marketing', 'Content Marketing', 'Affiliate Marketing']
    
    data = []
    for i in range(num_rows):
        campaign_start = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 800))
        impressions = random.randint(1000, 1000000)
        clicks = int(impressions * random.uniform(0.01, 0.1))
        conversions = int(clicks * random.uniform(0.01, 0.15))
        spend = round(random.uniform(100, 50000), 2)
        revenue = round(conversions * random.uniform(10, 500), 2)
        campaign_name = random.choice(MARKETING_CAMPAIGNS)
        campaign_manager = get_random_name()
        
        data.append({
            'Campaign_ID': f'CAMP-{10000 + i}',
            'Campaign_Name': campaign_name,
            'Campaign_Type': random.choice(['Brand Awareness', 'Lead Generation', 'Conversion', 'Retargeting', 'Product Launch']),
            'Channel': random.choice(channels),
            'Platform': random.choice(['Google', 'Meta', 'LinkedIn', 'Twitter', 'YouTube', 'TikTok', 'Mailchimp', 'HubSpot']),
            'Ad_Group_Name': f'{campaign_name} - {random.choice(["Broad", "Exact", "Phrase", "Interest", "Lookalike"])}',
            'Ad_Creative': f'{campaign_name} - {random.choice(["Video", "Image", "Carousel", "Text", "Story"])}',
            'Ad_Format': random.choice(['Banner 300x250', 'Banner 728x90', 'Video 15s', 'Video 30s', 'Carousel', 'Story', 'Native']),
            'Landing_Page': f'/campaigns/{campaign_name.lower().replace(" ", "-")}',
            'Target_Audience': random.choice(['18-24 Tech Enthusiasts', '25-34 Professionals', '35-44 Decision Makers', '45-54 Executives', 'B2B IT Managers']),
            'Target_Location': random.choice(['United States', 'North America', 'Europe', 'Asia Pacific', 'Global']),
            'Campaign_Manager': campaign_manager,
            'Start_Date': campaign_start.strftime('%Y-%m-%d'),
            'End_Date': (campaign_start + timedelta(days=random.randint(7, 90))).strftime('%Y-%m-%d'),
            'Status': random.choice(['Active', 'Paused', 'Completed', 'Draft']),
            'Budget_Total': round(random.uniform(500, 100000), 2),
            'Budget_Daily': round(random.uniform(50, 5000), 2),
            'Spend_Total': spend,
            'Impressions': impressions,
            'Reach': int(impressions * random.uniform(0.6, 0.95)),
            'Frequency': round(random.uniform(1, 10), 2),
            'Clicks': clicks,
            'CTR_Percent': round((clicks / impressions) * 100, 4) if impressions > 0 else 0,
            'CPC': round(spend / clicks, 2) if clicks > 0 else 0,
            'CPM': round((spend / impressions) * 1000, 2) if impressions > 0 else 0,
            'Conversions': conversions,
            'Conversion_Rate_Percent': round((conversions / clicks) * 100, 2) if clicks > 0 else 0,
            'Cost_Per_Conversion': round(spend / conversions, 2) if conversions > 0 else 0,
            'Revenue_Generated': revenue,
            'ROAS': round(revenue / spend, 2) if spend > 0 else 0,
            'Profit': round(revenue - spend, 2),
            'ROI_Percent': round(((revenue - spend) / spend) * 100, 2) if spend > 0 else 0,
            'Leads_Generated': random.randint(0, conversions * 2),
            'MQLs': random.randint(0, conversions),
            'SQLs': random.randint(0, int(conversions * 0.5)),
            'Video_Views': random.randint(0, impressions) if 'Video' in random.choice(['Video', 'Other']) else 0,
            'Video_Completion_Rate': round(random.uniform(20, 80), 2),
            'Engagement_Rate_Percent': round(random.uniform(0, 15), 2),
            'Social_Shares': random.randint(0, 1000),
            'Comments': random.randint(0, 500),
            'Bounce_Rate_Percent': round(random.uniform(20, 80), 2),
            'Avg_Session_Duration_Sec': round(random.uniform(30, 300), 2),
            'Pages_Per_Session': round(random.uniform(1, 10), 2),
            'Attribution_Model': random.choice(['Last Click', 'First Click', 'Linear', 'Time Decay', 'Data-Driven']),
            'Quality_Score': random.randint(1, 10),
            'Ad_Relevance': random.choice(['Above Average', 'Average', 'Below Average'])
        })
    
    return pd.DataFrame(data)

def generate_product_data(num_rows=200):
    data = []
    product_id = 10000
    
    for category, products in TECH_PRODUCTS.items():
        for product in products:
            if product_id >= 10000 + num_rows:
                break
            
            brand = random.choice(BRANDS.get(category, BRANDS['Computing']))
            base_cost = random.uniform(50, 800)
            retail_price = round(base_cost * random.uniform(1.3, 2.5), 2)
            
            data.append({
                'Product_ID': f'PROD-{product_id}',
                'SKU': f'SKU-{random.randint(100000, 999999)}',
                'Product_Name': product,
                'Product_Description': f'High-quality {product} from {brand}. Features premium build quality and excellent performance.',
                'Category': category,
                'Brand': brand,
                'Manufacturer': brand,
                'Supplier': random.choice(SUPPLIERS),
                'Cost_Price': round(base_cost, 2),
                'Wholesale_Price': round(base_cost * 1.2, 2),
                'Retail_Price': retail_price,
                'Sale_Price': round(retail_price * 0.85, 2) if random.random() > 0.5 else None,
                'Currency': 'USD',
                'Margin_Percent': round(((retail_price - base_cost) / retail_price) * 100, 2),
                'Tax_Rate_Percent': random.choice([0, 5, 7, 10]),
                'Weight_Kg': round(random.uniform(0.1, 15), 2),
                'Length_Cm': round(random.uniform(5, 60), 1),
                'Width_Cm': round(random.uniform(5, 40), 1),
                'Height_Cm': round(random.uniform(2, 30), 1),
                'Color': random.choice(['Space Gray', 'Silver', 'Black', 'White', 'Midnight Blue', 'Rose Gold']),
                'Warranty_Months': random.choice([12, 24, 36]),
                'Launch_Date': (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1400))).strftime('%Y-%m-%d'),
                'Status': random.choice(['Active', 'Inactive', 'Discontinued', 'Coming Soon']),
                'Stock_Quantity': random.randint(0, 5000),
                'Reorder_Level': random.randint(10, 200),
                'Lead_Time_Days': random.randint(3, 30),
                'Units_Sold_Total': random.randint(100, 50000),
                'Units_Sold_Last_30_Days': random.randint(10, 1000),
                'Revenue_Total': round(random.uniform(10000, 500000), 2),
                'Avg_Rating': round(random.uniform(3.5, 5), 2),
                'Review_Count': random.randint(50, 5000),
                'Return_Rate_Percent': round(random.uniform(1, 10), 2),
                'Is_Featured': random.choice([True, False]),
                'Is_Bestseller': random.choice([True, False]),
                'Page_Views_Monthly': random.randint(500, 50000),
                'Conversion_Rate_Percent': round(random.uniform(1, 8), 2),
                'Add_To_Cart_Rate_Percent': round(random.uniform(5, 25), 2),
                'Country_Of_Origin': random.choice(['USA', 'China', 'Taiwan', 'Japan', 'South Korea', 'Vietnam']),
                'UPC_Code': f'{random.randint(100000000000, 999999999999)}',
                'Image_URL': f'https://cdn.techstore.com/products/{product.lower().replace(" ", "-")}.jpg'
            })
            product_id += 1
    
    while len(data) < num_rows:
        category = random.choice(list(TECH_PRODUCTS.keys()))
        product = random.choice(TECH_PRODUCTS[category])
        brand = random.choice(BRANDS.get(category, BRANDS['Computing']))
        base_cost = random.uniform(50, 800)
        retail_price = round(base_cost * random.uniform(1.3, 2.5), 2)
        
        data.append({
            'Product_ID': f'PROD-{product_id}',
            'SKU': f'SKU-{random.randint(100000, 999999)}',
            'Product_Name': f'{product} {random.choice(["Pro", "Plus", "Elite", "Max", "Ultra"])}',
            'Product_Description': f'Premium {product} variant with enhanced features.',
            'Category': category,
            'Brand': brand,
            'Manufacturer': brand,
            'Supplier': random.choice(SUPPLIERS),
            'Cost_Price': round(base_cost, 2),
            'Wholesale_Price': round(base_cost * 1.2, 2),
            'Retail_Price': retail_price,
            'Sale_Price': round(retail_price * 0.85, 2) if random.random() > 0.5 else None,
            'Currency': 'USD',
            'Margin_Percent': round(((retail_price - base_cost) / retail_price) * 100, 2),
            'Tax_Rate_Percent': random.choice([0, 5, 7, 10]),
            'Weight_Kg': round(random.uniform(0.1, 15), 2),
            'Length_Cm': round(random.uniform(5, 60), 1),
            'Width_Cm': round(random.uniform(5, 40), 1),
            'Height_Cm': round(random.uniform(2, 30), 1),
            'Color': random.choice(['Space Gray', 'Silver', 'Black', 'White', 'Midnight Blue', 'Rose Gold']),
            'Warranty_Months': random.choice([12, 24, 36]),
            'Launch_Date': (datetime(2020, 1, 1) + timedelta(days=random.randint(0, 1400))).strftime('%Y-%m-%d'),
            'Status': random.choice(['Active', 'Inactive', 'Discontinued', 'Coming Soon']),
            'Stock_Quantity': random.randint(0, 5000),
            'Reorder_Level': random.randint(10, 200),
            'Lead_Time_Days': random.randint(3, 30),
            'Units_Sold_Total': random.randint(100, 50000),
            'Units_Sold_Last_30_Days': random.randint(10, 1000),
            'Revenue_Total': round(random.uniform(10000, 500000), 2),
            'Avg_Rating': round(random.uniform(3.5, 5), 2),
            'Review_Count': random.randint(50, 5000),
            'Return_Rate_Percent': round(random.uniform(1, 10), 2),
            'Is_Featured': random.choice([True, False]),
            'Is_Bestseller': random.choice([True, False]),
            'Page_Views_Monthly': random.randint(500, 50000),
            'Conversion_Rate_Percent': round(random.uniform(1, 8), 2),
            'Add_To_Cart_Rate_Percent': round(random.uniform(5, 25), 2),
            'Country_Of_Origin': random.choice(['USA', 'China', 'Taiwan', 'Japan', 'South Korea', 'Vietnam']),
            'UPC_Code': f'{random.randint(100000000000, 999999999999)}',
            'Image_URL': f'https://cdn.techstore.com/products/{product.lower().replace(" ", "-")}-v2.jpg'
        })
        product_id += 1
    
    return pd.DataFrame(data[:num_rows])

def generate_support_tickets_data(num_rows=350):
    issue_types = {
        'Technical': ['Software not installing', 'Device not turning on', 'Connectivity issues', 'Performance problems', 'Compatibility issues', 'Driver issues'],
        'Billing': ['Incorrect charge', 'Refund request', 'Payment failed', 'Invoice inquiry', 'Subscription cancellation', 'Pricing question'],
        'Shipping': ['Order not received', 'Wrong item delivered', 'Damaged package', 'Tracking not updating', 'Address change request', 'Expedite shipping'],
        'Returns': ['Return request', 'Exchange request', 'Warranty claim', 'Defective product', 'Wrong size/color', 'Changed mind'],
        'Account': ['Password reset', 'Account locked', 'Update information', 'Merge accounts', 'Delete account', 'Privacy concern']
    }
    
    data = []
    for i in range(num_rows):
        customer_name = get_random_name()
        agent_name = get_random_name()
        created_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 800))
        category = random.choice(list(issue_types.keys()))
        issue = random.choice(issue_types[category])
        
        all_products = []
        for cat_products in TECH_PRODUCTS.values():
            all_products.extend(cat_products)
        
        data.append({
            'Ticket_ID': f'TKT-{100000 + i}',
            'Customer_ID': f'CUST-{random.randint(10000, 99999)}',
            'Customer_Name': customer_name,
            'Customer_Email': get_random_email(customer_name),
            'Customer_Phone': f'+1-{random.randint(200, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}',
            'Customer_Tier': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
            'Created_Date': created_date.strftime('%Y-%m-%d'),
            'Created_Time': f'{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}',
            'Updated_Date': (created_date + timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d'),
            'Closed_Date': (created_date + timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d') if random.random() > 0.3 else None,
            'Status': random.choice(['Open', 'In Progress', 'Pending Customer', 'Resolved', 'Closed']),
            'Priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
            'Category': category,
            'Issue_Type': issue,
            'Subject': f'{issue} - {random.choice(all_products)}',
            'Product_Name': random.choice(all_products),
            'Order_ID': f'ORD-{random.randint(100000, 999999)}' if random.random() > 0.4 else None,
            'Channel': random.choice(['Email', 'Phone', 'Live Chat', 'Social Media', 'Web Form', 'Mobile App']),
            'Agent_ID': f'AGT-{random.randint(100, 999)}',
            'Agent_Name': agent_name,
            'Agent_Team': random.choice(['Tier 1 Support', 'Tier 2 Technical', 'Tier 3 Escalation', 'Billing Team', 'Returns Team']),
            'Department': random.choice(['Customer Support', 'Technical Support', 'Billing', 'Sales', 'Retention']),
            'Escalated': random.choice([True, False]),
            'Escalation_Level': random.randint(0, 3),
            'First_Response_Time_Hours': round(random.uniform(0.1, 24), 2),
            'Resolution_Time_Hours': round(random.uniform(1, 168), 2) if random.random() > 0.3 else None,
            'Handle_Time_Minutes': random.randint(5, 120),
            'Wait_Time_Minutes': random.randint(0, 60),
            'Interactions_Count': random.randint(1, 20),
            'Reopened_Count': random.randint(0, 5),
            'SLA_Breached': random.choice([True, False]),
            'SLA_Response_Met': random.choice([True, False]),
            'SLA_Resolution_Met': random.choice([True, False]),
            'CSAT_Score': random.randint(1, 5) if random.random() > 0.3 else None,
            'NPS_Response': random.randint(0, 10) if random.random() > 0.5 else None,
            'Resolution_Code': random.choice(['Resolved - Fixed', 'Resolved - Workaround', 'Resolved - Refunded', 'No Action Needed', 'Duplicate', 'Cannot Reproduce']),
            'Root_Cause': random.choice(['User Error', 'Software Bug', 'Hardware Defect', 'Documentation Gap', 'Process Issue', 'Third Party Issue']),
            'Sentiment': random.choice(['Positive', 'Neutral', 'Negative']),
            'Language': random.choice(['English', 'Spanish', 'French', 'German', 'Japanese', 'Portuguese']),
            'Country': random.choice(['USA', 'UK', 'Canada', 'Germany', 'France', 'Japan', 'Australia']),
            'First_Contact_Resolution': random.choice([True, False]),
            'Knowledge_Article_Used': random.choice(['KB-Setup Guide', 'KB-Troubleshooting', 'KB-Returns Policy', 'KB-Billing FAQ', None]),
            'Automation_Used': random.choice([True, False]),
            'Bot_Handled_Initially': random.choice([True, False])
        })
    
    return pd.DataFrame(data)

def generate_financial_data(num_rows=300):
    vendors = ['Amazon Web Services', 'Microsoft Azure', 'Google Cloud', 'Salesforce', 'Adobe Systems', 'Oracle Corporation',
               'SAP America', 'Workday Inc', 'ServiceNow', 'Zoom Video', 'Slack Technologies', 'Atlassian', 'HubSpot',
               'Zendesk', 'Twilio', 'Stripe Inc', 'Square Inc', 'DocuSign', 'Okta Inc', 'CrowdStrike']
    
    expense_categories = {
        'Software & SaaS': ['CRM License', 'ERP System', 'Cloud Hosting', 'Security Software', 'Productivity Suite'],
        'Marketing': ['Digital Advertising', 'Content Creation', 'Event Sponsorship', 'PR Services', 'Market Research'],
        'Operations': ['Office Supplies', 'Equipment Maintenance', 'Utilities', 'Insurance', 'Facilities'],
        'Travel': ['Airfare', 'Hotel', 'Ground Transportation', 'Meals', 'Conference Registration'],
        'Professional Services': ['Legal Fees', 'Consulting', 'Audit Services', 'Recruiting', 'Training']
    }
    
    data = []
    for i in range(num_rows):
        transaction_date = datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1000))
        category = random.choice(list(expense_categories.keys()))
        expense_type = random.choice(expense_categories[category])
        vendor = random.choice(vendors)
        approver = get_random_name()
        submitter = get_random_name()
        
        amount = round(random.uniform(100, 50000), 2)
        
        data.append({
            'Transaction_ID': f'TXN-{200000 + i}',
            'Transaction_Date': transaction_date.strftime('%Y-%m-%d'),
            'Posting_Date': (transaction_date + timedelta(days=random.randint(0, 5))).strftime('%Y-%m-%d'),
            'Account_Number': f'{random.randint(1000, 9999)}-{random.randint(100, 999)}',
            'Account_Name': expense_type,
            'Account_Type': random.choice(['Expense', 'Asset', 'Liability']),
            'Category': category,
            'Expense_Type': expense_type,
            'Cost_Center': random.choice(['Engineering', 'Sales', 'Marketing', 'Finance', 'HR', 'Operations', 'Executive']),
            'Department': random.choice(['Engineering', 'Sales', 'Marketing', 'Finance', 'HR', 'Operations']),
            'Project_Code': f'PRJ-{random.choice(["Website Redesign", "Q4 Campaign", "Infrastructure Upgrade", "New Product Launch", "Cost Optimization"])}',
            'Amount': amount,
            'Currency': random.choice(['USD', 'EUR', 'GBP']),
            'Exchange_Rate': round(random.uniform(0.85, 1.15), 4),
            'Amount_USD': round(amount * random.uniform(0.9, 1.1), 2),
            'Vendor_Name': vendor,
            'Vendor_ID': f'VND-{random.randint(1000, 9999)}',
            'Invoice_Number': f'INV-{random.randint(100000, 999999)}',
            'PO_Number': f'PO-{random.randint(10000, 99999)}',
            'Payment_Terms': random.choice(['Net 15', 'Net 30', 'Net 45', 'Net 60', 'Due on Receipt']),
            'Due_Date': (transaction_date + timedelta(days=random.randint(15, 60))).strftime('%Y-%m-%d'),
            'Payment_Status': random.choice(['Paid', 'Pending', 'Overdue', 'Scheduled']),
            'Payment_Method': random.choice(['ACH Transfer', 'Wire Transfer', 'Corporate Card', 'Check', 'Virtual Card']),
            'Bank_Account': random.choice(['Chase Operating', 'BofA Payroll', 'Wells Fargo Reserve', 'Citi Business']),
            'Reconciled': random.choice([True, False]),
            'Approved_By': approver,
            'Submitted_By': submitter,
            'Approval_Date': (transaction_date + timedelta(days=random.randint(0, 3))).strftime('%Y-%m-%d'),
            'Fiscal_Year': transaction_date.year,
            'Fiscal_Quarter': f'Q{((transaction_date.month - 1) // 3) + 1}',
            'Fiscal_Period': transaction_date.strftime('%Y-%m'),
            'Budget_Code': f'BUD-{category[:3].upper()}-{transaction_date.year}',
            'Budgeted_Amount': round(amount * random.uniform(0.8, 1.2), 2),
            'Variance': round(random.uniform(-5000, 5000), 2),
            'Variance_Percent': round(random.uniform(-20, 20), 2),
            'Tax_Amount': round(amount * random.uniform(0, 0.1), 2),
            'Description': f'{expense_type} - {vendor}',
            'Receipt_Attached': random.choice([True, False]),
            'Audit_Status': random.choice(['Approved', 'Pending Review', 'Flagged', 'Cleared']),
            'Notes': f'Monthly {expense_type.lower()} expense' if random.random() > 0.5 else None
        })
    
    return pd.DataFrame(data)

def generate_inventory_data(num_rows=350):
    warehouses = {
        'WH-EAST': {'name': 'East Coast Distribution Center', 'city': 'Newark', 'state': 'NJ'},
        'WH-WEST': {'name': 'West Coast Distribution Center', 'city': 'Los Angeles', 'state': 'CA'},
        'WH-CENTRAL': {'name': 'Central Distribution Hub', 'city': 'Dallas', 'state': 'TX'},
        'WH-SOUTH': {'name': 'Southern Fulfillment Center', 'city': 'Atlanta', 'state': 'GA'},
        'WH-NORTH': {'name': 'Northern Distribution Center', 'city': 'Chicago', 'state': 'IL'}
    }
    
    data = []
    sku_counter = 100000
    
    for category, products in TECH_PRODUCTS.items():
        for product in products:
            for wh_id, wh_info in warehouses.items():
                if len(data) >= num_rows:
                    break
                
                brand = random.choice(BRANDS.get(category, BRANDS['Computing']))
                unit_cost = round(random.uniform(50, 800), 2)
                
                data.append({
                    'SKU': f'SKU-{sku_counter}',
                    'Product_Name': product,
                    'Brand': brand,
                    'Category': category,
                    'Supplier': random.choice(SUPPLIERS),
                    'Warehouse_ID': wh_id,
                    'Warehouse_Name': wh_info['name'],
                    'Warehouse_City': wh_info['city'],
                    'Warehouse_State': wh_info['state'],
                    'Zone': random.choice(['A', 'B', 'C', 'D']),
                    'Aisle': f'{random.randint(1, 20)}',
                    'Rack': f'{random.randint(1, 50)}',
                    'Bin': f'{random.choice(["A", "B", "C", "D"])}{random.randint(1, 10)}',
                    'Quantity_On_Hand': random.randint(0, 2000),
                    'Quantity_Reserved': random.randint(0, 200),
                    'Quantity_Available': random.randint(0, 1800),
                    'Quantity_On_Order': random.randint(0, 500),
                    'Quantity_In_Transit': random.randint(0, 200),
                    'Reorder_Point': random.randint(20, 200),
                    'Reorder_Quantity': random.randint(100, 500),
                    'Safety_Stock': random.randint(10, 100),
                    'Maximum_Stock': random.randint(1000, 5000),
                    'Unit_Cost': unit_cost,
                    'Unit_Price': round(unit_cost * random.uniform(1.3, 2), 2),
                    'Total_Value': round(unit_cost * random.randint(100, 2000), 2),
                    'Weight_Kg': round(random.uniform(0.1, 15), 2),
                    'Unit_Of_Measure': random.choice(['Each', 'Box', 'Case']),
                    'Pack_Size': random.randint(1, 12),
                    'Lot_Number': f'LOT-{datetime.now().strftime("%Y%m")}-{random.randint(1000, 9999)}',
                    'Manufacturing_Date': (datetime.now() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d'),
                    'Last_Count_Date': (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d'),
                    'Last_Receipt_Date': (datetime.now() - timedelta(days=random.randint(1, 60))).strftime('%Y-%m-%d'),
                    'Last_Issue_Date': (datetime.now() - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d'),
                    'Days_On_Hand': random.randint(1, 180),
                    'Turnover_Rate': round(random.uniform(2, 20), 2),
                    'ABC_Classification': random.choice(['A', 'B', 'C']),
                    'Status': random.choice(['Active', 'Low Stock', 'Out of Stock', 'Discontinued']),
                    'Country_Of_Origin': random.choice(['USA', 'China', 'Taiwan', 'Japan', 'South Korea', 'Vietnam']),
                    'Cycle_Count_Variance': random.randint(-10, 10),
                    'Last_Cycle_Count_By': get_random_name()
                })
                sku_counter += 1
    
    return pd.DataFrame(data[:num_rows])

def generate_web_analytics_data(num_rows=500):
    pages = ['/home', '/products', '/products/laptops', '/products/monitors', '/products/keyboards', '/products/mice',
             '/products/headphones', '/cart', '/checkout', '/account', '/account/orders', '/support', '/contact',
             '/about', '/blog', '/blog/tech-news', '/blog/reviews', '/deals', '/new-arrivals', '/best-sellers']
    
    campaigns = ['google_brand', 'google_nonbrand', 'facebook_retargeting', 'facebook_prospecting', 'email_newsletter',
                 'email_abandoned_cart', 'linkedin_b2b', 'affiliate_techreviews', 'influencer_youtube', 'direct']
    
    data = []
    for i in range(num_rows):
        session_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        user_name = get_random_name() if random.random() > 0.4 else None
        
        data.append({
            'Session_ID': f'SES-{random.randint(10000000, 99999999)}',
            'User_ID': f'USER-{random.randint(10000, 99999)}' if user_name else None,
            'User_Name': user_name,
            'Session_Date': session_date.strftime('%Y-%m-%d'),
            'Session_Start_Time': f'{random.randint(0, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}',
            'Session_Duration_Seconds': random.randint(10, 1800),
            'Page_Views': random.randint(1, 25),
            'Unique_Page_Views': random.randint(1, 15),
            'Landing_Page': random.choice(pages),
            'Exit_Page': random.choice(pages),
            'Bounce': random.choice([True, False, False, False]),
            'Device_Category': random.choice(['Desktop', 'Mobile', 'Tablet']),
            'Device_Brand': random.choice(['Apple', 'Samsung', 'Google', 'Dell', 'HP', 'Lenovo', 'Microsoft']),
            'Operating_System': random.choice(['Windows 11', 'Windows 10', 'macOS Sonoma', 'macOS Ventura', 'iOS 17', 'Android 14', 'Chrome OS']),
            'Browser': random.choice(['Chrome', 'Safari', 'Firefox', 'Edge', 'Opera']),
            'Screen_Resolution': random.choice(['1920x1080', '2560x1440', '1366x768', '1440x900', '390x844', '412x915']),
            'Country': random.choice(['USA', 'UK', 'Canada', 'Germany', 'France', 'Australia', 'Japan', 'India']),
            'City': random.choice(['New York', 'Los Angeles', 'London', 'Toronto', 'Sydney', 'Berlin', 'Tokyo', 'Mumbai']),
            'Language': random.choice(['en-US', 'en-GB', 'es-ES', 'fr-FR', 'de-DE', 'ja-JP']),
            'Traffic_Source': random.choice(['Organic Search', 'Paid Search', 'Social', 'Email', 'Direct', 'Referral', 'Affiliate']),
            'Traffic_Medium': random.choice(['organic', 'cpc', 'social', 'email', '(none)', 'referral', 'affiliate']),
            'Campaign': random.choice(campaigns),
            'Keyword': random.choice(['best laptops 2024', 'wireless keyboard', 'gaming mouse', 'noise cancelling headphones', None]),
            'New_User': random.choice([True, False]),
            'Sessions_Total': random.randint(1, 50),
            'Days_Since_Last_Session': random.randint(0, 90),
            'Products_Viewed': random.randint(0, 15),
            'Products_Added_To_Cart': random.randint(0, 5),
            'Cart_Value': round(random.uniform(0, 2000), 2),
            'Checkout_Started': random.choice([True, False]),
            'Purchase_Completed': random.choice([True, False, False, False]),
            'Transaction_Revenue': round(random.uniform(0, 1500), 2) if random.random() > 0.7 else 0,
            'Items_Purchased': random.randint(0, 5),
            'Search_Events': random.randint(0, 5),
            'Search_Term': random.choice(['macbook', 'wireless mouse', 'monitor', 'keyboard', None]),
            'Video_Plays': random.randint(0, 3),
            'Scroll_Depth_Percent': random.choice([25, 50, 75, 90, 100]),
            'Time_On_Page_Avg_Seconds': random.randint(10, 180),
            'Engagement_Rate_Percent': round(random.uniform(20, 80), 2),
            'Click_Events': random.randint(1, 50),
            'Form_Submissions': random.randint(0, 2),
            'Newsletter_Signup': random.choice([True, False, False, False, False]),
            'Chat_Initiated': random.choice([True, False, False, False, False])
        })
    
    return pd.DataFrame(data)

def generate_operations_data(num_rows=300):
    carriers = {
        'FedEx': ['FedEx Ground', 'FedEx Express', 'FedEx 2Day', 'FedEx Overnight'],
        'UPS': ['UPS Ground', 'UPS 3 Day Select', 'UPS 2nd Day Air', 'UPS Next Day Air'],
        'USPS': ['USPS Priority Mail', 'USPS First Class', 'USPS Priority Express'],
        'DHL': ['DHL Express', 'DHL eCommerce'],
        'Amazon': ['Amazon Logistics']
    }
    
    data = []
    for i in range(num_rows):
        order_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        carrier_name = random.choice(list(carriers.keys()))
        shipping_method = random.choice(carriers[carrier_name])
        customer_name = get_random_name()
        picker_name = get_random_name()
        packer_name = get_random_name()
        
        ship_days = random.randint(1, 5)
        delivery_days = random.randint(2, 10)
        
        data.append({
            'Operation_ID': f'OPS-{100000 + i}',
            'Order_ID': f'ORD-{random.randint(100000, 999999)}',
            'Customer_Name': customer_name,
            'Order_Date': order_date.strftime('%Y-%m-%d'),
            'Promised_Ship_Date': (order_date + timedelta(days=2)).strftime('%Y-%m-%d'),
            'Actual_Ship_Date': (order_date + timedelta(days=ship_days)).strftime('%Y-%m-%d'),
            'Promised_Delivery_Date': (order_date + timedelta(days=7)).strftime('%Y-%m-%d'),
            'Actual_Delivery_Date': (order_date + timedelta(days=delivery_days)).strftime('%Y-%m-%d'),
            'Warehouse': random.choice(['East Coast DC - Newark', 'West Coast DC - LA', 'Central Hub - Dallas', 'Southern FC - Atlanta']),
            'Fulfillment_Center': random.choice(['FC-NJ-01', 'FC-CA-01', 'FC-TX-01', 'FC-GA-01']),
            'Carrier': carrier_name,
            'Shipping_Method': shipping_method,
            'Tracking_Number': f'{carrier_name[:3].upper()}{random.randint(100000000000, 999999999999)}',
            'Package_Weight_Lbs': round(random.uniform(0.5, 50), 2),
            'Package_Dimensions': f'{random.randint(5, 30)}x{random.randint(5, 20)}x{random.randint(2, 15)} in',
            'Shipping_Cost': round(random.uniform(5, 100), 2),
            'Handling_Cost': round(random.uniform(1, 10), 2),
            'Packaging_Cost': round(random.uniform(0.5, 5), 2),
            'Total_Fulfillment_Cost': round(random.uniform(10, 120), 2),
            'Order_Status': random.choice(['Delivered', 'Shipped', 'Processing', 'Cancelled', 'Returned']),
            'Delivery_Status': random.choice(['On Time', 'Early', 'Late', 'Failed Attempt', 'Delivered']),
            'Delivery_Attempts': random.randint(1, 3),
            'Signature_Required': random.choice([True, False]),
            'Pick_Time_Minutes': random.randint(2, 30),
            'Pack_Time_Minutes': random.randint(2, 15),
            'Ship_Time_Minutes': random.randint(5, 60),
            'Total_Processing_Hours': round(random.uniform(0.5, 24), 2),
            'Items_Count': random.randint(1, 10),
            'Units_Count': random.randint(1, 20),
            'Picker_Name': picker_name,
            'Packer_Name': packer_name,
            'Quality_Check_Passed': random.choice([True, True, True, False]),
            'Damage_Reported': random.choice([True, False, False, False, False]),
            'Return_Requested': random.choice([True, False, False, False, False]),
            'Return_Reason': random.choice(['Defective', 'Wrong Item', 'Not as Described', 'Changed Mind', None]),
            'Refund_Amount': round(random.uniform(0, 500), 2) if random.random() > 0.85 else 0,
            'Customer_Rating': random.randint(1, 5),
            'Delivery_Rating': random.randint(1, 5),
            'SLA_Met': random.choice([True, True, True, False]),
            'Exception_Code': random.choice(['None', 'Weather Delay', 'Address Issue', 'Capacity Constraint', 'Stock Issue']),
            'Priority_Level': random.choice(['Standard', 'Priority', 'Rush', 'Same Day']),
            'Shipping_Zone': random.randint(1, 8),
            'Distance_Miles': random.randint(50, 3000)
        })
    
    return pd.DataFrame(data)

print("Generating XLSX file with multiple sheets...")

with pd.ExcelWriter('analytics_data.xlsx', engine='openpyxl') as writer:
    print("  - Generating Sales Data...")
    generate_sales_data(600).to_excel(writer, sheet_name='Sales', index=False)
    
    print("  - Generating HR Data...")
    generate_hr_data(450).to_excel(writer, sheet_name='HR_Employees', index=False)
    
    print("  - Generating Financial Data...")
    generate_financial_data(400).to_excel(writer, sheet_name='Financial_Transactions', index=False)
    
    print("  - Generating Inventory Data...")
    generate_inventory_data(500).to_excel(writer, sheet_name='Inventory', index=False)
    
    print("  - Generating Marketing Data...")
    generate_marketing_data(350).to_excel(writer, sheet_name='Marketing_Campaigns', index=False)
    
    print("  - Generating Customer Data...")
    generate_customer_data(500).to_excel(writer, sheet_name='Customers', index=False)
    
    print("  - Generating Product Data...")
    generate_product_data(300).to_excel(writer, sheet_name='Products', index=False)
    
    print("  - Generating Operations Data...")
    generate_operations_data(400).to_excel(writer, sheet_name='Operations', index=False)
    
    print("  - Generating Web Analytics Data...")
    generate_web_analytics_data(600).to_excel(writer, sheet_name='Web_Analytics', index=False)
    
    print("  - Generating Support Tickets Data...")
    generate_support_tickets_data(450).to_excel(writer, sheet_name='Support_Tickets', index=False)

print("XLSX file created: analytics_data.xlsx")

print("\nGenerating CSV file with different data...")

ECOMMERCE_PRODUCTS = {
    'Electronics': [
        ('Apple iPhone 15 Pro Max', 1199.00), ('Samsung Galaxy S24 Ultra', 1299.00), ('Google Pixel 8 Pro', 999.00),
        ('Sony WH-1000XM5 Headphones', 349.99), ('Apple AirPods Pro 2', 249.00), ('Bose QuietComfort Ultra', 429.00),
        ('Apple Watch Series 9', 399.00), ('Samsung Galaxy Watch 6', 329.00), ('Fitbit Charge 6', 159.95),
        ('iPad Pro 12.9"', 1099.00), ('Samsung Galaxy Tab S9', 849.99), ('Microsoft Surface Pro 9', 999.00),
        ('Sony PlayStation 5', 499.00), ('Xbox Series X', 499.00), ('Nintendo Switch OLED', 349.00),
        ('GoPro Hero 12 Black', 399.00), ('DJI Mini 4 Pro', 759.00), ('Canon EOS R6 Mark II', 2499.00)
    ],
    'Computers': [
        ('MacBook Pro 14" M3 Pro', 1999.00), ('MacBook Air 15" M3', 1299.00), ('Dell XPS 15', 1799.00),
        ('HP Spectre x360 16', 1649.00), ('Lenovo ThinkPad X1 Carbon', 1429.00), ('ASUS ROG Zephyrus G14', 1599.00),
        ('Microsoft Surface Laptop 5', 999.00), ('Razer Blade 15', 2499.00), ('Acer Swift Go 14', 849.00),
        ('Apple Mac Mini M2', 599.00), ('Apple Mac Studio', 1999.00), ('Dell OptiPlex 7010', 899.00)
    ],
    'Home & Kitchen': [
        ('Dyson V15 Detect Vacuum', 749.99), ('iRobot Roomba j9+', 899.00), ('Ninja Foodi 14-in-1', 229.99),
        ('KitchenAid Artisan Mixer', 449.99), ('Instant Pot Pro Plus', 169.99), ('Breville Barista Express', 749.95),
        ('Vitamix A3500', 649.95), ('Le Creuset Dutch Oven', 419.95), ('All-Clad D5 Cookware Set', 699.95),
        ('Dyson Purifier Hot+Cool', 569.99), ('Philips Hue Starter Kit', 199.99), ('Nest Learning Thermostat', 249.00)
    ],
    'Fashion': [
        ('Nike Air Max 90', 130.00), ('Adidas Ultraboost 23', 190.00), ('New Balance 990v6', 199.99),
        ('Levi\'s 501 Original Jeans', 69.50), ('Patagonia Better Sweater', 139.00), ('The North Face Puffer', 229.00),
        ('Ray-Ban Aviator Classic', 163.00), ('Oakley Holbrook', 177.00), ('Apple Watch Band Sport', 49.00),
        ('Coach Leather Tote', 395.00), ('Michael Kors Crossbody', 298.00), ('Tumi Alpha Backpack', 495.00)
    ],
    'Sports & Outdoors': [
        ('Peloton Bike+', 2495.00), ('NordicTrack Commercial 1750', 1799.00), ('Bowflex SelectTech 552', 429.00),
        ('YETI Tundra 45 Cooler', 325.00), ('Hydro Flask 32oz', 44.95), ('Osprey Atmos AG 65', 320.00),
        ('REI Co-op Flash 55 Pack', 199.00), ('Garmin Fenix 7', 699.99), ('Theragun Pro', 599.00),
        ('TaylorMade Stealth Driver', 599.99), ('Callaway Paradym Irons', 1399.99), ('Titleist Pro V1 Golf Balls', 54.99)
    ]
}

def generate_ecommerce_transactions(num_rows=800):
    us_states = {
        'CA': 'California', 'TX': 'Texas', 'FL': 'Florida', 'NY': 'New York', 'PA': 'Pennsylvania',
        'IL': 'Illinois', 'OH': 'Ohio', 'GA': 'Georgia', 'NC': 'North Carolina', 'MI': 'Michigan',
        'NJ': 'New Jersey', 'VA': 'Virginia', 'WA': 'Washington', 'AZ': 'Arizona', 'MA': 'Massachusetts',
        'TN': 'Tennessee', 'IN': 'Indiana', 'MO': 'Missouri', 'MD': 'Maryland', 'WI': 'Wisconsin',
        'CO': 'Colorado', 'MN': 'Minnesota', 'SC': 'South Carolina', 'AL': 'Alabama', 'LA': 'Louisiana'
    }
    
    all_products = []
    for category, products in ECOMMERCE_PRODUCTS.items():
        for product_name, price in products:
            all_products.append((product_name, category, price))
    
    data = []
    for i in range(num_rows):
        transaction_date = datetime(2023, 1, 1) + timedelta(days=random.randint(0, 365))
        customer_name = get_random_name()
        product_name, category, base_price = random.choice(all_products)
        
        quantity = random.randint(1, 3)
        discount_percent = random.choice([0, 0, 0, 5, 10, 15, 20])
        unit_price = round(base_price * (1 - discount_percent / 100), 2)
        subtotal = round(unit_price * quantity, 2)
        state_code = random.choice(list(us_states.keys()))
        tax_rate = random.uniform(0.05, 0.10)
        tax = round(subtotal * tax_rate, 2)
        shipping = round(random.uniform(0, 15), 2) if subtotal < 50 else 0
        total = round(subtotal + tax + shipping, 2)
        cost = round(base_price * random.uniform(0.5, 0.7), 2)
        profit = round(total - (cost * quantity) - shipping, 2)
        
        data.append({
            'Transaction_ID': f'TXN-{1000000 + i}',
            'Transaction_Date': transaction_date.strftime('%Y-%m-%d'),
            'Transaction_Time': f'{random.randint(6, 23):02d}:{random.randint(0, 59):02d}:{random.randint(0, 59):02d}',
            'Customer_ID': f'C{random.randint(100000, 999999)}',
            'Customer_Name': customer_name,
            'Customer_Email': get_random_email(customer_name),
            'Customer_Age_Group': random.choice(['18-24', '25-34', '35-44', '45-54', '55-64', '65+']),
            'Customer_Gender': random.choice(['Male', 'Female', 'Other']),
            'Customer_Type': random.choice(['New', 'Returning', 'VIP']),
            'Lifetime_Orders': random.randint(1, 50),
            'Shipping_State': state_code,
            'Shipping_State_Name': us_states[state_code],
            'Shipping_City': random.choice(CITIES['USA']),
            'Shipping_Zip': f'{random.randint(10000, 99999)}',
            'Product_SKU': f'SKU{random.randint(10000, 99999)}',
            'Product_Name': product_name,
            'Product_Category': category,
            'Product_Brand': product_name.split()[0],
            'Product_Rating': round(random.uniform(3.5, 5.0), 1),
            'Product_Reviews': random.randint(50, 5000),
            'Quantity': quantity,
            'Original_Price': base_price,
            'Discount_Percent': discount_percent,
            'Unit_Price': unit_price,
            'Subtotal': subtotal,
            'Tax_Rate_Percent': round(tax_rate * 100, 2),
            'Tax_Amount': tax,
            'Shipping_Cost': shipping,
            'Total_Amount': total,
            'Cost_Per_Unit': cost,
            'Total_Cost': round(cost * quantity, 2),
            'Gross_Profit': profit,
            'Profit_Margin_Percent': round((profit / total) * 100, 2) if total > 0 else 0,
            'Payment_Method': random.choice(['Visa', 'Mastercard', 'American Express', 'PayPal', 'Apple Pay', 'Google Pay', 'Klarna']),
            'Payment_Status': random.choice(['Completed', 'Completed', 'Completed', 'Pending', 'Refunded']),
            'Order_Status': random.choice(['Delivered', 'Delivered', 'Shipped', 'Processing', 'Cancelled', 'Returned']),
            'Shipping_Method': random.choice(['Standard Shipping', 'Express Shipping', '2-Day Shipping', 'Next Day', 'Free Shipping']),
            'Shipping_Carrier': random.choice(['FedEx', 'UPS', 'USPS', 'DHL', 'Amazon Logistics']),
            'Delivery_Days_Estimated': random.randint(2, 7),
            'Delivery_Days_Actual': random.randint(2, 10),
            'On_Time_Delivery': random.choice([True, True, True, True, False]),
            'Device_Type': random.choice(['Desktop', 'Mobile', 'Tablet']),
            'Browser': random.choice(['Chrome', 'Safari', 'Firefox', 'Edge', 'Mobile App']),
            'Operating_System': random.choice(['Windows', 'macOS', 'iOS', 'Android']),
            'Traffic_Source': random.choice(['Organic Search', 'Paid Search', 'Social Media', 'Email', 'Direct', 'Referral']),
            'Campaign_Name': random.choice(MARKETING_CAMPAIGNS) if random.random() > 0.5 else None,
            'Coupon_Code': f'SAVE{discount_percent}' if discount_percent > 0 else None,
            'Is_Gift': random.choice([True, False, False, False, False]),
            'Warehouse_Location': random.choice(['East Coast DC', 'West Coast DC', 'Central DC', 'Southern DC']),
            'Return_Requested': random.choice([True, False, False, False, False, False]),
            'Return_Reason': random.choice(['Defective', 'Wrong Size', 'Not as Expected', 'Changed Mind']) if random.random() > 0.9 else None,
            'Customer_Rating': random.randint(1, 5) if random.random() > 0.4 else None,
            'Review_Submitted': random.choice([True, False, False]),
            'NPS_Score': random.randint(0, 10) if random.random() > 0.6 else None,
            'Session_Duration_Seconds': random.randint(60, 1200),
            'Pages_Viewed': random.randint(3, 20),
            'Cart_Abandonment_Count': random.randint(0, 3),
            'Days_Since_Last_Purchase': random.randint(0, 180),
            'Fiscal_Quarter': f'Q{((transaction_date.month - 1) // 3) + 1}',
            'Fiscal_Year': transaction_date.year,
            'Day_Of_Week': transaction_date.strftime('%A'),
            'Is_Weekend': transaction_date.weekday() >= 5,
            'Hour_Of_Day': random.randint(6, 23)
        })
    
    return pd.DataFrame(data)

csv_data = generate_ecommerce_transactions(1000)
csv_data.to_csv('ecommerce_transactions.csv', index=False)
print("CSV file created: ecommerce_transactions.csv")

print("\n" + "="*60)
print("Data generation complete with REALISTIC names and values!")
print("="*60)
print(f"\nXLSX File: analytics_data.xlsx")
print("  - 10 sheets with diverse business analytics data")
print("  - Real product names (Apple, Dell, Sony, etc.)")
print("  - Real person names, universities, cities")
print("  - Real company and vendor names")
print(f"\nCSV File: ecommerce_transactions.csv")
print("  - 1,000 rows of e-commerce transaction data")
print("  - Real product names (iPhone, MacBook, Nike, etc.)")
print("  - Real customer names and realistic pricing")

