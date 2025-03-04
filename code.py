from flask import Flask, render_template_string, request, jsonify
app = Flask(__name__)
class RestaurantChatbot:
    def __init__(self):
        self.north_indian_menu = {"paneer butter masala": 100, "dal makhani": 90, "biryani": 120, "mix veg": 80}
        self.south_indian_menu = {"idli": 60, "plain dosa": 70, "masala dosa": 80, "rava dosa": 85}
        self.starters_menu = {"samosa": 40, "spring rolls": 50, "paneer tikka": 80}
        self.drinks_menu = {"lassi": 30, "tea": 10, "coffee": 20}
        self.breads_menu = {"roti": 15, "naan": 20, "paratha": 25}
        self.sweets_menu = {"rasmalai": 40, "gulab jamun": 30}
        self.order = {}  
        self.order_status = "Pending"
        self.location = "Dehradun"
    def greet_customer(self):
        return "Welcome to our restaurant! How can I assist you today?"
    def show_menu(self):
        return ["1. North Indian", "2. South Indian", "3. Starters", "4. Drinks", "5. Breads", "6. Sweets"]
    def get_menu(self, choice):
        if choice == '1': return self.north_indian_menu
        elif choice == '2': return self.south_indian_menu
        elif choice == '3': return self.starters_menu
        elif choice == '4': return self.drinks_menu
        elif choice == '5': return self.breads_menu
        elif choice == '6': return self.sweets_menu
        return {}
    def place_order(self, item, quantity):
        item = item.lower()
        if item in self.north_indian_menu or item in self.south_indian_menu or item in self.starters_menu or item in self.drinks_menu or item in self.breads_menu or item in self.sweets_menu:
            if item in self.order:
                self.order[item] += quantity
            else:
                self.order[item] = quantity
            return f"{quantity} {item.capitalize()} added to your order."
        return "Sorry, we don't have that item."

    def calculate_total(self):
        total = 0
        itemized = {}
        for item, quantity in self.order.items():
            for menu in [self.north_indian_menu, self.south_indian_menu, self.starters_menu, self.drinks_menu, self.breads_menu, self.sweets_menu]:
                if item in menu:
                    price = menu[item]
                    total += price * quantity
                    itemized[item] = {"quantity": quantity, "total": price * quantity}
        return total, itemized

    def clear_order(self):
        self.order.clear()
        self.order_status = "Pending"
    def answer_question(self, question):
        question = question.lower()
        if "status" in question:
            return f"Your order is currently getting prepare."
        elif "track" in question or "delivery" in question:
            return "The expected delivery time is 30 minutes."
        elif "order" in question or "delivery" in question:
            return "The expected delivery time is 30 minutes."
        elif "time" in question or "delivery" in question:
            return "The expected delivery time is 30 minutes."
        elif "location" in question:
            return f"We are located in {self.location}."
        else:
            return "Sorry, I couldn't understand your question. Please ask something else."
chatbot = RestaurantChatbot()
index_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Chatbot</title>
    <style>
        body {
            justify-content: center;
            min-height: 100vh;
        }
        h1 {
            color: #3f51b5;
            text-align: center;
            font-size: 36px;
            margin-bottom: 40px;
        }
        button {
            background-color: #3f51b5;
            color: white;
            margin: 10px;
            font-size: 18px;
            cursor: pointer;

        }
        button:hover {
            background-color: #303f9f;
        }
        .container {
            text-align: center;
            padding: 20px;
            border-radius: 10px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            width: 80%;
            max-width: 500px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ greeting }}</h1>
        <button onclick="window.location='/menu'">View Menu</button>
        <button onclick="window.location='/cart'">View Cart</button>
        <button onclick="window.location='/ask_question'">Ask a Question</button>
    </div>
</body>
</html>
"""

menu_categories_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu Categories</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        h1 {
            color: #3f51b5;
            text-align: center;
            margin-bottom: 40px;
        }
        select, button {
            background-color: #3f51b5;
            color: white;
            padding: 15px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
        button:hover, select:hover {
            background-color: #303f9f;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 80%;
            max-width: 500px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Select a Menu Category</h1>
        <form action="/menu_details" method="POST">
            <select name="menu">
                {% for item in menu %}
                    <option value="{{ loop.index }}">{{ item }}</option>
                {% endfor %}
            </select>
            <button type="submit">Show Menu</button>
        </form>
        <a href="/" style="text-decoration: none; color: #3f51b5;">Go Back</a>
    </div>
</body>
</html>
"""

