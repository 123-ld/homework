from flask import Flask, render_template, request, redirect, url_for, session
import uuid

app = Flask(__name__)
app.secret_key = 'snack_store_2025_github'  # 会话密钥（可自定义）

# 商品数据（内置占位图，无需本地图片）
products = {
    # 零食类
    1: {"id": 1, "name": "薯片（原味）", "category": "零食", "price": 3.5, "stock": 100, "img": "https://via.placeholder.com/150/FF6B6B/FFFFFF?text=薯片"},
    2: {"id": 2, "name": "巧克力棒", "category": "零食", "price": 2.8, "stock": 80, "img": "https://via.placeholder.com/150/4ECDC4/FFFFFF?text=巧克力棒"},
    3: {"id": 3, "name": "牛肉干", "category": "零食", "price": 15.9, "stock": 50, "img": "https://via.placeholder.com/150/F9C80E/FFFFFF?text=牛肉干"},
    # 酒水类
    4: {"id": 4, "name": "可乐（500ml）", "category": "酒水", "price": 2.5, "stock": 200, "img": "https://via.placeholder.com/150/E74C3C/FFFFFF?text=可乐"},
    5: {"id": 5, "name": "啤酒（罐装）", "category": "酒水", "price": 3.0, "stock": 150, "img": "https://via.placeholder.com/150/3498DB/FFFFFF?text=啤酒"},
    6: {"id": 6, "name": "矿泉水", "category": "酒水", "price": 1.0, "stock": 300, "img": "https://via.placeholder.com/150/2ECC71/FFFFFF?text=矿泉水"},
    # 生活用品类
    7: {"id": 7, "name": "纸巾（小包）", "category": "生活用品", "price": 1.5, "stock": 180, "img": "https://via.placeholder.com/150/9B59B6/FFFFFF?text=纸巾"},
    8: {"id": 8, "name": "牙膏", "category": "生活用品", "price": 8.9, "stock": 60, "img": "https://via.placeholder.com/150/1ABC9C/FFFFFF?text=牙膏"},
    9: {"id": 9, "name": "垃圾袋", "category": "生活用品", "price": 2.0, "stock": 120, "img": "https://via.placeholder.com/150/34495E/FFFFFF?text=垃圾袋"},
}

# 初始化购物车
def init_cart():
    if 'cart' not in session:
        session['cart'] = {}
    if 'order_id' not in session:
        session['order_id'] = str(uuid.uuid4())[:8]

# 首页
@app.route('/')
def index():
    init_cart()
    category = request.args.get('category', '')
    filtered_products = [p for p in products.values() if p['category'] == category] if category else list(products.values())
    return render_template('index.html', products=filtered_products, current_category=category)

# 加入购物车
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    init_cart()
    quantity = int(request.form.get('quantity', 1))
    if product_id not in products or quantity > products[product_id]['stock']:
        return redirect(url_for('index'))
    session['cart'][product_id] = session['cart'].get(product_id, 0) + quantity
    return redirect(url_for('cart'))

# 购物车
@app.route('/cart')
def cart():
    init_cart()
    cart_items, total_price = [], 0.0
    for pid, qty in session['cart'].items():
        p = products.get(pid)
        if p:
            item_total = p['price'] * qty
            total_price += item_total
            cart_items.append({'product': p, 'quantity': qty, 'item_total': item_total})
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

# 移除购物车商品
@app.route('/remove/<int:product_id>')
def remove(product_id):
    if 'cart' in session and product_id in session['cart']:
        del session['cart'][product_id]
    return redirect(url_for('cart'))

# 结算
@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    init_cart()
    if request.method == 'POST':
        session['cart'] = {}
        return render_template('checkout.html', success=True, order_id=session['order_id'])
    total_price = sum(products[pid]['price'] * qty for pid, qty in session['cart'].items() if pid in products)
    return render_template('checkout.html', total_price=total_price, success=False)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)