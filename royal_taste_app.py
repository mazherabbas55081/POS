import streamlit as st
from datetime import datetime, date
import pandas as pd
import base64

# =========================================================
# HOTEL / RESTAURANT POS SYSTEM
# Single Python File
# Prepared by Mazhar Abbas
# =========================================================

st.set_page_config(
    page_title="ROYAL TASTE • VIP POS",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
* {font-family:'DM Sans',sans-serif;}
.stApp {
    background: radial-gradient(circle at top right,rgba(212,175,55,.12),transparent 30%),
                linear-gradient(135deg,#080b12 0%,#101522 50%,#080b12 100%);
    color:#f5f5f5;
}
section[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#0b0f18,#141a27);
    border-right:1px solid rgba(212,175,55,.25);
}
section[data-testid="stSidebar"] * {color:#f4f4f4 !important;}
.vip-title {font-family:'Playfair Display',serif;font-size:42px;font-weight:700;color:#d4af37;}
.hero {
    padding:28px;border-radius:22px;
    background:linear-gradient(90deg,rgba(0,0,0,.90),rgba(0,0,0,.45)),
    url("https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=1600&q=85");
    background-size:cover;background-position:center;
    border:1px solid rgba(212,175,55,.35);
    box-shadow:0 15px 45px rgba(0,0,0,.35);margin-bottom:25px;
}
.hero h1 {color:#fff;font-family:'Playfair Display',serif;font-size:44px;margin:0;}
.hero p {color:#ddd;font-size:17px;}
.gold {color:#d4af37;}
.metric-card {
    background:linear-gradient(145deg,#151c29,#0c111b);
    border:1px solid rgba(212,175,55,.25);border-radius:18px;padding:20px;
}
.metric-title {color:#9fa7b5;font-size:13px;}
.metric-value {color:#d4af37;font-size:29px;font-weight:700;}
.food-card {
    background:linear-gradient(145deg,#151b27,#0d121b);
    border:1px solid rgba(255,255,255,.08);border-radius:18px;padding:12px;margin-bottom:15px;
}
.food-name {color:#fff;font-weight:700;font-size:17px;}
.food-desc {color:#8993a3;font-size:12px;}
.food-price {color:#d4af37;font-weight:700;font-size:18px;}
.section-title {
    color:#fff;font-family:'Playfair Display',serif;font-size:28px;
    border-left:4px solid #d4af37;padding-left:12px;margin:18px 0;
}
.order-box {background:#101722;border:1px solid rgba(212,175,55,.25);border-radius:18px;padding:18px;}
div.stButton > button {border-radius:10px;border:1px solid rgba(212,175,55,.4);font-weight:600;}
div.stButton > button:hover {border-color:#d4af37;color:#d4af37;}
</style>
""", unsafe_allow_html=True)

if "cart" not in st.session_state: st.session_state.cart = []
if "orders" not in st.session_state: st.session_state.orders = []
if "customers" not in st.session_state: st.session_state.customers = []
if "expenses" not in st.session_state: st.session_state.expenses = []
if "stock" not in st.session_state: st.session_state.stock = []
if "order_no" not in st.session_state: st.session_state.order_no = 1001
if "selected_table" not in st.session_state: st.session_state.selected_table = "Table 01"

MENU = [
{"id":1,"name":"Royal Zinger Burger","category":"Burgers","price":650,"cost":380,"image":"https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=800&q=85","desc":"Crispy chicken, cheese, lettuce and signature sauce"},
{"id":2,"name":"Classic Beef Burger","category":"Burgers","price":750,"cost":430,"image":"https://images.unsplash.com/photo-1565299507177-b0ac66763828?auto=format&fit=crop&w=800&q=85","desc":"Premium beef patty with cheese and fresh vegetables"},
{"id":3,"name":"Margherita Pizza","category":"Pizza","price":1100,"cost":620,"image":"https://images.unsplash.com/photo-1574071318508-1cdbab80d002?auto=format&fit=crop&w=800&q=85","desc":"Tomato, mozzarella and Italian herbs"},
{"id":4,"name":"Pepperoni Pizza","category":"Pizza","price":1450,"cost":780,"image":"https://images.unsplash.com/photo-1628840042765-356cda07504e?auto=format&fit=crop&w=800&q=85","desc":"Loaded pepperoni, mozzarella and tomato sauce"},
{"id":5,"name":"Chicken Shawarma","category":"Shawarma","price":350,"cost":190,"image":"https://images.unsplash.com/photo-1529006557810-274b9b2fc783?auto=format&fit=crop&w=800&q=85","desc":"Juicy chicken, garlic sauce and fresh vegetables"},
{"id":6,"name":"Loaded French Fries","category":"Fries","price":450,"cost":230,"image":"https://images.unsplash.com/photo-1573080496219-bb080dd4f877?auto=format&fit=crop&w=800&q=85","desc":"Crispy fries with cheese and special sauce"},
{"id":7,"name":"Crispy Fried Chicken","category":"Chicken","price":850,"cost":460,"image":"https://images.unsplash.com/photo-1562967916-eb82221dfb36?auto=format&fit=crop&w=800&q=85","desc":"Golden crispy chicken with signature seasoning"},
{"id":8,"name":"Chicken Biryani","category":"Rice","price":450,"cost":250,"image":"https://images.unsplash.com/photo-1589302168068-964664d93dc0?auto=format&fit=crop&w=800&q=85","desc":"Aromatic basmati rice with spicy chicken"},
{"id":9,"name":"Chicken BBQ Platter","category":"BBQ","price":1350,"cost":760,"image":"https://images.unsplash.com/photo-1544025162-d76694265947?auto=format&fit=crop&w=800&q=85","desc":"Mixed grilled chicken BBQ platter"},
{"id":10,"name":"Club Sandwich","category":"Sandwiches","price":700,"cost":390,"image":"https://images.unsplash.com/photo-1553909489-cd47e0907980?auto=format&fit=crop&w=800&q=85","desc":"Triple-layer sandwich with chicken and cheese"},
{"id":11,"name":"Fresh Lemonade","category":"Drinks","price":250,"cost":100,"image":"https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=800&q=85","desc":"Fresh lemon juice with chilled water"},
{"id":12,"name":"Cold Coffee","category":"Drinks","price":350,"cost":150,"image":"https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=800&q=85","desc":"Creamy chilled coffee"},
{"id":13,"name":"Chocolate Cake","category":"Desserts","price":400,"cost":180,"image":"https://images.unsplash.com/photo-1578985545062-69928b1d9587?auto=format&fit=crop&w=800&q=85","desc":"Rich chocolate cake slice"},
{"id":14,"name":"Cheesecake","category":"Desserts","price":500,"cost":250,"image":"https://images.unsplash.com/photo-1565958011703-44f9829ba187?auto=format&fit=crop&w=800&q=85","desc":"Creamy premium cheesecake"}
]

def add_to_cart(item):
    for x in st.session_state.cart:
        if x["id"] == item["id"]:
            x["qty"] += 1
            return
    st.session_state.cart.append({"id":item["id"],"name":item["name"],"price":item["price"],"qty":1})

def cart_subtotal():
    return sum(x["price"] * x["qty"] for x in st.session_state.cart)

def money(value):
    return f"Rs. {value:,.0f}"

def generate_order_no():
    n = st.session_state.order_no
    st.session_state.order_no += 1
    return n

def create_bill_html(order):
    rows = "".join(
        f"<tr><td>{i['name']}</td><td>{i['qty']}</td><td>Rs. {i['price']:,.0f}</td><td>Rs. {i['price']*i['qty']:,.0f}</td></tr>"
        for i in order["items"]
    )
    return f"""<!doctype html><html><head><title>Royal Taste Bill</title>
    <style>body{{font-family:Arial;width:80mm;margin:auto;color:#000}}h2,h3,.center{{text-align:center}}table{{width:100%;border-collapse:collapse;font-size:12px}}th,td{{padding:5px 2px;border-bottom:1px dashed #999}}.total{{font-size:18px;font-weight:bold}}</style>
    </head><body><h2>ROYAL TASTE</h2><div class="center">HOTEL & RESTAURANT</div><hr>
    Order #: {order['order_no']}<br>Date: {order['date']}<br>Customer: {order['customer']}<br>
    Type: {order['order_type']}<br>Table: {order['table']}<br><br>
    <table><tr><th>Item</th><th>Qty</th><th>Price</th><th>Total</th></tr>{rows}</table><br>
    Subtotal: Rs. {order['subtotal']:,.0f}<br>Discount: Rs. {order['discount']:,.0f}<br>
    Tax: Rs. {order['tax']:,.0f}<br>Service: Rs. {order['service']:,.0f}
    <p class="total">GRAND TOTAL: Rs. {order['grand_total']:,.0f}</p>
    Payment: {order['payment']}<hr><div class="center">Thank you for visiting Royal Taste!<br>Prepared by Mazhar Abbas</div>
    <script>window.onload=function(){{window.print()}}</script></body></html>"""

def html_download(data, filename):
    encoded = base64.b64encode(data.encode()).decode()
    return f'<a href="data:text/html;base64,{encoded}" download="{filename}" target="_blank" style="display:inline-block;padding:10px 18px;background:#d4af37;color:#000;text-decoration:none;border-radius:8px;font-weight:bold;">🖨️ PRINT / OPEN BILL</a>'

with st.sidebar:
    st.markdown('<div style="text-align:center;padding:10px;"><div style="font-size:55px;">👑</div><h2 style="color:#d4af37;">ROYAL TASTE</h2><small>VIP POS MANAGEMENT</small></div>', unsafe_allow_html=True)
    st.divider()
    page = st.radio("MAIN MENU", [
        "🏠 Dashboard","🛒 POS / New Order","🍽️ Menu","🪑 Tables","👨‍🍳 Kitchen",
        "🚚 Delivery","👥 Customers","📦 Inventory","💰 Expenses","👨‍💼 Employees",
        "📊 Reports","🏨 Hotel Rooms","⚙️ Settings"
    ])
    st.divider()
    st.markdown('<div style="text-align:center;color:#999;font-size:11px;">ROYAL TASTE POS v1.0<br>Prepared by Mazhar Abbas</div>', unsafe_allow_html=True)

if page == "🏠 Dashboard":
    st.markdown('<div class="hero"><div class="vip-title">ROYAL TASTE</div><h1>VIP Restaurant POS</h1><p>Complete Hotel • Restaurant • Fast Food Management System</p></div>', unsafe_allow_html=True)
    total_sales = sum(o["grand_total"] for o in st.session_state.orders)
    total_expenses = sum(x["amount"] for x in st.session_state.expenses)
    c1,c2,c3,c4=st.columns(4)
    for col,title,value in [
        (c1,"TODAY SALES",money(total_sales)),(c2,"TOTAL ORDERS",len(st.session_state.orders)),
        (c3,"CUSTOMERS",len(st.session_state.customers)),(c4,"EXPENSES",money(total_expenses))]:
        with col: st.markdown(f'<div class="metric-card"><div class="metric-title">{title}</div><div class="metric-value">{value}</div></div>',unsafe_allow_html=True)
    st.markdown('<div class="section-title">Recent Orders</div>',unsafe_allow_html=True)
    if st.session_state.orders:
        st.dataframe(pd.DataFrame([{"Order":o["order_no"],"Customer":o["customer"],"Type":o["order_type"],"Payment":o["payment"],"Total":money(o["grand_total"]),"Status":o["status"]} for o in st.session_state.orders[-10:]]),use_container_width=True,hide_index=True)
    else: st.info("No orders yet. Create your first order from POS.")

elif page == "🛒 POS / New Order":
    st.markdown('<div class="section-title">🛒 New Order</div>',unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: order_type=st.selectbox("Order Type",["Dine-In","Takeaway","Delivery","Room Service"])
    with c2: table=st.selectbox("Table",[f"Table {i:02d}" for i in range(1,21)])
    with c3: customer_name=st.text_input("Customer Name","Walk-in Customer")
    search=st.text_input("🔎 Search food item")
    category=st.selectbox("Food Category",["All"]+sorted(set(x["category"] for x in MENU)))
    filtered=[x for x in MENU if category=="All" or x["category"]==category]
    if search: filtered=[x for x in filtered if search.lower() in x["name"].lower()]
    st.markdown('<div class="section-title">🍽️ Food Menu</div>',unsafe_allow_html=True)
    cols=st.columns(3)
    for i,item in enumerate(filtered):
        with cols[i%3]:
            st.markdown(f'<div class="food-card"><img src="{item["image"]}" style="width:100%;height:180px;object-fit:cover;border-radius:13px;"><div style="padding-top:10px;"><div class="food-name">{item["name"]}</div><div class="food-desc">{item["desc"]}</div><div class="food-price">{money(item["price"])}</div></div></div>',unsafe_allow_html=True)
            if st.button(f"➕ Add • {item['name']}",key=f"add_{item['id']}",use_container_width=True):
                add_to_cart(item); st.toast(f"{item['name']} added!"); st.rerun()
    st.markdown('<div class="section-title">🛒 Current Cart</div>',unsafe_allow_html=True)
    if not st.session_state.cart: st.info("Cart is empty. Select food items above.")
    else:
        for i,item in enumerate(st.session_state.cart):
            c1,c2,c3,c4=st.columns([4,1,1,1])
            c1.write(f"**{item['name']}**")
            item["qty"]=c2.number_input("Qty",min_value=1,value=item["qty"],key=f"qty_{i}")
            c3.write(money(item["price"]*item["qty"]))
            if c4.button("❌",key=f"remove_{i}"):
                st.session_state.cart.pop(i); st.rerun()
        subtotal=cart_subtotal()
        st.markdown('<div class="section-title">💳 Checkout</div>',unsafe_allow_html=True)
        c1,c2,c3=st.columns(3)
        discount=c1.number_input("Discount (Rs.)",min_value=0.0,value=0.0)
        tax_percent=c2.number_input("Tax (%)",min_value=0.0,value=5.0)
        service_percent=c3.number_input("Service Charge (%)",min_value=0.0,value=5.0)
        tax=max(0,(subtotal-discount)*tax_percent/100)
        service=max(0,(subtotal-discount)*service_percent/100)
        grand_total=subtotal-discount+tax+service
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Subtotal",money(subtotal)); c2.metric("Discount",money(discount)); c3.metric("Tax + Service",money(tax+service)); c4.metric("GRAND TOTAL",money(grand_total))
        payment=st.selectbox("Payment Method",["Cash","Card","JazzCash","EasyPaisa","Bank Transfer","Split Payment"])
        note=st.text_area("Order Note",placeholder="Extra cheese, less spicy, etc.")
        if st.button("✅ COMPLETE & SAVE ORDER",type="primary",use_container_width=True):
            order={"order_no":generate_order_no(),"date":datetime.now().strftime("%Y-%m-%d %H:%M"),"customer":customer_name,"order_type":order_type,"table":table,"items":[x.copy() for x in st.session_state.cart],"subtotal":subtotal,"discount":discount,"tax":tax,"service":service,"grand_total":grand_total,"payment":payment,"note":note,"status":"Completed"}
            st.session_state.orders.append(order)
            if customer_name!="Walk-in Customer": st.session_state.customers.append({"name":customer_name,"phone":"","date":str(date.today())})
            bill=create_bill_html(order); st.session_state.last_bill=bill; st.session_state.cart=[]
            st.success(f"Order #{order['order_no']} completed successfully!")
            st.markdown(html_download(bill,f"RoyalTaste_Order_{order['order_no']}.html"),unsafe_allow_html=True)

elif page == "🍽️ Menu":
    st.markdown('<div class="section-title">🍽️ Premium Food Menu</div>',unsafe_allow_html=True)
    search=st.text_input("Search Menu")
    data=[x for x in MENU if not search or search.lower() in x["name"].lower()]
    for item in data:
        c1,c2,c3,c4=st.columns([1,4,2,1])
        c1.image(item["image"],width=90); c2.write(f"### {item['name']}"); c2.caption(f"{item['category']} • {item['desc']}")
        c3.markdown(f"### <span class='gold'>{money(item['price'])}</span>",unsafe_allow_html=True)
        if c4.button("Add",key=f"menu_add_{item['id']}"): add_to_cart(item); st.toast("Added to cart!")

elif page == "🪑 Tables":
    st.markdown('<div class="section-title">🪑 Table Management</div>',unsafe_allow_html=True)
    cols=st.columns(4)
    for i in range(1,21):
        status="Reserved" if i%5==0 else "Available"
        with cols[(i-1)%4]:
            (st.warning if status=="Reserved" else st.success)(f"🟡 Table {i:02d}\n\n{status}")
            if st.button(f"Select Table {i:02d}",key=f"table_{i}"):
                st.session_state.selected_table=f"Table {i:02d}"; st.success(f"Selected {st.session_state.selected_table}")
    st.info(f"Current selected table: **{st.session_state.selected_table}**")

elif page == "👨‍🍳 Kitchen":
    st.markdown('<div class="section-title">👨‍🍳 Kitchen Display System</div>',unsafe_allow_html=True)
    if not st.session_state.orders: st.info("No kitchen orders.")
    for order in reversed(st.session_state.orders):
        with st.expander(f"Order #{order['order_no']} • {order['order_type']} • {order['status']}"):
            for item in order["items"]: st.write(f"🍽️ **{item['name']}** × {item['qty']}")
            c1,c2,c3=st.columns(3)
            if c1.button("👨‍🍳 Preparing",key=f"prep_{order['order_no']}"): order["status"]="Preparing"; st.rerun()
            if c2.button("✅ Ready",key=f"ready_{order['order_no']}"): order["status"]="Ready"; st.rerun()
            if c3.button("🍽️ Served",key=f"served_{order['order_no']}"): order["status"]="Served"; st.rerun()

elif page == "🚚 Delivery":
    st.markdown('<div class="section-title">🚚 Delivery Management</div>',unsafe_allow_html=True)
    delivery_orders=[o for o in st.session_state.orders if o["order_type"]=="Delivery"]
    if not delivery_orders: st.info("No delivery orders.")
    for o in delivery_orders:
        st.markdown(f'<div class="order-box"><h3>Order #{o["order_no"]}</h3>Customer: {o["customer"]}<br>Amount: {money(o["grand_total"])}<br>Status: {o["status"]}</div>',unsafe_allow_html=True)
        st.text_input("Delivery Address",key=f"addr_{o['order_no']}")
        st.selectbox("Rider",["Rider 01","Rider 02","Rider 03"],key=f"rider_{o['order_no']}")

elif page == "👥 Customers":
    st.markdown('<div class="section-title">👥 Customer Management</div>',unsafe_allow_html=True)
    with st.form("customer_form"):
        name=st.text_input("Customer Name"); phone=st.text_input("Phone"); address=st.text_area("Address")
        if st.form_submit_button("Save Customer") and name:
            st.session_state.customers.append({"name":name,"phone":phone,"address":address,"date":str(date.today())}); st.success("Customer saved.")
    if st.session_state.customers: st.dataframe(pd.DataFrame(st.session_state.customers),use_container_width=True,hide_index=True)

elif page == "📦 Inventory":
    st.markdown('<div class="section-title">📦 Inventory & Stock</div>',unsafe_allow_html=True)
    with st.form("stock_form"):
        item=st.text_input("Stock Item"); qty=st.number_input("Quantity",min_value=0.0); unit=st.selectbox("Unit",["KG","Litre","Piece","Packet","Box"]); supplier=st.text_input("Supplier")
        if st.form_submit_button("➕ Add Stock") and item:
            st.session_state.stock.append({"Item":item,"Quantity":qty,"Unit":unit,"Supplier":supplier,"Date":str(date.today())}); st.success("Stock added.")
    if st.session_state.stock: st.dataframe(pd.DataFrame(st.session_state.stock),use_container_width=True,hide_index=True)
    st.warning("⚠️ Low-stock monitoring is ready for database integration.")

elif page == "💰 Expenses":
    st.markdown('<div class="section-title">💰 Expense Management</div>',unsafe_allow_html=True)
    with st.form("expense_form"):
        title=st.text_input("Expense Name"); amount=st.number_input("Amount (Rs.)",min_value=0.0)
        category=st.selectbox("Category",["Food Purchase","Electricity","Gas","Rent","Salary","Maintenance","Other"])
        if st.form_submit_button("Save Expense") and title and amount:
            st.session_state.expenses.append({"title":title,"amount":amount,"category":category,"date":str(date.today())}); st.success("Expense saved.")
    if st.session_state.expenses: st.dataframe(pd.DataFrame(st.session_state.expenses),use_container_width=True,hide_index=True)

elif page == "👨‍💼 Employees":
    st.markdown('<div class="section-title">👨‍💼 Employee Management</div>',unsafe_allow_html=True)
    employees=pd.DataFrame([
        {"Name":"Admin","Role":"Administrator","Status":"Active"},
        {"Name":"Cashier 01","Role":"Cashier","Status":"Active"},
        {"Name":"Waiter 01","Role":"Waiter","Status":"Active"},
        {"Name":"Chef 01","Role":"Kitchen","Status":"Active"},
        {"Name":"Rider 01","Role":"Delivery","Status":"Active"}])
    st.dataframe(employees,use_container_width=True,hide_index=True)
    st.write("🔐 Roles: Administrator • Manager • Cashier • Waiter • Kitchen • Delivery")

elif page == "📊 Reports":
    st.markdown('<div class="section-title">📊 Business Reports</div>',unsafe_allow_html=True)
    if not st.session_state.orders: st.info("No sales data available.")
    else:
        df=pd.DataFrame([{"Order":o["order_no"],"Date":o["date"],"Customer":o["customer"],"Type":o["order_type"],"Payment":o["payment"],"Sales":o["grand_total"],"Status":o["status"]} for o in st.session_state.orders])
        c1,c2,c3,c4=st.columns(4)
        c1.metric("Sales",money(df["Sales"].sum())); c2.metric("Orders",len(df)); c3.metric("Average Order",money(df["Sales"].mean())); c4.metric("Cancelled",len(df[df["Status"]=="Cancelled"]))
        st.dataframe(df,use_container_width=True,hide_index=True)
        st.bar_chart(df.groupby("Payment")["Sales"].sum())
        st.download_button("⬇️ Download Sales CSV",df.to_csv(index=False),"royal_taste_sales.csv","text/csv",use_container_width=True)

elif page == "🏨 Hotel Rooms":
    st.markdown('<div class="section-title">🏨 Hotel Room Management</div>',unsafe_allow_html=True)
    rooms=[{"Room":str(100+i),"Type":"Deluxe" if i%2 else "Executive","Price":8500 if i%2 else 12000,"Status":"Occupied" if i%6==0 else ("Reserved" if i%4==0 else "Available")} for i in range(1,21)]
    df_rooms=pd.DataFrame(rooms); st.dataframe(df_rooms,use_container_width=True,hide_index=True)
    c1,c2,c3=st.columns(3)
    c1.metric("Available",len(df_rooms[df_rooms["Status"]=="Available"])); c2.metric("Occupied",len(df_rooms[df_rooms["Status"]=="Occupied"])); c3.metric("Reserved",len(df_rooms[df_rooms["Status"]=="Reserved"]))
    c1,c2=st.columns(2)
    with c1: guest=st.text_input("Guest Name"); room=st.selectbox("Room",df_rooms["Room"].tolist())
    with c2: checkin=st.date_input("Check-in",date.today()); checkout=st.date_input("Check-out",date.today())
    if st.button("🏨 Save Hotel Booking",use_container_width=True): st.success(f"Booking saved for {guest} • Room {room}")

elif page == "⚙️ Settings":
    st.markdown('<div class="section-title">⚙️ System Settings</div>',unsafe_allow_html=True)
    st.text_input("Restaurant / Hotel Name","ROYAL TASTE HOTEL & RESTAURANT")
    st.text_input("Phone","+92 300 0000000")
    st.text_input("Address","Karachi, Pakistan")
    st.number_input("Default Tax %",value=5.0)
    st.selectbox("Currency",["PKR - Rs.","USD - $","AED - د.إ"])
    st.selectbox("Theme",["VIP Dark Gold","Dark","Light"])
    st.markdown("### 🖨️ Receipt Settings")
    st.checkbox("Show Restaurant Logo",value=True); st.checkbox("Show Cashier Name",value=True)
    st.checkbox("Show Customer Name",value=True); st.checkbox("Show Tax",value=True)

st.markdown("""<hr style="border-color:rgba(212,175,55,.2);">
<div style="text-align:center;padding:15px;color:#777;font-size:12px;">
ROYAL TASTE • VIP HOTEL POS SYSTEM<br>Food • Restaurant • Hotel • Kitchen • Inventory • Reports<br><br>
<strong style="color:#d4af37;">Prepared by Mazhar Abbas</strong></div>""",unsafe_allow_html=True)
