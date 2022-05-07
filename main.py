import os
from website import create_app

app = create_app()

if __name__ == '__main__':
    # bind port if defined, otherwise default to 5000
    port = int(os.environ.get('PORT', 5006))
    app.run(debug=True, host='0.0.0.0', port=port)