menu_details_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Menu Details</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        h1 {
            color: #3f51b5;
            text-align: center;
            margin-bottom: 40px;
        }
        ul {
            list-style-type: none;
            padding: 0;
            width: 100%;
            max-width: 600px;
        }
        li {
            background-color: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        li:hover {
            background-color: #f1f1f1;
        }
        button {
            background-color: #3f51b5;
            color: white;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #303f9f;
        }
        .container {
            width: 80%;
            max-width: 600px;
            text-align: center;
            padding: 30px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Menu Details</h1>
        <ul>
            {% for item, price in menu.items() %}
                <li>
                    <span>{{ item.capitalize() }} - ₹{{ price }}</span>
                    <input type="number" id="quantity-{{ loop.index }}" value="1" min="1" style="width: 50px;">
                    <button onclick="addToOrder('{{ item }}', '{{ loop.index }}')">Add to Cart</button>
                </li>
            {% endfor %}
        </ul>
        <a href="/" style="text-decoration: none; color: #3f51b5;">Go Back</a>
    </div>
    <script>
        function addToOrder(item, index) {
            let quantity = document.getElementById('quantity-' + index).value;
            fetch('/add_order', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ item: item, quantity: quantity })
            })
            .then(response => response.json())
            .then(data => alert(data.message));
        }
    </script>
</body>
</html>
"""

cart_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Cart</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        h1 {
            color: #3f51b5;
            text-align: center;
            margin-bottom: 40px;
        }
        ul {
            list-style-type: none;
            padding: 0;
            width: 100%;
            max-width: 600px;
        }
        li {
            background-color: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        button {
            background-color: #3f51b5;
            color: white;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #303f9f;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Your Cart</h1>
        <ul>
            {% for item, details in itemized.items() %}
                <li>
                    <span>{{ item.capitalize() }} - Quantity: {{ details.quantity }} - ₹{{ details.total }}</span>
                </li>
            {% endfor %}
        </ul>
        <h2>Total: ₹{{ total }}</h2>
        <button onclick="window.location='/confirm_order'">Confirm Order</button>
        <a href="/" style="text-decoration: none; color: #3f51b5;">Go Back</a>
    </div>
</body>
</html>
"""

order_confirmation_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Confirm Your Order</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        h1 {
            color: #3f51b5;
            text-align: center;
            margin-bottom: 40px;
        }
        .container {
            width: 80%;
            max-width: 600px;
            text-align: center;
            padding: 30px;
            background-color: white;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
        }
        button {
            background-color: #3f51b5;
            color: white;
            padding: 15px 30px;
            margin: 20px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #303f9f;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Confirm Your Order</h1>
        <p>Total: ₹{{ total }}</p>
        <ul>
            {% for item, details in itemized.items() %}
                <li>{{ item.capitalize() }} - Quantity: {{ details.quantity }} - Total: ₹{{ details.total }}</li>
            {% endfor %}
        </ul>
        <button onclick="window.location='/finalize_order'">Confirm Order</button>
        <button onclick="window.location='/cart'">Go Back</button>
    </div>
</body>
</html>
"""

# Ask a Question Page Template
ask_question_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ask a Question</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f8f9fa;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            min-height: 100vh;
        }
        h1 {
            color: #3f51b5;
            text-align: center;
            margin-bottom: 40px;
        }
        input, button {
            background-color: #3f51b5;
            color: white;
            padding: 15px;
            font-size: 18px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px;
        }
        button:hover, input:hover {
            background-color: #303f9f;
        }
        .container {
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 30px;
            width: 80%;
            max-width: 600px;
            text-align: center;
        }
        .response {
            margin-top: 20px;
            font-size: 18px;
            color: #303f9f;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Ask a Question</h1>
        <input type="text" id="question" placeholder="Ask about your order...">
        <button onclick="askQuestion()">Ask</button>
        <div class="response" id="response"></div>
    </div>
    <script>
        function askQuestion() {
            let question = document.getElementById('question').value;
            fetch('/ask_question', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ question: question })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById('response').innerText = data.answer;
            });
        }
    </script>
</body>
</html>
"""

# Flask Routes
@app.route('/')
def index():
    return render_template_string(index_template, greeting=chatbot.greet_customer())

@app.route('/menu')
def menu():
    return render_template_string(menu_categories_template, menu=chatbot.show_menu())

@app.route('/menu_details', methods=['POST'])
def menu_details():
    choice = request.form.get('menu')
    menu = chatbot.get_menu(choice)
    return render_template_string(menu_details_template, menu=menu)

@app.route('/add_order', methods=['POST'])
def add_order():
    data = request.get_json()
    item = data['item']
    quantity = int(data['quantity'])
    message = chatbot.place_order(item, quantity)
    return jsonify({"message": message})

@app.route('/cart')
def cart():
    total, itemized = chatbot.calculate_total()
    return render_template_string(cart_template, total=total, itemized=itemized)

@app.route('/confirm_order')
def confirm_order():
    total, itemized = chatbot.calculate_total()
    return render_template_string(order_confirmation_template, total=total, itemized=itemized)

@app.route('/finalize_order')
def finalize_order():
    chatbot.clear_order()
    return "Your order has been confirmed! Thank you for ordering."

@app.route('/ask_question', methods=['GET', 'POST'])
def ask_question():
    if request.method == 'POST':
        data = request.get_json()
        question = data['question']
        answer = chatbot.answer_question(question)
        return jsonify({"answer": answer})
    return render_template_string(ask_question_template)

if __name__ == '__main__':
    app.run(debug=True)
