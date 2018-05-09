from flask import Flask, render_template
import database

app = Flask(__name__)


@app.route('/')
def index():
    parse = database.ParseDatabase()
    addr_list = ['122 Reeds Rd, 856 N New Rd']
    for i in addr_list:
        selected_data = parse.select_data(address=i)
        print(selected_data)
        json_data = parse.parse_json_url(selected_data)

        return render_template('home.html', data=json_data)


if __name__ == '__main__':
    app.run(debug=True)